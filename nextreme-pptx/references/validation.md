# Validation — No Overlap, No Overflow, No Glitch

Run `python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --strict` (or `python nextreme-pptx/scripts/validate_pptx.py deck.pptx --strict`) plus a 30-second visual in PowerPoint + one other viewer. Unzipping the OOXML proves more than a preview.

## 1. File Validity

- [ ] Valid ZIP (`file` says `Zip archive`). `zipfile.testzip()` is `None`.
- [ ] Required parts: `ppt/presentation.xml`, `ppt/slides/slide*.xml`, `ppt/slideLayouts/*.xml`, `ppt/slideMasters/*.xml`, `ppt/theme/theme*.xml`, `[_Content_Types].xml`, `docProps/core.xml`.
- [ ] No OLE2 header (`D0 CF 11 E0`) — that’s `.ppt`, not `.pptx`.
- [ ] ≥1 slide; ≤150 slides without explicit user approval for longer (sanity gate).

## 2. Anti-Overlap — The Glitch That Kills Trust

- [ ] **No shape overlap** — for every `p:sp`/`p:cxnSp`/`p:graphicFrame` (tables/charts) on a slide, `left+width ≤ right_of_next - GUTTER` and `top+height ≤ bottom_of_next - CARD_GAP`. Checker uses `a:xfrm` (`a:off x/y` + `a:ext cx/cy`) in EMU (1″ = 914400 EMU). Fail on any overlap > `0.04″` (tolerance for rounded rect stroke).
- [ ] **Gutters honoured** — inter-card gaps equal `GUTTER` ± `0.02″`; inter-row gaps equal `SECTION_GAP` ± `0.02″`. Drift of one card 7px while others snap = fail.
- [ ] **Off-canvas → fail** — `left < MARGIN - 0.02″` or `left+width > SLIDE_WIDTH-MARGIN + 0.02″` or `top+height > SLIDE_HEIGHT-MARGIN` is hard fail (PowerPoint silently clips).

`--check-overlap` enforces all of the above via EMU math.

## 3. Anti-Overflow — Text That Wraps Without Glitch

- [ ] **No overflow** — every `a:txBody` with `noAutofit` does not exceed its `a:ext` bounds. Checker compares `estimated line count × line height` vs `height`; and also `largest run width` vs `width` for single-line titles.
- [ ] **`autoFit off` where expected** — body textboxes use `noAutofit` (so a long word `wordWrap`s instead of shrinking glitchy to 4pt via `normAutofit`). `normAutofit` (`fontScale`/`lnSpcReduction`) is allowed only for hero cover titles that intentionally shrink.
- [ ] **`wordWrap=True`** on every `p:txBody` that holds prose/bullets. Missing `wordWrap` → `validate_pptx.py` warns.
- [ ] **Narrow box gate:** no text box narrower than `2.5″` holds body/bullets (forces mid-word break). KPI cards get `3-col (≈2.8″)` min.

`--check-overflow` enforces.

## 4. No AI Slop / Placeholders Residue

- [ ] Search (case-insensitive) `lorem ipsum`, `lorem`, `placeholder`, `your text here`, `insert text`, `TBD`, `xxx`; plus PPTX-specific residue: `Click to add title`, `Click to add text`, `TODO` without `[CONTENT REQUIRED:`. Zero hits unless the user approved a `[CONTENT REQUIRED: ...]` marker.
- [ ] No screenshot charts: flag `p:pic` whose `descr` suggests “chart” while a native `c:chart` exists nearby with same numbers → you pasted a chart as image; replace with `c:chart`.
- [ ] No full-slide raster: flag slide where single `p:pic` covers `≥90%` of `SLIDE_WIDTH×SLIDE_HEIGHT` — likely an exported PNG deck.
- [ ] `Ghost-deck` passes — titles alone tell the story (spot-check).

`--check-editable` + slop scan enforces.

## 5. Theme Preservation (Not Overlay)

- [ ] **No hard RGB where theme expects indirection** — for slides using a profiled template (presence of `config.json`), `--check-theme` scans `a:solidFill` writing: `a:srgbClr` vs `a:schemeClr`. Hard `srgbClr` on a slot that the template master maps to `accent1` → fail (breaks global recolor).
- [ ] **Font stack intact:** runs don’t hard-override master `a:fontRef` unless token demands it — `validate_pptx.py` cross-checks `style-system.md` stacks.
- [ ] **Master not mutated mid-pipeline:** editing `ppt/slideMasters` during deck build is hard fail.

## 6. List & Numbering Hygiene

- [ ] Bullets are `a:buChar`/`a:buBlip`, not typed `• ` or `1. ` in `a:t`.
- [ ] Multilevel indents use `marL`/`indent` at `a:pPr`, not spaces.
- [ ] ≤7 bullets per slide (`MAX_BULLETS`); violations fail strict.

## 7. Geometry Spot-Check (Human 30-sec)

Open in PowerPoint + Keynote or Google Slides:

- [ ] Grid: `View → Guides` shows equal gutters; no card drifted 7px.
- [ ] Alignment: titles sit on same baseline across consecutive slides.
- [ ] Reflow: add a bullet mid-slide — does anything wrap glitchy?

Fix at root: geometry → fix bounds math; theme → fix `schemeClr`; placeholder → fill `ph` `idx` via `_element`, not overlay.

## Running the Validator

```bash
# Full strict (skills.sh):
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --strict
# Local clone:
python nextreme-pptx/scripts/validate_pptx.py deck.pptx --strict

# Focused:
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --check-overlap
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --check-overflow
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --check-theme
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py deck.pptx --check-editable

# Render gate (optional, if soffice on PATH):
soffice --headless --convert-to pdf deck.pptx --outdir . && pdftoppm deck.pdf deck -png
# Visually inspect deck-1.png … deck-N.png for clipping/overlap at render fidelity
```

Exit 0 = pass; non-zero = fail with geometry numbers proving the fix. Do not ship a failing deck.

## Golden-Rules Spot-Check

Pick 3 functions in `scripts/create_pptx.py` and verify: names tell truth, one job, guard clauses, no duplication, no magic numbers (every `Inches()` is a token), errors logged with context.
