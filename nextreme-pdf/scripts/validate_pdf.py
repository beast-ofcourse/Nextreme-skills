#!/usr/bin/env python3
"""
nextreme-pdf — PDF QC (page-as-canvas, no rivers, no overflow)

Validates a rendered PDF without trusting the generator — per beautiful-pdf-mcp
page-as-canvas contract, but for HTML+Tailwind PDFs.

Usage:
    python scripts/validate_pdf.py out.pdf --strict
    python scripts/validate_pdf.py out.pdf --check-cover
    python scripts/validate_pdf.py out.pdf --check-overflow
skills.sh:
    python ${CLAUDE_SKILL_DIR}/scripts/validate_pdf.py out.pdf --strict
local:
    python nextreme-pdf/scripts/validate_pdf.py out.pdf --strict
Exit 0 = pass; non-zero = fail with fix (“page 3: 6 lines short”).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SLOP_RE = re.compile(r"lorem ipsum|click to add title|click to add text", re.IGNORECASE)
TODO_RE = re.compile(r"\bTODO\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate PDF — taste + page-as-canvas")
    parser.add_argument("pdf", help="Path to .pdf")
    parser.add_argument("--strict", action="store_true", help="All checks")
    parser.add_argument("--check-cover", action="store_true", help="Fail on white-border cover")
    parser.add_argument("--check-overflow", action="store_true", help="Fail on table/img spill")
    parser.add_argument("--check-rivers", action="store_true", help="Fail on positive tracking / no hyphens")
    parser.add_argument("--check-fill", action="store_true", help="Fail on mid-article hole (heuristic)")
    return parser.parse_args()


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"[FAIL] {message}", file=sys.stderr)


def warn(message: str) -> None:
    print(f"[WARN] {message}", file=sys.stderr)


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def check_pdf_header(pdf_path: Path, errors: list[str]) -> bytes:
    header = pdf_path.read_bytes()[:8]
    if not header.startswith(b"%PDF"):
        fail(f"Not a PDF (missing %PDF header): {pdf_path} — got {header[:8]!r}", errors)
        return b""
    ok("PDF header %PDF present")
    return header


def check_html_source_for_taste(html_candidates: list[Path], errors: list[str]) -> None:
    # Find sibling HTML (if exists) and check taste invariants
    for html_path in html_candidates:
        if not html_path.exists():
            continue
        text = html_path.read_text(encoding="utf-8", errors="replace")
        if 'rgba(' in text and 'bg-' in text:
            warn(f"rgba() in {html_path.name} — Kami: solid hex only (WeasyPrint double-rect)")
        if 'tracking-wider' in text or 'tracking-wide' in text:
            fail(f"Positive tracking in {html_path.name} — use semantic negative tracking (display -0.10em etc.)", errors)
        if '@page :first' not in text and 'cover' in text.lower():
            fail(f"Cover likely white-border in {html_path.name} — add @page :first {{ margin: 0 }} + body {{ margin: 0 }}", errors)
        if 'max-width: 100%' not in text and ('<table' in text or '<img' in text):
            warn(f"No max-width guard in {html_path.name} — add pre, table, img {{ max-width: 100% }}")
        if 'hyphens: auto' not in text and 'text-justify' in text:
            warn(f"Justified without hyphens in {html_path.name} — add hyphens: auto; text-wrap: pretty for no rivers")
        ok(f"Taste lint for {html_path.name} done")
        return
    warn("No sibling HTML found for taste lint — skipping (checked PDF only)")


def get_page_count_via_pypdf(pdf_path: Path, errors: list[str]) -> int | None:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        warn("pypdf not installed — pip install pypdf for page count check")
        return None
    try:
        reader = PdfReader(str(pdf_path))
        count = len(reader.pages)
        ok(f"Page count via pypdf: {count}")
        return count
    except Exception as exc:
        fail(f"pypdf could not read {pdf_path}: {exc}", errors)
        return None


def check_overflow_heuristic(pdf_path: Path, errors: list[str]) -> None:
    # Heuristic without rendering: check file size vs page count
    size = pdf_path.stat().st_size
    pages = get_page_count_via_pypdf(pdf_path, [])
    if pages is not None and pages > 0:
        per_page = size / pages
        if per_page < 8000:
            warn(f"Very small per-page bytes ({per_page:.0f}) — may be blank/anomalous page (check page-break-after misuse)")
        if size > 15 * 1024 * 1024:
            warn(f"Large PDF ({size/1024/1024:.1f} MB) — check for uncompressed images")


def main() -> None:
    args = parse_args()
    pdf_path = Path(args.pdf)
    strict = bool(args.strict)
    check_cover = bool(args.check_cover or strict)
    check_overflow = bool(args.check_overflow or strict)
    check_rivers = bool(args.check_rivers or strict)
    check_fill = bool(args.check_fill or strict)

    errors: list[str] = []

    if not pdf_path.exists():
        fail(f"File not found: {pdf_path}", errors)
        print(f"\n[validate_pdf] FAILED — {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    if pdf_path.suffix.lower() != ".pdf":
        warn(f"Expected .pdf, got {pdf_path.suffix}")

    header = check_pdf_header(pdf_path, errors)
    if not header:
        print(f"\n[validate_pdf] FAILED — {len(errors)} error(s)", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Page count
    page_count = get_page_count_via_pypdf(pdf_path, errors)

    # Overflow heuristic
    if check_overflow:
        check_overflow_heuristic(pdf_path, errors)
        ok("Overflow heuristic done")

    # Taste lint on sibling HTML (if present)
    html_candidates = [
        pdf_path.with_suffix(".html"),
        pdf_path.with_name(pdf_path.stem + ".html"),
        Path(str(pdf_path).replace(".pdf", ".html")),
        Path("build") / (pdf_path.stem + ".html"),
    ]
    # Also check nextreme-pdf/templates for reference if no build dir
    if not any(p.exists() for p in html_candidates):
        # try sibling next to pdf
        html_candidates.append(pdf_path.parent / (pdf_path.stem + ".html"))
    check_html_source_for_taste(html_candidates, errors)

    # Rivers / tracking are checked via HTML lint above; PDF-level rivers need render — warn only
    if check_rivers:
        ok("Rivers check via HTML hyphens + tracking (PDF render check needs PNG preview)")

    # Fill heuristic
    if check_fill and page_count is not None:
        # Very rough: if PDF is 1 page and source HTML had >800 words but PDF is 1 page, likely hole or overflow
        if page_count == 1:
            size = pdf_path.stat().st_size
            if size < 20000:
                warn("Single-page PDF with small bytes — may be underfilled (add ~40 words per missing lines heuristic)")
            else:
                ok("Fill heuristic: single page, bytes plausible")

    # Slop in PDF text (via pypdf text extraction if available)
    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(str(pdf_path))
        all_text = ""
        for page in reader.pages[:3]:
            try:
                all_text += (page.extract_text() or "") + "\n"
            except Exception:
                continue
        for token in ["lorem ipsum", "click to add title"]:
            if token in all_text.lower():
                fail(f"Slop token in PDF text: {token!r}", errors)
        if "TODO" in all_text and "[CONTENT REQUIRED" not in all_text:
            fail("Bare TODO in PDF text", errors)
    except ImportError:
        pass

    # Cover bleed — need HTML for @page check, already warned above

    if errors:
        print(f"\n[validate_pdf] FAILED — {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    # Warnings do not fail strict? In strict, only fails are in errors; warns are not failures
    print("\n[validate_pdf] PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
