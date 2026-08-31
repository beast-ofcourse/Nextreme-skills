# Validation — Strict Checklist (When Code Can Run)

Run `python ${CLAUDE_SKILL_DIR}/scripts/validate_svg.py icon.svg --strict` or fallback to this list.

## Strict (via script)

- [ ] XML well-formed (`ET.parse` no error)
- [ ] `viewBox` present, `xmlns="http://www.w3.org/2000/svg"` present
- [ ] No banned: `<script>`, event handlers (`onclick`), `javascript:` URLs, `<foreignObject>`, external CSS/`@import`, external fonts, embedded raster (`data:image`), `width`/`height` without `viewBox`
- [ ] ID resolution: every `url(#id)` has a matching `id="..."` in `<defs>`
- [ ] Path `d` sanity: valid BNF (`M/L/H/V/C/S/Q/T/A/Z`), smooth reflection valid, no empty `d`
- [ ] Security: W3C/OWASP/DOMPurify deny list — same as above plus `v:`, `o:` prefixes
- [ ] A11y: meaningful graphics have `role="img"` + `<title>` + `<desc>`; decorative have `aria-hidden="true"`; `lang` where needed
- [ ] SMIL hijack: no `<animate>` that moves outside viewBox by >2×

## Manual (when script can’t run)

Same list, eyeballed. Plus:

- [ ] No flat 2-stop gradient (need 4–8)
- [ ] No pure-black shadow
- [ ] No arrow through box/text
- [ ] No text overflow (every label’s `char × 0.6 × fontSize` < box width)
- [ ] No `foreignObject`

Fix every fail and rerun until clean. Then `render_svg.py` at 2× for visual check.
