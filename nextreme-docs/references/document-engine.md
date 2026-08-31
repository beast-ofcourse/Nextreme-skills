# Document Engine — python-docx Contract + OOXML Escape Hatches

This is the authoritative API surface for the skill. Verify against the installed `python-docx` before calling — never invent methods.

## 1. Install + Version Check

```bash
# skills.sh — deps ship as code, you install once:
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt
# local clone:
pip install -r nextreme-docs/requirements.txt
# minimal:
pip install "python-docx>=0.8.11" "pyyaml>=6.0"
pip install "python-docx-template>=0.16"  # only when filling a .docx template with Jinja2
python -c "import docx; print(docx.__version__)"
```

`python-docx` writes **.docx only** (OOXML). It cannot read or write legacy `.doc` (OLE2 binary). For `.doc` or `.docx→PDF`, convert via LibreOffice (section 12). `requirements.txt` ships inside the skill (`skills.sh` copies `nextreme-docs/` with all scripts/templates/references).

---

## 2. Document Lifecycle

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.section import WD_SECTION, WD_ORIENTATION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

document = Document()  # blank, one section, styles: Normal, Heading 1..9, Title...
# ... mutate sections, styles, paragraphs, tables, images, fields ...
document.save("output.docx")
```

`Document("existing.docx")` opens an existing file — use for `python-docx-template` or to clone a styled base.

---

## 3. Sections — Page Geometry Is Explicit

A `Document` has `document.sections` (at least one). Every section owns its paper + margins + headers/footers. Adding `document.add_section()` appends a new section starting at the current paragraph.

```python
from docx.shared import Inches

SECTION_CONTENT_WIDTH_IN = 6.5  # computed, not guessed

section = document.sections[0]
section.page_width = Inches(8.5)    # Letter: 8.5x11; A4: 8.27x11.69 (Inches(8.27), Inches(11.69))
section.page_height = Inches(11)
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.85)
section.right_margin = Inches(0.85)
section.header_distance = Inches(0.3)
section.footer_distance = Inches(0.3)
section.gutter = Inches(0)
section.orientation = WD_ORIENTATION.PORTRAIT

# Landscape appendix — new section
new_section = document.add_section(WD_SECTION.NEW_PAGE)
new_section.orientation = WD_ORIENTATION.LANDSCAPE
new_section.page_width = Inches(11)   # swap
new_section.page_height = Inches(8.5)
new_section.left_margin = Inches(0.6)
new_section.right_margin = Inches(0.6)
```

**Content width math — use it for every table and image:**

```python
content_width_emu = section.page_width.emu - section.left_margin.emu - section.right_margin.emu
content_width_in = content_width_emu / 914400  # 1 inch = 914400 EMU
MAX_IMAGE_WIDTH = Inches(content_width_in - 0.1)  # breathing room
```

**Columns (for newsletters, datasheets):**

```python
sectPr = section._sectPr
cols = OxmlElement("w:cols")
cols.set(qn("w:num"), "2")
cols.set(qn("w:space"), "720")  # 0.5 inch = 720 twips (1/20 pt; 1440 twips = 1 inch)
sectPr.append(cols)
```

---

## 4. Styles — The Single Source of Truth

All block formatting lives in styles. Never mimic a heading with bold+size on `Normal`.

```python
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ACCENT_HEX = "1B4F72"
TEXT_PRIMARY_HEX = "262626"

style = document.styles["Normal"]
font = style.font
font.name = "Calibri"
font.size = Pt(11)
font.color.rgb = RGBColor.from_string(TEXT_PRIMARY_HEX)
paragraph_format = style.paragraph_format
paragraph_format.space_after = Pt(8)
paragraph_format.line_spacing = 1.07
paragraph_format.space_before = Pt(0)

# Heading 1 — explicit, not inherited accident
heading1 = document.styles["Heading 1"]
heading1.font.name = "Calibri Light"
heading1.font.size = Pt(16)
heading1.font.color.rgb = RGBColor.from_string(ACCENT_HEX)
heading1.font.bold = True
heading1.paragraph_format.space_before = Pt(18)
heading1.paragraph_format.space_after = Pt(6)
heading1.paragraph_format.keep_with_next = True  # heading stays with next paragraph
heading1.paragraph_format.keep_together = True
heading1.paragraph_format.outline_level = 0  # 0=H1, 1=H2, ... 9=body

heading2 = document.styles["Heading 2"]
heading2.font.size = Pt(13)
heading2.font.color.rgb = RGBColor.from_string(ACCENT_HEX)
heading2.paragraph_format.space_before = Pt(14)
heading2.paragraph_format.space_after = Pt(4)
heading2.paragraph_format.outline_level = 1

# Caption — for tables and figures
try:
    caption = document.styles.add_style("Caption", 1)  # 1 = paragraph style
except ValueError:
    caption = document.styles["Caption"]
caption.font.size = Pt(9)
caption.font.italic = True
caption.font.color.rgb = RGBColor.from_string("595959")
caption.paragraph_format.space_before = Pt(4)
caption.paragraph_format.space_after = Pt(10)
caption.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Quote / Intense Quote
quote = document.styles["Intense Quote"]
quote.font.size = Pt(11)
quote.font.italic = True
```

**Creating a truly new style (e.g., "Compact Bullet"):**

```python
try:
    compact = document.styles.add_style("Compact Bullet", 1)
except ValueError:
    compact = document.styles["Compact Bullet"]
compact.base_style = document.styles["List Bullet"]
compact.font.size = Pt(10)
compact.paragraph_format.space_after = Pt(2)
compact.paragraph_format.left_indent = Inches(0.25)
```

**Inspect styles (debug):**

```python
for s in document.styles:
    if s.type == 1:  # paragraph
        print(s.name, s.font.name, s.font.size, s.font.color.rgb)
```

---

## 5. Paragraphs, Runs, Breaks

```python
from docx.shared import Pt, RGBColor

# Styled paragraph — preferred
paragraph = document.add_paragraph("Executive Summary", style="Heading 1")

# Empty + runs — for mixed formatting inside one paragraph
paragraph = document.add_paragraph(style="Normal")
run = paragraph.add_run("This figure is ")
run = paragraph.add_run("critical")
run.bold = True
run.font.color.rgb = RGBColor.from_string("1B4F72")
paragraph.add_run(" for Q4 planning.")

# Alignment, spacing, pagination
paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
paragraph.paragraph_format.space_after = Pt(8)
paragraph.paragraph_format.keep_with_next = False
paragraph.paragraph_format.widow_control = True
paragraph.paragraph_format.page_break_before = False

# Manual break — page and line
run = paragraph.add_run()
run.add_break(WD_BREAK.PAGE)
run.add_break(WD_BREAK.LINE)
```

**Do not use** `paragraph.text = "..."` to replace a styled paragraph — it preserves the style but strips runs. Use `add_run` composition.

---

## 6. Lists

Single-level via named styles:

```python
document.add_paragraph("First item", style="List Bullet")
document.add_paragraph("Second item", style="List Bullet")
document.add_paragraph("Step one", style="List Number")
```

**Multilevel (contracts: 1., 1.1, 1.1.1)** — requires a numbering definition in `word/numbering.xml`. The skill ships a helper:

```python
from scripts.create_docx import ensure_multilevel_numbering  # in skill

numbering_id = ensure_multilevel_numbering(document, levels=[
    {"format": "decimal", "text": "%1.", "left": Inches(0.25), "hanging": Inches(0.25)},
    {"format": "decimal", "text": "%1.%2.", "left": Inches(0.5), "hanging": Inches(0.35)},
    {"format": "decimal", "text": "%1.%2.%3.", "left": Inches(0.75), "hanging": Inches(0.45)},
])
# Apply by setting paragraph's numPr (helper does it):
paragraph = document.add_paragraph("Definitions", style="Normal")
apply_numbering(paragraph, numbering_id, level=0)
paragraph = document.add_paragraph("Term means...", style="Normal")
apply_numbering(paragraph, numbering_id, level=1)
```

If helpers unavailable, define `w:abstractNum` + `w:num` via raw `OxmlElement` — see `scripts/create_docx.py` for the exact XML.

---

## 7. Tables — Must Carry a Style

```python
from docx.shared import Inches, Pt
from docx.enum.table import WD_TABLE_ALIGNMENT

table = document.add_table(rows=1, cols=4)
table.style = "Light Grid Accent 1"  # required — never leave table.style == "Table Grid" by accident if a branded style exists
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = True  # then optionally fix widths after fill

# Header row
header_cells = table.rows[0].cells
headers = ["Item", "Quantity", "Unit Price", "Amount"]
for idx, text in enumerate(headers):
    cell = header_cells[idx]
    cell.text = text
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in paragraph.runs:
            run.bold = True

# Data rows
row_cells = table.add_row().cells
row_cells[0].text = "Consulting Services"
row_cells[1].text = "40 hrs"
row_cells[2].text = "$180.00"

# Column widths — set after content, then freeze
total_width = content_width_emu
widths = [0.5, 0.15, 0.15, 0.2]  # proportions must sum to 1.0
for row in table.rows:
    for idx, cell in enumerate(row.cells):
        cell.width = int(total_width * widths[idx])
table.autofit = False

# Banded rows / header row — via table style flags (OOXML)
tblPr = table._tbl.tblPr
tblLook = OxmlElement("w:tblLook")
tblLook.set(qn("w:firstRow"), "1")
tblLook.set(qn("w:noHBand"), "0")
tblLook.set(qn("w:noVBand"), "1")
tblPr.append(tblLook)

# Cell shading (header fill) — raw OOXML
shading = OxmlElement("w:shd")
shading.set(qn("w:fill"), "1B4F72")
header_cells[0]._tc.get_or_add_tcPr().append(shading)

# Merged cells
table.cell(0, 0).merge(table.cell(0, 1))
```

**Table caption (before or after, style `Caption`):**

```python
caption = document.add_paragraph("Table 1 — Pricing Breakdown", style="Caption")
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

---

## 8. Images — Inline Only, Sized, Captioned

```python
from docx.shared import Inches

paragraph = document.add_paragraph(style="Normal")
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = paragraph.add_run()
inline_shape = run.add_picture("assets/figure-1.png", width=Inches(5.5))
# Height auto-scales to preserve aspect ratio; never set both width and height manually unless you own the aspect math

# Alt text (for accessibility + Google Docs)
inline_shape._inline.docPr.set("descr", "Revenue trend 2023–2026, bar chart")
inline_shape._inline.docPr.set("title", "Figure 1")

# Caption after
caption = document.add_paragraph("Figure 1 — Revenue Trend (2023–2026)", style="Caption")
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

**Sizing rule:** `image_width <= SECTION_CONTENT_WIDTH`. Compute per section. If an image is 2400px wide, `Inches(6.0)` may still be too wide for a 0.6in-margin landscape section — always compute.

**Supported formats:** PNG, JPEG preferred. Avoid EMF/WMF (Windows-only), SVG (not supported inline — convert to PNG first), and BMP (bloat).

---

## 9. Headers, Footers, Page Numbers, Fields

Headers/footers live per section; they are **not** paragraphs in the body.

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

section = document.sections[0]
section.different_first_page_header_footer = False  # set True for title page without header

# Header
header = section.header
paragraph = header.paragraphs[0]
paragraph.text = "CONFIDENTIAL — ACME Proposal"
paragraph.style = document.styles["Header"]
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Footer with PAGE field — raw OOXML field codes
footer = section.footer
paragraph = footer.paragraphs[0]
paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_page_number(paragraph):
    """Insert a real PAGE field, not typed '1'."""
    run = paragraph.add_run()
    fldChar_begin = OxmlElement("w:fldChar")
    fldChar_begin.set(qn("w:fldCharType"), "begin")
    run._r.append(fldChar_begin)

    run = paragraph.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("w:space"), "preserve")
    instr.text = " PAGE "
    run._r.append(instr)

    run = paragraph.add_run()
    fldChar_separate = OxmlElement("w:fldChar")
    fldChar_separate.set(qn("w:fldCharType"), "separate")
    run._r.append(fldChar_separate)

    run = paragraph.add_run()
    fldChar_end = OxmlElement("w:fldChar")
    fldChar_end.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar_end)

paragraph.add_run("Page ")
add_page_number(paragraph)
paragraph.add_run(" of ")
# NUMPAGES
run = paragraph.add_run()
fldChar_begin = OxmlElement("w:fldChar"); fldChar_begin.set(qn("w:fldCharType"), "begin"); run._r.append(fldChar_begin)
run = paragraph.add_run(); instr = OxmlElement("w:instrText"); instr.set(qn("w:space"), "preserve"); instr.text = " NUMPAGES "; run._r.append(instr)
run = paragraph.add_run(); fldChar_separate = OxmlElement("w:fldChar"); fldChar_separate.set(qn("w:fldCharType"), "separate"); run._r.append(fldChar_separate)
run = paragraph.add_run(); fldChar_end = OxmlElement("w:fldChar"); fldChar_end.set(qn("w:fldCharType"), "end"); run._r.append(fldChar_end)
```

**TOC field (real, not typed):**

```python
def add_toc_field(paragraph):
    run = paragraph.add_run()
    fldChar_begin = OxmlElement("w:fldChar"); fldChar_begin.set(qn("w:fldCharType"), "begin"); run._r.append(fldChar_begin)
    run = paragraph.add_run()
    instr = OxmlElement("w:instrText"); instr.set(qn("w:space"), "preserve")
    instr.text = ' TOC \\o "1-3" \\h \\z \\u '  # outline 1-3, hyperlinks, hide tab leader in Web
    run._r.append(instr)
    run = paragraph.add_run()
    fldChar_separate = OxmlElement("w:fldChar"); fldChar_separate.set(qn("w:fldCharType"), "separate"); run._r.append(fldChar_separate)
    run = paragraph.add_run()  # Word replaces this on update; keep a placeholder
    run.text = ""
    run = paragraph.add_run()
    fldChar_end = OxmlElement("w:fldChar"); fldChar_end.set(qn("w:fldCharType"), "end"); run._r.append(fldChar_end)

toc_heading = document.add_paragraph("Contents", style="Heading 1")
add_toc_field(document.add_paragraph())
```

User must press `Ctrl+A` → `F9` or open-and-update in Word to populate page numbers in the TOC — this is correct Word behavior.

---

## 10. Core Properties + Settings

```python
core = document.core_properties
core.title = "ACME Q4 Report"
core.subject = "Quarterly Financial Analysis"
core.author = "ACME Analytics"
core.keywords = "report, Q4, finance"
core.category = "Business"
core.comments = "Generated via nextreme-docs"

# Settings — hyphenation, even/odd headers, background shapes
settings = document.settings.element
even_and_odd = OxmlElement("w:evenAndOddHeaders")
settings.append(even_and_odd)
```

---

## 11. python-docx-template (Jinja2) — When Filling a Template

Use only when the user provides a branded `.docx` with placeholders.

```python
from docxtpl import DocxTemplate

template = DocxTemplate("branded-letterhead.docx")
# Template contains: {{ client_name }}, {% for item in items %} etc.
context = {
    "client_name": "Ava Morgan",
    "date": "2026-08-31",
    "items": [{"name": "Consulting", "qty": 40, "price": 180}],
}
template.render(context)
template.save("filled.docx")
```

Rules: the template's styles are preserved — do not re-apply style tokens from section 4 on top. Validate the output still passes `validate_docx.py`.

---

## 12. Conversion — .doc and .docx→PDF

`python-docx` cannot write `.doc`. Convert via LibreOffice headless:

```bash
# .docx → .doc (legacy OLE2)
soffice --headless --convert-to doc output.docx --outdir ./

# .docx → PDF
soffice --headless --convert-to pdf output.docx --outdir ./

# Verify soffice exists
where soffice  # Windows
which soffice  # macOS/Linux
```

In Python, guard:

```python
import shutil, subprocess

def convert_with_libreoffice(source_path, target_format):
    if shutil.which("soffice") is None:
        raise RuntimeError("LibreOffice 'soffice' not on PATH — install LibreOffice to convert to .doc/PDF")
    result = subprocess.run(
        ["soffice", "--headless", "--convert-to", target_format, source_path, "--outdir", "."],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
```

On Windows Server/CI without LibreOffice, `docx2pdf` (Windows-only, requires Word) is an alternative for PDF: `pip install docx2pdf`.

---

## 13. Common Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `AttributeError: 'Document' has no attribute 'add_header'` | Headers live on `section.header`, not `document` | Use `section.header.paragraphs[0]` |
| `ValueError: style 'Caption' already exists` | Adding a style that already exists | `try: add_style / except ValueError: styles[name]` |
| Table has no borders | `table.style` left as default `Table Grid` but style gallery expects `Light Grid` | Set `table.style = "Light Grid Accent 1"` explicitly |
| Image overflows margin | Hard-coded `Inches(7)` on a narrow-margin section | Compute `content_width_in` per section and cap |
| Field shows `{ PAGE }` literal | Missing `fldChar` begin/separate/end trio | Use the exact 3-element recipe above |
| Section margins ignored | Set after `add_section()` without selecting the new section | Assign to `new_section`, not `document.sections[0]` |

---

## 14. OOXML Escape Hatch — When python-docx Has No Helper

Drop to raw `OxmlElement` with `qn("w:...")`. Every such block must be commented with the OOXML element it emits and why the high-level API is insufficient. Example:

```python
# OOXML: <w:shd w:fill="1B4F72" w:val="clear"/> — table header shading; python-docx has no Cell.shading API
shading = OxmlElement("w:shd")
shading.set(qn("w:fill"), "1B4F72")
shading.set(qn("w:val"), "clear")
cell._tc.get_or_add_tcPr().append(shading)
```

Keep escape hatches isolated in one helper module — not scattered across the generation code.
