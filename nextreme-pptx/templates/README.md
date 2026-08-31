# Templates — Starter Specs for Nextreme PPTX

Copy a spec, replace the bracketed content with real story, run `create_pptx.py`. Every template is a valid YAML that renders a geometry-clean `.pptx` with zero edits beyond content — swap `theme_key` to recolor without touching slides.

**Install (once):**
```bash
# skills.sh
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt
# local clone
pip install -r nextreme-pptx/requirements.txt
# JS lane (optional, for PptxGenJS speed):
npm install --prefix ${CLAUDE_SKILL_DIR}/scripts pptxgenjs
```

**Run — skills.sh vs local:**

```bash
# Pitch (skills.sh)
python ${CLAUDE_SKILL_DIR}/scripts/create_pptx.py --spec ${CLAUDE_SKILL_DIR}/templates/pitch_spec.yaml --output ./pitch.pptx
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py ./pitch.pptx --strict

# Report (local clone)
python nextreme-pptx/scripts/create_pptx.py --spec nextreme-pptx/templates/report_spec.yaml --output ./report.pptx
python nextreme-pptx/scripts/validate_pptx.py ./report.pptx --strict

# JS lane (PptxGenJS)
node ${CLAUDE_SKILL_DIR}/scripts/render_pptx.mjs --spec ${CLAUDE_SKILL_DIR}/templates/pitch_spec.yaml --out ./pitch-js.pptx --theme vc_clean

# Branded template (fidelity path)
python ${CLAUDE_SKILL_DIR}/scripts/create_pptx.py --spec ./my-deck.yaml --output ./deck.pptx --template ./branded-template.pptx
```

**Specs included:**
- `pitch_spec.yaml` — founder/investor pitch (10 slides: cover → problem → why_now → bento → matrix → stats → timeline → team → ask → closing)
- `report_spec.yaml` — board KPI report (cover → section → bar_chart → results_table → bento → quote)
- `academic_spec.yaml` — research talk (cover → method → results_table → bar_chart → references)
- `editorial_spec.yaml` — brand story (cream editorial, quote-driven)
- `bento_spec.yaml` — 7 Bento Grid layout demos (one per layout)

Each `slides[]` item is one of 17+ `type`s (see `references/slide-types.md`). Validate before sharing:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/validate_pptx.py ./deck.pptx --strict
# or local
python nextreme-pptx/scripts/validate_pptx.py ./deck.pptx --strict
```
