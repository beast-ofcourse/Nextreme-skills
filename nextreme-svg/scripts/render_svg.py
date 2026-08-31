#!/usr/bin/env python3
"""
nextreme-svg — SVG → PNG at 2× (render-verify-fix loop)

Renders SVG to PNG via CairoSVG (preferred) or librsvg fallback for visual self-review.
Scale 2× = crisp on retina and for social share.

Usage:
    python scripts/render_svg.py icon.svg --out icon.png --scale 2
    python scripts/render_svg.py icon.svg --out icon.png --scale 1
skills.sh:
    python ${CLAUDE_SKILL_DIR}/scripts/render_svg.py icon.svg --out icon.png --scale 2
local:
    python nextreme-svg/scripts/render_svg.py icon.svg --out icon.png --scale 2

Exit 0 = rendered; non-zero = fail.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render SVG → PNG at 2× for verification")
    parser.add_argument("svg", help="Input .svg")
    parser.add_argument("--out", required=True, help="Output .png")
    parser.add_argument("--scale", type=float, default=2.0, help="Scale factor (2.0 = 2× viewBox, crisp)")
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"[render_svg] {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    args = parse_args()
    svg_path = Path(args.svg)
    out_path = Path(args.out)
    scale = float(args.scale)

    if not svg_path.exists():
        fail(f"SVG not found: {svg_path}")
    if scale <= 0 or scale > 4:
        fail(f"Scale must be 0-4, got {scale}")

    # Try CairoSVG first (pure Python + Cairo)
    try:
        import cairosvg  # type: ignore

        # Read SVG to get viewBox size for intrinsic sizing
        svg_text = svg_path.read_text(encoding="utf-8")
        # Let CairoSVG handle sizing via viewBox; we scale by dpi
        # CairoSVG 2.7: cairosvg.svg2png(url=..., write_to=..., scale=2)
        cairosvg.svg2png(url=str(svg_path), write_to=str(out_path), scale=scale)  # type: ignore[arg-type]
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"[render_svg] Wrote {out_path} ({out_path.stat().st_size} bytes) via CairoSVG scale={scale}")
            sys.exit(0)
        else:
            fail("CairoSVG produced no output")
    except ImportError:
        print("[render_svg] CairoSVG not installed — pip install cairosvg (or use librsvg fallback)", file=sys.stderr)
    except Exception as exc:
        print(f"[render_svg] CairoSVG failed: {exc}", file=sys.stderr)

    # Fallback: try rsvg-convert (librsvg)
    import shutil
    import subprocess

    if shutil.which("rsvg-convert") is not None:
        try:
            # rsvg-convert --zoom 2 --keep-aspect-ratio
            result = subprocess.run(
                ["rsvg-convert", "-z", str(scale), "-o", str(out_path), str(svg_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and out_path.exists():
                print(f"[render_svg] Wrote {out_path} via rsvg-convert scale={scale}")
                sys.exit(0)
            else:
                print(f"[render_svg] rsvg-convert failed: {result.stderr[:300]}", file=sys.stderr)
        except Exception as exc:
            print(f"[render_svg] rsvg-convert error: {exc}", file=sys.stderr)

    # Last fallback: Chromium via playwright (if installed) — screenshot
    try:
        from playwright.sync_api import sync_playwright  # type: ignore

        html = f"""<!DOCTYPE html><html><body style="margin:0;background:white;display:flex;align-items:center;justify-content:center;min-height:100vh"><img src="file://{svg_path.resolve()}" style="max-width:100%;height:auto"></body></html>"""
        tmp_html = out_path.with_suffix(".html")
        tmp_html.write_text(html, encoding="utf-8")
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{tmp_html.resolve()}")
            page.wait_for_timeout(400)
            page.screenshot(path=str(out_path), full_page=False)
            browser.close()
        tmp_html.unlink(missing_ok=True)
        if out_path.exists():
            print(f"[render_svg] Wrote {out_path} via Playwright screenshot")
            sys.exit(0)
    except ImportError:
        pass
    except Exception as exc:
        print(f"[render_svg] Playwright fallback failed: {exc}", file=sys.stderr)

    fail("No renderer available — install cairosvg (pip install cairosvg) or librsvg (rsvg-convert) or playwright")


if __name__ == "__main__":
    main()
