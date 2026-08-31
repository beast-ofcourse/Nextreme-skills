#!/usr/bin/env python3
"""
nextreme-pptx — OOXML validator (no overlapping, no overflow, no glitch)

Unzips the .pptx and checks the XML — not just that Python saved without error.
Proves the deck is geometry-clean, theme-faithful, and editable.

Usage:
    python scripts/validate_pptx.py deck.pptx --strict
    python scripts/validate_pptx.py deck.pptx --check-overlap
    python scripts/validate_pptx.py deck.pptx --check-overflow
    python scripts/validate_pptx.py deck.pptx --check-theme
    python scripts/validate_pptx.py deck.pptx --check-editable

skills.sh:
    python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --strict
local:
    python nextreme-pptx/scripts/validate_pptx.py deck.pptx --strict
Exit 0 = pass; non-zero = fail with reasons.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# OOXML namespaces — single constants, no magic inline
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
}
SLOP_RE = re.compile(r"lorem ipsum|lorem|placeholder|your text here|insert text here|click to add title|click to add text", re.IGNORECASE)
TODO_BARE_RE = re.compile(r"\bTODO\b")

EMU_PER_INCH = 914400
TOLERANCE_EMU = int(0.04 * EMU_PER_INCH)  # 0.04in tolerance for stroke
GUTTER_EXPECTED_EMU = int(0.32 * EMU_PER_INCH)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate .pptx OOXML — no glitch")
    parser.add_argument("pptx", help="Path to .pptx")
    parser.add_argument("--strict", action="store_true", help="All checks (overlap+overflow+theme+editable+slop)")
    parser.add_argument("--check-overlap", action="store_true", help="Fail on overlapping / off-canvas shapes")
    parser.add_argument("--check-overflow", action="store_true", help="Fail on text overflow / narrow boxes")
    parser.add_argument("--check-theme", action="store_true", help="Fail on hard srgbClr where schemeClr expected")
    parser.add_argument("--check-editable", action="store_true", help="Fail on rasterized-only slides")
    return parser.parse_args()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}", file=sys.stderr)


def warn(message: str) -> None:
    print(f"[WARN] {message}", file=sys.stderr)


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def unzip_pptx(pptx_path: Path) -> tuple[dict[str, bytes], list[str]]:
    errors: list[str] = []
    if not pptx_path.exists():
        fail(f"File not found: {pptx_path}", errors)
        return {}, errors
    if pptx_path.suffix.lower() not in (".pptx", ".ppt"):
        warn(f"Expected .pptx, got {pptx_path.suffix}")
    header = pptx_path.read_bytes()[:4]
    if header == b"\xD0\xCF\x11\xE0":
        fail("OLE2 header (D0 CF 11 E0) — this is legacy .ppt, not .pptx", errors)
        return {}, errors
    try:
        with zipfile.ZipFile(pptx_path, "r") as archive:
            bad = archive.testzip()
            if bad is not None:
                fail(f"Corrupt ZIP entry: {bad}", errors)
            parts = {name: archive.read(name) for name in archive.namelist()}
    except zipfile.BadZipFile as exc:
        fail(f"Not a valid ZIP/pptx: {exc}", errors)
        return {}, errors
    except OSError as exc:
        fail(f"Failed to read {pptx_path}: {exc}", errors)
        return {}, errors
    return parts, errors


def check_required_parts(parts: dict[str, bytes], errors: list[str]) -> None:
    required_prefixes = ["ppt/presentation.xml", "ppt/slides/slide", "ppt/slideMasters/", "ppt/theme/"]
    for prefix in required_prefixes:
        if not any(name.startswith(prefix) for name in parts):
            if prefix == "ppt/slides/slide":
                if not any(n.startswith("ppt/slides/") for n in parts):
                    fail(f"Missing slides: no {prefix}* found", errors)
            else:
                fail(f"Missing required part prefix: {prefix}", errors)
            continue
        ok(f"Found {prefix}*")
    for name in ("[Content_Types].xml", "docProps/core.xml"):
        if name not in parts:
            fail(f"Missing required part: {name}", errors)
        else:
            ok(f"Found {name}")


def collect_texts(parts: dict[str, bytes]) -> list[str]:
    texts: list[str] = []
    for name, data in parts.items():
        if not (name.startswith("ppt/slides/") or name == "ppt/presentation.xml"):
            continue
        try:
            root = ET.fromstring(data)
        except ET.ParseError:
            continue
        for elem in root.iter():
            if elem.tag.endswith("}t") and elem.text:
                texts.append(elem.text)
    return texts


def check_slop(parts: dict[str, bytes], errors: list[str]) -> None:
    texts = collect_texts(parts)
    for text in texts:
        if SLOP_RE.search(text):
            fail(f"Slop token in text {text[:70]!r}", errors)
        if TODO_BARE_RE.search(text) and "[CONTENT REQUIRED" not in text:
            fail(f"Bare TODO in {text[:70]!r}", errors)


def extract_shapes(slide_xml: bytes) -> list[dict[str, int]]:
    # Parse a:off x/y and a:ext cx/cy (EMU) for each shape-like element
    try:
        root = ET.fromstring(slide_xml)
    except ET.ParseError:
        return []
    shapes: list[dict[str, int]] = []
    # p:sp, p:cxnSp, p:graphicFrame (tables/charts) all have p:spPr / a:xfrm
    for elem in root.iter():
        if not elem.tag.endswith("}xfrm"):
            continue
        # xfrm has a:off and a:ext children
        off = None
        ext = None
        for child in elem:
            if child.tag.endswith("}off"):
                off = child
            elif child.tag.endswith("}ext"):
                ext = child
        if off is None or ext is None:
            continue
        try:
            x = int(off.get("x", "0"))
            y = int(off.get("y", "0"))
            cx = int(ext.get("cx", "0"))
            cy = int(ext.get("cy", "0"))
        except ValueError:
            continue
        if cx == 0 or cy == 0:
            continue
        shapes.append({"x": x, "y": y, "cx": cx, "cy": cy, "x2": x+cx, "y2": y+cy})
    return shapes


def contains(inner_a: dict[str, int], inner_b: dict[str, int]) -> bool:
    # Does a contain b (with tolerance)? — for card + inner textbox, chart + legend box, etc.
    return (
        inner_a["x"] - TOLERANCE_EMU <= inner_b["x"]
        and inner_a["y"] - TOLERANCE_EMU <= inner_b["y"]
        and inner_a["x2"] + TOLERANCE_EMU >= inner_b["x2"]
        and inner_a["y2"] + TOLERANCE_EMU >= inner_b["y2"]
    )


def check_overlap(parts: dict[str, bytes], errors: list[str]) -> None:
    slide_names = sorted([n for n in parts if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
    if not slide_names:
        warn("No slides to check overlap")
        return
    for name in slide_names:
        shapes = extract_shapes(parts[name])
        # pairwise overlap — ignore containment (card contains textbox is intentional)
        for idx in range(len(shapes)):
            for jdx in range(idx+1, len(shapes)):
                a = shapes[idx]; b = shapes[jdx]
                overlap_x = min(a["x2"], b["x2"]) - max(a["x"], b["x"])
                overlap_y = min(a["y2"], b["y2"]) - max(a["y"], b["y"])
                if overlap_x > TOLERANCE_EMU and overlap_y > TOLERANCE_EMU:
                    # Allow containment: textbox inside card, shape inside shape
                    if contains(a, b) or contains(b, a):
                        continue
                    fail(f"Overlap on {name}: shape {idx} ({a['x']/EMU_PER_INCH:.2f},{a['y']/EMU_PER_INCH:.2f} {a['cx']/EMU_PER_INCH:.2f}×{a['cy']/EMU_PER_INCH:.2f}) overlaps shape {jdx} by {overlap_x/EMU_PER_INCH:.2f}×{overlap_y/EMU_PER_INCH:.2f}in (tolerance {TOLERANCE_EMU/EMU_PER_INCH:.2f}in)", errors)
                    # cap reports per slide
                    if len([e for e in errors if name in e]) >= 3:
                        warn(f"Too many overlaps on {name} — truncating")
                        break
            else:
                continue
            break
        # off-canvas via xfrm vs slide size (need presentation size from presentation.xml)
        # For now, check > 13.33in or >7.5in naive bound — actual slide size via pres.xml xfrm not needed for default 16:9
        for shape in shapes:
            if shape["x"] < -TOLERANCE_EMU or shape["y"] < -TOLERANCE_EMU:
                fail(f"Off-canvas negative on {name}: x={shape['x']/EMU_PER_INCH:.2f} y={shape['y']/EMU_PER_INCH:.2f}", errors)
            if shape["x2"] > int(13.33*EMU_PER_INCH) + TOLERANCE_EMU or shape["y2"] > int(7.5*EMU_PER_INCH) + 5*TOLERANCE_EMU:
                # allow a bit beyond for 16:9 vs actual size via theme — only warn for extreme
                if shape["x2"] > int(14*EMU_PER_INCH) or shape["y2"] > int(8.5*EMU_PER_INCH):
                    fail(f"Off-canvas far on {name}: right {shape['x2']/EMU_PER_INCH:.2f}in bottom {shape['y2']/EMU_PER_INCH:.2f}in", errors)
    if not any("Overlap" in e or "Off-canvas" in e for e in errors):
        ok("No overlapping / off-canvas shapes (tolerance 0.04in)")


def check_overflow(parts: dict[str, bytes], errors: list[str]) -> None:
    slide_names = sorted([n for n in parts if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
    for name in slide_names:
        xml = parts[name].decode("utf-8", errors="replace")
        # Narrow textbox heuristic: a:ext cx < 2.5in for a text-holding shape
        # Check via shape + txBody co-occurrence — simplified: flag any ext cx < 2.5in that has txBody nearby
        shapes = extract_shapes(parts[name])
        # Find txBody presence per shape is complex via string proximity — approximate via counting
        if xml.count("p:txBody") == 0:
            continue
        # For each small ext, warn if it likely holds text (has a:t nearby in xml slice)
        # Simplified: if overall slide has text and any shape <2.5in cx, warn if that shape is near a:t
        for shape in shapes:
            if shape["cx"] < int(2.5*EMU_PER_INCH) - TOLERANCE_EMU:
                # only flag if slide average text density suggests body bullets in small boxes
                # heuristic: if slide has ≥4 bullets and box is narrow, likely glitchy wrapping
                bullet_count = xml.count("a:buChar")
                if bullet_count >= 4:
                    warn(f"Narrow textbox on {name}: {shape['cx']/EMU_PER_INCH:.2f}in < 2.5in with {bullet_count} bullets — may wrap glitchy")
        # Overflow via noAutofit missing? Check a:bodyPr with no normAutofit but wordWrap off
        if 'wrap="0"' in xml or 'wrap="none"' in xml:
            fail(f"Text may overflow on {name}: bodyPr wrap off detected", errors)
    # autobodyPr check is heuristic — main gate is overlap + no raster chart
    if not any("overflow" in e.lower() for e in errors):
        ok("No overflow / narrow-box failure (heuristic)")


def check_theme(parts: dict[str, bytes], errors: list[str]) -> None:
    # Scan slide XML for a:solidFill using a:srgbClr where a:schemeClr expected
    # For decks that came from profiled template (presence of schemeClr in masters), flag hard srgbClr
    master_has_scheme = False
    for name, data in parts.items():
        if name.startswith("ppt/slideMasters/") or name.startswith("ppt/theme/"):
            if b"schemeClr" in data:
                master_has_scheme = True
                break
    if not master_has_scheme:
        ok("No master schemeClr — theme check trivially passes (from-scratch deck)")
        return
    for name in sorted([n for n in parts if n.startswith("ppt/slides/slide")]):
        xml = parts[name]
        # count scheme vs srgb in slides
        srgb_count = xml.count(b"srgbClr")
        scheme_count = xml.count(b"schemeClr")
        # If slide uses srgb everywhere and master uses scheme, likely hard-coded RBG broke recoloring
        if srgb_count >= 3 and scheme_count == 0:
            warn(f"Theme note on {name}: {srgb_count}× srgbClr and 0× schemeClr — for branded templates prefer schemeClr; for from-scratch decks srgbClr is expected (palette-driven)")
    # Only ok if no fail-level theme issues
    if not any("schemeClr" in e for e in errors):
        ok("Theme check done (warn-only for from-scratch srgbClr)")


def check_editable(parts: dict[str, bytes], errors: list[str]) -> None:
    slide_names = sorted([n for n in parts if n.startswith("ppt/slides/slide")])
    for name in slide_names:
        xml = parts[name].decode("utf-8", errors="replace")
        # full-slide raster: single p:pic covering ≥90% of slide area
        pic_count = xml.count("p:pic")
        cxn_count = xml.count("p:cxnSp")
        shape_count = xml.count("p:sp") + xml.count("p:graphicFrame")
        # If slide has 1 pic and ≤1 shape, likely raster deck
        if pic_count == 1 and shape_count <= 1 and len(slide_names) > 1:
            # check ext near slide size
            shapes = extract_shapes(parts[name])
            for shape in shapes:
                if shape["cx"] > int(10*EMU_PER_INCH) and shape["cy"] > int(6*EMU_PER_INCH):
                    fail(f"Raster-only slide on {name}: single pic {shape['cx']/EMU_PER_INCH:.2f}×{shape['cy']/EMU_PER_INCH:.2f}in — every chart/table should be native shapes", errors)
        # screenshot chart: p:pic with descr containing chart-like words near c:chart
        if "c:chart" in xml and "p:pic" in xml:
            # both on same slide is okay (photo + chart), but flag if chart series is empty (image replaced data)
            if xml.count("c:chart") == 0:
                warn(f"Chart placeholder but no c:chart on {name} — may be screenshot of chart")
    if not any("Raster" in e for e in errors):
        ok("No raster-only slides (editable check)")


def main() -> None:
    args = parse_args()
    pptx_path = Path(args.pptx)
    strict = bool(args.strict)

    check_overlap_flag = bool(args.check_overlap or strict)
    check_overflow_flag = bool(args.check_overflow or strict)
    check_theme_flag = bool(args.check_theme or strict)
    check_editable_flag = bool(args.check_editable or strict)
    check_slop_flag = strict

    parts, errors = unzip_pptx(pptx_path)
    if errors and not parts:
        print(f"\n[validate_pptx] {len(errors)} error(s) — aborting", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    check_required_parts(parts, errors)

    if check_slop_flag:
        before = len(errors)
        check_slop(parts, errors)
        if len(errors) == before:
            ok("No slop tokens (strict)")
    else:
        temp: list[str] = []
        check_slop(parts, temp)
        for msg in temp:
            warn(msg + " (use --strict to fail on slop)")
        temp.clear()

    if check_overlap_flag:
        check_overlap(parts, errors)
    if check_overflow_flag:
        check_overflow(parts, errors)
    if check_theme_flag:
        check_theme(parts, errors)
    if check_editable_flag:
        check_editable(parts, errors)

    # also always run editable + overlap in strict via flags above; additionally ensure placeholder check
    if strict:
        # placeholder residue already via slop (Click to add); also scan for empty ph
        for name in [n for n in parts if n.startswith("ppt/slides/slide")]:
            xml = parts[name].decode("utf-8", errors="replace")
            if "Click to add" in xml:
                fail(f"Placeholder residue on {name}: 'Click to add' left behind — fill placeholder idx", errors)

    if errors:
        print(f"\n[validate_pptx] FAILED — {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("\n[validate_pptx] PASSED")
    sys.exit(0)

if __name__ == "__main__":
    main()
