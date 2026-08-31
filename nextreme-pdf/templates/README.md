# Templates — Taste-Driven HTML for Nextreme PDF

Copy an HTML, replace the bracketed content with real story, render via `generate_pdf.py` (or `render_pdf.mjs`). Every template is a self-contained HTML with Tailwind CDN (or compiled Oxide) + Paged.js-ready `@page`, zinc or parchment taste, geometric spacing, and one-accent law.

**Install once:**

```bash
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt
# for HTML+Tailwind+Playwright (best taste):
npm install -D playwright && npx playwright install chromium
# optional: Typst for GOST/book page-as-canvas
brew install typst
```

**Render:**

```bash
# skills.sh — HTML+Tailwind → PDF (auto-engine)
python ${CLAUDE_SKILL_DIR}/scripts/generate_pdf.py --html ${CLAUDE_SKILL_DIR}/templates/report.html --out ./report.pdf
# local clone
python nextreme-pdf/scripts/generate_pdf.py --html nextreme-pdf/templates/report.html --out ./report.pdf

# Node direct (Playwright + Paged.js)
node ${CLAUDE_SKILL_DIR}/scripts/render_pdf.mjs --html ${CLAUDE_SKILL_DIR}/templates/report.html --out ./report.pdf --format A4

# Validate (page-as-canvas QC)
python ${CLAUDE_SKILL_DIR}/scripts/validate_pdf.py ./report.pdf --strict
```

**Templates:**

- `report.html` — fullbleed dark dot-grid cover (Playfair), zinc body, three-line tables, 550–650w/p
- `proposal.html` — split cover (Syne), problem→solution, pricing, signature
- `resume.html` — typographic (DM Serif), auto-fit 1p, two-col skills
- `portfolio.html` — atmospheric near-black + radial glow (Fraunces), meander grid
- `magazine.html` — cream Lora + Cormorant, 2-col, meander + pull quote
- `letter.html` + `minimal.html` — see `references/document-types.md` (extend from `report.html` boilerplate)

Each HTML’s `<style>` owns `@page` and taste tokens — no external build step. See `references/design-taste.md` for the HTML boilerplate to copy for new docs.
