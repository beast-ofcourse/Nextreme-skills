#!/usr/bin/env node
/**
 * nextreme-pdf — HTML + Tailwind → PDF via Playwright + Paged.js (best taste)
 *
 * Self-contained, no React build, no component lib — flat DOM, geometric spacing,
 * Paged.js polyfill injected by this script (not by source HTML).
 *
 * Install once:
 *   npm install -D playwright
 *   npx playwright install chromium
 *   # Tailwind CDN needs internet; for offline compile: npx tailwindcss -i ./src/input.css -o ./dist/tailwind.css
 *
 * Usage (skills.sh):
 *   node ${CLAUDE_SKILL_DIR}/scripts/render_pdf.mjs --html ${CLAUDE_SKILL_DIR}/templates/report.html --out ./report.pdf --format A4
 * Local:
 *   node nextreme-pdf/scripts/render_pdf.mjs --html ./build/report.html --out ./report.pdf
 *
 * Mirrors pdf-forge / Kami HTML Route (Playwright + Paged.js) with correct polyfill handling.
 */

import { readFileSync, existsSync } from "fs";
import { resolve } from "path";
import { fileURLToPath } from "url";

function parseArgs() {
  const a = process.argv.slice(2);
  const g = (k) => {
    const i = a.indexOf(k);
    return i !== -1 && i + 1 < a.length ? a[i + 1] : null;
  };
  return {
    html: g("--html"),
    out: g("--out"),
    format: g("--format") || "A4",
  };
}

function fail(msg) {
  console.error(`[render_pdf] ${msg}`);
  process.exit(1);
}

async function main() {
  const { html: htmlPath, out: outPath, format } = parseArgs();
  if (!htmlPath || !outPath) fail("Usage: node render_pdf.mjs --html <html> --out <pdf> [--format A4]");
  if (!existsSync(htmlPath)) fail(`HTML not found: ${htmlPath}`);

  let chromium;
  try {
    const { chromium: ch } = await import("playwright");
    chromium = ch;
  } catch (e) {
    fail(`playwright not installed — run: npm install -D playwright && npx playwright install chromium\n${e.message}`);
  }

  // Resolve Chromium — support system chromium fallback via browser_helper pattern
  let browser;
  try {
    browser = await chromium.launch({ args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  } catch (e) {
    fail(`Chromium launch failed — missing libs? Run: npx playwright install chromium --with-deps\n${e.message}`);
  }

  try {
    const page = await browser.newPage();
    const html = readFileSync(htmlPath, "utf-8");

    // Guard: source must not already load paged.polyfill.js (it corrupts layout)
    if (html.includes("paged.polyfill")) {
      console.warn("[render_pdf] WARN: source HTML already loads paged.polyfill.js — remove it, this script injects it");
    }
    // Guard: counter-reset conflict (html_to_pdf.js 192-208)
    if (/counter-reset\s*:/i.test(html)) {
      console.warn("[render_pdf] WARN: CSS counter-reset detected — Paged.js owns counters, may conflict");
    }

    await page.setContent(html, { waitUntil: "networkidle" });

    // Inject Paged.js polyfill — prefer local vendor, else CDN
    const pagedCandidates = [
      resolve("node_modules/pagedjs/dist/paged.polyfill.js"),
      resolve("node_modules/pagedjs/dist/paged.polyfill.mjs"),
      // fallback CDN (requires network)
      null,
    ];
    let injected = false;
    for (const cand of pagedCandidates) {
      if (cand && existsSync(cand)) {
        await page.addScriptTag({ path: cand });
        injected = true;
        break;
      }
    }
    if (!injected) {
      // CDN fallback (pdf-forge style)
      try {
        await page.addScriptTag({ url: "https://unpkg.com/pagedjs/dist/paged.polyfill.js" });
        injected = true;
      } catch {
        console.warn("[render_pdf] Paged.js not injected — headers/footers via @page may not paginate; continuing with native print");
      }
    }

    // Wait for fonts + Paged.js + Mermaid/KaTeX
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(1500); // Mermaid/KaTeX settle (html_to_pdf.js delay)
    // Let Paged.js finish: wait for .pagedjs_pages or fallback timeout
    try {
      await page.waitForSelector(".pagedjs_pages", { timeout: 4000 });
    } catch {
      // No Paged.js pages — ok, will use native print
    }

    // Overflow guard (from Kami HTML Route): pre, table, img > page width
    const overflow = await page.evaluate(() => {
      const bad = [];
      for (const el of document.querySelectorAll("pre, table, img")) {
        if (el.scrollWidth > document.documentElement.clientWidth + 1) bad.push(el.tagName);
      }
      return bad;
    });
    if (overflow.length) console.warn(`[render_pdf] Overflow guard: ${overflow.join(",")} exceeds page width — add max-width:100%`);

    await page.pdf({
      path: outPath,
      format,
      printBackground: true,
      preferCSSPageSize: true,
      margin: undefined, // honor @page margins
    });

    console.log(`[render_pdf] Wrote ${outPath} (${format}, Paged.js ${injected ? "injected" : "fallback"})`);
  } finally {
    await browser.close();
  }
}

main().catch((e) => fail(String(e.stack || e)));
