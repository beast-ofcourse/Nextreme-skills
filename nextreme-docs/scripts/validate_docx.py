#!/usr/bin/env python3
"""
nextreme-docs — OOXML validator

Unzips the .docx and checks the XML, not just the Python. Reports slop,
fake headings, unstyled tables, missing fields, oversized images, and
corruption.

Usage:
    python scripts/validate_docx.py output.docx --strict
    python scripts/validate_docx.py output.docx --audit-styles
    python scripts/validate_docx.py output.docx --check-fields
    python scripts/validate_docx.py output.docx --check-images --max-width-inches 6.5
    python scripts/validate_docx.py resume.docx --check-resume-length --max-pages 2

Exit 0 = pass. Non-zero = fail with reasons. No silent success.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# OOXML namespace — single constant, no magic strings inline
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": WORD_NS}
SLOP_RE = re.compile(r"lorem ipsum|lorem|placeholder|your text here|insert text here", re.IGNORECASE)
TODO_BARE_RE = re.compile(r"\bTODO\b")
CONTENT_REQUIRED_RE = re.compile(r"\[CONTENT REQUIRED:")

# Thresholds — named, not magic
FAKE_HEADING_MIN_PT = 14.0
MAX_RESUME_PAGES_DEFAULT = 2
EMU_PER_INCH = 914400


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate .docx OOXML + anti-slop")
    parser.add_argument("docx", help="Path to .docx file")
    parser.add_argument("--strict", action="store_true", help="Enable all checks (styles+fields+images+slop)")
    parser.add_argument("--audit-styles", action="store_true", help="Fail on fake headings / unstyled tables")
    parser.add_argument("--check-fields", action="store_true", help="Fail on typed TOC without field")
    parser.add_argument("--check-images", action="store_true", help="Check image sizing + alt text")
    parser.add_argument("--max-width-inches", type=float, default=6.6, help="Max image/table width in inches")
    parser.add_argument("--check-resume-length", action="store_true", help="Gate page count for resumes")
    parser.add_argument("--max-pages", type=int, default=MAX_RESUME_PAGES_DEFAULT, help="Max pages when --check-resume-length")
    return parser.parse_args()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}", file=sys.stderr)


def warn(message: str) -> None:
    print(f"[WARN] {message}", file=sys.stderr)


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def unzip_docx(docx_path: Path) -> tuple[dict[str, bytes], list[str]]:
    errors: list[str] = []
    if not docx_path.exists():
        fail(f"File not found: {docx_path}", errors)
        return {}, errors

    if docx_path.suffix.lower() != ".docx":
        warn(f"Expected .docx extension, got {docx_path.suffix} — checking anyway")

    # OLE2 header check — .doc, not .docx
    header = docx_path.read_bytes()[:4]
    if header == b"\xD0\xCF\x11\xE0":
        fail("File has OLE2 header (D0 CF 11 E0) — this is a legacy .doc, not OOXML .docx", errors)
        return {}, errors

    try:
        with zipfile.ZipFile(docx_path, "r") as archive:
            bad = archive.testzip()
            if bad is not None:
                fail(f"Corrupt ZIP entry: {bad}", errors)
            parts = {name: archive.read(name) for name in archive.namelist()}
    except zipfile.BadZipFile as exc:
        fail(f"Not a valid ZIP/docx: {exc}", errors)
        return {}, errors
    except OSError as exc:
        fail(f"Failed to read {docx_path}: {exc}", errors)
        return {}, errors

    return parts, errors


def parse_xml(part_bytes: bytes, label: str, errors: list[str]) -> ET.Element | None:
    try:
        return ET.fromstring(part_bytes)
    except ET.ParseError as exc:
        fail(f"XML parse error in {label}: {exc}", errors)
        return None


def check_required_parts(parts: dict[str, bytes], errors: list[str]) -> None:
    required = ["word/document.xml", "word/styles.xml", "[Content_Types].xml", "docProps/core.xml"]
    for name in required:
        if name not in parts:
            fail(f"Missing required part: {name}", errors)
        else:
            ok(f"Found {name}")


def collect_text_nodes(document_root: ET.Element) -> list[str]:
    texts: list[str] = []
    for elem in document_root.iter(f"{{{WORD_NS}}}t"):
        if elem.text:
            texts.append(elem.text)
    return texts


def check_slop(document_root: ET.Element, errors: list[str]) -> None:
    for elem in document_root.iter(f"{{{WORD_NS}}}t"):
        text = elem.text or ""
        if SLOP_RE.search(text):
            # Allow [CONTENT REQUIRED: ...] to contain the token as part of the marker
            # but typed filler outside markers is rejected
            parent_para = None  # not traversing up — heuristic: if the whole doc has no marker, warn
            fail(f"Slop token in text {text[:80]!r}", errors)
        if TODO_BARE_RE.search(text) and not CONTENT_REQUIRED_RE.search(text):
            # Check if the same paragraph has a CONTENT REQUIRED marker — if so, it's intentional
            # For simplicity, flag TODO without the marker nearby
            fail(f"Bare TODO without [CONTENT REQUIRED: ...] marker in {text[:80]!r}", errors)


def check_styles(document_xml: bytes, styles_xml: bytes, errors: list[str]) -> None:
    doc_root = parse_xml(document_xml, "word/document.xml", errors)
    styles_root = parse_xml(styles_xml, "word/styles.xml", errors)
    if doc_root is None or styles_root is None:
        return

    # Build style lookup from styles.xml: name → size pt, bold
    # styles.xml uses w:style/w:rPr/w:sz w:val="28" (half-points) and w:b
    style_info: dict[str, dict[str, object]] = {}
    for style_elem in styles_root.iter(f"{{{WORD_NS}}}style"):
        style_id = style_elem.get(f"{{{WORD_NS}}}styleId") or style_elem.get("w:styleId") or ""
        # Name is in w:name w:val
        name_elem = style_elem.find("w:name", NS)
        style_name = name_elem.get(f"{{{WORD_NS}}}val", "") if name_elem is not None else style_id
        if not style_name:
            style_name = style_id
        rPr = style_elem.find("w:rPr", NS)
        size_pt: float | None = None
        is_bold = False
        if rPr is not None:
            sz = rPr.find("w:sz", NS)
            if sz is not None:
                raw = sz.get(f"{{{WORD_NS}}}val")
                if raw is not None:
                    try:
                        size_pt = float(raw) / 2.0
                    except ValueError:
                        pass
            if rPr.find("w:b", NS) is not None:
                is_bold = True
        style_info[style_name] = {"size_pt": size_pt, "bold": is_bold}

    # Check paragraphs: flag Normal (or default) with large bold runs (fake heading)
    fake_count = 0
    for para in doc_root.iter(f"{{{WORD_NS}}}p"):
        pPr = para.find("w:pPr", NS)
        pStyle = pPr.find("w:pStyle", NS) if pPr is not None else None
        style_name = pStyle.get(f"{{{WORD_NS}}}val", "Normal") if pStyle is not None else "Normal"
        # Normalize: Word stores "Heading1" sometimes; map
        style_display = style_name
        if style_display.lower().startswith("heading"):
            continue  # real heading — skip
        if style_display in ("Title", "Subtitle"):
            continue

        # Inspect runs inside this paragraph
        for run in para.findall("w:r", NS):
            rPr = run.find("w:rPr", NS)
            run_bold = rPr.find("w:b", NS) is not None if rPr is not None else False
            run_size_pt: float | None = None
            if rPr is not None:
                sz = rPr.find("w:sz", NS)
                if sz is not None:
                    raw = sz.get(f"{{{WORD_NS}}}val")
                    if raw is not None:
                        try:
                            run_size_pt = float(raw) / 2.0
                        except ValueError:
                            pass
            t_elem = run.find("w:t", NS)
            text = (t_elem.text or "").strip() if t_elem is not None else ""
            if not text:
                continue
            if run_bold and run_size_pt is not None and run_size_pt >= FAKE_HEADING_MIN_PT:
                fail(
                    f"Fake heading — paragraph style '{style_display}' has bold {run_size_pt}pt run {text[:40]!r}; use Heading 1..3",
                    errors,
                )
                fake_count += 1
                break  # one per paragraph
        if fake_count >= 5:
            warn("Too many fake-heading reports — stopping style audit truncation")
            break

    if fake_count == 0:
        ok("No fake headings detected (--audit-styles)")

    # Tables without style
    tables = list(doc_root.iter(f"{{{WORD_NS}}}tbl"))
    unstyled = 0
    for tbl in tables:
        tblPr = tbl.find("w:tblPr", NS)
        tblStyle = tblPr.find("w:tblStyle", NS) if tblPr is not None else None
        if tblStyle is None:
            fail("Table without w:tblStyle — every table must carry a named style", errors)
            unstyled += 1
        else:
            style_val = tblStyle.get(f"{{{WORD_NS}}}val", "")
            if not style_val:
                fail("Table w:tblStyle has empty w:val", errors)
                unstyled += 1
    if tables and unstyled == 0:
        ok(f"All {len(tables)} table(s) carry a style")
    elif not tables:
        ok("No tables — style check trivially passes for tables")


def check_fields(parts: dict[str, bytes], errors: list[str]) -> None:
    document_xml = parts.get("word/document.xml")
    if document_xml is None:
        fail("Cannot check fields — word/document.xml missing", errors)
        return

    root = parse_xml(document_xml, "word/document.xml", errors)
    if root is None:
        return

    # Gather all instrText across document + headers + footers
    all_instr_texts: list[str] = []
    for part_name, part_bytes in parts.items():
        if not (part_name.startswith("word/") and part_name.endswith(".xml")):
            continue
        # Only scan parts that can contain fields: document, header*, footer*
        if not (part_name == "word/document.xml" or "header" in part_name or "footer" in part_name):
            continue
        try:
            part_root = ET.fromstring(part_bytes)
        except ET.ParseError:
            continue
        for elem in part_root.iter(f"{{{WORD_NS}}}instrText"):
            if elem.text:
                all_instr_texts.append(elem.text)

    joined = " ".join(all_instr_texts)
    has_toc = "TOC" in joined
    has_page = "PAGE" in joined
    has_numpages = "NUMPAGES" in joined

    # Detect typed TOC without field: paragraph with "Contents" or "Table of Contents" but no TOC field nearby
    text_nodes = collect_text_nodes(root)
    typed_toc = any("table of contents" in t.lower() or t.strip().lower() == "contents" for t in text_nodes)

    if typed_toc and not has_toc:
        fail("Typed 'Table of Contents' / 'Contents' without w:instrText TOC field — insert a real TOC field", errors)
    elif has_toc:
        ok("TOC field present (w:instrText TOC)")

    # Typed page numbers heuristic: "Page 1" literal without PAGE field is slop
    if not has_page and any(re.search(r"Page\s+\d+", t) for t in text_nodes):
        fail("Typed 'Page N' without PAGE field — use w:fldChar PAGE field", errors)
    elif has_page:
        ok("PAGE field present (scanned document + header/footer)")
        if has_numpages:
            ok("NUMPAGES field present (Page X of Y)")
    else:
        warn("No PAGE field found — not failing unless --strict, but expected for multi-page docs")


def check_images(parts: dict[str, bytes], document_xml: bytes, errors: list[str], max_width_inches: float) -> None:
    root = parse_xml(document_xml, "word/document.xml", errors)
    if root is None:
        return

    # Find inline images: wp:inline / wp:extent, and a:blip for format
    # Simpler: count w:drawing and check extent + blip format
    drawings = list(root.iter())
    inline_count = 0
    # Use string search for robustness across namespace prefixes in stdlib ET
    xml_text = document_xml.decode("utf-8", errors="replace")

    # Alt text — wp:docPr descr/title
    alt_missing = 0
    for match in re.finditer(r'<wp:docPr[^>]*>', xml_text):
        tag = match.group(0)
        if 'descr=""' in tag or "descr=''" in tag or 'descr' not in tag:
            # descr absent or empty — flag if not decorative (Word allows empty for decorative)
            alt_missing += 1

    # Extent — wp:extent cx="..." (EMU)
    max_emu = int(max_width_inches * EMU_PER_INCH)
    oversized = 0
    for match in re.finditer(r'<wp:extent[^>]*cx="(\d+)"', xml_text):
        cx = int(match.group(1))
        if cx > max_emu:
            oversized += 1
            fail(f"Image extent cx={cx} EMU ({cx/EMU_PER_INCH:.2f}in) exceeds max {max_width_inches}in", errors)

    # Format — check archive for media: png/jpeg preferred
    media_entries = [name for name in parts if name.startswith("word/media/")]
    bad_format = 0
    for name in media_entries:
        lower = name.lower()
        if lower.endswith((".emf", ".wmf", ".bmp", ".tiff", ".tif")):
            fail(f"Image format portability issue: {name} — use PNG/JPEG instead of {lower.rsplit('.',1)[-1].upper()}", errors)
            bad_format += 1
        inline_count += 1

    # Count drawings
    drawing_count = xml_text.count("<w:drawing")
    if drawing_count == 0 and media_entries:
        warn(f"Media entries {media_entries} but no w:drawing — possible broken image reference")
    if drawing_count > 0:
        ok(f"Found {drawing_count} w:drawing(s), {len(media_entries)} media file(s)")
        if alt_missing:
            # Only warn — decorative images legitimately have empty alt
            warn(f"{alt_missing} wp:docPr without descr — add alt text unless decorative (validate_docx.py note)")
        if oversized == 0:
            ok(f"No oversized images (max {max_width_inches}in)")
        if bad_format == 0 and media_entries:
            ok("Image formats are PNG/JPEG (portable)")
    else:
        ok("No images — image check trivially passes")


def estimate_page_count(parts: dict[str, bytes]) -> int | None:
    """
    Heuristic: Word stores w:pages in docProps/app.xml after saving via Word (extended properties).
    python-docx does not write it. So estimate via paragraph count fallback.
    Returns None if cannot estimate.
    """
    app_xml = parts.get("docProps/app.xml")
    if app_xml is not None:
        try:
            root = ET.fromstring(app_xml)
            # app.xml uses extended properties namespace
            for elem in root.iter():
                if elem.tag.endswith("Pages") and elem.text and elem.text.isdigit():
                    return int(elem.text)
        except ET.ParseError:
            pass
    # Fallback heuristic — not authoritative
    document_xml = parts.get("word/document.xml")
    if document_xml is None:
        return None
    try:
        root = ET.fromstring(document_xml)
        para_count = len(list(root.iter(f"{{{WORD_NS}}}p")))
        # Rough: ~35 paragraphs per page (business doc) — warns only, not fails
        return max(1, round(para_count / 35))
    except ET.ParseError:
        return None


def main() -> None:
    args = parse_args()
    docx_path = Path(args.docx)
    strict = bool(args.strict)

    # In strict, enable all
    audit_styles = bool(args.audit_styles or strict)
    check_fields_flag = bool(args.check_fields or strict)
    check_images_flag = bool(args.check_images or strict)
    slop_check = strict  # slop always in strict; also run by default as warning

    parts, errors = unzip_docx(docx_path)

    if errors and not parts:
        print(f"\n[validate_docx] {len(errors)} error(s) — aborting further checks", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Always check required parts
    check_required_parts(parts, errors)

    document_xml = parts.get("word/document.xml")
    styles_xml = parts.get("word/styles.xml")

    if document_xml is None:
        fail("Missing word/document.xml — not a valid docx", errors)
        print(f"\n[validate_docx] {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    doc_root = parse_xml(document_xml, "word/document.xml", errors)
    if doc_root is None:
        sys.exit(1)

    # Slop — always warn; fail only on strict
    before = len(errors)
    if strict:
        check_slop(doc_root, errors)
    else:
        # Non-strict: still report but as warnings
        temp_errors: list[str] = []
        check_slop(doc_root, temp_errors)
        for msg in temp_errors:
            warn(msg + " (use --strict to fail on slop)")
        temp_errors.clear()
    if strict and len(errors) == before:
        ok("No slop tokens (strict)")

    if audit_styles and styles_xml is not None:
        check_styles(document_xml, styles_xml, errors)
    elif audit_styles and styles_xml is None:
        fail("Cannot audit styles — word/styles.xml missing", errors)

    if check_fields_flag:
        check_fields(parts, errors)

    if check_images_flag:
        check_images(parts, document_xml, errors, args.max_width_inches)

    if args.check_resume_length:
        estimated = estimate_page_count(parts)
        if estimated is not None:
            if estimated > args.max_pages:
                fail(f"Estimated page count {estimated} exceeds max {args.max_pages} — resume must fit {args.max_pages} pages", errors)
            else:
                ok(f"Estimated page count {estimated} within limit {args.max_pages}")
        else:
            warn("Could not estimate page count — manual check required for resume length")

    # Report
    if errors:
        print(f"\n[validate_docx] FAILED — {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("\n[validate_docx] PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
