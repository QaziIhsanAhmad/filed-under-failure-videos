// Brand-locked social renderer (free: HTML/CSS + Playwright Chromium).
// Usage: node render.js <posts.json> [outDir]
// posts.json: [{id, brand: "xenova"|"frontdesk", slides: [{layout, theme?, ...}]}]
// Each slide -> <outDir>/<brand>/<id>-<n>.jpg at 1080x1350 (4:5, the tallest ratio IG/FB/LinkedIn feeds show uncropped).
// Colours are fixed per brand below and must not be changed per post: brand recognition depends on them.
const fs = require("fs"), path = require("path");
const { chromium } = require("playwright");

const FONTS = path.join(__dirname, "node_modules", "@fontsource");
const ff = (fam, pkg, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url('file://${FONTS}/${pkg}/files/${pkg}-latin-${w}-normal.woff2') format('woff2')}`;
const FONT_CSS = [
  ...[400, 600, 700, 800].map(w => ff("Bricolage", "bricolage-grotesque", w)),
  ...[400, 500, 600].map(w => ff("Plex", "ibm-plex-sans", w)),
  ...[400, 500].map(w => ff("PlexMono", "ibm-plex-mono", w)),
  ...[400, 500, 600, 700, 800].map(w => ff("Poppins", "poppins", w)),
  ...[400, 600].map(w => ff("JBMono", "jetbrains-mono", w)),
].join("\n");

// Palettes taken from the live brands: xenovasolutions.com theme.json presets; FrontDesk studio/reels.py + Stories.
const BRANDS = {
  xenova: {
    handle: "@xenovasolutionsofficial", site: "xenovasolutions.com",
    dark: { bg: "#030F24", panel: "#071A36", line: "#16345F", text: "#F1F6F9", muted: "#93A6BE", accent: "#7FD6B3", accent2: "#3FA383", onAccent: "#030F24" },
    light: { bg: "#F1F6F9", panel: "#FFFFFF", line: "#C9D6E3", text: "#030F24", muted: "#4E6380", accent: "#3FA383", accent2: "#16345F", onAccent: "#F1F6F9" },
    display: "Bricolage", body: "Plex", mono: "PlexMono", radius: 14,
    logo: (c) => `<div class="logo"><span class="mark" style="border-color:${c.line};background:${c.panel}">
      <svg width="34" height="34" viewBox="0 0 24 24" fill="none"><path d="M4 4 20 20M20 4 4 20" stroke="${c.text}" stroke-width="2.1" stroke-linecap="round" opacity=".85"/>
      <circle cx="12" cy="12" r="3.4" fill="${c.panel}"/><circle cx="12" cy="12" r="2.2" fill="${c.accent}"/></svg></span>
      <span class="wm"><b>XENOVA</b><i>SOLUTIONS</i></span></div>`,
  },
  frontdesk: {
    handle: "@frontdeskflows", site: "frontdeskflows",
    dark: { bg: "#0B1220", panel: "#111A2E", line: "#1E2A44", text: "#F8FAFC", muted: "#94A3B8", accent: "#F59E0B", accent2: "#22C55E", onAccent: "#0B1220", teal: "#0F766E" },
    light: { bg: "#F8FAFC", panel: "#FFFFFF", line: "#E2E8F0", text: "#0B1220", muted: "#475569", accent: "#F59E0B", accent2: "#0F766E", onAccent: "#0B1220", teal: "#0F766E" },
    display: "Poppins", body: "Poppins", mono: "JBMono", radius: 22,
    logo: (c) => `<div class="logo"><span class="mark fd" style="background:${c.accent};color:#0B1220">F</span>
      <span class="wm fd">FrontDesk Flows</span></div>`,
  },
};

const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// *word* -> accent highlight, _word_ -> muted; \n -> line break
const md = (s) => esc(s).replace(/\*(.+?)\*/g, '<span class="hl">$1</span>').replace(/(^|\s)_(.+?)_/g, '$1<span class="mu">$2</span>').replace(/\n/g, "<br>").replace(/&lt;(\/?)b&gt;/g, "<$1b>");

function css(b, c, layout) {
  const disp = b.display, xen = b === BRANDS.xenova;
  return `${FONT_CSS}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{background:${c.bg};color:${c.text};font-family:'${b.body}';position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}
.bgfx{position:absolute;inset:0;pointer-events:none}
.frame{position:absolute;inset:0;padding:78px 84px 72px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;height:56px}
.logo{display:flex;align-items:center;gap:16px}
.mark{width:56px;height:56px;border-radius:14px;border:2px solid;display:inline-flex;align-items:center;justify-content:center}
.mark.fd{border:none;border-radius:16px;font:800 34px 'Poppins'}
.wm{display:flex;flex-direction:column;line-height:1}
.wm b{font:700 27px '${disp}';letter-spacing:-.04em}
.wm i{font:500 13px '${b.mono}';font-style:normal;letter-spacing:.32em;color:${c.muted};margin-top:5px}
.wm.fd{font:600 28px 'Poppins';letter-spacing:-.01em}
.idx{font:500 22px '${b.mono}';color:${c.muted};letter-spacing:.08em}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
.kicker{font:500 24px '${b.mono}';letter-spacing:${xen ? ".22em" : ".08em"};text-transform:uppercase;color:${c.accent};display:flex;align-items:center;gap:14px;margin-bottom:34px}
.kicker:before{content:"";width:${xen ? "12px" : "14px"};height:${xen ? "12px" : "14px"};border-radius:50%;background:${c.accent};box-shadow:0 0 0 6px ${c.accent}22}
h1{font-family:'${disp}';font-weight:800;letter-spacing:${xen ? "-.035em" : "-.025em"};line-height:1.02;font-size:var(--h1,104px)}
h2{font-family:'${disp}';font-weight:${xen ? 700 : 700};letter-spacing:-.02em;line-height:1.1;font-size:var(--h2,74px)}
.hl{color:${c.accent}}
.mu{color:${c.muted}}
.sub{font:400 38px/1.42 '${b.body}';color:${c.muted};margin-top:36px;max-width:880px}
.sub b{color:${c.text};font-weight:600}
.body{font:400 44px/1.45 '${b.body}';color:${c.text};opacity:.92;margin-top:30px}
.bot{display:flex;justify-content:space-between;align-items:center;height:48px;font:500 22px '${b.mono}';color:${c.muted};letter-spacing:.04em}
.swipe{display:flex;align-items:center;gap:12px;color:${c.accent}}
.pill{display:inline-flex;align-items:center;gap:12px;background:${c.accent};color:${c.onAccent};font:700 32px '${disp}';padding:24px 38px;border-radius:${b.radius * 4}px;letter-spacing:-.01em}
.card{background:${c.panel};border:2px solid ${c.line};border-radius:${b.radius + 6}px;padding:38px 42px}
.mono{font:400 30px/1.55 '${b.mono}'}
.num{font:800 190px/0.9 '${disp}';color:${c.accent};letter-spacing:-.05em}
.opt{display:flex;align-items:center;gap:30px;padding:30px 36px;border:2px solid ${c.line};background:${c.panel};border-radius:${b.radius + 4}px;margin-top:22px;font:500 40px '${b.body}'}
.opt .l{width:66px;height:66px;flex:none;border-radius:${xen ? "14px" : "50%"};background:${c.accent};color:${c.onAccent};display:flex;align-items:center;justify-content:center;font:800 34px '${disp}'}
.bubble{max-width:780px;padding:26px 32px;border-radius:30px;font:400 35px/1.38 '${b.body}';margin-top:22px;position:relative}
.bubble.them{background:${c.panel};border:2px solid ${c.line};border-bottom-left-radius:8px;align-self:flex-start}
.bubble.us{background:${c.accent};color:${c.onAccent};border-bottom-right-radius:8px;align-self:flex-end}
.bubble .t{display:block;font:400 22px '${b.mono}';opacity:.6;margin-top:10px}
.bubble.sys{align-self:center;background:transparent;border:2px dashed ${c.line};color:${c.muted};font:500 26px '${b.mono}';border-radius:14px;padding:14px 22px}
.chat{display:flex;flex-direction:column}
.ben{display:flex;gap:28px;align-items:flex-start;margin-top:34px}
.ben .tick{width:52px;height:52px;flex:none;border-radius:${xen ? "12px" : "50%"};background:${c.accent2}${xen ? "" : ""};display:flex;align-items:center;justify-content:center;margin-top:4px}
.ben h3{font:700 40px/1.15 '${disp}';letter-spacing:-.015em}
.ben p{font:400 31px/1.42 '${b.body}';color:${c.muted};margin-top:8px}
.node{display:flex;align-items:center;gap:26px;padding:24px 30px;border:2px solid ${c.line};background:${c.panel};border-radius:${b.radius + 2}px}
.node .ic{width:58px;height:58px;flex:none;border-radius:14px;background:${c.accent}22;border:2px solid ${c.accent};display:flex;align-items:center;justify-content:center;font:600 24px '${b.mono}';color:${c.accent}}
.node h4{font:600 37px '${b.body}'}
.node p{font:400 27px '${b.mono}';color:${c.muted};margin-top:4px}
.wire{width:4px;height:30px;background:${c.line};margin-left:57px}
.file{display:flex;align-items:center;gap:22px;padding:24px 30px;border-bottom:2px solid ${c.line};font:400 31px '${b.mono}'}
.file:last-child{border-bottom:none}
.file .x{width:40px;height:48px;flex:none;border-radius:6px;background:${c.accent2};position:relative}
.file .x:after{content:"";position:absolute;right:0;top:0;border-left:14px solid transparent;border-top:14px solid ${c.panel}}
.file.cur{background:${c.accent}18;color:${c.accent}}
.src{font:400 22px '${b.mono}';color:${c.muted};margin-top:30px}
`;
}

// Background treatment: Xenova = blueprint grid + one signal dot; FrontDesk = soft amber glow + node dots.
function bgfx(brand, c, theme, seed) {
  if (brand === "xenova") {
    const g = theme === "dark" ? "#16345F55" : "#16345F14";
    return `<svg class="bgfx" width="1080" height="1350"><defs><pattern id="g" width="54" height="54" patternUnits="userSpaceOnUse"><path d="M54 0H0V54" fill="none" stroke="${g}" stroke-width="1.5"/></pattern>
      <radialGradient id="r" cx="${seed % 2 ? 0.88 : 0.12}" cy="${seed % 3 ? 0.08 : 0.92}" r=".75"><stop offset="0" stop-color="${c.accent}" stop-opacity="${theme === "dark" ? 0.13 : 0.10}"/><stop offset="1" stop-color="${c.accent}" stop-opacity="0"/></radialGradient></defs>
      <rect width="1080" height="1350" fill="url(#g)"/><rect width="1080" height="1350" fill="url(#r)"/>
      <rect x="0" y="0" width="1080" height="8" fill="${c.accent}"/></svg>`;
  }
  return `<svg class="bgfx" width="1080" height="1350"><defs>
    <radialGradient id="r" cx="${seed % 2 ? 0.95 : 0.05}" cy="${seed % 3 ? 0.0 : 1}" r=".8"><stop offset="0" stop-color="${c.accent}" stop-opacity="${theme === "dark" ? 0.16 : 0.14}"/><stop offset="1" stop-color="${c.accent}" stop-opacity="0"/></radialGradient>
    <pattern id="d" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="2" fill="${theme === "dark" ? "#94A3B81c" : "#0B122012"}"/></pattern></defs>
    <rect width="1080" height="1350" fill="url(#d)"/><rect width="1080" height="1350" fill="url(#r)"/></svg>`;
}

const tick = (c) => `<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="${c.bg === "#F1F6F9" || c.bg === "#F8FAFC" ? "#FFFFFF" : c.bg}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>`;
const arrow = `<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;

function main(s, c, b) {
  const st = (k, v) => (s[k] ? `style="--${k}:${s[k]}px"` : "");
  switch (s.layout) {
    case "cover": case "hook":
      return `${s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : ""}<h1 ${st("h1")}>${md(s.title)}</h1>${s.sub ? `<p class="sub">${md(s.sub)}</p>` : ""}`;
    case "step":
      return `<div class="num">${esc(s.n)}</div><h2 style="margin-top:38px;${s.h2 ? `--h2:${s.h2}px` : ""}">${md(s.title)}</h2>${s.body ? `<p class="body">${md(s.body)}</p>` : ""}${s.code ? `<div class="card mono" style="margin-top:38px">${md(s.code)}</div>` : ""}`;
    case "poll":
      return `<div class="kicker">${esc(s.kicker || "Quick poll")}</div><h2 ${st("h2")}>${md(s.question)}</h2><div style="margin-top:30px">${s.options.map((o, i) => `<div class="opt"><span class="l">${"ABCD"[i]}</span><span>${md(o)}</span></div>`).join("")}</div>${s.foot ? `<p class="src" style="font-size:29px;line-height:1.4">${md(s.foot)}</p>` : ""}`;
    case "chat":
      return `${s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : ""}${s.title ? `<h2 ${st("h2")} style="margin-bottom:26px">${md(s.title)}</h2>` : ""}<div class="chat">${s.chat.map(m => `<div class="bubble ${m.who}">${md(m.text)}${m.time ? `<span class="t">${esc(m.time)}</span>` : ""}</div>`).join("")}</div>${s.punch ? `<h2 style="margin-top:46px;--h2:${s.punchSize || 54}px">${md(s.punch)}</h2>` : ""}`;
    case "files":
      return `${s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : ""}<h2 ${st("h2")}>${md(s.title)}</h2><div class="card" style="padding:12px 0;margin-top:40px">${s.files.map((f, i) => `<div class="file ${i === s.files.length - 1 ? "cur" : ""}"><span class="x"></span>${esc(f)}</div>`).join("")}</div>${s.punch ? `<p class="sub">${md(s.punch)}</p>` : ""}`;
    case "stat":
      return `<div class="kicker">${esc(s.kicker)}</div><div class="num" style="font-size:${s.numSize || 230}px">${esc(s.big)}</div><h2 style="margin-top:30px">${md(s.title)}</h2>${s.body ? `<p class="sub">${md(s.body)}</p>` : ""}<p class="src">${esc(s.source)}</p>`;
    case "flow":
      return `${s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : ""}<h2 ${st("h2")} style="margin-bottom:34px">${md(s.title)}</h2>${s.nodes.map((n, i) => `${i ? '<div class="wire"></div>' : ""}<div class="node"><span class="ic">${esc(n.icon || String(i + 1).padStart(2, "0"))}</span><div><h4>${md(n.label)}</h4>${n.sub ? `<p>${esc(n.sub)}</p>` : ""}</div></div>`).join("")}${s.foot ? `<p class="src" style="font-size:25px">${md(s.foot)}</p>` : ""}`;
    case "promo":
      return `${s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : ""}<h2 ${st("h2")} style="--h2:${s.h2 || 70}px">${md(s.title)}</h2>${s.benefits.map(x => `<div class="ben"><span class="tick">${tick(c)}</span><div><h3>${md(x.h)}</h3>${x.p ? `<p>${md(x.p)}</p>` : ""}</div></div>`).join("")}${s.cta ? `<div style="margin-top:52px"><span class="pill">${esc(s.cta)} ${arrow}</span></div>` : ""}`;
    case "cta":
      return `${s.kicker ? `<div class="kicker">${esc(s.kicker)}</div>` : ""}<h1 ${st("h1")} style="--h1:${s.h1 || 92}px">${md(s.title)}</h1>${s.sub ? `<p class="sub">${md(s.sub)}</p>` : ""}${s.cta ? `<div style="margin-top:56px"><span class="pill">${esc(s.cta)} ${arrow}</span></div>` : ""}`;
    default:
      throw new Error("unknown layout " + s.layout);
  }
}

function html(post, s, i, n) {
  const b = BRANDS[post.brand], theme = s.theme || post.theme || "dark", c = b[theme];
  const idx = n > 1 ? `${String(i + 1).padStart(2, "0")} / ${String(n).padStart(2, "0")}` : (s.tag || "");
  const left = s.footLeft ?? b.handle;
  const right = n > 1 && i < n - 1 ? `<span class="swipe">Swipe ${arrow}</span>` : esc(s.footRight ?? (post.brand === "xenova" ? b.site : ""));
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(b, c, s.layout)}</style></head><body>
  ${bgfx(post.brand, c, theme, (post.id.length + i) | 0)}
  <div class="frame"><div class="top">${b.logo(c)}<span class="idx">${esc(idx)}</span></div>
  <div class="main">${main(s, c, b)}</div>
  <div class="bot"><span>${esc(left)}</span>${right}</div></div></body></html>`;
}

(async () => {
  const [, , src, outDir = path.join(__dirname, "..", "img")] = process.argv;
  const posts = JSON.parse(fs.readFileSync(src, "utf8"));
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const p of posts) {
    fs.mkdirSync(path.join(outDir, p.brand), { recursive: true });
    for (let i = 0; i < p.slides.length; i++) {
      const tmp = path.join(outDir, `.tmp-${process.pid}.html`);
      fs.writeFileSync(tmp, html(p, p.slides[i], i, p.slides.length));
      await page.goto("file://" + tmp);
      await page.evaluate(() => document.fonts.ready);
      // guard: text must not overflow the frame (would be cut off on the image)
      const over = await page.evaluate(() => { const m = document.querySelector(".main"); return m.scrollHeight > m.clientHeight + 2; });
      if (over) console.error(`WARN overflow: ${p.id} slide ${i + 1}`);
      const out = path.join(outDir, p.brand, `${p.id}-${i + 1}.jpg`);
      await page.screenshot({ path: out, type: "jpeg", quality: 90 });
      fs.unlinkSync(tmp);
      console.log(out);
    }
  }
  await browser.close();
})();
