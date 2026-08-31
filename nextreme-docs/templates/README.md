# Templates — Starter Specs for Nextreme Docs

Copy a spec, replace the bracketed content with real data, and run `create_docx.py`. Every template is a complete, valid YAML that generates a styled `.docx` with zero edits — replace the example content, never the structure. All `scripts/` and `templates/` ship inside the skill ( `skills.sh` copies the whole `nextreme-docs/` folder ).

**Install deps once (skills.sh):**
```bash
pip install -r ${CLAUDE_SKILL_DIR}/requirements.txt
# local clone:
pip install -r nextreme-docs/requirements.txt
```

**Run — skills.sh ( `${CLAUDE_SKILL_DIR}` is the installed skill dir ) vs local clone:**

```bash
# Report — skills.sh
python ${CLAUDE_SKILL_DIR}/scripts/create_docx.py --spec ${CLAUDE_SKILL_DIR}/templates/report_spec.yaml --output ./report.docx
# Report — local clone
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/report_spec.yaml --output ./report.docx

# Proposal — local clone
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/proposal_spec.yaml --output ./proposal.docx

# Resume (gated to 2 pages)
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/resume_spec.yaml --output ./resume.docx
python nextreme-docs/scripts/validate_docx.py ./resume.docx --check-resume-length --max-pages 2

# Invoice
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/invoice_spec.yaml --output ./invoice.docx

# Letter
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/letter_spec.yaml --output ./letter.docx

# Contract
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/contract_spec.yaml --output ./contract.docx

# Manual
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/manual_spec.yaml --output ./manual.docx

# Certificate (landscape)
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/certificate_spec.yaml --output ./certificate.docx

# Academic paper
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/academic_spec.yaml --output ./paper.docx

# Convert to PDF or legacy .doc (always from canonical .docx) — requires LibreOffice on PATH
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/report_spec.yaml --output ./report.docx --pdf
python nextreme-docs/scripts/create_docx.py --spec nextreme-docs/templates/report_spec.yaml --output ./report.docx --doc
```

Each spec's `content` is an ordered list of blocks. See `references/document-engine.md` for the full block schema.

Validation:

```bash
# skills.sh
python ${CLAUDE_SKILL_DIR}/scripts/validate_docx.py ./output.docx --strict
# local clone
python nextreme-docs/scripts/validate_docx.py ./output.docx --strict
```
