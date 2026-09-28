<?php
// JADIEL SITE CHECK — página pública
session_start();
$dataDir = __DIR__ . '/data';
if (!is_dir($dataDir)) { @mkdir($dataDir, 0755, true); }
$noticeFile = $dataDir . '/notice.json';
$notice = null;
if (is_file($noticeFile)) {
    $raw = @file_get_contents($noticeFile);
    $decoded = json_decode($raw ?: '', true);
    if (is_array($decoded) && !empty($decoded['active'])) {
        $expires = !empty($decoded['expires_at']) ? strtotime($decoded['expires_at']) : null;
        if (!$expires || $expires >= time()) $notice = $decoded;
    }
}
?>
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>JADIEL CHECK — Verificação de sites</title>
<meta name="description" content="Analise um endereço de site e consulte informações públicas de segurança e identidade.">
<style>
:root{--bg:#050807;--panel:rgba(14,22,19,.72);--line:rgba(120,255,190,.16);--green:#5cffaa;--text:#f4fff9;--muted:#91a99d}*{box-sizing:border-box}html,body{margin:0;min-height:100%;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:radial-gradient(circle at 50% 0,#123d2b 0,transparent 42%),linear-gradient(135deg,#030504,#07100c 55%,#020403);color:var(--text)}body:before{content:"";position:fixed;inset:0;pointer-events:none;background-image:radial-gradient(rgba(92,255,170,.18) 1px,transparent 1px);background-size:32px 32px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.8),transparent 75%)}.wrap{width:min(1120px,92%);margin:auto}.top{padding:24px 0;display:flex;align-items:center;justify-content:space-between}.brand{font-weight:900;letter-spacing:.08em}.brand span{color:var(--green)}.badge{border:1px solid var(--line);padding:8px 12px;border-radius:999px;color:var(--green);font-size:12px;background:rgba(92,255,170,.06)}.hero{min-height:76vh;display:grid;place-items:center;text-align:center;padding:60px 0}.orb{width:96px;height:96px;margin:0 auto 28px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#d7ffea,#5cffaa 24%,#087c4b 55%,#021b10 72%);box-shadow:0 0 40px rgba(92,255,170,.45),0 0 120px rgba(92,255,170,.12);animation:float 4s ease-in-out infinite}.hero h1{font-size:clamp(40px,8vw,82px);line-height:.95;margin:0 0 20px;letter-spacing:-.05em}.hero h1 i{font-style:normal;color:var(--green)}.hero p{max-width:680px;margin:0 auto 34px;color:var(--muted);font-size:18px;line-height:1.6}.search{display:flex;gap:10px;max-width:760px;margin:auto;padding:10px;border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(22px);border-radius:22px;box-shadow:0 20px 70px rgba(0,0,0,.35)}input{flex:1;min-width:0;border:0;outline:0;background:transparent;color:#fff;padding:17px;font-size:16px}button{border:0;border-radius:15px;padding:0 25px;background:var(--green);color:#03130b;font-weight:800;cursor:pointer;transition:.25s}button:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(92,255,170,.25)}.notice{position:fixed;right:20px;bottom:20px;width:min(390px,calc(100% - 40px));padding:18px;border:1px solid var(--line);border-radius:20px;background:rgba(8,18,14,.92);backdrop-filter:blur(20px);box-shadow:0 20px 60px #0008;z-index:5}.notice strong{display:block;margin-bottom:6px}.notice p{margin:0;color:var(--muted);line-height:1.5}.result{display:none;max-width:900px;margin:35px auto 0;text-align:left;padding:24px;border:1px solid var(--line);border-radius:22px;background:rgba(10,18,14,.75);backdrop-filter:blur(18px)}.result.show{display:block}.result h2{margin-top:0}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{padding:8px 11px;border-radius:999px;background:#ffffff0b;color:#b7d7c6;border:1px solid #ffffff12;font-size:13px}@keyframes float{50%{transform:translateY(-10px)}}@media(max-width:640px){.search{flex-direction:column}button{height:54px}.hero{padding-top:30px}.top{padding:18px 0}.badge{display:none}}
</style>
</head><body>
<div class="wrap"><header class="top"><div class="brand">JADIEL <span>CHECK</span></div><div class="badge">ANÁLISE DE URL</div></header>
<main class="hero"><section><div class="orb"></div><h1>Verifique um <i>site</i>.</h1><p>Cole o endereço de um site para consultar informações públicas, identidade do domínio e sinais técnicos disponíveis. O relatório distingue dados encontrados de conclusões que não podem ser confirmadas automaticamente.</p>
<form class="search" id="checkForm"><input id="url" type="url" required placeholder="https://exemplo.com" autocomplete="url"><button>ANALISAR</button></form>
<div class="result" id="result"><h2>Consulta iniciada</h2><p id="resultText"></p><div class="chips"><span class="chip">URL válida</span><span class="chip">HTTPS</span><span class="chip">Análise pública</span></div></div>
</section></main></div>
<?php if ($notice): ?><aside class="notice"><strong><?= htmlspecialchars($notice['title'] ?? 'Aviso') ?></strong><p><?= nl2br(htmlspecialchars($notice['message'] ?? '')) ?></p></aside><?php endif; ?>
<script>document.getElementById('checkForm').addEventListener('submit',e=>{e.preventDefault();const u=document.getElementById('url').value.trim();const r=document.getElementById('result');const t=document.getElementById('resultText');try{const x=new URL(u);t.textContent='Endereço recebido: '+x.hostname+'. A interface está pronta para conectar a uma rotina PHP de consulta real, sem simular resultados.';r.classList.add('show')}catch{t.textContent='Informe uma URL válida, como https://exemplo.com.';r.classList.add('show')}});</script>
</body></html>
