# Validation — Page-as-Canvas QC

Run `python ${CLAUDE_SKILL_DIR}/scripts/validate_pdf.py out.pdf --strict` (or `python nextreme-pdf/scripts/validate_pdf.py out.pdf --strict`) plus visual PNG proofs before delivery.

## 1. File Validity

- [ ] Starts with `%PDF` magic. `file` says `PDF document`.
- [ ] `pypdf`/`pdfinfo` reports page count, no corrupt stream.
- [ ] No OLE2 header, no ZIP (that’s PPTX/DOCX).

## 2. Per-Page Fill — Page-as-Canvas (No Holes Mid-Article)

From beautiful-pdf-mcp: every page but the last must be **filled to the bottom** (text carries mid-sentence, even mid-hyphen). A hole mid-article is a defect; a short final page (book chapter end) is allowed per `data/styles.json` contract.

- [ ] `layout_report` (when using Typst) shows each page `fill %` within contract thresholds.
- [ ] Heuristic (HTML+Playwright): page count vs budget: `expected = ceil(total_words / words_per_page)` ±1 page.
- [ ] No stranded single line (widow) / orphan at page top/bottom — `widows: 3` / `orphans: 3` via CSS + `hyphens: auto`.

## 3. Cover Bleed

- [ ] `@page :first { margin: 0 }` + `body { margin: 0 }` + `.cover { width: 210mm; height: 297mm }` → cover edge-to-edge, no white border. Screenshot at 100% shows no 8px gap.

## 4. Overflow

- [ ] `pre, table, img { max-width: 100% }` — no element exceeds `content_width`.
- [ ] `validate_pdf.py` checks: `img`/`table`/`pre` width vs `page_width - margins` — fail on spill.
- [ ] No `page-break-after: always` residue causing blank pages.

## 5. Rivers & Gaps (Typography)

- [ ] Justified text uses `hyphens: auto; text-wrap: pretty; hyphenate-limit-chars: 6 3 2` — no rivers (wide word gaps).
- [ ] Tracking all negative: `display -0.10em` etc. — positive tracking in CSS → fail (AI marker).

## 6. Accent Law

- [ ] One accent per spread — `grep -c "bg-\[#"` on HTML shows accent appears ≤ once per page as hero (cover, h1 rule, or callout bar). Gradient only on that hero.
- [ ] `rgba` not used for tags (solid hex only — WeasyPrint bug).

## 7. Images — Two-Pass Placement (When Using Typst)

- [ ] `position: "auto"` images re-placed via `after:N` after `typst query` pass — no torn layout or lonely image on empty page.
- [ ] HTML path: images via `max-width: 100%`, `figure` caption present, `alt` present.

## 8. Visual Proof — PNG per Page

After `validate_pdf.py`, render PNGs:

```bash
# via pdf2image/pdftoppm or preview pipeline:
python ${CLAUDE_SKILL_DIR}/scripts/compile_preview.py out.pdf --pages 1-3
# → out-preview/page-01.png (cover), page-02.png (dense), page-03.png (sparse)
# Inspect: ring/whisper shadow only, no hard drop; line-heights 1.1–1.55; zinc vs parchment coherent.
```

## Running the Validator

```bash
# Full strict (skills.sh):
python ${CLAUDE_SKILL_DIR}/scripts/validate_pdf.py out.pdf --strict
# Local:
python nextreme-pdf/scripts/validate_pdf.py out.pdf --strict

# Checks:
# --check-cover   : fail on white-border cover
# --check-overflow: fail on table/img spill
# --check-rivers  : fail on positive tracking / no hyphens
# --check-fill    : fail on mid-article hole
python nextreme-pdf/scripts/validate_pdf.py out.pdf --check-cover --check-overflow
```

Exit 0 = pass; non-zero = fail with fix (“page 3: 6 lines short, add ~40 words”).

## Golden-Rules Spot-Check

Pick 3 functions in `scripts/generate_pdf.py` and verify: names tell truth, one job, guard clauses, no duplication, no magic numbers (every `8px` is a token), errors logged.
