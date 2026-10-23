// Xenova Solutions vertical video frames (1080x1920) for Reels / Shorts. Free: HTML/CSS + Playwright Chromium.
// Usage: node xreel.js <spec.json> <outDir>   -> <outDir>/s01.png, s02.png ...
// Spec: {id, scenes:[{layout:"hook"|"step"|"flow"|"cta", kicker, title, body, n, nodes:[{label,sub}], label, say}]}
// Brand colours are fixed (xenovasolutions.com theme). *word* = accent emphasis.
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");

const F = path.join(__dirname, "node_modules", "@fontsource");
const ff = (fam, pkg, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url('file://${F}/${pkg}/files/${pkg}-latin-${w}-normal.woff2') format('woff2')}`;
const FONTS = [...[600, 700, 800].map(w => ff("Bric", "bricolage-grotesque", w)), ...[400, 500, 600].map(w => ff("Plex", "ibm-plex-sans", w)),
  ...[400, 500].map(w => ff("Mono", "ibm-plex-mono", w))].join("\n");
const C = { bg: "#030F24", panel: "#071A36", line: "#16345F", text: "#F1F6F9", muted: "#93A6BE", accent: "#7FD6B3", accent2: "#3FA383" };
const esc = s => String(s ?? "").replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
const md = s => esc(s).replace(/\*(.+?)\*/g, '<em>$1</em>').replace(/\n/g, "<br>");

const CSS = `${FONTS}
*{box-sizing:border-box;margin:0}
body{width:1080px;height:1920px;background:${C.bg};color:${C.text};font-family:Plex,sans-serif;overflow:hidden;position:relative}
.grid{position:absolute;inset:0;background-image:linear-gradient(${C.line}55 1.5px,transparent 1.5px),linear-gradient(90deg,${C.line}55 1.5px,transparent 1.5px);background-size:60px 60px}
.glow{position:absolute;inset:0;background:radial-gradient(circle at 85% 12%,${C.accent}26,transparent 55%)}
.bar{position:absolute;top:0;left:0;right:0;height:10px;background:${C.accent}}
.frame{position:absolute;inset:150px 84px 230px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;justify-content:space-between}
.logo{display:flex;align-items:center;gap:18px}
.mark{width:72px;height:72px;border:2px solid ${C.line};background:${C.panel};border-radius:16px;display:grid;place-items:center}
.wm b{display:block;font:800 34px Bric;letter-spacing:.06em}.wm i{display:block;font:500 17px Mono;letter-spacing:.32em;color:${C.muted};font-style:normal}
.prog{display:flex;gap:10px}.prog span{width:44px;height:8px;border-radius:4px;background:${C.line}}.prog span.on{background:${C.accent}}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
.kicker{font:500 30px Mono;letter-spacing:.14em;text-transform:uppercase;color:${C.accent};margin-bottom:34px;display:flex;align-items:center;gap:16px}
.kicker:before{content:"";width:14px;height:14px;border-radius:50%;background:${C.accent}}
h1{font:800 112px/1.02 Bric;letter-spacing:-.02em}
h2{font:700 84px/1.06 Bric;letter-spacing:-.015em}
em{font-style:normal;color:${C.accent}}
.body{font:400 42px/1.42 Plex;color:${C.muted};margin-top:40px}
.body em{color:${C.text};font-weight:600}
.num{font:800 220px/1 Bric;color:${C.accent};margin-bottom:24px}
.node{display:flex;gap:28px;align-items:center;background:${C.panel};border:2px solid ${C.line};border-radius:22px;padding:30px 34px}
.node .ic{flex:none;width:76px;height:76px;border-radius:18px;border:2px solid ${C.accent2};color:${C.accent};display:grid;place-items:center;font:500 30px Mono}
.node h4{font:600 42px Plex}.node p{font:400 30px Mono;color:${C.muted};margin-top:6px}
.wire{width:2px;height:30px;background:${C.accent2};margin-left:72px}
.pill{display:inline-flex;align-items:center;gap:16px;background:${C.accent};color:${C.bg};font:600 40px Plex;padding:26px 44px;border-radius:999px;margin-top:60px;align-self:flex-start}
.label{position:absolute;left:84px;right:84px;bottom:150px;font:400 28px Mono;color:${C.muted}}
.bot{position:absolute;left:84px;right:84px;bottom:90px;display:flex;justify-content:space-between;font:400 28px Mono;color:${C.muted}}
`;
const logo = `<div class="logo"><span class="mark"><svg width="40" height="40" viewBox="0 0 24 24" fill="none"><path d="M4 4 20 20M20 4 4 20" stroke="${C.text}" stroke-width="2.1" stroke-linecap="round" opacity=".85"/><circle cx="12" cy="12" r="3.4" fill="${C.panel}"/><circle cx="12" cy="12" r="2.2" fill="${C.accent}"/></svg></span><span class="wm"><b>XENOVA</b><i>SOLUTIONS</i></span></div>`;

function body(s) {
  const k = s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : "";
  switch (s.layout) {
    case "hook": return `${k}<h1>${md(s.title)}</h1>${s.body ? `<p class="body">${md(s.body)}</p>` : ""}`;
    case "step": return `<div class="num">${esc(s.n)}</div>${k}<h2>${md(s.title)}</h2>${s.body ? `<p class="body">${md(s.body)}</p>` : ""}`;
    case "flow": return `${k}<h2 style="margin-bottom:46px">${md(s.title)}</h2>${s.nodes.map((n, i) => `${i ? '<div class="wire"></div>' : ""}<div class="node"><span class="ic">${String(i + 1).padStart(2, "0")}</span><div><h4>${md(n.label)}</h4>${n.sub ? `<p>${esc(n.sub)}</p>` : ""}</div></div>`).join("")}`;
    case "cta": return `${k}<h1 style="font-size:96px">${md(s.title)}</h1>${s.body ? `<p class="body">${md(s.body)}</p>` : ""}<span class="pill">${esc(s.cta || "xenovasolutions.com/contact")}</span>`;
    default: throw new Error("unknown layout " + s.layout);
  }
}

(async () => {
  const [, , specPath, outDir] = process.argv;
  const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  const out = path.resolve(outDir); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  const n = spec.scenes.length; let bad = 0;
  for (let i = 0; i < n; i++) {
    const s = spec.scenes[i];
    const prog = Array.from({ length: n }, (_, j) => `<span class="${j <= i ? "on" : ""}"></span>`).join("");
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body><div class="grid"></div><div class="glow"></div><div class="bar"></div>
      <div class="frame"><div class="top">${logo}<div class="prog">${prog}</div></div><div class="main">${body(s)}</div></div>
      ${s.label ? `<div class="label">${esc(s.label)}</div>` : ""}<div class="bot"><span>@xenovasolutionsofficial</span><span>xenovasolutions.com</span></div></body></html>`;
    const tmp = path.join(out, `.s${i}.html`); fs.writeFileSync(tmp, html);
    await page.goto("file://" + tmp); await page.evaluate(() => document.fonts.ready);
    const over = await page.evaluate(() => { const m = document.querySelector(".main"); return m.scrollHeight > m.clientHeight + 2; });
    if (over) { console.error(`OVERFLOW scene ${i + 1}`); bad++; }
    await page.screenshot({ path: path.join(out, `s${String(i + 1).padStart(2, "0")}.png`) }); fs.unlinkSync(tmp);
  }
  await browser.close(); if (bad) process.exit(2);
})();
