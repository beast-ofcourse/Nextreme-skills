# Style System — Tokens, Not Templates

You don’t pick “style 14”. You derive palette, type, and density from the story — tokens make the deck coherent without cloning one of Akxan’s 26.

## 1. Canvas Presets — Geometry Is Law

| Preset | `SLIDE_WIDTH` | `SLIDE_HEIGHT` | `MARGIN` | `GUTTER` | `GRID_COLS` | Use |
|---|---|---|---|---|---|---|
| **16:9 Pitch** (default) | 13.33″ | 7.5″ | 0.6″ | 0.32″ | 12 | Pitch, report, board — widescreen projector |
| **16:9 Wide** | 13.33″ | 7.5″ | 0.45″ | 0.28″ | 12 | Dense editorial, Bento showcase |
| **4:3 Academic** | 10″ | 7.5″ | 0.5″ | 0.30″ | 10 | Conference, defense — legacy projector |
| **A4 Print** | 11.69″ | 8.27″ | 0.55″ | 0.30″ | 12 | Print-first handout |

**Bounds math (use for every shape):**
```
CONTENT_WIDTH  = SLIDE_WIDTH  - 2*MARGIN
CONTENT_HEIGHT = SLIDE_HEIGHT - 2*MARGIN - HEADER_BAND (if any)
COL_WIDTH = (CONTENT_WIDTH - (GRID_COLS-1)*GUTTER) / GRID_COLS
slot_width(cols) = cols*COL_WIDTH + (cols-1)*GUTTER
assert(left >= MARGIN and left+width <= SLIDE_WIDTH-MARGIN)
assert(top  >= MARGIN and top+height  <= SLIDE_HEIGHT-MARGIN)
```

---

## 2. Color — Derived Palettes, Not Hard Slots

**Core tokens (recoloring layer, after PHY041):**

| Token | Default Hex | Role |
|---|---|---|
| `BG` | `#FFFFFF` | Slide fill |
| `FG` | `#1A1A1E` | Body text |
| `FG_MUTED` | `#6B7280` | Caption, metadata |
| `ACCENT` | `#1B4F72` | Heading, CTA, chart series 1 |
| `ACCENT_2` | `#2E86AB` | Series 2, bento border |
| `ACCENT_3` | `#A8DADC` | Series 3, tint bg |
| `SURFACE` | `#F3F4F6` | Card fill, table band |
| `BORDER` | `#E5E7EB` | Grid lines, card stroke |
| `SUCCESS` / `WARN` / `DANGER` | `#10B981` / `#F59E0B` / `#EF4444` | KPI deltas only |

**Derive per story (don’t hard-code Navy for everything):**
- Investor trust → Navy `ACCENT #1B4F72` + cream `BG #FFFBEB`
- Academic → Ink `#111827` + muted `ACCENT_2 #374151` + serif
- Editorial → `ACCENT #E11D48` on cream `BG #FFF1F2` + editorial serif
- Dark research → `BG #0F172A`, `FG #E2E8F0`, `ACCENT #38BDF8`

**Palette rule:** One `ACCENT` per deck + two tints (`ACCENT_2/3` derived at 70%/40% mix with `BG`). Changing `ACCENT` recolors all slides — hard `srgbClr` only where `schemeClr` not reachable.

---

## 3. Typography — Iron Law (7 Steps, Not Vibes)

**Borrowed from Akxan, enforced via tokens:**

| Level | Size | Weight | Tracking | Case | Use |
|---|---|---|---|---|---|
| `DISPLAY` | 44pt | 800 | -1.5% | — | Cover title (one line) |
| `H1` | 28pt | 700 | -1.2% | — | Section header |
| `H2` | 20pt | 600 | -0.8% | — | Slide title |
| `H3` | 14pt | 600 | -0.2% | `uppercase` + `ls 0.08em` | Eyebrow / kicker |
| `BODY` | 11pt | 400 | 0 | — | Bullets, body |
| `CAPTION` | 9pt | 400 | 0 | — | Source, footnote |
| `MONO` | 9pt | 500 | 0 | `tabular-nums` | KPI numbers, tables |

**Font stacks (3-layer downgrade, after Akxan + slide-kit):**
- Sans: `Inter → Calibri → Arial → Aptos` (covers Windows/Mac/Linux sans fallback)
- Serif: `Georgia → Times → Cambria → Noto Serif`
- Mono: `JetBrains Mono → Consolas → Menlo → monospace`
- Display serif mix: use serif for one word (italic) + sans for rest — not all-seriffed paragraph

**Hard rules:**
- `tabular-nums` for every number column/table/KPI (so “111” aligns over “888”).
- `font-feature-settings: "ss01","tnum"` where available; at least set `tabular-nums`.
- Never below 9pt for body-captions; never above 7 bullets (from Noi1r 29-rule set).
- One serif-italic word per deck is editorial signal; a serif-italic paragraph is noise.

---

## 4. Bento Grid — 7 Layouts, 12 Card Types (Palette, Not Prison)

**Grid:** 12 cols (16:9) / 10 cols (4:3), `GUTTER` as above. Every card snaps to column boundaries — never `left=Inches(2.37)` ad-hoc.

**7 Bento Layouts (from Akxan, simplified):**

| Layout | Columns | When | Geometry |
|---|---|---|---|
| **Single Focus** | 12 | One big claim | 12-col hero card, centered |
| **50-50 Symmetric** | 6+6 | Before/after | Two equal cards |
| **Asymmetric** | 7+5 | Primary-Secondary story | 7-col main + 5-col side |
| **Three-col Equal** | 4+4+4 | 3 features | Three cards |
| **Primary-Secondary** | 8+4 | Evidence + insight | 8-col chart/table + 4-col takeaway |
| **Hero + Subs** | 12 top + 3×4 bottom | Hero claim + 3 proofs | Top 12-col hero + bottom 3×4 |
| **Mixed Grid** | 6+3+3 / 8+2+2 | Dense proof | Mosaic — but still column-snapped |

**12 Card Types (what lives inside a card):**

`text` · `bullets` · `kpi` · `stat_grid` · `bar_chart` · `line_chart` · `table` · `quote` · `timeline` · `process` · `comparison` · `image_text` — each card declares its own inner padding `CARD_PAD = 0.28″` and min height.

**Density rhythm (cross-page narrative, after Akxan+PHY041):**
```
Cover (sparse, DISPLAY) → Section header (sparse) → Evidence dense (stats_grid/bar_chart/table) → Insight sparse (quote/takeaway) → Repeat
```
Two dense slides back-to-back = density leak → insert sparse palette cleanser.

---

## 5. Spacing — Card & Slide Rhythm

| Token | Value | Role |
|---|---|---|
| `CARD_PAD` | 0.28″ | Inset text from card border |
| `CARD_GAP` | `GUTTER` | Between cards on same slide |
| `SECTION_GAP` | 1.2″ | Between card rows |
| `BULLET_SPACE_AFTER` | 6pt | Tight, not airy |
| `TITLE_SPACE_AFTER` | 14–18pt | Breathing after H2 before body |
| `KPI_NUM_SIZE` | MONO 28pt tabular | KPI hero number |
| `KPI_LABEL_SIZE` | H3 9pt uppercase | KPI label |

---

## 6. Shadows & Borders — One Logic

- **Card border:** `stroke=BORDER 0.75pt` + `fill=SURFACE @ 40% opacity` for elevated cards, `fill=BG` for flat. No dual shadows.
- **Rounded:** `rx=8pt` for cards, `rx=4pt` for inner chips. Never mix `rx=0` rects with `rx=16` pills on same deck.
- **Elevation:** One shadow (`blur 12pt @ 10% black, y=4pt`) for hero cards only; secondary cards flat. Two shadows stacked = mud.

---

## 7. Theme as Recoloring Layer (After PHY041)

A deck is **content × theme**. Swapping `theme_key` must recolor all slides without touching `slides.md`/`spec.yaml`:

- **Theme files:** `${CLAUDE_SKILL_DIR}/themes/{vc_clean, academic_minimal, research_dark, editorial}.json` (4 starter themes; add yours as `themes/custom.json`).
- **Mapping:** Each token above maps to `a:schemeClr` (`bg1`, `tx1`, `accent1`…) in OOXML — not hard `srgbClr`. Changing `accent1` in `ppt/theme/theme1.xml` recolors every `a:schemeClr val="accent1"` shape.

---

## 8. Visual QA Tokens (For Validation Gate)

| Token | Gate |
|---|---|
| `MIN_TEXTBOX_WIDTH` | 2.5″ — narrower forces glitchy wrapping |
| `MAX_BULLETS` | 7 — more → overflow or density leak |
| `MIN_CARD_HEIGHT` | 1.1″ — smaller is unreadable at 80% zoom |
| `TITLE_MAX_LINES` | 2 — longer → wrapping badge mis-aligns decorative line |
| `TABLE_MIN_ROW_H` | 0.28″ — tighter clips descenders |

If a value breaches its token, `validate_pptx.py` fails with the exact geometry.
