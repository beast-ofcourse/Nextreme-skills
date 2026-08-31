# Validation Checklist — Anti-Slop + Golden Rules + OOXML Integrity

Run `python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py output.docx --strict` (skills.sh) or `python nextreme-docs/scripts/validate_docx.py output.docx --strict` (local clone) plus this manual pass before delivery. All scripts ship inside the skill — `skills.sh` copies `nextreme-docs/` with `scripts/`, `references/`, `templates/`.

## 1. File Validity

- [ ] File is a valid ZIP (docx is a ZIP). `validate_docx.py` can unzip it.
- [ ] Required parts exist: `word/document.xml`, `word/styles.xml`, `word/numbering.xml` (if lists), `word/settings.xml`, `[Content_Types].xml`, `docProps/core.xml`.
- [ ] `zipfile.testzip()` returns `None` — no corrupt entries.
- [ ] No OLE2 header (`D0 CF 11 E0`) — that is a `.doc`, not `.docx`.

## 2. Styles — No Fake Headings

- [ ] Every heading in the document uses a `Heading 1`–`Heading 9`, `Title`, or `Subtitle` style — not `Normal` + bold/larger font.
- [ ] `validate_docx.py --audit-styles` reports zero fake headings (heuristic: `Normal` with `run.bold=True` and `font.size ≥ 14pt`).
- [ ] All body text is `Normal` (or `Quote`/`Intense Quote` where intended) — not `Default Paragraph Font` + direct formatting.
- [ ] All tables have `table.style != None` and the style name matches the token sheet (`Light Grid Accent 1`, etc.).
- [ ] `python-docx` style audit: every style's `font.name`, `font.size`, `color.rgb`, `paragraph_format.space_before/after` matches the token sheet — no bare numbers in code, no magic.

## 3. Page Geometry

- [ ] `section.page_width/height` matches requested paper (Letter 8.5×11 or A4 8.27×11.69) within 1pt.
- [ ] Margins match tokens (check `section.top_margin`, `bottom_margin`, `left_margin`, `right_margin`, `header_distance`, `footer_distance`, `gutter`).
- [ ] If landscape section exists: `orientation == LANDSCAPE` and width/height are swapped; `header_distance/footer_distance` not zeroed by accident.
- [ ] `SECTION_CONTENT_WIDTH` computed as `page_width - left - right`; every table's total column widths and every image width ≤ that value.

## 4. Fields — Real, Not Typed

- [ ] TOC: `word/document.xml` contains `w:fldChar w:fldCharType="begin"` + `w:instrText` containing `TOC` + `w:fldCharType="separate"` + `w:fldCharType="end"`. Search for `instrText` with `TOC` — typed "Table of Contents" alone fails.
- [ ] Page numbers: footer/header contains `PAGE` field (and optionally `NUMPAGES`). Typed "Page 1" fails.
- [ ] Date: if auto-date, `DATE` field; typed date is allowed only when user supplied a fixed date.
- [ ] Cross-refs (if any): `REF` fields with matching `w:bookmarkStart/End` — typed "see Table 1" without a bookmark is a warning.

## 5. Tables

- [ ] Every table has a caption paragraph (`Caption` style) with prefix `Table N — ` or user-approved variant — untitled tables fail.
- [ ] Header row is distinct: bold runs and `w:shd` fill `ACCENT` — plain tables with no header distinction fail.
- [ ] Numeric columns right-aligned, text left-aligned — heuristic check.
- [ ] No table bleeds past `SECTION_CONTENT_WIDTH` — computed column widths sum correctly.
- [ ] Merged cells only where intended (header spanning) — no accidental `merge()` artifacts.

## 6. Images & Figures

- [ ] Every image has a caption (`Caption` style `Figure N — `) and `descr` alt text on `wp:docPr`.
- [ ] Image format is PNG or JPEG — EMF/WMF/BMP fail on portability check.
- [ ] `inline_shape.width <= SECTION_CONTENT_WIDTH` — oversized images fail.
- [ ] No floating anchored images unless the document is a manual with explicit side-by-side table layout.

## 7. Lists & Numbering

- [ ] Bulleted/numbered lists use `List Bullet` / `List Number` styles — typed `•` or `1.` in `Normal` fails.
- [ ] Multilevel contracts use a single `numId` with levels `0..2` — typed `1.1.1` in `Normal` fails.
- [ ] Sequence: 1, 2, 3 with no skips; contract: 1, 1.1, 1.1.1 with no gaps — validator checks `w:numPr` hierarchy.

## 8. Headers, Footers, Sections

- [ ] If `different_first_page=True`: first-page header/footer are populated (or explicitly empty by intent), and primary header/footer appear on page 2 — not blank.
- [ ] If duplex (`evenAndOddHeaders`): even-page header/footer populated — not blank mirror of odd.
- [ ] Footer page number field appears on page 2+ — not only page 1.
- [ ] No orphaned section breaks — each `w:sectPr` has matching paper/margins.

## 9. Properties & Settings

- [ ] `core_properties.title`, `author` set to user/brand values — not default `""` or "Python-docx".
- [ ] `core_properties.created` is set (not epoch).
- [ ] No leftover tracked changes (`w:ins`, `w:del`) or comments (`w:comment`) unless user requested review markup.
- [ ] No empty paragraphs at document start/end beyond one intentional spacer.

## 10. Content Integrity — No AI Slop

- [ ] Search for slop tokens (case-insensitive): `lorem ipsum`, `lorem`, `placeholder`, `TODO` without ticket, `TBD`, `sample text`, `your text here`, `insert ... here`. Zero hits unless the user explicitly approved a `[CONTENT REQUIRED: ...]` marker.
- [ ] No typed filler to hit a page count — page count is a consequence of real content + geometry, not a target inflated with padding.
- [ ] Cross-reader sanity: open in Word + one other viewer (Google Docs, LibreOffice, or Pages) — no vanished images, no reflow that hides the footer, no clipped table.
- [ ] Reflow test: insert a new paragraph mid-document and verify page numbers, headers, and TOC hints survive — fields reflow, typed text does not.

## 11. Conversion Artifacts (Only When Delivering .doc / PDF)

- [ ] `.doc` is a conversion from the canonical `.docx` via `soffice --headless --convert-to doc` — log the command and its exit code. No claim of native `.doc` write.
- [ ] `.pdf` is a conversion via `soffice --headless --convert-to pdf` or `docx2pdf` — same logging.
- [ ] Converted file page count matches source ±0 ( LibreOffice faithful ) — report count.
- [ ] Deliver alongside the canonical `.docx` — never `.doc`/`.pdf` alone.

## 12. Golden Rules Spot-Check

Pick 3 functions from the generation script and verify:

- [ ] Names tell the truth (no `data`/`handler`/`manager`).
- [ ] One job per function — would you need "and" to describe it?
- [ ] Guard clauses — no pyramid `if: if: if:` deeper than 2–3.
- [ ] No duplication — search for repeated 4+ line blocks.
- [ ] No magic numbers — every `Pt(11)`, `Inches(0.85)`, `#1B4F72` is a named constant.
- [ ] Errors handled with context — `except` plus log, not silent `pass`.

If any of the above fails, the deliverable is not ready. Fix the root (style, field, geometry, or content) and re-run validation.

## Running the Validator

```bash
# Full strict pass — skills.sh:
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py output.docx --strict
# Local clone:
python nextreme-docs/scripts/validate_docx.py output.docx --strict

# Focused audits (use ${CLAUDE_SKILL_DIR} or nextreme-docs prefix as above)
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py output.docx --audit-styles
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py output.docx --check-fields
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py output.docx --check-images --max-width-inches 6.5

# Resume length gate
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py resume.docx --check-resume-length --max-pages 2
```

Exit 0 = pass, non-zero = fail with explicit reasons. Do not ship a failing file.
