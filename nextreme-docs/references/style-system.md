# Style System — Design Tokens for Word Documents

Every Word document this skill produces uses **explicit, named tokens**. No viewer defaults, no "it looked fine on my machine." Copy this file's preset, then tailor.

## 1. Page Geometry Presets

All values in inches unless noted. 1 inch = 72 pt = 1440 twips (OOXML) = 914400 EMU.

| Preset | Paper | Top | Bottom | Left | Right | Header | Footer | Gutter | Best For |
|---|---|---|---|---|---|---|---|---|---|
| **Standard Report** | A4 (8.27×11.69) | 0.85 | 0.85 | 0.85 | 0.85 | 0.35 | 0.35 | 0 | Reports, proposals, manuals |
| **Compact Letter** | Letter (8.5×11) | 0.75 | 0.75 | 0.75 | 0.75 | 0.30 | 0.30 | 0 | Letters, invoices, US business |
| **Resume Tight** | Letter | 0.45 | 0.45 | 0.50 | 0.50 | 0.20 | 0.20 | 0 | Resumes — one page must fit |
| **Academic** | A4 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 0.15 | Papers — binding gutter |
| **Certificate** | A4 Landscape (11.69×8.27) | 0.60 | 0.60 | 0.70 | 0.70 | 0.30 | 0.30 | 0 | Landscape certificates |

**Computation helpers:**

```python
from docx.shared import Inches

PAPER_A4_WIDTH = Inches(8.27)
PAPER_A4_HEIGHT = Inches(11.69)
PAPER_LETTER_WIDTH = Inches(8.5)
PAPER_LETTER_HEIGHT = Inches(11)

MARGIN_TOP = Inches(0.85)
MARGIN_BOTTOM = Inches(0.85)
MARGIN_LEFT = Inches(0.85)
MARGIN_RIGHT = Inches(0.85)
HEADER_DISTANCE = Inches(0.35)
FOOTER_DISTANCE = Inches(0.35)

SECTION_CONTENT_WIDTH = PAPER_A4_WIDTH - MARGIN_LEFT - MARGIN_RIGHT  # ~6.57in on A4 report
SECTION_CONTENT_HEIGHT = PAPER_A4_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM  # ~9.99in
```

**Columns (for datasheets, newsletters):**

- 2-column: `w:cols w:num="2" w:space="720"` (0.5in gutter, 720 twips)
- 3-column: `w:num="3" w:space="480"` (0.33in gutter)

---

## 2. Typography Scale

| Style | Font | Size | Color | Space Before | Space After | Line Spacing | Keep With Next | Outline Level |
|---|---|---|---|---|---|---|---|---|
| **Normal** (body) | Calibri | 11pt | #262626 | 0pt | 8pt | 1.07 (multiple) | false | 9 (body) |
| **Title** | Calibri Light | 28pt | #1B4F72 | 0pt | 14pt | 1.0 | true | 0 |
| **Subtitle** | Calibri Light | 14pt | #595959 | 0pt | 18pt | 1.0 | true | 1 |
| **Heading 1** | Calibri Light | 16pt | #1B4F72 | 18pt | 6pt | 1.0 | true | 0 |
| **Heading 2** | Calibri | 13pt | #1B4F72 | 14pt | 4pt | 1.0 | true | 1 |
| **Heading 3** | Calibri | 11pt | #1B4F72 | 10pt | 3pt | 1.0 | true | 2 |
| **Caption** | Calibri | 9pt italic | #595959 | 4pt | 10pt | 1.0 | false | 9 |
| **Quote** | Calibri | 11pt italic | #404040 | 6pt | 6pt | 1.07 | false | 9 |
| **Intense Quote** | Calibri Light | 11pt italic | #1B4F72 | 8pt | 8pt | 1.07 | false | 9 |
| **List Bullet** | Calibri | 11pt | #262626 | 0pt | 2pt | 1.07 | false | 9 |
| **List Number** | Calibri | 11pt | #262626 | 0pt | 2pt | 1.07 | false | 9 |
| **Header** | Calibri | 8pt | #808080 | 0pt | 0pt | 1.0 | false | 9 |
| **Footer** | Calibri | 8pt | #808080 | 0pt | 0pt | 1.0 | false | 9 |

**Font pairing presets:**

| Pairing | Body | Heading | When |
|---|---|---|---|
| **Corporate Calibri** (default) | Calibri 11 | Calibri Light 16/13 | Reports, proposals, invoices — maximum compatibility |
| **Academic Times** | Times New Roman 12 | Times New Roman 14/12 bold | Papers that mandate serif |
| **Modern Garamond** | Garamond 11.5 | Calibri Light 16 | Premium proposals, certificates |
| **Mono Technical** | Consolas 9.5 | Calibri 13 | Manuals, datasheets with code |

**Fallback stack:** set via `w:rFonts` — `ascii="Calibri" hAnsi="Calibri" cs="Calibri" eastAsia="Calibri"` plus theme. On non-Windows, Word substitutes but the name stays valid OOXML.

**Line spacing rule:**

- Body: `1.07` (Word default for readability; `1.15` if the audience prints dense reports — never `1.0` for body)
- Headings/captions/headers: `1.0` (single)

**Widow/orphan:** `paragraph_format.widow_control = True` for Normal; `keep_together = True` for headings.

---

## 3. Color Palette

| Token | Hex | Usage |
|---|---|---|
| `TEXT_PRIMARY` | #262626 | Body, headings (when not accent) |
| `TEXT_SECONDARY` | #595959 | Captions, subtitles |
| `TEXT_MUTED` | #808080 | Headers, footers, page numbers |
| `ACCENT` | #1B4F72 | Heading 1/2/3, table header fill, hyperlink |
| `ACCENT_LIGHT` | #D6EAF8 | Table banded row fill, quote left border bg |
| `ACCENT_DARK` | #154360 | Certificate border, cover band |
| `GRID_LINE` | #BDC3C7 | Table grid lines |
| `PAGE_BG` | #FFFFFF | Page background (almost never tinted) |

**Preset variants:**

| Variant | Accent | Header Fill | Best For |
|---|---|---|---|
| **Navy Corporate** (default) | #1B4F72 | #1B4F72 (white text) | Reports, proposals |
| **Slate Professional** | #2C3E50 | #2C3E50 | Resumes, invoices |
| **Forest Authority** | #1E6B3E | #1E6B3E | Certificates, environmental reports |
| **Burgundy Legal** | #6B1D2A | #6B1D2A | Contracts, formal letters |

Hyperlink color: same as `ACCENT`, underline single. Visited: `ACCENT_DARK`.

---

## 4. Spacing Rhythm

| Element | Before | After | Line | Notes |
|---|---|---|---|---|
| Body paragraph → body paragraph | 0pt | 8pt | 1.07 | No first-line indent in business docs |
| Heading 1 → body | 18pt | 6pt | 1.0 | Keep-with-next |
| Heading 2 → body | 14pt | 4pt | 1.0 | |
| Body → Heading (any) | 10–18pt | — | — | Air before, not after body |
| Bullet item → bullet item | 0pt | 2pt | 1.07 | Tight list |
| Table → caption | 4pt | 10pt | 1.0 | Caption outside table |
| Caption → next heading | 10pt | — | — | |
| Image (centered) margins | 6pt above/below | | | `paragraph_format.space_before/after` on image paragraph |

**First-line indent:** 0 for business docs; 0.25in (`Inches(0.25)`) only for academic papers with no space-after between body paragraphs.

---

## 5. Tables

| Token | Value | Notes |
|---|---|---|
| `TABLE_STYLE_DEFAULT` | `Light Grid Accent 1` | Branded grid + header shading + banded rows |
| `TABLE_STYLE_MINIMAL` | `Light Shading Accent 1` | For invoices — lighter grid |
| `TABLE_ALIGNMENT` | `WD_TABLE_ALIGNMENT.CENTER` | Always centered to content width |
| `CELL_MARGIN_TOP/BOTTOM` | 42 twips (3pt) | `w:tblCellMar` per cell or table |
| `CELL_MARGIN_LEFT/RIGHT` | 84 twips (6pt) | Breathing room |
| `HEADER_FILL` | `ACCENT` (#1B4F72) | White text `#FFFFFF` on header row |
| `BANDED_ROW_FILL` | `ACCENT_LIGHT` (#D6EAF8) | Every even row |
| `HEADER_TEXT_BOLD` | True | Plus `color=white` |
| `FIRST_ROW_LOOK` | `w:firstRow="1"` | Bolds via style flag |

**Catalog — pick by pattern:**

| Need | Style Name | Flags |
|---|---|---|
| Report data table | `Light Grid Accent 1` | `firstRow=1, noHBand=0, noVBand=1` |
| Pricing / invoice | `Light Shading Accent 1` | `firstRow=1, noHBand=0` |
| Specs / datasheet | `Medium Grid 2 Accent 1` | `firstRow=1` |
| Minimal (resume skills matrix) | `Table Grid` + manual shading | No style banding; shade header via `w:shd` |

**Never** use direct `cell.fill`; use `w:shd` OOXML shading via helper so theme survives.

---

## 6. Images & Figures

| Token | Value |
|---|---|
| `MAX_FIGURE_WIDTH` | `SECTION_CONTENT_WIDTH - Inches(0.1)` |
| `DEFAULT_FIGURE_WIDTH` | `Inches(5.5)` on A4 report (≈84% of content width) |
| `FIGURE_ALIGNMENT` | `WD_ALIGN_PARAGRAPH.CENTER` |
| `FIGURE_CAPTION_STYLE` | `Caption` (9pt italic #595959) |
| `FIGURE_CAPTION_PREFIX` | `Figure N — ` (em dash) |
| `TABLE_CAPTION_PREFIX` | `Table N — ` |
| `ALT_TEXT_REQUIRED` | True — every image gets `descr` + `title` |

**Callout:** for manual steps with side-by-side figure + text, use a 2-column borderless table (figure left, steps right) — not floating anchored images.

---

## 7. Lists & Numbering

| Level | Format | Left Indent | Hanging | Example |
|---|---|---|---|---|
| Bullet L1 | `•` (disc) | 0.25in | 0.25in | • Item |
| Bullet L2 | `–` (en dash) | 0.50in | 0.25in | – Sub-item |
| Number L1 | `1.` decimal | 0.25in | 0.25in | 1. First |
| Number L2 | `1.1` | 0.50in | 0.35in | 1.1 Sub-step |
| Number L3 (contracts) | `1.1.1` | 0.75in | 0.45in | 1.1.1 Clause |

Contract multilevel must be a single `numId`; resume bullet lists can be simple `List Bullet` style.

---

## 8. Headers, Footers, Sections

| Token | Value |
|---|---|
| `HEADER_STYLE` | `Header` 8pt #808080 centered or left/right |
| `FOOTER_STYLE` | `Footer` 8pt #808080 centered |
| `PAGE_NUMBER_FORMAT` | `Page {PAGE} of {NUMPAGES}` or `— {PAGE} —` |
| `DIFFERENT_FIRST_PAGE` | True for reports/proposals with cover; False for letters/resumes |
| `EVEN_AND_ODD_HEADERS` | True for academic/contract duplex printing |
| `TITLE_PAGE_SECTION` | Separate first section with `different_first_page=True`, no footer on cover |

---

## 9. Cover / Title Page

| Element | Style | Notes |
|---|---|---|
| Document title | `Title` 28pt #1B4F72 | Centered, 2.5in from top via spacing |
| Subtitle | `Subtitle` 14pt #595959 | Below title |
| Author / org | `Normal` 11pt #595959 | Below subtitle, 18pt before |
| Date | `Normal` 10pt #808080 | At bottom margin |
| Cover band | `w:shd` fill `ACCENT` at top 1.5in | Optional — corporate reports |

---

## 10. TOC & Fields

| Field | Instr | Placement |
|---|---|---|
| TOC | `TOC \o "1-3" \h \z` | After cover, before body |
| Page number | `PAGE` | Footer |
| Page count | `NUMPAGES` | Footer (`Page X of Y`) |
| Date | `DATE \@ "MMMM d, yyyy"` | Letter date block |
| Cross-ref | `REF _Ref123 \h` | After captioning, requires bookmark |

TOC heading: `Heading 1` "Contents" or `TOC Heading` style; TOC entries themselves are `TOC 1`, `TOC 2`, `TOC 3` styles inherited from field.
