<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#075e54"><title>AZION IA</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#d8dbd7;font-family:Inter,Arial,sans-serif;color:#111}.app{height:100dvh;max-width:900px;margin:auto;background:#efeae2;display:flex;flex-direction:column;box-shadow:0 0 35px #0002}.top{height:68px;background:#075e54;color:#fff;display:flex;align-items:center;padding:8px 16px;gap:12px;cursor:pointer}.ava{width:48px;height:48px;border-radius:50%;background:linear-gradient(145deg,#25d366,#0a8f78);display:grid;place-items:center;font-size:19px;font-weight:800;box-shadow:0 2px 8px #0003}.name{font-size:17px;font-weight:700}.verified{display:inline-grid;place-items:center;width:17px;height:17px;border-radius:50%;background:#1686f8;color:#fff;font-size:11px;margin-left:4px}.online{font-size:12px;opacity:.85;margin-top:2px}.msgs{flex:1;overflow:auto;padding:18px;background-color:#efeae2;background-image:radial-gradient(#00000009 1px,transparent 1px);background-size:18px 18px}.msg{max-width:80%;padding:11px 14px;margin:8px 0;border-radius:12px;white-space:pre-wrap;overflow-wrap:anywhere;box-shadow:0 1px 1px #0001}.in{background:#fff;border-top-left-radius:4px}.out{background:#d9ffc7;margin-left:auto;border-top-right-radius:4px}.bar{display:flex;padding:10px;background:#f0f2f5;gap:8px}.bar input{flex:1;border:0;outline:0;border-radius:25px;padding:14px 16px;font-size:15px}.bar button,.primary{border:0;border-radius:50%;width:48px;height:48px;background:#25d366;color:#fff;font-size:20px}.typing{padding:4px 18px;background:#f0f2f5;color:#667781;font-size:12px}.gate{position:fixed;inset:0;background:linear-gradient(135deg,#052e2a,#075e54);display:grid;place-items:center;padding:20px;z-index:5}.card{width:min(440px,100%);background:#fff;border-radius:24px;padding:28px;box-shadow:0 20px 70px #0005}.profile{display:flex;align-items:center;gap:14px;margin-bottom:22px}.bigava{width:64px;height:64px;border-radius:50%;background:linear-gradient(145deg,#25d366,#075e54);display:grid;place-items:center;color:#fff;font-size:24px;font-weight:800}.card h1{font-size:24px;margin:0}.sub{color:#667781;margin:4px 0 0}.card p{line-height:1.5;color:#445}.actions{display:flex;gap:10px}.actions button,.sendcode{flex:1;padding:14px;border:0;border-radius:12px;font-weight:700;cursor:pointer}.yes,.sendcode{background:#075e54;color:#fff}.no{background:#e8f5e9;color:#075e54}.field{width:100%;padding:13px;border:1px solid #d7dcda;border-radius:12px;margin:6px 0 10px;font-size:15px;outline:0}.hidden{display:none!important}.back{border:0;background:none;color:#075e54;font-weight:700;cursor:pointer;margin-bottom:12px}.profilebox{position:fixed;inset:0;background:#0008;display:grid;place-items:center;z-index:8;padding:20px}.profilebox .card{max-width:360px;text-align:center}.close{float:right;border:0;background:#eee;border-radius:50%;width:32px;height:32px}.danger{color:#b3261e;font-size:12px}.azmodal{position:fixed;inset:0;background:rgba(3,25,23,.68);backdrop-filter:blur(8px);display:grid;place-items:center;padding:20px;z-index:20;opacity:0;pointer-events:none;transition:.2s}.azmodal.show{opacity:1;pointer-events:auto}.azmodal-card{width:min(390px,100%);background:#fff;border-radius:24px;padding:25px;box-shadow:0 24px 80px #0006;transform:translateY(12px) scale(.98);transition:.2s}.azmodal.show .azmodal-card{transform:none}.azmodal-icon{width:52px;height:52px;border-radius:16px;background:#e8f8ef;color:#087f5b;display:grid;place-items:center;font-size:25px;margin-bottom:14px}.azmodal-title{margin:0 0 7px;font-size:20px}.azmodal-text{margin:0 0 20px;color:#667781;line-height:1.5}.azmodal-actions{display:flex;gap:10px}.azmodal-actions button{flex:1;border:0;border-radius:13px;padding:13px;font-weight:700;cursor:pointer}.social-actions{display:flex;gap:10px;margin-top:10px}.social-btn{flex:1;text-decoration:none;text-align:center;padding:12px 10px;border-radius:12px;font-weight:700;background:#1686f8;color:#fff;box-shadow:0 2px 6px #0002;display:flex;align-items:center;justify-content:center;gap:7px}.social-btn.instagram{background:#e1306c}.social-icon{width:20px;height:20px;display:inline-block;fill:currentColor}.azmodal-ok{background:#075e54;color:#fff}.azmodal-cancel{background:#edf2ef;color:#075e54}
</style></head>
<body><div class="app">
<header class="top" id="profile"><div class="ava">AZ</div><div><div class="name">AZION IA <span class="verified">✓</span></div><div class="online">Assistente profissional • online</div></div></header>
<main id="msgs" class="msgs"></main><div id="typing" class="typing hidden">AZION IA está digitando…</div>
<form id="bar" class="bar"><input id="text" placeholder="Digite uma mensagem..." maxlength="4000" autocomplete="off"><button aria-label="Enviar">➤</button></form></div>

<div id="gate" class="gate"><div class="card">
<div class="profile"><div class="bigava">AZ</div><div><h1>AZION IA <span class="verified">✓</span></h1><div class="sub">Atendimento inteligente e profissional</div></div></div>
<div id="step0"><p>Olá! Eu sou a <b>AZION IA</b>. Antes de iniciar o atendimento, preciso confirmar uma informação.</p><p><b>Você já tem uma conta no AZION IA?</b></p><div class="actions"><button type="button" class="yes" id="btnExisting" onclick="window.AZION_SHOW_EXISTING()">SIM</button><button type="button" class="no" id="btnNew" onclick="window.AZION_SHOW_NEW()">NÃO</button></div></div>
<div id="step1" class="hidden"><button type="button" class="back" id="btnBack1">← Voltar</button><h2 id="formTitle">Entrar</h2><p id="formDesc">Informe o e-mail da sua conta para receber o código.</p><input id="name" class="field hidden" placeholder="Seu nome"><input id="email" class="field" type="email" placeholder="Seu e-mail"><input id="phone" class="field hidden" placeholder="Telefone (opcional)"><button type="button" class="sendcode" id="btnRequestCode">Enviar código de verificação</button></div>
<div id="step2" class="hidden"><button type="button" class="back" id="btnBack2">← Voltar</button><h2>Verificar e-mail</h2><p>Digite o código de 6 dígitos enviado para <b id="shownEmail"></b>.</p><input id="code" class="field" inputmode="numeric" maxlength="6" placeholder="Código de verificação"><button type="button" class="sendcode" id="btnVerifyCode">Verificar e entrar</button><p id="resend" class="sub"></p></div>
<p class="danger">Nunca informe senhas, tokens ou códigos de segurança de outros serviços.</p>
</div></div>

<div id="profilebox" class="profilebox hidden"><div class="card"><button type="button" class="close" id="btnCloseProfile">×</button><div class="bigava" style="margin:auto">AZ</div><h2>AZION IA <span class="verified">✓</span></h2><p>Assistente profissional de atendimento. Clique no botão acima do chat para conhecer o perfil da IA.</p><p class="sub">Atendimento por texto • Inteligência artificial</p></div></div>
<div id="azmodal" class="azmodal" aria-hidden="true"><div class="azmodal-card" role="dialog" aria-modal="true"><div class="azmodal-icon">✓</div><h3 id="azmodalTitle" class="azmodal-title">AZION IA</h3><p id="azmodalText" class="azmodal-text"></p><div class="azmodal-actions"><button id="azmodalCancel" class="azmodal-cancel" type="button">Fechar</button><button id="azmodalOk" class="azmodal-ok" type="button">Continuar</button></div></div></div>
<script>
'use strict';

document.addEventListener('DOMContentLoaded', function(){
  const $ = id => document.getElementById(id);
  let mode = 'existing';
  let email = '';

  function showModal(message,title='AZION IA',okText='Entendi',cancel=false){
    $('azmodalTitle').textContent=title;
    $('azmodalText').textContent=message;
    $('azmodalOk').textContent=okText;
    $('azmodalCancel').style.display=cancel?'block':'none';
    $('azmodal').classList.add('show');
    $('azmodal').setAttribute('aria-hidden','false');
  }
  function closeModal(){
    $('azmodal').classList.remove('show');
    $('azmodal').setAttribute('aria-hidden','true');
  }

  async function api(data){
    const r=await fetch('api.php',{
      method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json'},
      credentials:'same-origin',
      body:JSON.stringify(data)
    });
    const text=await r.text();
    let j;
    try{j=JSON.parse(text)}catch(e){throw new Error('O servidor não retornou uma resposta válida.')}
    if(!r.ok) throw new Error(j.error||'Não foi possível concluir.');
    return j;
  }

  function showExisting(){
    mode='existing';
    $('step0').classList.add('hidden');
    $('step2').classList.add('hidden');
    $('step1').classList.remove('hidden');
    $('formTitle').textContent='Entrar no AZION IA';
    $('formDesc').textContent='Informe o e-mail da sua conta para receber o código.';
    $('name').classList.add('hidden');
    $('phone').classList.add('hidden');
    $('email').focus();
  }

  function showNew(){
    mode='new';
    $('step0').classList.add('hidden');
    $('step2').classList.add('hidden');
    $('step1').classList.remove('hidden');
    $('formTitle').textContent='Criar acesso';
    $('formDesc').textContent='Informe seus dados para criar o acesso ao AZION IA.';
    $('name').classList.remove('hidden');
    $('phone').classList.remove('hidden');
    $('name').focus();
  }

  function goBack(){
    $('step1').classList.add('hidden');
    $('step2').classList.add('hidden');
    $('step0').classList.remove('hidden');
  }

  async function requestCode(){
    try{
      email=$('email').value.trim();
      if(!email) throw new Error('Informe seu e-mail.');
      if(mode==='new'&&!$('name').value.trim()) throw new Error('Informe seu nome.');
      const j=await api({
        action:'request_code',
        mode:mode,
        email:email,
        name:$('name').value.trim(),
        phone:$('phone').value.trim()
      });
      $('shownEmail').textContent=email;
      $('step1').classList.add('hidden');
      $('step2').classList.remove('hidden');
      $('code').value='';
      $('code').focus();
      $('resend').textContent='O código expira em 10 minutos.';
    }catch(e){
      showModal(e.message,'Não foi possível continuar');
    }
  }

  async function verifyCode(){
    try{
      const code=$('code').value.trim();
      if(!/^\d{6}$/.test(code)) throw new Error('Digite o código de 6 dígitos.');
      const j=await api({action:'verify_code',email:email,code:code});
      $('gate').classList.add('hidden');
      $('msgs').innerHTML='';
      (j.messages||[]).forEach(x=>msg(x.text,(x.role==='assistant'||x.role==='human')?'in':'out'));
    }catch(e){
      showModal(e.message,'Código não validado');
    }
  }

  function wantsImageRequest(text){
    return /(?:crie|criar|gere|gerar|faca|faça|faz|fazer|desenhe|desenha|desenhar|produza|produzir|cria|quero)\s+(?:uma?\s+)?(?:imagem|foto|desenho|arte)\b|\b(?:imagem|foto|desenho|arte)\s+(?:de|do|da|com|mostrando)\b/i.test(text);
  }
  function extractImagePrompt(text){
    return String(text).replace(/^\s*(?:por favor[, ]*)?(?:crie|criar|gere|gerar|faca|faça|faz|fazer|desenhe|desenha|desenhar|produza|produzir|cria|quero)\s+(?:uma?\s+)?(?:imagem|foto|desenho|arte)\s*(?:de|do|da|com|mostrando)?\s*/i,'').trim() || String(text).trim();
  }
  function imageMsg(data){
    const d=document.createElement('div');
    d.className='msg in';
    const label=document.createElement('div');
    label.textContent='Imagem criada pela AZION IA';
    label.style.marginBottom='8px';
    const img=document.createElement('img');
    img.src=data.image;
    img.alt='Imagem criada pela AZION IA';
    img.loading='lazy';
    img.style.maxWidth='100%';
    img.style.borderRadius='10px';
    d.appendChild(label);
    d.appendChild(img);
    $('msgs').appendChild(d);
    $('msgs').scrollTop=$('msgs').scrollHeight;
  }

  function msg(t,c){
    const d=document.createElement('div');
    d.className='msg '+c;
    const text=String(t||'');
    if(c==='in'&&((/telegram/i.test(text)&&/instagram/i.test(text))||(/\b(jadiel|desenvolvedor|desenvolveu|criou|criador|dono|proprietário|proprietario|jdl programing)\b/i.test(text)))){
      const clean=text.replace(/https?:\/\/\S+/gi,'').trim();
      if(clean){
        const p=document.createElement('div');
        p.textContent=clean;
        d.appendChild(p);
      }
      const actions=document.createElement('div');
      actions.className='social-actions';
      const tg=document.createElement('a');
      tg.className='social-btn';
      tg.href='https://t.me/JADIEL_TM';
      tg.target='_blank';
      tg.rel='noopener noreferrer';
      tg.innerHTML='<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21.4 3.2 2.9 10.3c-1.3.5-1.3 1.4-.2 1.7l4.7 1.5 1.8 5.6c.2.7.4.9.9 1.1l2.3-2.2 4.8 3.5c.9.5 1.5.2 1.7-.8l3.1-14.5c.3-1.3-.5-1.9-1.8-1.4ZM8.1 13.1l10.9-6.9c.5-.3 1-.1.6.2l-9 8.1-.3 3.4-.3 3.4-1.7-4.8-2.9-.9c-.6-.2-.6-.6-.1-.9l2.3-.9Z"/></svg><span>Telegram</span>';
      actions.appendChild(tg);
      const ig=document.createElement('a');
      ig.className='social-btn instagram';
      ig.href='https://www.instagram.com/jadiel_strb_brd?stkn=cmZoNWxmcHo3ZGd5';
      ig.target='_blank';
      ig.rel='noopener noreferrer';
      ig.innerHTML='<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7Zm5 3.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 0 1 12 7.5Zm0 2A2.5 2.5 0 1 0 14.5 12 2.5 2.5 0 0 0 12 9.5ZM17.5 6a1.25 1.25 0 1 1-1.25 1.25A1.25 1.25 0 0 1 17.5 6Z"/></svg><span>Instagram</span>';
      actions.appendChild(ig);
      d.appendChild(actions);
    }else{
      d.textContent=text;
    }
    $('msgs').appendChild(d);
    $('msgs').scrollTop=$('msgs').scrollHeight;
  }

  window.AZION_SHOW_EXISTING=showExisting;
  window.AZION_SHOW_NEW=showNew;
  $('btnExisting').addEventListener('click',showExisting);
  $('btnNew').addEventListener('click',showNew);
  $('btnBack1').addEventListener('click',goBack);
  $('btnBack2').addEventListener('click',goBack);
  $('btnRequestCode').addEventListener('click',requestCode);
  $('btnVerifyCode').addEventListener('click',verifyCode);
  $('btnCloseProfile').addEventListener('click',()=> $('profilebox').classList.add('hidden'));
  $('azmodalOk').addEventListener('click',closeModal);
  $('azmodalCancel').addEventListener('click',closeModal);
  $('azmodal').addEventListener('click',e=>{if(e.target===$('azmodal'))closeModal()});
  $('profile').addEventListener('click',()=> $('profilebox').classList.remove('hidden'));

  $('bar').addEventListener('submit',async function(e){
    e.preventDefault();
    const t=$('text').value.trim();
    if(!t)return;
    $('text').value='';
    msg(t,'out');
    $('typing').classList.remove('hidden');
    try{
      if(wantsImageRequest(t)){
        $('typing').textContent='AZION IA está criando sua imagem…';
        const prompt=extractImagePrompt(t);
        const j=await api({action:'generate_image',prompt:prompt});
        if(j.image){imageMsg(j);if(j.prompt)msg('Imagem criada com sucesso.','in');}
        else msg('A Groq não cria imagens; essa função precisa de um serviço de geração de imagens.','in');
      }else{
        $('typing').textContent='AZION IA está digitando…';
        const j=await api({action:'chat',message:t});
        msg(j.reply||j.error||'Não recebi uma resposta válida.','in');
      }
    }catch(e){msg(e.message,'in')}
    finally{$('typing').textContent='AZION IA está digitando…';$('typing').classList.add('hidden')}
  });

  (async function(){
    try{
      const j=await api({action:'me'});
      if(j.authenticated){
        $('gate').classList.add('hidden');
        $('msgs').innerHTML='';
        (j.messages||[]).forEach(x=>msg(x.text,(x.role==='assistant'||x.role==='human')?'in':'out'));
      }
    }catch(e){}
  })();
});
</script>
</body></html>