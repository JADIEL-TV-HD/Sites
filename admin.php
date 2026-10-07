<?php ?><!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Painel IA</title><style>
body{font-family:Arial;margin:0;background:#f3f5f6;color:#17212b}.wrap{max-width:1100px;margin:auto;padding:20px}.card{background:#fff;padding:18px;border-radius:14px;margin:10px 0;box-shadow:0 2px 8px #0001}input,textarea{width:100%;box-sizing:border-box;padding:12px;margin:5px 0;border:1px solid #ddd;border-radius:9px}button{background:#075e54;color:#fff;border:0;border-radius:9px;padding:11px 15px;margin:4px;cursor:pointer}.login{max-width:400px;margin:12vh auto}.row{display:grid;grid-template-columns:1fr 1fr;gap:15px}.bubble{padding:10px;margin:6px;border-radius:9px;background:#f0f2f5}.in{margin-right:20%}.out{margin-left:20%;background:#d9ffc7}.muted{color:#667781}@media(max-width:700px){.row{grid-template-columns:1fr}}
 .danger{color:#b3261e;font-weight:700}.muted{color:#667781}@media(max-width:700px){.row{grid-template-columns:1fr}}
</style></head><body><div id="login" class="card login"><h2>Painel administrativo</h2><input id="u" value="admin"><input id="p" type="password" placeholder="Senha"><button type="button" onclick="login()">Entrar</button><p class="muted">Use a senha definida no config.php.</p></div><div id="app" class="wrap" style="display:none"><h1>Atendimento IA</h1><div class="row"><section><h2>Conversas</h2><div id="list"></div></section><section><h2>Conversa</h2><div id="view" class="card muted">Selecione uma conversa.</div></section></div><section><h2>Contas cadastradas</h2><div id="clients"></div></section><section><h2>Base de conhecimento</h2><div id="kb"></div><button type="button" onclick="add()">+ Adicionar</button><button type="button" onclick="saveKb()">Salvar</button></section></div><script>const $=x=>document.getElementById(x);let data=[],csrfToken='';
async function api(d){
 if(d.action!=='login'&&csrfToken)d.csrf=csrfToken;
 const r=await fetch('api.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});
 const j=await r.json();
 if(!r.ok)throw Error(j.error||'Erro');
 if(j.csrf)csrfToken=j.csrf;
 return j
}
async function login(){
 try{
  const j=await api({action:'login',user:$('u').value,pass:$('p').value});
  csrfToken=j.csrf||'';
  $('login').style.display='none';
  $('app').style.display='block';
  await load()
 }catch(e){alert(e.message)}
}
async function load(){
 const j=await api({action:'list'});
 data=j.conversations;
 const l=$('list');l.innerHTML='';
 data.slice().reverse().forEach(c=>{
  const b=document.createElement('button');
  b.type='button';b.style.width='100%';b.style.textAlign='left';
  b.textContent=(c.client.name||'Sem nome')+' — '+(c.status||'ia');
  b.onclick=()=>view(c);
  l.appendChild(b)
 });
 const cl=await api({action:'clients'});
 renderClients(cl.clients||[]);
 const k=await api({action:'knowledge'});
 render(k.knowledge||[])
}
function renderClients(clients){
 const box=$('clients');box.innerHTML='';
 if(!clients.length){box.innerHTML='<div class="card muted">Nenhuma conta cadastrada.</div>';return}
 clients.slice().reverse().forEach(c=>{
  const card=document.createElement('div');card.className='card';
  const banned=!!c.banned;
  card.innerHTML='<b>'+esc(c.name||'Sem nome')+'</b><br><span class="muted">'+esc(c.email||'')+'</span><br><span class="muted">'+esc(c.phone||'')+'</span><br><span class="'+(banned?'danger':'muted')+'">'+(banned?'BANIDO':'ATIVO')+'</span>';
  const btn=document.createElement('button');btn.type='button';btn.textContent=banned?'Desbanir':'Banir conta';btn.onclick=()=>setBan(c.id,!banned);card.appendChild(btn);
  box.appendChild(card)
 })
}
async function setBan(id,ban){
 if(!confirm(ban?'Tem certeza que deseja banir esta conta?':'Deseja liberar esta conta?'))return;
 await api({action:ban?'ban':'unban',id});await load()
}
function view(c){
 $('view').innerHTML='<b>'+esc(c.client.name)+'</b><br>'+esc(c.client.phone)+'<hr>'+c.messages.map(m=>'<div class="bubble '+(m.role==='assistant'||m.role==='human'?'in':'out')+'">'+esc(m.text)+'</div>').join('')+'<button type="button" onclick="take(\''+c.id+'\')">Assumir</button><form onsubmit="reply(event,\''+c.id+'\')"><input id="r" placeholder="Resposta humana"><button type="submit">Enviar</button></form>'
}
async function take(id){await api({action:'take',id});await load()}
async function reply(e,id){e.preventDefault();const v=$('r').value.trim();if(!v)return;await api({action:'reply',id,message:v});await load()}
function render(a){$('kb').innerHTML='';a.forEach(x=>add(x.title,x.content))}
function add(t='',c=''){
 let d=document.createElement('div');d.className='card';
 d.innerHTML='<input class="kt" placeholder="Título"><textarea class="kc" placeholder="Informação que a IA deve conhecer"></textarea><button type="button" onclick="this.parentNode.remove()">Remover</button>';
 d.querySelector('.kt').value=t;d.querySelector('.kc').value=c;$('kb').appendChild(d)
}
async function saveKb(){
 let a=[...document.querySelectorAll('#kb .card')].map(d=>({title:d.querySelector('.kt')?.value,content:d.querySelector('.kc')?.value})).filter(x=>x.title);
 await api({action:'knowledge',knowledge:a});alert('Base salva.')
}
function esc(s){return String(s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]))}</script></body></html>