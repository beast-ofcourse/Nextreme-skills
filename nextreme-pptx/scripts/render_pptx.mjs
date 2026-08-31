#!/usr/bin/env node
/**
 * nextreme-pptx — PptxGenJS fallback lane (JS)
 * Same Bento tokens as Python; for Node-available envs or when user prefers PptxGenJS.
 *
 * Ships inside the skill so `skills.sh` copies it. Requires Node >=18.
 *
 * Install (once):
 *   npm install pptxgenjs
 *   # or via skill: npm install --prefix ${CLAUDE_SKILL_DIR}/scripts pptxgenjs
 *
 * Usage (skills.sh):
 *   node ${CLAUDE_SKILL_DIR}/scripts/render_pptx.mjs --spec ${CLAUDE_SKILL_DIR}/templates/pitch_spec.yaml --out ./deck.pptx --theme vc_clean
 * Local:
 *   node nextreme-pptx/scripts/render_pptx.mjs --spec nextreme-pptx/templates/pitch_spec.yaml --out ./deck.pptx
 *
 * Spec: same YAML/JSON as scripts/create_pptx.py — theme_key, slide_size, slides[{type, title, ...}]
 * This lane is intentionally thin: it mirrors the 7 Bento layouts + 12 card types with PptxGenJS primitives.
 * For geometry-critical enterprise decks (brand template), prefer the Python slide-master lane.
 */

import { readFileSync, writeFileSync, existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const PALETTES = {
  vc_clean:        { BG: "FFFFFF", FG: "1A1A1E", FG_MUTED: "6B7280", ACCENT: "1B4F72", ACCENT_2: "2E86AB", ACCENT_3: "A8DADC", SURFACE: "F3F4F6", BORDER: "E5E7EB" },
  academic_minimal: { BG: "FFFFFF", FG: "111827", FG_MUTED: "6B7280", ACCENT: "374151", ACCENT_2: "9CA3AF", ACCENT_3: "E5E7EB", SURFACE: "F9FAFB", BORDER: "E5E7EB" },
  research_dark:    { BG: "0F172A", FG: "E2E8F0", FG_MUTED: "94A3B8", ACCENT: "38BDF8", ACCENT_2: "FB923C", ACCENT_3: "334155", SURFACE: "1E293B", BORDER: "334155" },
  editorial:       { BG: "FFF1F2", FG: "1F2937", FG_MUTED: "6B7280", ACCENT: "E11D48", ACCENT_2: "FB7185", ACCENT_3: "FFE4E6", SURFACE: "FFF7F7", BORDER: "FFE4E6" },
};

function parseArgs() {
  const args = process.argv.slice(2);
  const get = (flag) => {
    const idx = args.indexOf(flag);
    return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : null;
  };
  return {
    spec: get("--spec"),
    out: get("--out"),
    theme: get("--theme") || null,
  };
}

function loadSpec(specPath) {
  const text = readFileSync(specPath, "utf-8");
  if (specPath.endsWith(".json")) return JSON.parse(text);
  // light YAML for .yaml — require js-yaml if present, else naive
  try {
    const yaml = awaitImportYaml();
    return yaml.load(text);
  } catch {
    throw new Error(`Cannot parse YAML ${specPath}: install 'js-yaml' (npm install js-yaml) or use JSON`);
  }
}

function awaitImportYaml() {
  // dynamic import across CJS/ESM boundary — try require first
  try {
    return eval("require")("js-yaml");
  } catch {
    throw new Error("js-yaml not installed");
  }
}

async function main() {
  const { spec: specPath, out: outPath, theme: themeArg } = parseArgs();
  if (!specPath || !outPath) {
    console.error("Usage: node render_pptx.mjs --spec <yaml|json> --out <pptx> [--theme vc_clean]");
    process.exit(2);
  }
  let PptxGenJS;
  try {
    PptxGenJS = (await import("pptxgenjs")).default;
  } catch (e) {
    console.error("[render_pptx] Missing 'pptxgenjs' — run: npm install pptxgenjs  (or npm install --prefix ${CLAUDE_SKILL_DIR}/scripts pptxgenjs)");
    console.error(String(e));
    process.exit(2);
  }

  let raw;
  try {
    // handle YAML via dynamic import
    if (specPath.endsWith(".yaml") || specPath.endsWith(".yml")) {
      const jsYaml = (await import("js-yaml")).default || (await import("js-yaml"));
      raw = jsYaml.load(readFileSync(specPath, "utf-8"));
    } else {
      raw = JSON.parse(readFileSync(specPath, "utf-8"));
    }
  } catch (e) {
    console.error(`[render_pptx] Load failed: ${e.message}`);
    process.exit(1);
  }

  const themeKey = themeArg || raw.theme_key || "vc_clean";
  const palette = PALETTES[themeKey];
  if (!palette) {
    console.error(`[render_pptx] Unknown theme '${themeKey}' — expected one of ${Object.keys(PALETTES).join(", ")}`);
    process.exit(1);
  }

  const pptx = new PptxGenJS();
  // 16:9 default
  const size = String(raw.slide_size || "16:9");
  if (size === "4:3") pptx.layout = "LAYOUT_4x3";
  else pptx.layout = "LAYOUT_WIDE";

  const slides = raw.slides || [];
  if (!Array.isArray(slides) || slides.length === 0) {
    console.error("[render_pptx] spec.slides must be non-empty array");
    process.exit(1);
  }

  for (const slideSpec of slides) {
    const type = String(slideSpec.type || "").toLowerCase();
    const slide = pptx.addSlide();
    slide.background = { color: palette.BG };

    if (type === "cover") {
      slide.addText(String(slideSpec.title || raw.title || ""), { x: 0.6, y: 2.0, w: 12.1, h: 1.2, fontSize: 32, bold: true, color: palette.ACCENT, align: "center", fontFace: "Calibri" });
      if (slideSpec.subtitle) slide.addText(String(slideSpec.subtitle), { x: 0.6, y: 3.4, w: 12.1, h: 0.6, fontSize: 10, color: palette.FG_MUTED, align: "center" });
    } else if (type === "section_header") {
      slide.addText(String(slideSpec.kicker || "").toUpperCase(), { x: 0.8, y: 2.3, w: 8, h: 0.3, fontSize: 8, bold: true, color: palette.FG_MUTED });
      slide.addText(String(slideSpec.title || ""), { x: 0.8, y: 2.75, w: 8, h: 0.9, fontSize: 26, bold: true, color: palette.FG });
      slide.addShape(pptx.ShapeType.rect, { x: 0.6, y: 2.4, w: 0.08, h: 1.2, fill: { color: palette.ACCENT } });
    } else if (type === "quote") {
      slide.addText(`“${slideSpec.quote || ""}”`, { x: 2.5, y: 2.2, w: 8.3, h: 1.6, fontSize: 16, italic: true, color: palette.FG, align: "center", fontFace: "Georgia" });
      if (slideSpec.attribution) slide.addText(String(slideSpec.attribution), { x: 2.5, y: 3.9, w: 8.3, h: 0.4, fontSize: 9, color: palette.FG_MUTED, align: "right" });
    } else if (type === "bento_features" || type === "moat_columns" || type === "comparison") {
      if (slideSpec.title) slide.addText(String(slideSpec.title), { x: 0.6, y: 0.5, w: 12.1, h: 0.45, fontSize: 14, bold: true, color: palette.FG });
      const items = slideSpec.items || [];
      const span = items.length === 2 ? 6 : items.length === 3 ? 4 : items.length === 4 ? 3 : 12;
      const cardW = (12.13 - (12 / span - 1) * 0.32) / (12 / span); // approx slot width 12-col
      let left = 0.6;
      for (const item of items) {
        const t = typeof item === "string" ? item : (item.title || "");
        const b = typeof item === "string" ? "" : (item.body || "");
        slide.addShape(pptx.ShapeType.roundRect, { x: left, y: 1.4, w: cardW, h: 3.4, fill: { color: palette.SURFACE }, line: { color: palette.BORDER, width: 0.75 } });
        slide.addText(t, { x: left + 0.28, y: 1.6, w: cardW - 0.56, h: 0.4, fontSize: 10, bold: true, color: palette.FG });
        if (b) slide.addText(b, { x: left + 0.28, y: 2.05, w: cardW - 0.56, h: 1.8, fontSize: 8, color: palette.FG_MUTED });
        left += cardW + 0.32;
      }
    } else if (type === "stats_grid") {
      if (slideSpec.title) slide.addText(String(slideSpec.title), { x: 0.6, y: 0.5, w: 12.1, h: 0.45, fontSize: 14, bold: true, color: palette.FG });
      const stats = slideSpec.stats || [];
      const cardW = stats.length === 4 ? 2.8 : stats.length === 3 ? 3.8 : 5.8;
      let left = 0.6;
      for (const s of stats) {
        slide.addShape(pptx.ShapeType.roundRect, { x: left, y: 2.2, w: cardW, h: 1.9, fill: { color: palette.SURFACE }, line: { color: palette.BORDER, width: 0.75 } });
        slide.addText(String(s.value || ""), { x: left + 0.28, y: 2.4, w: cardW - 0.56, h: 0.7, fontSize: 22, bold: true, color: palette.FG, fontFace: "Consolas" });
        slide.addText(String(s.label || "").toUpperCase(), { x: left + 0.28, y: 3.15, w: cardW - 0.56, h: 0.3, fontSize: 8, bold: true, color: palette.FG_MUTED });
        if (s.delta) slide.addText(String(s.delta), { x: left + 0.28, y: 3.55, w: cardW - 0.56, h: 0.3, fontSize: 8, color: palette.ACCENT });
        left += cardW + 0.32;
      }
    } else if (type === "matrix_2x2" || type === "matrix") {
      if (slideSpec.title) slide.addText(String(slideSpec.title), { x: 0.6, y: 0.5, w: 12.1, h: 0.45, fontSize: 14, bold: true, color: palette.FG });
      // outer rect 8x4.2 centered
      slide.addShape(pptx.ShapeType.rect, { x: 2.66, y: 1.6, w: 8.0, h: 4.2, fill: { color: "FFFFFF" }, line: { color: palette.BORDER } });
      slide.addShape(pptx.ShapeType.rect, { x: 6.65, y: 1.6, w: 0.02, h: 4.2, fill: { color: palette.BORDER } });
      slide.addShape(pptx.ShapeType.rect, { x: 2.66, y: 3.68, w: 8.0, h: 0.02, fill: { color: palette.BORDER } });
      for (const it of (slideSpec.items || [])) {
        const x = 2.66 + 8.0 * Math.max(0.05, Math.min(0.95, it.x || 0.5));
        const y = 1.6 + 4.2 * Math.max(0.05, Math.min(0.95, it.y || 0.5));
        slide.addShape(pptx.ShapeType.oval, { x: x - 0.07, y: y - 0.07, w: 0.14, h: 0.14, fill: { color: palette.ACCENT } });
        if (it.label) slide.addText(String(it.label), { x: x - 0.6, y: y + 0.12, w: 1.3, h: 0.25, fontSize: 7, bold: true, color: palette.FG, align: "center" });
      }
    } else if (type === "timeline") {
      if (slideSpec.title) slide.addText(String(slideSpec.title), { x: 0.6, y: 0.5, w: 12.1, h: 0.45, fontSize: 14, bold: true, color: palette.FG });
      slide.addShape(pptx.ShapeType.rect, { x: 0.6, y: 3.4, w: 12.13, h: 0.04, fill: { color: palette.BORDER } });
      const ms = slideSpec.milestones || [];
      const span = 12.13 / Math.max(1, ms.length);
      ms.forEach((m, idx) => {
        const cx = 0.6 + span / 2 + idx * span;
        slide.addShape(pptx.ShapeType.oval, { x: cx - 0.09, y: 3.32, w: 0.18, h: 0.18, fill: { color: palette.ACCENT } });
        slide.addText(String(m.label || `M${idx + 1}`), { x: cx - 0.9, y: 3.65, w: 1.8, h: 0.3, fontSize: 8, bold: true, color: palette.ACCENT, align: "center" });
        if (m.title) slide.addText(String(m.title), { x: cx - 0.9, y: 3.95, w: 1.8, h: 0.5, fontSize: 7, color: palette.FG, align: "center" });
      });
    } else {
      // fallback: title + bullets
      if (slideSpec.title) slide.addText(String(slideSpec.title), { x: 0.6, y: 0.5, w: 12.1, h: 0.45, fontSize: 14, bold: true, color: palette.FG });
      const bullets = slideSpec.bullets || slideSpec.items || [];
      if (Array.isArray(bullets) && bullets.length) {
        slide.addText(bullets.map(b => typeof b === "string" ? b : (b.title || b.text || "")).join("\n"), { x: 0.6, y: 1.4, w: 12.1, h: 4.0, fontSize: 10, color: palette.FG, bullet: { type: "bullet" } });
      }
    }
  }

  await pptx.writeFile({ fileName: outPath });
  console.log(`[render_pptx] Wrote ${outPath} — ${slides.length} slides — theme ${themeKey}`);
}

main().catch(e => { console.error("[render_pptx] Failed:", e); process.exit(1); });
