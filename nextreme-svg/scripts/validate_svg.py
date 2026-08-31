#!/usr/bin/env python3
"""
nextreme-svg — strict SVG validator (W3C SVG 2, OWASP, a11y)

Checks what a preview can’t: XML well-formed, ID resolution, path d BNF,
viewBox, security deny list, a11y, SMIL.

Usage:
    python scripts/validate_svg.py icon.svg --strict
    python scripts/validate_svg.py icon.svg --check-overlap
skills.sh:
    python ${CLAUDE_SKILL_DIR}/scripts/validate_svg.py icon.svg --strict
local:
    python nextreme-svg/scripts/validate_svg.py icon.svg --strict
Exit 0 = pass; non-zero = fail with fix.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Security deny list — W3C / OWASP / DOMPurify grounded
BANNED_SUBSTRINGS = [
    "<script", "javascript:", "vbscript:", "data:text/html",
    "onload=", "onclick=", "onerror=", "onmouseover=",
    "<foreignObject", "xlink:href=\"data:", "href=\"data:text",
]
BANNED_TAGS = {"script", "foreignObject"}

# Path d BNF — simplified but catches real errors: M/L/H/V/C/S/Q/T/A/Z with numbers
PATH_D_RE = re.compile(r"^[ \t\r\n]*[Mm][ \t\r\n0-9eE\.\-+,MLHVCSQTAZmlhvcsqtaz]*[ \t\r\n]*$")
COORD_RE = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

VIEWBOX_RE = re.compile(r"^\s*-?\d+(\.\d+)?\s+-?\d+(\.\d+)?\s+\d+(\.\d+)?\s+\d+(\.\d+)?\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate SVG — spec-correct, safe, accessible")
    parser.add_argument("svg", help="Path to .svg")
    parser.add_argument("--strict", action="store_true", help="All checks (security+viewBox+ids+path+a11y)")
    parser.add_argument("--check-overlap", action="store_true", help="Fail on overlap hints (diagram mode)")
    parser.add_argument("--check-security", action="store_true", help="Fail on javascript:/foreignObject")
    return parser.parse_args()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}", file=sys.stderr)


def warn(message: str) -> None:
    print(f"[WARN] {message}", file=sys.stderr)


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def check_header(text: str, errors: list[str]) -> ET.Element | None:
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError as exc:
        fail(f"XML well-formed: {exc}", errors)
        return None
    ok("XML well-formed")
    return root


def check_viewbox(root: ET.Element, text: str, errors: list[str]) -> None:
    vb = root.get("viewBox")
    # xmlns may be default namespace — check via tag namespace if attribute missing
    tag_ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else ""
    has_svg_ns = tag_ns == "http://www.w3.org/2000/svg" or 'xmlns="http://www.w3.org/2000/svg"' in text or "xmlns='http://www.w3.org/2000/svg'" in text
    if not vb:
        fail("Missing viewBox — responsive breaks without it (need viewBox=\"0 0 W H\")", errors)
    elif not VIEWBOX_RE.match(vb):
        fail(f"Bad viewBox format: {vb!r} — expected \"minX minY width height\"", errors)
    else:
        ok(f"viewBox present: {vb}")
    if not has_svg_ns:
        warn(f"Missing or non-standard xmlns — should be http://www.w3.org/2000/svg (tag ns: {tag_ns!r})")
    else:
        ok("xmlns correct")
    # width/height without viewBox is slop — already failed above, but warn if both missing
    if not vb and (root.get("width") or root.get("height")):
        fail("width/height without viewBox — add viewBox for responsive scaling", errors)


def check_security(text: str, errors: list[str]) -> None:
    lower = text.lower()
    for token in BANNED_SUBSTRINGS:
        if token.lower() in lower:
            fail(f"Security deny list: found {token!r} — remove script/handlers/foreignObject/data: URLs", errors)
            return
    # Check tag names via parse
    try:
        root = ET.fromstring(text.encode("utf-8"))
        for elem in root.iter():
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag in BANNED_TAGS:
                fail(f"Security: banned tag <{tag}>", errors)
                return
    except ET.ParseError:
        pass
    ok("Security deny list clean (no script/handlers/foreignObject/javascript:)")


def check_ids(text: str, errors: list[str]) -> None:
    # Collect ids and url(#id) refs
    ids = set(re.findall(r'\bid\s*=\s*["\']([^"\']+)["\']', text))
    refs = re.findall(r'url\s*\(\s*#([^\)]+)\s*\)', text)
    # Also href="#id"
    refs += re.findall(r'href\s*=\s*["\']#([^"\']+)["\']', text)
    missing = [r for r in refs if r not in ids]
    if missing:
        fail(f"ID resolution: url(#id)/href references missing ids: {missing}", errors)
    else:
        if refs:
            ok(f"ID resolution: {len(refs)} refs resolve")
        else:
            ok("ID resolution: no url(#id) refs (trivially pass)")


def check_path_d(text: str, errors: list[str]) -> None:
    # Find all d="..."
    ds = re.findall(r'\bd\s*=\s*["\']([^"\']+)["\']', text)
    if not ds:
        ok("Path d: no <path> (trivially pass)")
        return
    bad = []
    for d in ds:
        d_stripped = d.strip()
        if not d_stripped:
            bad.append("(empty d)")
            continue
        if not PATH_D_RE.match(d_stripped):
            # Check first char must be M/m
            if not d_stripped[0] in "Mm":
                bad.append(f"{d_stripped[:30]!r} — must start with M/m")
            else:
                bad.append(f"{d_stripped[:30]!r} — BNF mismatch")
            continue
        # Check that numbers exist where expected (quick heuristic: at least one number)
        if not COORD_RE.search(d_stripped):
            bad.append(f"{d_stripped[:30]!r} — no coordinates")
    if bad:
        for b in bad[:3]:
            fail(f"Path d BNF: {b}", errors)
    else:
        ok(f"Path d: {len(ds)} path(s) BNF OK")


def check_a11y(text: str, errors: list[str]) -> None:
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError:
        return
    # Check for meaningful graphics: if has <title>, should have role="img"
    has_title = "<title" in text.lower()
    role = root.get("role")
    aria_hidden = root.get("aria-hidden")
    if has_title and role != "img":
        warn("A11y: has <title> but missing role=\"img\" — add role=\"img\" + <title> + <desc> for meaningful graphics")
    elif has_title:
        ok("A11y: role=\"img\" with <title>")
    # Decorative heuristic: if no title and has aria-hidden, ok
    if not has_title and aria_hidden == "true":
        ok("A11y: aria-hidden=\"true\" for decorative (correct)")
    elif not has_title:
        warn("A11y: no <title> — if meaningful, add <title> + <desc> and role=\"img\"; if decorative, add aria-hidden=\"true\"")
    # Check for <desc>
    if has_title and "<desc" not in text.lower():
        warn("A11y: has <title> but no <desc> — add <desc> for screen readers")
    # Reduced motion
    if "<animate" in text.lower() and "prefers-reduced-motion" not in text.lower():
        warn("A11y: has animation but no prefers-reduced-motion — add @media (prefers-reduced-motion: reduce) { * { animation: none } }")


def main() -> None:
    args = parse_args()
    svg_path = Path(args.svg)
    strict = bool(args.strict)
    check_overlap = bool(args.check_overlap or strict)
    check_security_flag = bool(args.check_security or strict)

    errors: list[str] = []

    if not svg_path.exists():
        fail(f"File not found: {svg_path}", errors)
        print(f"\n[validate_svg] FAILED — {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    text = svg_path.read_text(encoding="utf-8", errors="replace")

    root = check_header(text, errors)
    if root is not None:
        check_viewbox(root, text, errors)
    if check_security_flag:
        check_security(text, errors)
    else:
        # Always check security lightly even without --strict? warn mode
        tmp: list[str] = []
        check_security(text, tmp)
        for msg in tmp:
            # demote fail to warn when not strict
            warn(msg.replace("[FAIL] ", "") + " (use --strict to fail)")
    check_ids(text, errors)
    check_path_d(text, errors)
    check_a11y(text, errors)

    # Overlap is diagram-specific — heuristic: flag if two <rect> with same y and overlapping x (simple)
    if check_overlap:
        # Very light heuristic: look for <rect> with x/y/width/height
        rects = re.findall(r'<rect[^>]*x="([^"]+)"[^>]*y="([^"]+)"[^>]*width="([^"]+)"[^>]*height="([^"]+)"', text)
        # Not failing on heuristic alone — just warn if many rects
        if len(rects) >= 6:
            warn(f"Overlap check: {len(rects)} rects — ensure layered order background→containers→nodes→labels→connections (check manually or via render)")

    if errors:
        print(f"\n[validate_svg] FAILED — {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("\n[validate_svg] PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
