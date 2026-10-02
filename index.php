<?php
declare(strict_types=1);
?><!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#07110d">
<title>JADIEL IA Web — IDE</title>
<style>
:root{--bg:#060a0f;--panel:#0b121a;--panel2:#0e1721;--line:#1c2a38;--text:#e7eef7;--muted:#718196;--green:#21e58a;--green2:#0fa968;--blue:#4ea3ff;--danger:#ff5570;--shadow:0 20px 60px #0008}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--bg);color:var(--text);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}body{overflow:hidden}
#particles{position:fixed;inset:0;z-index:0;opacity:.5;pointer-events:none}.app{position:relative;z-index:1;height:100%;display:grid;grid-template-rows:58px 1fr 27px}
.top{display:flex;align-items:center;gap:13px;padding:0 15px;background:#080e15e8;border-bottom:1px solid var(--line);backdrop-filter:blur(16px)}
.brand{font-weight:850;letter-spacing:.2px;white-space:nowrap}.brand b{color:var(--green)}.live{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 15px var(--green);margin-right:7px;animation:pulse 1.8s infinite}@keyframes pulse{50%{opacity:.45;transform:scale(.75)}}
.project{color:var(--muted);font-size:12px;border-left:1px solid var(--line);padding-left:13px}.actions{margin-left:auto;display:flex;gap:7px;align-items:center}.btn{border:1px solid #263647;background:#0d1722;color:#dce7f2;border-radius:8px;padding:8px 11px;font-size:12px;cursor:pointer;transition:.18s}.btn:hover{border-color:#3b5269;transform:translateY(-1px)}.btn.primary{background:var(--green);border-color:var(--green);color:#04150d;font-weight:800}.btn.icon{padding:8px 9px}.btn.danger{color:#ff91a2}
.workspace{min-height:0;display:grid;grid-template-columns:225px minmax(320px,1fr) minmax(320px,1fr);gap:1px;background:var(--line)}
.sidebar,.editor,.preview{min-width:0;min-height:0;background:var(--panel)}.sidebar{padding:14px;overflow:auto}.section-title{font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:#56677a;margin:17px 7px 7px}.section-title:first-child{margin-top:2px}
.lesson{border:1px solid var(--line);background:linear-gradient(135deg,#0e1b18,#0d151e);border-radius:12px;padding:13px;margin-bottom:12px}.lesson strong{font-size:13px}.lesson p{font-size:11px;line-height:1.5;color:var(--muted);margin:5px 0 0}.file{display:flex;align-items:center;gap:9px;padding:9px 8px;border-radius:7px;color:#9babbc;font:12px ui-monospace,monospace;cursor:pointer}.file:hover,.file.active{background:#10221b;color:#eafff3}.file .ico{width:18px;text-align:center}.shortcut{font-size:10px;color:#526275;line-height:1.8;padding:5px 7px}.shortcut kbd{background:#111c27;border:1px solid #28394b;border-radius:4px;padding:2px 4px;color:#94a5b8}
.editor{display:grid;grid-template-rows:43px minmax(0,1fr) 125px}.tabs{display:flex;overflow:auto;border-bottom:1px solid var(--line);background:#091019}.tab{display:flex;align-items:center;gap:7px;padding:0 14px;color:#66778b;border-right:1px solid var(--line);font:12px ui-monospace,monospace;cursor:pointer;white-space:nowrap}.tab.active{color:#fff;background:#0d1721;box-shadow:inset 0 -2px var(--green)}.tabdot{width:7px;height:7px;border-radius:50%}.html{background:#ff7b55}.css{background:#4ea3ff}.js{background:#f4cf54}
.codearea{position:relative;min-height:0;background:#070c12}.numbers{position:absolute;top:0;bottom:0;left:0;width:48px;padding:14px 8px 14px 0;text-align:right;color:#354456;font:13px/1.65 ui-monospace,monospace;overflow:hidden;user-select:none}.code{display:block;width:100%;height:100%;resize:none;border:0;outline:0;background:transparent;color:#d9e5f1;padding:14px 17px 20px 62px;font:13px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace;tab-size:2;white-space:pre;overflow:auto}.code::selection{background:#1d5b46;color:#fff}
.bottom{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line);background:#080e15}.console,.tips{padding:10px 13px;overflow:auto}.bottom h4{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#62748a;margin:0 0 7px}.log{font:11px/1.7 ui-monospace,monospace;color:#8293a7}.ok{color:var(--green)}.warn{color:#e9c86b}.err{color:#ff7188}
.preview{display:grid;grid-template-rows:43px minmax(0,1fr);background:#090f16}.preview-head{display:flex;align-items:center;gap:8px;padding:0 12px;border-bottom:1px solid var(--line);font-size:11px;color:#8292a6}.preview-head .spacer{margin-left:auto}.browser{margin:10px;border:1px solid #263545;border-radius:12px;overflow:hidden;background:#fff;display:grid;grid-template-rows:34px minmax(0,1fr);box-shadow:var(--shadow);min-height:0}.browserbar{display:flex;align-items:center;gap:6px;background:#e8edf2;padding:0 10px}.bub{width:8px;height:8px;border-radius:50%;background:#9da8b4}.address{margin-left:7px;flex:1;background:#fff;border:1px solid #d7dde4;border-radius:6px;color:#687788;padding:4px 8px;font:10px ui-monospace,monospace}.frame{border:0;width:100%;height:100%;background:#fff}
.status{display:flex;align-items:center;padding:0 11px;border-top:1px solid var(--line);color:#607187;font-size:10px}.status .right{margin-left:auto;display:flex;gap:12px}.green{color:var(--green)}
.modal-back{display:none;position:fixed;inset:0;background:#0009;z-index:20;align-items:center;justify-content:center;padding:18px}.modal-back.open{display:flex}.modal{width:min(560px,100%);background:#0c141d;border:1px solid #263749;border-radius:14px;box-shadow:0 30px 100px #000b;padding:18px}.modal h2{margin:0 0 5px;font-size:17px}.modal p{color:var(--muted);font-size:12px}.modal input,.modal textarea{width:100%;background:#070d14;border:1px solid #263749;color:#e8eef5;border-radius:8px;padding:10px;outline:0;margin:7px 0;font:12px ui-monospace,monospace}.modal textarea{height:260px;resize:vertical}.modal-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:8px}
.toast{position:fixed;right:18px;bottom:42px;z-index:30;background:#0d171f;border:1px solid #294052;border-radius:9px;padding:10px 13px;font-size:12px;box-shadow:var(--shadow);transform:translateY(15px);opacity:0;pointer-events:none;transition:.2s}.toast.show{transform:none;opacity:1}
@media(max-width:1050px){.workspace{grid-template-columns:190px minmax(300px,1fr)}.preview{display:none}}@media(max-width:680px){body{overflow:auto}.app{height:100dvh;min-height:620px}.sidebar{display:none}.workspace{grid-template-columns:1fr}.top .project{display:none}.top{padding:0 9px}.actions .optional{display:none}.editor{grid-template-rows:43px minmax(0,1fr) 115px}.bottom{grid-template-columns:1fr}.tips{display:none}}
</style>
</head>
<body>
<canvas id="particles"></canvas>
<div class="app">
<header class="top">
  <div class="brand"><span class="live"></span>JADIEL <b>IA Web</b></div>
  <div class="project">Projeto: <span id="projectName">Meu primeiro site</span></div>
  <div class="actions">
    <button class="btn optional" id="newBtn">Novo</button>
    <button class="btn optional" id="importBtn">Colar código</button>
    <button class="btn" id="saveBtn">Salvar</button>
    <button class="btn primary" id="runBtn">▶ Executar</button>
  </div>
</header>
<main class="workspace">
<aside class="sidebar">
  <div class="lesson"><strong>🚀 Aprenda criando</strong><p>Escreva o código e veja o site real funcionando ao lado. Nada de simulação.</p></div>
  <div class="section-title">Aulas</div>
  <div class="file active">01 · Primeiro site</div><div class="file">02 · HTML</div><div class="file">03 · CSS</div><div class="file">04 · JavaScript</div><div class="file">05 · Projeto final</div>
  <div class="section-title">Arquivos</div>
  <div class="file active" data-tab="html"><span class="ico">🌐</span>index.html</div>
  <div class="file" data-tab="css"><span class="ico">🎨</span>style.css</div>
  <div class="file" data-tab="js"><span class="ico">⚡</span>script.js</div>
  <div class="section-title">Atalhos</div>
  <div class="shortcut"><kbd>Ctrl</kbd> + <kbd>Enter</kbd> executar<br><kbd>Ctrl</kbd> + <kbd>S</kbd> salvar<br><kbd>Tab</kbd> indentar</div>
</aside>
<section class="editor">
  <div class="tabs">
    <div class="tab active" data-tab="html"><i class="tabdot html"></i>index.html</div>
    <div class="tab" data-tab="css"><i class="tabdot css"></i>style.css</div>
    <div class="tab" data-tab="js"><i class="tabdot js"></i>script.js</div>
  </div>
  <div class="codearea"><div id="numbers" class="numbers"></div><textarea id="code" class="code" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off"></textarea></div>
  <div class="bottom"><div class="console"><h4>Terminal / Console</h4><div id="log" class="log"><span class="ok">●</span> JADIEL IA Web iniciado.</div></div><div class="tips"><h4>Assistente de aprendizagem</h4><div class="log">Você pode editar os três arquivos. Ao executar, HTML + CSS + JavaScript são enviados para a prévia real em um iframe isolado.</div></div></div>
</section>
<section class="preview">
  <div class="preview-head"><span class="green">●</span> Pré-visualização real <span class="spacer"></span><span id="previewState">pronto</span></div>
  <div class="browser"><div class="browserbar"><i class="bub"></i><i class="bub"></i><i class="bub"></i><div class="address">https://jadiel-ia-web.local/preview</div></div><iframe id="previewFrame" class="frame" sandbox="allow-scripts allow-forms allow-modals"></iframe></div>
</section>
</main>
<footer class="status"><span>JADIEL IA Web · IDE educacional</span><span class="right"><span>HTML</span><span>CSS</span><span>JavaScript</span><span class="green">● online</span></span></footer>
</div>

<div class="modal-back" id="modal">
 <div class="modal">
  <h2 id="modalTitle">Salvar projeto</h2><p id="modalText">Escolha um nome para salvar o projeto no servidor.</p>
  <input id="projectInput" placeholder="Nome do projeto">
  <div id="projectList"></div>
  <div class="modal-actions"><button class="btn" id="cancelModal">Cancelar</button><button class="btn primary" id="confirmModal">Confirmar</button></div>
 </div>
</div>
<div class="toast" id="toast"></div>

<script>
const defaults={
html:'<!doctype html>\n<html lang="pt-BR">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <title>Meu primeiro site</title>\n</head>\n<body>\n  <main class="hero">\n    <h1>Olá, mundo! 🚀</h1>\n    <p>Estou aprendendo a programar com JADIEL IA Web.</p>\n    <button onclick="saudar()">Clique aqui</button>\n  </main>\n</body>\n</html>',
css:'*{box-sizing:border-box}\nbody{margin:0;font-family:system-ui;background:#08110d;color:#fff}\n.hero{min-height:100vh;display:grid;place-content:center;text-align:center;padding:30px}\nh1{font-size:clamp(36px,7vw,70px);margin:0 0 10px;color:#21e58a}\np{color:#b7c4d2;font-size:18px}\nbutton{padding:12px 20px;border:0;border-radius:10px;background:#21e58a;color:#04150d;font-weight:800;cursor:pointer}',
js:'function saudar(){\n  alert("Você está programando de verdade! 🚀");\n}\n'
};
let files={...defaults},active='html',dirty=false;
const $=s=>document.querySelector(s), code=$('#code'), numbers=$('#numbers'), frame=$('#previewFrame'), log=$('#log'), toast=$('#toast');
function toastMsg(t){toast.textContent=t;toast.classList.add('show');clearTimeout(window.tt);window.tt=setTimeout(()=>toast.classList.remove('show'),2200)}
function lineNumbers(){numbers.innerHTML=Array.from({length:Math.max(1,code.value.split('\n').length)},(_,i)=>i+1).join('<br>')}
function setActive(t){files[active]=code.value;active=t;code.value=files[t];document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x.dataset.tab===t));lineNumbers();code.focus()}
function escapeScript(s){return s.replaceAll('</script>','<\\/script>')}
function run(){files[active]=code.value;const html=files.html;const css='<style>\n'+files.css+'\n</style>';const js='<script>\n'+escapeScript(files.js)+'\n<\\/script>';let out=html;out=out.includes('</head>')?out.replace('</head>',css+'</head>'):css+out;out=out.includes('</body>')?out.replace('</body>',js+'</body>'):out+js;frame.srcdoc=out;dirty=false;$('#previewState').textContent='atualizado';log.innerHTML='<span class="ok">●</span> Executado com sucesso · prévia atualizada.'}
document.querySelectorAll('[data-tab]').forEach(x=>x.addEventListener('click',()=>setActive(x.dataset.tab)));
code.addEventListener('input',()=>{files[active]=code.value;dirty=true;lineNumbers();$('#previewState').textContent='alterado'});
code.addEventListener('scroll',()=>numbers.scrollTop=code.scrollTop);
code.addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();const s=code.selectionStart;code.setRangeText('  ',s,code.selectionEnd,'end');files[active]=code.value;dirty=true;lineNumbers()}});
$('#runBtn').onclick=run;
$('#newBtn').onclick=()=>{if(dirty&&!confirm('Existem alterações não salvas. Criar novo projeto mesmo assim?'))return;files={...defaults};active='html';setActive('html');run();toastMsg('Novo projeto criado')};
$('#importBtn').onclick=()=>openModal('import');
$('#saveBtn').onclick=()=>openModal('save');
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();run()}if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();openModal('save')}});
let mode='';
function openModal(m){mode=m;$('#modal').classList.add('open');$('#projectInput').value=$('#projectName').textContent;$('#projectList').innerHTML='';$('#modalTitle').textContent=m==='save'?'Salvar projeto':'Colar código';$('#modalText').textContent=m==='save'?'O projeto será salvo no servidor e poderá ser carregado depois.':'Cole um HTML completo. CSS e JavaScript podem continuar nos arquivos separados.';$('#projectInput').style.display=m==='save'?'block':'none';if(m==='import'){$('#projectInput').style.display='block';$('#projectInput').value='';$('#projectInput').placeholder='Cole seu código HTML aqui';$('#modalText').textContent='Cole o HTML abaixo. Ele substituirá apenas o index.html.'}$('#confirmModal').textContent=m==='save'?'Salvar':'Importar';$('#projectInput').focus()}
$('#cancelModal').onclick=()=>$('#modal').classList.remove('open');
$('#confirmModal').onclick=async()=>{const v=$('#projectInput').value.trim();if(mode==='import'){if(!v){toastMsg('Cole algum código HTML');return}files.html=v;setActive('html');run();$('#modal').classList.remove('open');toastMsg('Código importado')}else{const name=v||'Meu projeto';await saveProject(name)}};
async function saveProject(name){files[active]=code.value;const r=await fetch('api.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'save',name,files})});const d=await r.json();if(d.ok){$('#projectName').textContent=name;dirty=false;$('#modal').classList.remove('open');toastMsg('Projeto salvo no servidor')}else toastMsg(d.error||'Erro ao salvar')}
async function loadProject(name){const r=await fetch('api.php?action=load&name='+encodeURIComponent(name));const d=await r.json();if(!d.ok){toastMsg(d.error||'Erro ao carregar');return}files={...defaults,...d.files};$('#projectName').textContent=name;setActive('html');run();toastMsg('Projeto carregado')}
async function init(){try{const r=await fetch('api.php?action=list');const d=await r.json();if(d.ok&&d.projects.length){const wrap=document.createElement('div');wrap.style.margin='10px 0';wrap.innerHTML='<div class="section-title" style="margin-left:0">Projetos salvos</div>';d.projects.forEach(p=>{const b=document.createElement('div');b.className='file';b.textContent='💾 '+p;b.onclick=()=>loadProject(p);wrap.appendChild(b)});document.querySelector('.sidebar').appendChild(wrap)}}catch(e){}setActive('html');run()}init();

const pc=$('#particles'),ctx=pc.getContext('2d');let pts=[];
function resize(){pc.width=innerWidth;pc.height=innerHeight}addEventListener('resize',resize);resize();
for(let i=0;i<85;i++)pts.push({x:Math.random()*innerWidth,y:Math.random()*innerHeight,vx:(Math.random()-.5)*.28,vy:(Math.random()-.5)*.28,r:Math.random()*1.4+.3});
(function particles(){ctx.clearRect(0,0,pc.width,pc.height);for(const p of pts){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>pc.width)p.vx*=-1;if(p.y<0||p.y>pc.height)p.vy*=-1;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fillStyle='rgba(33,229,138,.42)';ctx.fill()}requestAnimationFrame(particles)})();
</script>
</body>
</html>