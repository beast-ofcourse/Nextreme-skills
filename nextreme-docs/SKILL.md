---
name: nextreme-docs
description: "Generate publication-grade .docx (and legacy .doc via conversion) Word documents from any content — reports, proposals, resumes, invoices, letters, contracts, manuals, academic papers, and certificates. Uses python-docx as the primary engine with python-docx-template (Jinja2) for template filling and LibreOffice headless for .doc↔.docx↔PDF conversion. This is THE extreme skill for ANY Word document — distinct from markdown/README, charts, diagrams, or flowcharts. Trigger whenever the user asks for a doc, docx, Word document, letter, report, resume, CV, invoice, proposal, contract, manual, certificate, or any printable office document — even if they say \"make a document\" without naming Word. Also trigger for \"convert to Word\", \"export as docx\", or \"Word template\". Do NOT trigger for README.md, slides (pptx), or spreadsheets (xlsx)."
license: MIT
compatibility: python>=3.9
---

# Nextreme Docs — Extreme .docx / .doc Generation

This skill produces **print-ready, publication-grade Word documents** that survive real-world use: opened in Microsoft Word, Google Docs, LibreOffice, and Apple Pages without layout breakage. Every output is a valid OOXML `.docx` with disciplined styles, explicit page geometry, calibrated typography, and zero AI slop. The user gets three deliverables: the **.docx**, an optional **PDF**, and the **spec/source that generated it**.

---

## Why This Skill Is Not Generic

Most AI-generated docx files fail in the wild: phantom spacing,_heading-is-just-bold-paragraph_, tables that overflow margins, images that vanish in Google Docs, no header/footer on page 2, a TOC that is just typed text, and `Lorem ipsum` where real content should be. Operators then hand-fix the file for an hour.

This skill treats a Word document as a **designed artifact**, not a dump of paragraphs:

- **Styles govern everything** — no direct formatting outside a named style. A heading is `Heading 1`, not 16pt bold. Changing the style fixes the whole document.
- **Page geometry is explicit** — every section declares paper size, margins, orientation, header distance, gutter, and column count. No viewer-dependent defaults.
- **OOXML is validated** — the output is unzipped and its `word/document.xml`, `word/styles.xml`, and `word/settings.xml` are checked before delivery.
- **.doc is legacy, not magic** — `.doc` is OLE2 binary, not OOXML. `python-docx` cannot write `.doc`. This skill writes `.docx` and converts via LibreOffice only when `.doc` is explicitly requested.

A generic skill says "use python-docx to create a document." This skill tells you the exact style name, pt size, hex color, spacing, and validation check for every element.

---

## Golden Code Quality Rules — ENFORCED

These are non-negotiable. Every document and every script this skill produces must pass them. Violation = task fails.

Keep code human-readable, small, and obvious. No AI slop.

* **Names tell the truth** — variables/functions reveal intent. No `data`, `info`, `result`, `handler`, `manager`, `helper`, `utils`, `foo`. A function that inserts a styled heading is `insert_heading`, not `process_data`.
* **One job per unit** — if you need "and" to describe what a function does, split it. A function that builds a table does not also set page margins. Files own one domain.
* **Guard clauses over nesting** — early returns, fail fast. No pyramids, no `else` after `return`. Nesting past 2–3 levels is a signal to restructure.
* **No duplication** — never copy-paste. Third occurrence of the same logic = must abstract. Two occurrences is coincidence, not a pattern.
* **No dead weight** — zero dead code, commented-out code, `console.log`, unused imports/vars. Delete, don't comment out.
* **Types are contracts** — no `any`, no silent `as` casts, narrow `unknown` explicitly. At an untyped boundary (`JSON.parse`, third-party API), a cast is allowed only alongside visible runtime validation — a parse function or schema check the reader can see.
* **Errors never silent** — every failure path is handled, returned, or logged with context. Never an empty `except`, never a swallowed promise. A failed image load logs the path and continues; a missing font falls back visibly.
* **No magic** — no unexplained numbers or strings. Name every constant. `PARAGRAPH_SPACE_AFTER_PT = 8` not `8`. No cryptic one-liners.
* **Explicit dependencies** — no hidden globals, no surprise side effects. Inputs in, outputs out. Pure where possible.
* **Readability > cleverness** — code reads like prose: linear flow, consistent style, self-documenting. Comments explain why, not what.
* **No premature abstraction** — no wrappers, layers, or helpers you don't need today. YAGNI. Abstract on the real second pattern, not the second line that looks similar.
* **Leave it cleaner, not bigger** — boy-scout rule applies to code you're already touching. Not license to refactor unrelated duplication silently.
* **State assumptions, don't guess silently** — if the spec is ambiguous, say what you assumed and why, in a comment or PR note. Wrong-but-confident is worse than incomplete.

**Auto-rejected AI slop:** placeholder `TODO` without a ticket, generic scaffolding, empty `try/except`, `lorem`-ish names, duplicated boilerplate, over-engineered factories/managers, unvalidated `as` casts at boundaries, silent assumptions about ambiguous specs, inconsistent style within one file, and any code you wouldn't defend in review.

**Document-level slop that is also rejected:** filler paragraphs (`Lorem ipsum`, "This is a sample"), typed TOC instead of `w:fldChar` field TOC, headings that are just bold `Normal` paragraphs, tables without a named style, images without alt text/caption, and any `.docx` that fails `validate_docx.py`.

---

## Engine Selection

| Context | Primary Engine | Output | Why |
|---|---|---|---|
| **New .docx from scratch** (90% of cases) | `python-docx` | `.docx` — native OOXML | Full style/section/table/image control, no Word install, pure Python |
| **Fill an existing .docx template** | `python-docx-template` + Jinja2 | `.docx` | Enterprise letterheads, contracts, mail-merge; keeps template's styles intact |
| **Legacy .doc required** | `python-docx` → LibreOffice headless | `.doc` | Writes `.docx` first, then `soffice --headless --convert-to doc` |
| **.docx → PDF** | LibreOffice headless or `docx2pdf` | `.pdf` | Print-ready PDF without manual Word export |
| **Headless server / CI** | `python-docx` only | `.docx` | No GUI, no COM, <50ms cold start per document |

**Install (skills.sh — ships with scripts, you install deps once):**

```bash
# Via skills.sh (recommended) — skill folder is copied with all scripts/templates/references
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt
# Local clone alternative:
pip install -r nextreme-docs/requirements.txt
# Minimal (no requirements.txt):
pip install "python-docx>=0.8.11" "pyyaml>=6.0"

# Optional — only if you fill an existing .docx template with Jinja2:
pip install "python-docx-template>=0.16"

# Optional: for .doc (legacy OLE2) / PDF conversion — LibreOffice headless
# Windows: install LibreOffice, ensure soffice.exe on PATH
# macOS: brew install libreoffice
# Linux: apt-get install libreoffice-writer
```

> `skills.sh` (`npx skills add ...`) **ships** `scripts/create_docx.py`, `scripts/validate_docx.py`, `references/` and `templates/` inside the skill folder. It does **not** run `pip install` — run the one-liner above once per env. After that, pure `python-docx` handles 90% of cases (`.docx`); LibreOffice is only needed when you pass `--doc` or `--pdf`.

Check installed contract before calling — never invent API:

```bash
pip show python-docx
python -c "import docx; print(docx.__version__)"
```

---

## Core Workflow

Do these steps in order. Each ends on a completion criterion — do not proceed until it passes.

### 1. Inventory the Content (No Hallucination)

Ask or infer: what is this document, who reads it, and what must it contain? Extract the real inventory — titles, sections, tables, figures, lists, signatures, page count estimate, paper size (A4 vs Letter), and whether it needs headers/footers, page numbers, TOC, or watermarks.

Never invent content to fill silence. If the user gave you two bullet points for a "10-page report," ask what the remaining 8 pages should contain, or mark the gap explicitly: `[CONTENT REQUIRED: methodology details]`. Do not generate `Lorem ipsum`.

Reference: `references/document-types.md` — catalog of document patterns and their required blocks.

Completion criterion: you can list every section/table/figure the document will contain, and every gap is either filled with user-provided content or an explicit `[CONTENT REQUIRED: ...]` marker — zero silent invention, zero filler.

### 2. Choose the Document Pattern

Match the inventory to the correct pattern. Picking the wrong pattern produces a confusing layout.

| Pattern | When to Use | Structural Signature |
|---|---|---|
| **Report** | Analyses, findings, business/technical reports | Title page → TOC → Executive summary → Body (H1/H2) → Tables/Figures with captions → Conclusion → Appendix |
| **Proposal** | Bids, pitches, project proposals | Cover → TOC → Problem/Solution → Scope/Timeline → Pricing table → Terms → Signature block |
| **Resume / CV** | Job applications | Single page (1–2 max), header with contact → Summary → Experience (reverse chrono) → Skills matrix → Education |
| **Invoice** | Billing | Header (seller/buyer) → Line-item table (banded) → Totals → Payment terms → Footer |
| **Letter** | Formal correspondence | Letterhead header → Date → Recipient block → Subject → Body → Closing → Signature |
| **Contract** | Legal agreements | Title → Parties → Definitions → Numbered clauses (multilevel) → Signature blocks → Exhibit attachments |
| **Manual / Datasheet** | Product docs, SOPs | Cover → TOC → Safety/Overview → Step-by-step (numbered + figures) → Specs table → Revision history |
| **Academic Paper** | Research papers | Title/Abstract/Keywords → Introduction → Methods → Results (tables/figures) → References (bibliography style) |
| **Certificate** | Awards, completion | Single landscape page, centered title, recipient name (display font), issuer/signature, border/frame |

Completion criterion: pattern is chosen and justified in one sentence referencing the user's inventory; you can name the sections/blocks the pattern mandates.

### 3. Lock the Style Tokens

Before writing any Python, write down the design tokens. Every value is explicit — no viewer defaults.

Copy the token set from `references/style-system.md` and tailor it. At minimum lock:

- **Page:** `PAPER_SIZE` (A4 or Letter), `MARGIN_TOP/BOTTOM/INSIDE/OUTSIDE` (0.75in–1.0in), `HEADER_DISTANCE`, `FOOTER_DISTANCE`, `GUTTER`, `ORIENTATION`, per-section overrides
- **Typography:** `FONT_BODY` (e.g., Calibri 11pt), `FONT_HEADING` (e.g., Calibri Light), `FONT_MONO`, `LINE_SPACING` (1.07–1.15 for body), `SPACE_AFTER_PARAGRAPH_PT`, `HEADING_SIZES_PT` (H1 16–18, H2 13–14, H3 11–12)
- **Color:** `ACCENT_HEX`, `TEXT_PRIMARY_HEX` (`#262626`), `TEXT_SECONDARY_HEX` (`#595959`), `TABLE_HEADER_FILL_HEX`, `TABLE_BAND_HEX`
- **Table:** `TABLE_STYLE_NAME` (e.g., `Light Grid Accent 1`), `CELL_MARGIN_PT`, `HEADER_BOLD`, `FIRST_ROW_HEADER` flag
- **Numbering:** list style names, multilevel format (`1.`, `1.1`, `1.1.1` for contracts)

Reference: `references/style-system.md` — complete token catalog with measured defaults.

Completion criterion: a token sheet exists as named constants (in code or comment) covering page, type, color, table, and numbering — no bare numbers in the generation code.

### 4. Scaffold the Document Skeleton

Create the `.docx` with `Document()`, then immediately configure:

1. **Sections** — `document.sections[0].page_height/page_width/top_margin/...` per tokens. Add extra `document.add_section()` only when orientation or margins change (e.g., landscape appendix).
2. **Styles** — create or modify `document.styles['Normal']`, `Heading 1`–`Heading 9`, `Title`, `Subtitle`, `Caption`, `Quote`, `List Bullet`, `List Number`. Set font name/size/color, paragraph spacing, keep-with-next, outline level, and next-style. Never use direct formatting for what a style should carry.
3. **Headers/Footers** — `section.header.paragraph` and `section.footer.paragraph`. Wire first-page/even-odd if required (`section.different_first_page_header_footer = True`). Footer hosts page number field.
4. **Numbering** — multilevel lists via `word/numbering.xml` helpers (see `references/document-engine.md`).

Reference: `references/document-engine.md` — exact python-docx API contracts and OOXML field codes.

Completion criterion: a blank `.docx` opens in Word with correct page size/margins, a style gallery where each heading level visibly differs, and headers/footers present on page 2 (not just page 1) — zero direct formatting on the scaffold.

### 5. Populate Content (Styles Only)

Insert every element through its named style:

- **Paragraphs** — `document.add_paragraph(text, style='Normal')` or `style='Quote'`. Runs for inline emphasis (`run.bold`, `run.italic`, `run.font.color.rgb`) are allowed — block-level bypass is not.
- **Headings** — `document.add_heading(text, level=1)` — never `add_paragraph` + `run.bold` + larger font to fake a heading. Set `paragraph.outline_level` and `paragraph.style` stays `Heading N`.
- **Lists** — use `List Bullet` / `List Number` styles. For multilevel contracts, use the numbering definition created in step 4.
- **Tables** — `document.add_table(rows, cols, style=TABLE_STYLE_NAME)` with `table.style`, `table.autofit = True`, header row bold + fill, `allow_autofit` and column widths set explicitly. Every table gets a `Caption` paragraph before or after (`Table 1 — ...`).
- **Images** — `document.add_picture(path, width=Inches(WIDTH))` or `run.add_picture`. Set `inline_shape.width`, add alt text, and add a `Caption` with figure number. Never let an image exceed `SECTION_WIDTH - (CELL_MARGIN * 2)`.
- **Fields** — TOC via `w:fldChar` (`TOC \\o "1-3" \\h \\z`), page numbers via `w:fldChar` with `PAGE` and `NUMPAGES`, date via `DATE`, cross-refs via `REF`. Typed text "Table of Contents" without a field is rejected.

Reference: `references/document-engine.md` — field code recipes and image sizing math.

Completion criterion: every block in the inventory from step 1 appears in the document under its correct named style; a style audit (`validate_docx.py --audit-styles`) shows zero paragraphs with direct heading-like formatting and zero tables without a style.

### 6. Finish: TOC, Numbers, Properties, Protection

1. **TOC** — insert at the position chosen in step 2 (after cover, before body). Uses a real field; Word will prompt "Update TOC" on open — that is correct. Optionally pre-fill with `python-docx` paragraph entries as a fallback for preview.
2. **Page numbers** — footer field `PAGE` / `NUMPAGES` or `Page X of Y`. First page can suppress via `different_first_page_header_footer`.
3. **Core properties** — `document.core_properties.title/author/subject/keywords/created`.
4. **Settings** — `w:settings` flags: `w:displayBackgroundShape`, `w:evenAndOddHeaders`, `w:autoHyphenation` as needed.
5. **No tracked changes or comments** left behind unless the user requested review markup.

Completion criterion: the document shows a field-backed TOC, page numbers on every page (verified on page 2+), and `core_properties` filled — all visible in Word's File → Info.

### 7. Validate the Output

Run the bundled validator — it unzips the `.docx` and checks the OOXML, not just the Python:

```bash
# skills.sh install:
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py output.docx --strict
# local clone:
python nextreme-docs/scripts/validate_docx.py output.docx --strict
# --audit-styles  : fail on fake headings / unstyled tables
# --check-fields  : fail on typed TOC without field
# --check-images  : fail on oversized / missing alt text
```

Manual verification (open in Word, Google Docs, Pages):

- **Styles** — does the style gallery show distinct Heading 1/2/3? Does changing Heading 1 recolor every H1?
- **Margins** — does text stay inside margins on every page, including tables?
- **Reflow** — add a paragraph mid-document: do page numbers, TOC page hints, and headers stay correct?
- **Cross-reader** — open in Google Docs and LibreOffice: any vanished images, broken tables, or shifted headers?
- **No slop** — search for `Lorem`, `TODO`, `sample`, `[CONTENT REQUIRED` markers without user sign-off.

Fix failures at the root: wrong style → fix the style, not the paragraph; broken field → fix the `w:fldChar` XML, not the text.

Reference: `references/validation-checklist.md` — full checklist.

Completion criterion: `validate_docx.py --strict` exits 0, and a 30-second visual check in two viewers (Word + one other) shows no clipping, no vanishing elements, and no filler text.

### 8. Deliver Everything

Always deliver:

1. **The .docx** — valid OOXML, passes `--strict`, opens clean in Word.
2. **The spec/source** — the YAML spec or Python file that generated it, so the user can regenerate or edit.
3. **The PDF (if requested)** — via LibreOffice: `soffice --headless --convert-to pdf output.docx`.
4. **The .doc (if requested)** — via LibreOffice: `soffice --headless --convert-to doc output.docx` — explain it is a conversion, not a native write.
5. **Validation log** — the `validate_docx.py` output proving the file is clean.

Do not deliver `.doc` as primary output without stating the conversion path. Do not claim "Word PDF export" can be done by `python-docx` alone — it cannot.

---

## Document-Type Quick Picks

Copy the matching template from `templates/` and fill content; do not start from zero. All templates ship inside the skill ( `skills.sh` copies `templates/` ), so use `${CLAUDE_SKILL_DIR}/templates/` when installed — `nextreme-docs/templates/` for a local clone.

Typical run (skills.sh):
```bash
python ${CLAUDE_SKILL_DIR}/scripts/create_docx.py --spec ${CLAUDE_SKILL_DIR}/templates/report_spec.yaml --output ./report.docx
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py ./report.docx --strict
```

| Need | Template | Why this one |
|---|---|---|
| Business report | `templates/report_spec.yaml` → `create_docx.py` | Title page + field TOC + executive summary + captioned tables/figures + appendix |
| Project proposal | `templates/proposal_spec.yaml` | Cover + scope/timeline + pricing table + signature |
| Resume / CV | `templates/resume_spec.yaml` | Single-section, tight margins, two-column skills matrix, no headers on page 1 |
| Invoice | `templates/invoice_spec.yaml` | Banded line-item table, calculated totals, payment terms footer |
| Formal letter | `templates/letter_spec.yaml` | Letterhead, date/recipient/subject blocks, signature with image slot |
| Contract | `templates/contract_spec.yaml` | Multilevel numbered clauses (1., 1.1, 1.1.1), defined terms, signature blocks |
| Manual / SOP | `templates/manual_spec.yaml` | Numbered steps with figure callouts, specs table, revision history |
| Academic paper | `templates/academic_spec.yaml` | Abstract/keywords, IMRaD headings, bibliography, double-line option |
| Certificate | `templates/certificate_spec.yaml` | Landscape A4, border frame, centered display typography |

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| Headings look like body text | Used direct formatting instead of `Heading N` style | Use `add_heading(level=N)` or `add_paragraph(style='Heading N')`; set style font/size there |
| TOC is just typed text | Inserted "Table of Contents" without `w:fldChar` field | Insert field recipe from `references/document-engine.md` — must include `fldChar begin`, `instrText TOC`, `fldChar separate`, `fldChar end` |
| Table bleeds past margin | `autofit` off or column widths exceed `section.width - margins` | Compute `SECTION_CONTENT_WIDTH = section.page_width - left_margin - right_margin`; set each `cell.width` proportionally; enable `table.autofit = False` after setting |
| Image vanishes in Google Docs | Anchored/floating image without fallback, or EMF/WMF format | Use `add_picture` (inline) with PNG/JPEG; keep width ≤ `SECTION_CONTENT_WIDTH`; add alt text |
| Page numbers only on page 1 | Header/footer set on `section.header` but `different_first_page_header_footer` is True and other headers empty | Populate `section.first_page_header/footer`, `section.even_page_header/footer` as needed; verify on page 2+ |
| .doc output is corrupt | Tried to write `.doc` with `python-docx` directly | Write `.docx` first, then `soffice --headless --convert-to doc output.docx` — `.doc` is OLE2, not OOXML |
| Styles don't change when edited | Direct formatting overrides style | Remove per-run `run.font.*` that duplicates style; use `run.style` or rely on paragraph style |
| Second section has wrong orientation | `add_section()` without setting `new_section.start_type` and `orientation` | Set `new_section.orientation = WD_ORIENTATION.LANDSCAPE` and `new_section.page_width/height` swapped; set `start_type = WD_SECTION_START.NEW_PAGE` |
| validate_docx.py reports fake heading | Paragraph has `run.bold=True` + `run.font.size > 14pt` but style is `Normal` | Change to styled heading; reserve bold+size deviations for emphasis runs only |

---

## Reference Files

- `references/document-engine.md` — python-docx contract: `Document`, `Section`, `Paragraph`, `Run`, `Table`, `Image`, field codes (`TOC`, `PAGE`, `DATE`), numbering, and OOXML escape hatches.
- `references/style-system.md` — design tokens: page geometry, typography scale, color palette, spacing rhythm, table/image/numbering presets.
- `references/document-types.md` — nine document patterns: inventory, required blocks, and section order for each type.
- `references/validation-checklist.md` — anti-slop + golden-rules + OOXML validation checklist for steps 7–8.
- `scripts/create_docx.py` — spec→.docx engine (YAML/JSON → python-docx) with style enforcement.
- `scripts/validate_docx.py` — OOXML validator (styles, fields, tables, images, properties).
- `templates/` — starter specs for report, proposal, resume, invoice, letter, contract, manual, academic paper, and certificate.

---

## Principles

- **Styles are law** — a document without disciplined styles is a document that cannot be maintained. Every format decision lives in a style.
- **State the geometry** — a document without explicit page geometry will drift across viewers. Every section declares its dimensions.
- **Validate the XML, not the preview** — a .docx that looks fine in one viewer but has broken OOXML will fail in the next. Unzip and check.
- **No filler is better than fake content** — a visible `[CONTENT REQUIRED: ...]` marker preserves trust; invented prose destroys it.
- **Conversion is not native** — `.doc` and `.pdf` are derived artifacts from a canonical `.docx`. Name the conversion path explicitly.
