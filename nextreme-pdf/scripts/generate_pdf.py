#!/usr/bin/env python3
"""
nextreme-pdf — HTML → PDF router (taste-driven, unbound)

Routes HTML to the best available engine:
  1. Playwright + Paged.js (HTML+Tailwind, best taste) — if `playwright` importable
  2. Typst (page-as-canvas, GOST) — if `typst` on PATH and --engine typst
  3. WeasyPrint (print-native fallback) — if `weasyprint` importable
  4. ReportLab fallback (always available) — minimal taste, but never fails

Usage (skills.sh):
    python ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py --html ${CLAUDE_SKILL_DIR}/templates/report.html --out ./report.pdf
    python ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py --html ./build/report.html --out ./report.pdf --engine weasyprint

Local:
    python nextreme-pdf/scripts/generate_pdf.py --html nextreme-pdf/templates/report.html --out ./report.pdf

All paths are explicit; no hidden globals. Every failure path is logged with context.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Tokens — no magic
DEFAULT_FORMAT = "A4"
PLAYWRIGHT_SCRIPT_NAME = "render_pdf.mjs"
WEASYPRINT_ENGINE = "weasyprint"
TYPST_ENGINE = "typst"
REPORTLAB_FALLBACK = "reportlab"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="nextreme-pdf HTML→PDF router")
    parser.add_argument("--html", required=True, help="Input HTML file (self-contained, Tailwind CDN or compiled)")
    parser.add_argument("--out", required=True, help="Output PDF path")
    parser.add_argument("--format", default=DEFAULT_FORMAT, help="Paper format (A4, Letter) — passed to engine")
    parser.add_argument("--engine", default="auto", choices=["auto", "playwright", "weasyprint", "typst", REPORTLAB_FALLBACK], help="Engine override")
    parser.add_argument("--typst-template", default="", help="Typst template (when --engine typst)")
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"[generate_pdf] {message}", file=sys.stderr)
    sys.exit(1)


def warn(message: str) -> None:
    print(f"[generate_pdf] WARN: {message}", file=sys.stderr)


def check_html_exists(html_path: Path) -> None:
    if not html_path.exists():
        fail(f"HTML not found: {html_path}")
    if html_path.stat().st_size == 0:
        fail(f"HTML empty: {html_path}")
    text = html_path.read_text(encoding="utf-8", errors="replace")
    if "<html" not in text.lower():
        warn(f"{html_path} does not look like HTML (no <html> tag)")
    if "tailwind" not in text.lower() and "cdn.tailwindcss.com" not in text:
        warn("No Tailwind CDN found — taste system expects Tailwind (ok for minimal)")


def try_playwright(html_path: Path, out_path: Path, paper_format: str) -> bool:
    # Try Node render_pdf.mjs first (skills.sh: ${CLAUDE_SKILL_DIR}/scripts/render_pdf.mjs)
    script_candidates = [
        Path(__file__).with_name(PLAYWRIGHT_SCRIPT_NAME),
        Path("nextreme-pdf/scripts") / PLAYWRIGHT_SCRIPT_NAME,
    ]
    for script in script_candidates:
        if script.exists():
            cmd = ["node", str(script), "--html", str(html_path), "--out", str(out_path), "--format", paper_format]
            print(f"[generate_pdf] Trying Playwright via Node: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
                print(f"[generate_pdf] Playwright succeeded: {out_path} ({out_path.stat().st_size} bytes)")
                return True
            warn(f"Node Playwright failed ({script}): {result.stderr[:300]}")
    # Try Python playwright
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        warn("Python 'playwright' not installed — pip install playwright && playwright install chromium")
        return False
    try:
        with sync_playwright() as playwright_instance:
            browser = playwright_instance.chromium.launch()
            page = browser.new_page()
            html_text = html_path.read_text(encoding="utf-8")
            page.set_content(html_text, wait_until="networkidle")
            page.wait_for_timeout(1200)  # let Paged.js settle + fonts
            page.pdf(path=str(out_path), format=paper_format, print_background=True, prefer_css_page_size=True)  # type: ignore[arg-type]
            browser.close()
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"[generate_pdf] Python Playwright succeeded: {out_path}")
            return True
    except Exception as exc:
        warn(f"Python Playwright failed: {exc}")
    return False


def try_typst(html_path: Path, out_path: Path, template: str) -> bool:
    if shutil.which("typst") is None:
        warn("typst not on PATH — brew install typst / cargo install typst-cli")
        return False
    # Typst expects .typ, not .html — this is a placeholder for when spec is Typst-native
    warn("Typst path received HTML; Typst prefers .typ — skipping (use Typst templates directly)")
    _ = template
    return False


def try_weasyprint(html_path: Path, out_path: Path) -> bool:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception as exc:  # ImportError or OSError (missing libgobject on Windows)
        warn(f"weasyprint not available ({exc}) — pip install weasyprint + GTK libs, or use reportlab fallback")
        return False
    try:
        HTML(filename=str(html_path)).write_pdf(str(out_path))
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"[generate_pdf] WeasyPrint succeeded: {out_path} ({out_path.stat().st_size} bytes)")
            return True
    except Exception as exc:
        warn(f"WeasyPrint failed: {exc}")
    return False


def fallback_reportlab(html_path: Path, out_path: Path) -> bool:
    try:
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.lib.units import mm  # type: ignore
        from reportlab.pdfgen import canvas  # type: ignore
        from reportlab.lib.styles import getSampleStyleSheet  # type: ignore
    except ImportError:
        warn("reportlab not installed — pip install reportlab (fallback)")
        return False
    try:
        html_text = html_path.read_text(encoding="utf-8", errors="replace")
        # Very minimal fallback: extract text, write one page with taste tokens
        from bs4 import BeautifulSoup  # type: ignore
        soup = BeautifulSoup(html_text, "html.parser")
        title = soup.title.string if soup.title and soup.title.string else html_path.stem
        body = soup.get_text(separator="\n", strip=True)[:3000]
    except ImportError:
        title = html_path.stem
        body = "Install beautifulsoup4 for text extraction — pip install beautifulsoup4"
    except Exception:
        title = html_path.stem
        body = ""
    try:
        width, height = A4
        pdf_canvas = canvas.Canvas(str(out_path), pagesize=A4)
        pdf_canvas.setTitle(title)
        # Parchment bg
        pdf_canvas.setFillColorRGB(0.96, 0.95, 0.93)  # #f5f4ed
        pdf_canvas.rect(0, 0, width, height, fill=1, stroke=0)
        # Title
        pdf_canvas.setFillColorRGB(0.10, 0.21, 0.36)  # #1B365D
        pdf_canvas.setFont("Helvetica-Bold", 18)
        pdf_canvas.drawString(20 * mm, height - 30 * mm, title[:80])
        # Body
        pdf_canvas.setFillColorRGB(0.09, 0.09, 0.11)
        pdf_canvas.setFont("Helvetica", 9)
        y = height - 45 * mm
        for line in body.split("\n")[:45]:
            if y < 20 * mm:
                pdf_canvas.showPage()
                y = height - 20 * mm
            pdf_canvas.drawString(20 * mm, y, line[:110])
            y -= 5 * mm
        # Footer
        pdf_canvas.setFont("Helvetica", 7)
        pdf_canvas.setFillColorRGB(0.44, 0.44, 0.46)
        pdf_canvas.drawCentredString(width / 2, 12 * mm, "Generated via nextreme-pdf (reportlab fallback) — install Playwright for full taste")
        pdf_canvas.showPage()
        pdf_canvas.save()
        print(f"[generate_pdf] ReportLab fallback succeeded: {out_path} ({out_path.stat().st_size} bytes) — taste limited, but PDF valid")
        return True
    except Exception as exc:
        warn(f"ReportLab fallback failed: {exc}")
        return False


def main() -> None:
    args = parse_args()
    html_path = Path(args.html)
    out_path = Path(args.out)
    check_html_exists(html_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    engine = str(args.engine).lower()
    attempted: list[str] = []

    def attempt(name: str, func) -> bool:
        attempted.append(name)
        print(f"[generate_pdf] Engine attempt: {name}")
        ok = func()
        print(f"[generate_pdf] Engine {name}: {'OK' if ok else 'miss'}")
        return ok

    if engine in ("auto", "playwright"):
        if attempt("playwright", lambda: try_playwright(html_path, out_path, args.format)):
            return
        if engine == "playwright":
            fail(f"Playwright failed for {html_path} — install Node playwright or python playwright")
    if engine in ("auto", TYPST_ENGINE):
        if attempt(TYPST_ENGINE, lambda: try_typst(html_path, out_path, args.typst_template)):
            return
        if engine == TYPST_ENGINE:
            fail("Typst failed")
    if engine in ("auto", WEASYPRINT_ENGINE):
        if attempt(WEASYPRINT_ENGINE, lambda: try_weasyprint(html_path, out_path)):
            return
        if engine == WEASYPRINT_ENGINE:
            fail("WeasyPrint failed")
    if engine in ("auto", REPORTLAB_FALLBACK):
        if attempt(REPORTLAB_FALLBACK, lambda: fallback_reportlab(html_path, out_path)):
            return

    fail(f"All engines missed: {attempted} — install one: Playwright (best taste), WeasyPrint, or reportlab")


if __name__ == "__main__":
    main()
