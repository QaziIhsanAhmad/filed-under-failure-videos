const {chromium}=require('/home/claude/social-studio/node_modules/playwright');
const F='/home/claude/social-studio/node_modules/@fontsource';
const ff=(f,p,w)=>`@font-face{font-family:'${f}';font-weight:${w};src:url('file://${F}/${p}/files/${p}-latin-${w}-normal.woff2')}`;
const css=[ff('P','poppins',800),ff('P','poppins',600),ff('M','jetbrains-mono',600)].join('');
const T=[
 {co:'CARILLION',stamp:'COLLAPSED',a:'£7BN',b:'HOLE',small:'Why it collapsed'},
 {co:'SVB',stamp:'BANK RUN',a:'$40BN',b:'IN 1 DAY',small:'Why SVB collapsed'},
 {co:'THERANOS',stamp:'VERDICT',a:'GUILTY 4',b:'CLEARED 4',small:'',fs:128},
];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:1280,height:720}});
for(const [i,t] of T.entries()){
require('fs').writeFileSync(__dirname+'/t.html',`<html><head><style>${css}*{margin:0}body{width:1280px;height:720px;background:radial-gradient(circle at 75% 40%,#1c2a48,#0b1220 70%);font-family:P;overflow:hidden;position:relative}
.file{position:absolute;left:70px;top:95px;width:430px;height:540px;background:#f3efe6;transform:rotate(-5deg);box-shadow:0 30px 60px #0009;padding:40px;box-sizing:border-box}
.file h3{font:600 40px M;color:#111}.l{height:16px;background:#cfc8b8;margin:22px 0;border-radius:3px}
.stamp{position:absolute;left:60px;bottom:70px;border:9px solid #e0352b;color:#e0352b;font:800 62px M;padding:4px 22px;transform:rotate(-12deg);letter-spacing:2px}
.big{position:absolute;left:560px;top:120px;color:#fff;font:800 ${t.fs||168}px/0.92 P;letter-spacing:-6px;text-shadow:0 8px 0 #0006}
.big span{color:#ff3b2f;display:block}
.tag{position:absolute;left:566px;bottom:70px;font:600 30px M;color:#9fb0c8;letter-spacing:3px}</style></head><body>
<div class="file"><h3>${t.co}</h3>${'<div class="l"></div>'.repeat(8)}<div class="stamp">${t.stamp}</div></div>
<div class="big">${t.a}<span>${t.b}</span></div><div class="tag">FILED UNDER FAILURE</div></body></html>`);await p.goto('file://'+__dirname+'/t.html');
await p.waitForTimeout(300);await p.screenshot({path:`v2-${i}.png`,type:'png'});}
await b.close();})();
