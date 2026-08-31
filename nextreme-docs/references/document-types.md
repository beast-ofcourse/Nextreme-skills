# Document Types — Patterns, Inventories, and Section Order

Pick the pattern that matches the user's inventory. Each pattern lists **required blocks** — if a block has no content, mark `[CONTENT REQUIRED: ...]` visibly; do not invent.

---

## 1. Report (Business / Technical)

**When:** analyses, findings, quarterly reports, audit reports, research summaries.
**Paper:** A4 Standard Report (0.85in margins). Different first page (cover without header/footer).

**Required blocks in order:**

1. **Cover page** — Title (`Title` style, 28pt accent), Subtitle, Author/org, Date (`Normal` 10pt muted, bottom-aligned). Optional accent band at top.
2. **TOC** — Heading "Contents" + field `TOC \o "1-3" \h \z` on page 2.
3. **Executive Summary** — Heading 1, 1–2 paragraphs. What was done, what was found, what is recommended — in that order.
4. **Body** — Heading 1 per chapter (Introduction, Methodology, Findings, Analysis, Recommendations). Heading 2/3 for subsections. Body in `Normal` with 8pt after.
5. **Tables** — caption `Caption` style `Table N — Title` before or after table; style `Light Grid Accent 1`; header row fill `ACCENT` white text; banded rows.
6. **Figures** — centered image `width ≤ SECTION_CONTENT_WIDTH - 0.1in`, caption `Figure N — Title` in `Caption` after figure, alt text on image.
7. **Conclusion** — Heading 1.
8. **Appendix** — optional; if landscape tables needed, new section with `orientation=LANDSCAPE`.
9. **Footer** — `Page X of Y` from page 2 onward; header "CONFIDENTIAL — {title}" if requested.

**Validation:** cover has no page number; TOC field exists; every table/figure is captioned and referenced in text ("see Table 1").

---

## 2. Proposal (Bid / Pitch)

**When:** project proposals, SOWs, grant proposals.
**Paper:** A4 Standard, cover band optional.

**Required blocks:**

1. **Cover** — Project name, client name, issuer, date.
2. **TOC** — field-backed.
3. **Problem → Solution** — Heading 1 "1. Overview" with problem statement + proposed approach.
4. **Scope & Timeline** — table or Gantt-style table (`Task | Owner | Start | End`); or numbered steps.
5. **Pricing table** — `Light Shading Accent 1` style, columns: Item, Qty, Unit Price, Amount, Total row bold with shading. Totals computed, not typed guesswork.
6. **Terms & Conditions** — numbered clauses (List Number) or contract-style multilevel if legal weight needed.
7. **Signature blocks** — two-column borderless table: left "Client", right "Provider", each with line (`___`), name, title, date.
8. **Footer** — proposal validity date + page numbers.

**Validation:** pricing totals sum correctly; signature lines are real table borders, not underscore text that reflows.

---

## 3. Resume / CV

**When:** job applications.
**Paper:** Letter Resume Tight (0.45/0.50in margins) — must fit 1 page, overflow to 2 only with user approval. No header/footer, no TOC, no page numbers.

**Required blocks:**

1. **Header** — Name (`Title` or 20pt bold accent, centered), Contact line (`Normal` 9pt muted, centered: email • phone • location • links). One line.
2. **Summary** — 2–3 sentences, `Normal` 10.5pt.
3. **Experience** — Heading 2 "Experience", each role: Role — Company — Location — Dates (right-aligned tab or table), bullets for impact (`List Bullet` tight, 2pt after).
4. **Skills matrix** — borderless or `Table Grid` with light shading header; columns: Category, Skills (e.g., "Languages | Python, TypeScript").
5. **Education** — Heading 2, degree — institution — dates.
6. **Optional** — Projects, Certifications, Publications as Heading 2 sections.

**Rules:** tight spacing (`space_after=2pt` for bullets, `line_spacing=1.0`), no justified text, no images, no tables with outer borders except skills matrix. Validate with `validate_docx.py --check-resume-length`.

---

## 4. Invoice

**When:** billing.
**Paper:** Letter Compact, single page preferred.

**Required blocks:**

1. **Header** — Seller block (logo if provided, name, address, tax ID) left; "INVOICE" title + number/date right; Buyer block ("Bill To:") below.
2. **Line-item table** — style `Light Shading Accent 1`, columns: # | Description | Qty | Unit Price | Amount. Header fill `ACCENT` white text. Banded rows. Right-align numeric columns.
3. **Totals** — Subtotal, Tax, Discount, Total rows — last row bold, larger, shaded `ACCENT_LIGHT`.
4. **Payment terms** — paragraph `Normal` 9.5pt muted: due date, method, bank details.
5. **Footer** — "Thank you for your business" + page 1 of 1, plus legal footer if required.
6. **No TOC, no headers** on invoice — keep it flat.

**Validation:** `Amount = Qty × Unit Price` per row; `Total = Subtotal + Tax - Discount` — compute, don't trust typed totals.

---

## 5. Formal Letter

**When:** correspondence, cover letters, official notices.
**Paper:** Letter Compact (0.75in margins), no TOC, first-page header is the letterhead.

**Required blocks:**

1. **Letterhead header** — org name/logo, address line, phone/email. In `section.header` or first paragraphs if no letterhead file.
2. **Date** — `DATE \@ "MMMM d, yyyy"` field or plain text right/left aligned per user preference. Use field for auto-current-date only if user wants it.
3. **Recipient block** — Name, Title, Org, Address, left-aligned, `Normal`.
4. **Subject** — `Subject: ...` bold, `Normal` + `run.bold=True` for the subject phrase.
5. **Salutation** — "Dear ...,".
6. **Body** — `Normal` with `first_line_indent=0` (block style) and `space_after=8pt`; or indent style per local convention — ask or default to block.
7. **Closing** — "Sincerely," / "Regards," + 3 blank paragraphs for signature gap + Name / Title / Org.
8. **Signature image** — optional inline image of signature centered over the gap.
9. **Footer** — optional confidentiality line, page numbers only if 2+ pages.

---

## 6. Contract / Agreement

**When:** legal agreements.
**Paper:** A4 Standard with gutter 0.15in, even/odd headers (`evenAndOddHeaders`), line numbers optional.

**Required blocks:**

1. **Title** — "AGREEMENT", "MASTER SERVICES AGREEMENT" in `Title` centered.
2. **Parties** — "This Agreement is between ... (\"Company\") and ... (\"Client\")".
3. **Recitals** — "WHEREAS ..." if needed.
4. **Definitions** — Heading 1 "1. Definitions", terms bold + quoted.
5. **Clauses** — multilevel numbering single `numId`: `1.` → `1.1` → `1.1.1`. Every clause is a paragraph with numbering, not typed "1.1.1".
6. **Exhibits** — Heading 1 "Exhibit A — ...", each on new page (`page_break_before=True` on heading).
7. **Signature blocks** — borderless 2-column table with lines, name, title, date.
8. **Footer** — "Page X of Y — Confidential" centered; first page may suppress.

**Rules:** never type numbering; use the multilevel helper. Exhibit pages break explicitly. Validate numbering has no duplicate or skipped levels.

---

## 7. Manual / SOP / Datasheet

**When:** product docs, procedures, technical specs.
**Paper:** A4 Standard, portrait body + landscape appendix for wide specs tables.

**Required blocks:**

1. **Cover** — product name, version, date, org.
2. **Revision history** — table: Version | Date | Author | Changes (style `Light Grid Accent 1`).
3. **TOC** — field.
4. **Safety / Overview** — Heading 1 with warning callouts (shaded `Intense Quote` or table with icon).
5. **Procedure steps** — numbered list (`List Number`) with figure per step. Prefer 2-column borderless table: left = figure, right = steps — not floating images.
6. **Specs table** — `Medium Grid 2 Accent 1` style, spec/value columns.
7. **Appendix** — landscape section for schematics or wide tables.
8. **Back cover / footer** — doc control ID + version + page numbers.

---

## 8. Academic Paper (IMRaD)

**When:** research papers.
**Paper:** A4 Academic (1in margins, gutter 0.15in), first-line indent 0.25in for body, no space-after between body paragraphs, double spacing optional (`line_spacing=2.0`).

**Required blocks:**

1. **Title / Authors / Affiliations / Abstract / Keywords** — centered, `Normal` + bold for title line, abstract in `Quote`.
2. **Introduction, Methods, Results, Discussion** — Heading 1 per IMRaD, Heading 2 subsections.
3. **Tables/Figures** — caption style `Caption`; in academic, caption above table, below figure.
4. **References / Bibliography** — Heading 1, hanging indent `0.5in` (`left_indent=Inches(0.5)`, `first_line_indent=Inches(-0.5)`), numbered or author-year per required style — ask which.
5. **Appendix, Acknowledgments** — if needed.

**Rules:** choose indentation or space-after, not both. Ask citation style (APA, IEEE, Chicago) if not stated.

---

## 9. Certificate

**When:** awards, completion, recognition.
**Paper:** A4 Landscape Certificate (0.60/0.70in margins), single page, no header/footer, no TOC.

**Required blocks:**

1. **Border frame** — page border via `w:pgBorders` with `w:top/left/bottom/right w:val="single" w:sz="12" w:color="154360"`.
2. **Title** — "CERTIFICATE OF COMPLETION" centered, `Title` 32pt `ACCENT_DARK`, letter-spacing via `w:spacing w:val="60"` (0.6pt expanded).
3. **Recipient name** — 24–28pt display, italic or script if available, centered, `ACCENT_DARK`.
4. **Body** — "is hereby awarded to ..." centered, 12pt.
5. **Issuer / Signature** — two-column borderless table at bottom: left issuer org, right signature line + name/title + date.
6. **Seal** — optional centered image (PNG) above signatures.

**Validation:** single section, landscape, one page only; `validate_docx.py` checks `page_count_estimate == 1`.

---

## Anti-Patterns (All Types)

- Typed page numbers ("Page 1") instead of `PAGE` field.
- Typed TOC instead of field.
- Headings as `Normal` + bold + larger font.
- Tables without style, captions, or column width math.
- Images wider than `SECTION_CONTENT_WIDTH`.
- Copy-pasted filler to reach a page count.
- `Lorem ipsum`, `TODO`, `TBD` without a ticketed `[CONTENT REQUIRED: ...]` marker.
