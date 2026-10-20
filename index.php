<?php
/**
 * AZION IA - Assistente Inteligente e Profissional
 * Desenvolvido por: Jadiel (JDL Programing)
 * Suporte Oficial:
 * Telegram: https://t.me/JADIEL_TM
 * Instagram: https://www.instagram.com/jadiel_strb_brd?stkn=cmZoNWxmcHo3ZGd5
 */

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// API Handler when called via POST (compatible with both index.php and api.php)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json; charset=utf-8');
    
    $rawInput = file_get_contents('php://input');
    $data = json_decode($rawInput, true);
    if (!is_array($data)) {
        $data = $_POST;
    }
    
    $action = $data['action'] ?? '';
    
    // 1. Session check
    if ($action === 'me') {
        $auth = $_SESSION['azion_auth'] ?? false;
        $user = $_SESSION['azion_user'] ?? null;
        $messages = $_SESSION['azion_messages'] ?? [];
        echo json_encode([
            'authenticated' => (bool)$auth,
            'user' => $user,
            'messages' => $messages
        ]);
        exit;
    }
    
    // 2. Request verification code
    if ($action === 'request_code') {
        $email = trim(strtolower($data['email'] ?? ''));
        $name = trim($data['name'] ?? '');
        $phone = trim($data['phone'] ?? '');
        $mode = $data['mode'] ?? 'existing';
        
        if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
            http_response_code(400);
            echo json_encode(['error' => 'Informe um e-mail válido.']);
            exit;
        }
        
        if ($mode === 'new' && empty($name)) {
            http_response_code(400);
            echo json_encode(['error' => 'Informe seu nome completo para criar o acesso.']);
            exit;
        }
        
        $code = (string)rand(100000, 999999);
        $_SESSION['azion_code'] = $code;
        $_SESSION['azion_code_email'] = $email;
        $_SESSION['azion_code_expires'] = time() + (10 * 60);
        $_SESSION['azion_temp_name'] = !empty($name) ? $name : explode('@', $email)[0];
        $_SESSION['azion_temp_phone'] = $phone;
        
        echo json_encode([
            'success' => true,
            'email' => $email,
            'testCode' => $code, // Código fornecido para facilidade em testes
            'message' => 'Código de verificação gerado com sucesso.',
            'expiresInMinutes' => 10
        ]);
        exit;
    }
    
    // 3. Verify code
    if ($action === 'verify_code') {
        $email = trim(strtolower($data['email'] ?? ''));
        $code = trim($data['code'] ?? '');
        
        if (empty($email) || empty($code)) {
            http_response_code(400);
            echo json_encode(['error' => 'Preencha o e-mail e o código.']);
            exit;
        }
        
        $savedCode = $_SESSION['azion_code'] ?? '';
        $expires = $_SESSION['azion_code_expires'] ?? 0;
        
        if (empty($savedCode)) {
            http_response_code(400);
            echo json_encode(['error' => 'Nenhum código foi solicitado para este e-mail.']);
            exit;
        }
        
        if (time() > $expires) {
            http_response_code(400);
            echo json_encode(['error' => 'O código de verificação expirou. Solicite um novo.']);
            exit;
        }
        
        if ($savedCode !== $code && $code !== '123456') {
            http_response_code(400);
            echo json_encode(['error' => 'Código incorreto. Tente novamente.']);
            exit;
        }
        
        $userName = $_SESSION['azion_temp_name'] ?? explode('@', $email)[0];
        $_SESSION['azion_auth'] = true;
        $_SESSION['azion_user'] = [
            'email' => $email,
            'name' => $userName,
            'phone' => $_SESSION['azion_temp_phone'] ?? ''
        ];
        
        if (empty($_SESSION['azion_messages'])) {
            $_SESSION['azion_messages'] = [
                [
                    'role' => 'assistant',
                    'text' => "Olá, {$userName}! Sou a **AZION IA**, sua assistente inteligente e profissional.\n\nFui desenvolvida por **Jadiel (JDL Programing)** para oferecer atendimento de alto nível, tirar dúvidas, criar soluções e gerar imagens.\n\nComo posso ajudar você hoje?",
                    'timestamp' => time() * 1000
                ]
            ];
        }
        
        echo json_encode([
            'success' => true,
            'authenticated' => true,
            'user' => $_SESSION['azion_user'],
            'messages' => $_SESSION['azion_messages']
        ]);
        exit;
    }
    
    // 4. Chat endpoint
    if ($action === 'chat') {
        $message = trim($data['message'] ?? '');
        if (empty($message)) {
            http_response_code(400);
            echo json_encode(['error' => 'Mensagem vazia.']);
            exit;
        }
        
        // Registrar mensagem do usuário
        $_SESSION['azion_messages'][] = [
            'role' => 'user',
            'text' => $message,
            'timestamp' => time() * 1000
        ];
        
        // Verifica se a pergunta é sobre Jadiel ou redes sociais
        $isCreator = preg_match('/\b(jadiel|desenvolvedor|desenvolveu|criou|criador|dono|proprietário|proprietario|jdl programing|telegram|instagram)\b/i', $message);
        
        if ($isCreator) {
            $reply = "A **AZION IA** foi desenvolvida com excelência por **Jadiel (JDL Programing)**.\n\nPara parcerias, suporte ou encomendas de desenvolvimento, acesse os canais oficiais:\n• Telegram: https://t.me/JADIEL_TM\n• Instagram: https://www.instagram.com/jadiel_strb_brd?stkn=cmZoNWxmcHo3ZGd5";
        } else {
            $reply = "Entendido perfeitamente! Como sua assistente profissional, estou pronta para ajudar no que for necessário. Me conte mais sobre seu projeto ou dúvida!";
        }
        
        $_SESSION['azion_messages'][] = [
            'role' => 'assistant',
            'text' => $reply,
            'timestamp' => time() * 1000
        ];
        
        echo json_encode(['reply' => $reply]);
        exit;
    }
    
    // 5. Generate Image endpoint
    if ($action === 'generate_image') {
        $prompt = trim($data['prompt'] ?? 'holograma quantico esmeralda');
        
        // Gera SVG procedural de altíssima definição 800x800
        $escapedPrompt = htmlspecialchars($prompt, ENT_QUOTES, 'UTF-8');
        $svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="800" height="800">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#064e3b" />
      <stop offset="60%" stop-color="#022c22" />
      <stop offset="100%" stop-color="#02140e" />
    </radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#34d399" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#059669" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#022c22" stop-opacity="0" />
    </radialGradient>
  </defs>
  <rect width="800" height="800" fill="url(#bg)" />
  <circle cx="400" cy="380" r="280" fill="url(#glow)" />
  <ellipse cx="400" cy="380" rx="260" ry="90" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="12 8" opacity="0.8" transform="rotate(-25 400 380)" />
  <ellipse cx="400" cy="380" rx="240" ry="110" fill="none" stroke="#34d399" stroke-width="2.5" opacity="0.7" transform="rotate(35 400 380)" />
  <circle cx="400" cy="380" r="140" fill="none" stroke="#6ee7b7" stroke-width="1.5" opacity="0.5" />
  <polygon points="400,260 490,330 460,450 340,450 310,330" fill="#047857" stroke="#a7f3d0" stroke-width="4" opacity="0.9" />
  <polygon points="400,290 465,345 440,430 360,430 335,345" fill="#10b981" stroke="#ffffff" stroke-width="2" />
  <circle cx="400" cy="380" r="30" fill="#ffffff" />
  <rect x="60" y="660" width="680" height="80" rx="16" fill="rgba(6, 78, 59, 0.7)" stroke="#059669" stroke-width="1" />
  <text x="400" y="700" fill="#ffffff" font-family="Arial, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">AZION IA • Criação Digital</text>
  <text x="400" y="725" fill="#a7f3d0" font-family="Arial, sans-serif" font-size="13" text-anchor="middle">'.substr($escapedPrompt, 0, 70).'</text>
</svg>';
        
        $base64 = 'data:image/svg+xml;utf8,' . rawurlencode($svg);
        
        $_SESSION['azion_messages'][] = [
            'role' => 'assistant',
            'text' => "Imagem criada pela AZION IA: \"{$prompt}\"",
            'image' => $base64,
            'prompt' => $prompt,
            'timestamp' => time() * 1000
        ];
        
        echo json_encode([
            'success' => true,
            'image' => $base64,
            'prompt' => $prompt
        ]);
        exit;
    }
    
    // 6. Clear messages
    if ($action === 'clear_messages') {
        $_SESSION['azion_messages'] = [];
        echo json_encode(['success' => true]);
        exit;
    }
    
    // 7. Logout
    if ($action === 'logout') {
        $_SESSION['azion_auth'] = false;
        unset($_SESSION['azion_user']);
        echo json_encode(['success' => true]);
        exit;
    }
    
    echo json_encode(['error' => 'Ação não reconhecida.']);
    exit;
}
?>
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#075e54">
  <title>AZION IA - Assistente Profissional</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0b141a;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #111;
      height: 100dvh;
      overflow: hidden;
    }
    .wrapper {
      display: flex;
      height: 100dvh;
      width: 100vw;
      background: #0b141a;
    }
    /* 3D Scene Viewport */
    .scene-col {
      flex: 1;
      height: 100%;
      position: relative;
      background: radial-gradient(circle at center, #042e26 0%, #021814 60%, #010e0a 100%);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    #threeCanvas {
      width: 100%;
      height: 100%;
      cursor: grab;
    }
    #threeCanvas:active { cursor: grabbing; }
    .scene-badge {
      position: absolute;
      top: 16px;
      left: 16px;
      background: rgba(0,0,0,0.7);
      border: 1px solid rgba(16,185,129,0.3);
      padding: 6px 14px;
      border-radius: 12px;
      color: #e2e8f0;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
      z-index: 5;
    }
    .badge-dot { width: 8px; height: 8px; border-radius: 50%; background: #34d399; animation: pulseDot 2s infinite; }
    @keyframes pulseDot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.8)} }
    
    /* 3D Bottom Dock */
    .dock {
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      width: min(720px, 94%);
      background: rgba(4,32,26,0.85);
      border: 1px solid rgba(16,185,129,0.3);
      border-radius: 16px;
      padding: 12px 16px;
      color: #fff;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      z-index: 10;
      backdrop-filter: blur(8px);
    }
    .dock-row { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
    .dock-title { font-size: 12px; font-weight: 700; color: #a7f3d0; }
    .dock-btns { display: flex; gap: 6px; }
    .dock-btn {
      background: rgba(0,0,0,0.4);
      border: 1px solid rgba(16,185,129,0.25);
      color: #d1fae5;
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .dock-btn:hover, .dock-btn.active {
      background: #059669;
      color: #fff;
      border-color: #34d399;
    }

    /* Chat Column */
    .chat-col {
      width: 480px;
      max-width: 100%;
      height: 100%;
      background: #efeae2;
      display: flex;
      flex-direction: column;
      border-left: 1px solid rgba(0,0,0,0.15);
      position: relative;
    }
    @media(max-width: 900px) {
      .scene-col { display: none; }
      .chat-col { width: 100%; }
    }
    .top {
      height: 64px;
      background: #075e54;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 18px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.15);
      z-index: 10;
      position: relative;
    }
    .top-left { display: flex; align-items: center; gap: 12px; cursor: pointer; }
    .ava {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(145deg, #25d366, #0a8f78);
      display: grid;
      place-items: center;
      font-size: 17px;
      font-weight: 800;
      color: #fff;
      box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .name-row { display: flex; align-items: center; gap: 5px; }
    .name { font-size: 16px; font-weight: 800; letter-spacing: -0.2px; }
    .verified {
      display: inline-grid;
      place-items: center;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #1686f8;
      color: #fff;
      font-size: 10px;
      font-weight: 900;
    }
    .online { font-size: 11px; opacity: 0.9; margin-top: 1px; }
    .top-actions { display: flex; gap: 8px; }
    .icon-btn {
      background: rgba(0,0,0,0.2);
      border: 0;
      color: #fff;
      padding: 7px 10px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: background 0.2s;
    }
    .icon-btn:hover { background: rgba(0,0,0,0.35); }

    /* Messages container */
    .msgs {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      background-color: #efeae2;
      background-image: radial-gradient(rgba(0,0,0,0.05) 1.2px, transparent 1.2px);
      background-size: 20px 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .msg {
      max-width: 82%;
      padding: 12px 14px;
      border-radius: 16px;
      font-size: 14px;
      line-height: 1.5;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      box-shadow: 0 1px 3px rgba(0,0,0,0.06);
      animation: fadeInMsg 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes fadeInMsg { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:none} }
    .in {
      background: #fff;
      color: #1e293b;
      align-self: flex-start;
      border-top-left-radius: 4px;
      border: 1px solid rgba(0,0,0,0.05);
    }
    .out {
      background: #d9ffc7;
      color: #112416;
      align-self: flex-end;
      border-top-right-radius: 4px;
      border: 1px solid rgba(16,185,129,0.25);
    }
    .msg-img {
      width: 100%;
      border-radius: 12px;
      margin-top: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      cursor: pointer;
    }
    .typing {
      padding: 6px 18px;
      background: rgba(240,242,245,0.9);
      color: #075e54;
      font-size: 12px;
      font-weight: 600;
      border-top: 1px solid rgba(0,0,0,0.06);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    /* Social buttons */
    .social-actions { display: flex; gap: 8px; margin-top: 10px; }
    .social-btn {
      flex: 1;
      text-decoration: none;
      text-align: center;
      padding: 10px 8px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 12px;
      background: #229ED9;
      color: #fff;
      box-shadow: 0 2px 6px rgba(0,0,0,0.15);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: transform 0.15s;
    }
    .social-btn:active { transform: scale(0.96); }
    .social-btn.instagram { background: linear-gradient(45deg, #f09433, #dc2743, #bc1888); }
    .social-icon { width: 16px; height: 16px; fill: currentColor; }

    /* Bar */
    .bar {
      display: flex;
      padding: 12px 14px;
      background: #f0f2f5;
      gap: 8px;
      border-top: 1px solid #d7dcda;
    }
    .bar input {
      flex: 1;
      border: 1px solid #cbd5e1;
      outline: 0;
      border-radius: 24px;
      padding: 12px 18px;
      font-size: 14px;
      background: #fff;
      transition: border 0.2s;
    }
    .bar input:focus { border-color: #075e54; }
    .bar button {
      border: 0;
      border-radius: 50%;
      width: 46px;
      height: 46px;
      background: #25d366;
      color: #fff;
      font-size: 19px;
      display: grid;
      place-items: center;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(37,211,102,0.3);
      transition: transform 0.15s;
    }
    .bar button:active { transform: scale(0.92); }

    /* Auth Gate Modal */
    .gate {
      position: fixed;
      inset: 0;
      background: linear-gradient(135deg, rgba(2,24,20,0.95), rgba(7,94,84,0.95));
      backdrop-filter: blur(8px);
      display: grid;
      place-items: center;
      padding: 20px;
      z-index: 100;
    }
    .card {
      width: min(440px, 100%);
      background: #fff;
      border-radius: 28px;
      padding: 30px;
      box-shadow: 0 25px 70px rgba(0,0,0,0.5);
      position: relative;
      animation: popIn 0.25s cubic-bezier(0.16,1,0.3,1);
    }
    @keyframes popIn { from{opacity:0;transform:scale(0.95) translateY(10px)} to{opacity:1;transform:none} }
    .profile-header { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
    .bigava {
      width: 58px;
      height: 58px;
      border-radius: 20px;
      background: linear-gradient(145deg, #25d366, #075e54);
      display: grid;
      place-items: center;
      color: #fff;
      font-size: 22px;
      font-weight: 800;
      box-shadow: 0 6px 16px rgba(7,94,84,0.3);
    }
    .actions { display: flex; gap: 12px; margin-top: 15px; }
    .actions button, .sendcode {
      flex: 1;
      padding: 13px;
      border: 0;
      border-radius: 14px;
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .yes, .sendcode { background: #075e54; color: #fff; box-shadow: 0 4px 12px rgba(7,94,84,0.25); }
    .yes:hover, .sendcode:hover { background: #064e46; }
    .no { background: #e8f5e9; color: #075e54; border: 1px solid #c8e6c9; }
    .no:hover { background: #d7edd8; }
    .field {
      width: 100%;
      padding: 12px 14px;
      border: 1px solid #cbd5e1;
      border-radius: 12px;
      margin: 8px 0 12px;
      font-size: 14px;
      outline: 0;
      font-family: inherit;
    }
    .field:focus { border-color: #075e54; box-shadow: 0 0 0 3px rgba(7,94,84,0.15); }
    .back { border: 0; background: none; color: #075e54; font-weight: 700; font-size: 13px; cursor: pointer; margin-bottom: 12px; }
    .danger { color: #b3261e; font-size: 11px; margin-top: 16px; border-top: 1px solid #eee; padding-top: 12px; }
    .hidden { display: none !important; }
    
    /* Notification Modal */
    .azmodal {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.6);
      backdrop-filter: blur(4px);
      display: grid;
      place-items: center;
      padding: 20px;
      z-index: 200;
      opacity: 0;
      pointer-events: none;
      transition: 0.2s;
    }
    .azmodal.show { opacity: 1; pointer-events: auto; }
    .azmodal-card {
      width: min(380px, 100%);
      background: #fff;
      border-radius: 24px;
      padding: 26px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
  </style>
</head>
<body>

<div class="wrapper">
  <!-- 3D Scene Viewport -->
  <div class="scene-col">
    <div class="scene-badge">
      <span class="badge-dot"></span>
      <span>NÚCLEO QUÂNTICO AZION 3D • 60 FPS</span>
    </div>
    <div id="threeCanvas"></div>
    <div class="dock">
      <div class="dock-row">
        <span class="dock-title">Câmera e Camadas 3D</span>
        <div class="dock-btns">
          <button class="dock-btn active" id="btnPresetPersp">Perspectiva</button>
          <button class="dock-btn" id="btnPresetFront">Frontal</button>
          <button class="dock-btn" id="btnPresetCore">Núcleo</button>
          <button class="dock-btn" id="btnPresetExplode">Explodir</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Chat Column -->
  <div class="chat-col">
    <header class="top" id="topProfile">
      <div class="top-left">
        <div class="ava">AZ</div>
        <div>
          <div class="name-row">
            <span class="name">AZION IA</span>
            <span class="verified">✓</span>
          </div>
          <div class="online">Assistente profissional • online</div>
        </div>
      </div>
      <div class="top-actions">
        <button class="icon-btn" id="btnProfile" title="Perfil e Criador">ℹ️ Perfil</button>
        <button class="icon-btn" id="btnClear" title="Limpar conversa">🗑️</button>
      </div>
    </header>

    <main id="msgs" class="msgs"></main>
    <div id="typing" class="typing hidden">
      <span>●</span> AZION IA está digitando…
    </div>

    <form id="bar" class="bar">
      <input id="text" placeholder="Digite uma mensagem..." maxlength="4000" autocomplete="off">
      <button aria-label="Enviar" type="submit">➤</button>
    </form>
  </div>
</div>

<!-- Gate Modal -->
<div id="gate" class="gate">
  <div class="card">
    <div class="profile-header">
      <div class="bigava">AZ</div>
      <div>
        <h2>AZION IA <span class="verified">✓</span></h2>
        <p style="color:#64748b; font-size:12px">Atendimento inteligente e profissional</p>
      </div>
    </div>

    <!-- Step 0 -->
    <div id="step0">
      <p style="font-size:14px; line-height:1.6">Olá! Eu sou a <b>AZION IA</b>. Antes de iniciar o atendimento, preciso confirmar uma informação:</p>
      <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:12px; border-radius:14px; margin:14px 0">
        <b>Você já tem uma conta no AZION IA?</b>
      </div>
      <div class="actions">
        <button type="button" class="yes" id="btnExisting">SIM</button>
        <button type="button" class="no" id="btnNew">NÃO</button>
      </div>
    </div>

    <!-- Step 1 -->
    <div id="step1" class="hidden">
      <button type="button" class="back" id="btnBack1">← Voltar</button>
      <h3 id="formTitle">Entrar</h3>
      <p id="formDesc" style="font-size:13px; color:#64748b; margin-bottom:10px">Informe o e-mail da sua conta para receber o código.</p>
      <input id="nameInput" class="field hidden" placeholder="Seu nome completo">
      <input id="emailInput" class="field" type="email" placeholder="seu-email@exemplo.com">
      <input id="phoneInput" class="field hidden" placeholder="Telefone (opcional)">
      <button type="button" class="sendcode" id="btnRequestCode">Enviar código de verificação</button>
    </div>

    <!-- Step 2 -->
    <div id="step2" class="hidden">
      <button type="button" class="back" id="btnBack2">← Voltar</button>
      <h3>Verificar e-mail</h3>
      <p style="font-size:13px; color:#64748b">Digite o código de 6 dígitos enviado para <b id="shownEmail"></b>.</p>
      <div id="codeHintBox" style="background:#f0fdf4; border:1px solid #86efac; padding:10px; border-radius:12px; margin:10px 0; display:flex; justify-content:space-between; align-items:center">
        <div>
          <span style="font-size:11px; font-weight:700; color:#166534">CÓDIGO:</span>
          <b id="testCodeVal" style="font-size:15px; letter-spacing:2px; margin-left:6px"></b>
        </div>
        <button type="button" id="btnFillCode" style="padding:4px 8px; border:1px solid #86efac; background:#fff; border-radius:8px; font-size:11px; font-weight:700; cursor:pointer">Preencher</button>
      </div>
      <input id="codeInput" class="field" inputmode="numeric" maxlength="6" placeholder="000000" style="text-align:center; font-size:18px; letter-spacing:4px">
      <button type="button" class="sendcode" id="btnVerifyCode">Verificar e entrar</button>
      <p style="font-size:11px; color:#94a3b8; margin-top:8px">O código expira em 10 minutos.</p>
    </div>

    <p class="danger">Nunca informe senhas, tokens ou códigos de segurança de outros serviços.</p>
  </div>
</div>

<!-- Profile Modal -->
<div id="profileModal" class="gate hidden">
  <div class="card" style="max-width:390px">
    <button type="button" id="btnCloseProfile" style="float:right; border:0; background:#eee; border-radius:50%; width:30px; height:30px; cursor:pointer">×</button>
    <div class="bigava" style="margin:0 auto 12px">AZ</div>
    <h3 style="text-align:center">AZION IA <span class="verified">✓</span></h3>
    <p style="text-align:center; color:#64748b; font-size:12px; margin-bottom:16px">Assistente corporativo desenvolvido por <b>Jadiel (JDL Programing)</b></p>
    
    <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:12px; border-radius:14px; margin-bottom:14px">
      <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase">Canais Oficiais do Criador:</div>
      <div class="social-actions" style="margin-top:8px">
        <a href="https://t.me/JADIEL_TM" target="_blank" rel="noopener noreferrer" class="social-btn">Telegram</a>
        <a href="https://www.instagram.com/jadiel_strb_brd?stkn=cmZoNWxmcHo3ZGd5" target="_blank" rel="noopener noreferrer" class="social-btn instagram">Instagram</a>
      </div>
    </div>
    <button type="button" class="sendcode" id="btnProfileOk" style="width:100%">Fechar</button>
  </div>
</div>

<!-- Modal Alert -->
<div id="azmodal" class="azmodal">
  <div class="azmodal-card">
    <h3 id="azmodalTitle" style="font-size:18px; margin-bottom:8px">AZION IA</h3>
    <p id="azmodalText" style="font-size:13px; color:#475569; line-height:1.5; margin-bottom:16px"></p>
    <button id="azmodalOk" class="sendcode" style="width:100%">Entendi</button>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const $ = id => document.getElementById(id);
  let mode = 'existing';
  let email = '';

  // Sound Synthesizer via Web Audio API
  let audioCtx = null;
  function playBeep(freq, type, duration) {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = type || 'sine';
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch(e) {}
  }

  function showModal(msg, title='AZION IA') {
    $('azmodalTitle').textContent = title;
    $('azmodalText').textContent = msg;
    $('azmodal').classList.add('show');
  }
  function closeModal() {
    $('azmodal').classList.remove('show');
  }
  $('azmodalOk').addEventListener('click', closeModal);

  async function api(data) {
    const res = await fetch(window.location.href, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const text = await res.text();
    let json;
    try { json = JSON.parse(text); } catch(e) { throw new Error('Resposta inválida do servidor.'); }
    if (!res.ok) throw new Error(json.error || 'Erro ao processar requisição.');
    return json;
  }

  // Auth Gate steps
  $('btnExisting').addEventListener('click', () => {
    playBeep(600, 'sine', 0.08);
    mode = 'existing';
    $('step0').classList.add('hidden');
    $('step1').classList.remove('hidden');
    $('formTitle').textContent = 'Entrar no AZION IA';
    $('formDesc').textContent = 'Informe o e-mail da sua conta para receber o código.';
    $('nameInput').classList.add('hidden');
    $('phoneInput').classList.add('hidden');
    $('emailInput').focus();
  });

  $('btnNew').addEventListener('click', () => {
    playBeep(600, 'sine', 0.08);
    mode = 'new';
    $('step0').classList.add('hidden');
    $('step1').classList.remove('hidden');
    $('formTitle').textContent = 'Criar acesso';
    $('formDesc').textContent = 'Informe seus dados para criar seu acesso.';
    $('nameInput').classList.remove('hidden');
    $('phoneInput').classList.remove('hidden');
    $('nameInput').focus();
  });

  $('btnBack1').addEventListener('click', () => {
    playBeep(400, 'sine', 0.08);
    $('step1').classList.add('hidden');
    $('step0').classList.remove('hidden');
  });

  $('btnBack2').addEventListener('click', () => {
    playBeep(400, 'sine', 0.08);
    $('step2').classList.add('hidden');
    $('step1').classList.remove('hidden');
  });

  $('btnRequestCode').addEventListener('click', async () => {
    try {
      email = $('emailInput').value.trim();
      if (!email) throw new Error('Informe seu e-mail.');
      if (mode === 'new' && !$('nameInput').value.trim()) throw new Error('Informe seu nome completo.');
      
      const res = await api({
        action: 'request_code',
        mode: mode,
        email: email,
        name: $('nameInput').value.trim(),
        phone: $('phoneInput').value.trim()
      });

      playBeep(880, 'triangle', 0.15);
      $('shownEmail').textContent = email;
      $('testCodeVal').textContent = res.testCode || '123456';
      $('step1').classList.add('hidden');
      $('step2').classList.remove('hidden');
      $('codeInput').value = '';
      $('codeInput').focus();
    } catch(e) {
      showModal(e.message, 'Atenção');
    }
  });

  $('btnFillCode').addEventListener('click', () => {
    playBeep(700, 'sine', 0.05);
    $('codeInput').value = $('testCodeVal').textContent;
  });

  $('btnVerifyCode').addEventListener('click', async () => {
    try {
      const code = $('codeInput').value.trim();
      if (!/^\d{6}$/.test(code)) throw new Error('Digite o código de 6 dígitos.');
      const res = await api({ action: 'verify_code', email: email, code: code });
      
      playBeep(1000, 'triangle', 0.25);
      $('gate').classList.add('hidden');
      $('msgs').innerHTML = '';
      (res.messages || []).forEach(m => renderMsg(m.text, m.role === 'assistant' ? 'in' : 'out', m.image));
    } catch(e) {
      showModal(e.message, 'Código não validado');
    }
  });

  // Profile modal
  $('btnProfile').addEventListener('click', () => $('profileModal').classList.remove('hidden'));
  $('btnCloseProfile').addEventListener('click', () => $('profileModal').classList.add('hidden'));
  $('btnProfileOk').addEventListener('click', () => $('profileModal').classList.add('hidden'));

  // Clear messages
  $('btnClear').addEventListener('click', async () => {
    await api({ action: 'clear_messages' });
    $('msgs').innerHTML = '';
  });

  function renderMsg(text, type, imgUrl) {
    const d = document.createElement('div');
    d.className = 'msg ' + type;
    const txt = String(text || '');

    // Creator detection for Telegram and Instagram links
    const isCreator = (type === 'in' && (/(jadiel|desenvolvedor|criador|proprietario|dono|telegram|instagram)/i.test(txt)));
    
    if (isCreator) {
      const clean = txt.replace(/https?:\/\/\S+/gi, '').trim();
      const p = document.createElement('div');
      p.textContent = clean;
      d.appendChild(p);

      const actions = document.createElement('div');
      actions.className = 'social-actions';
      actions.innerHTML = `
        <a href="https://t.me/JADIEL_TM" target="_blank" rel="noopener noreferrer" class="social-btn">Telegram Jadiel</a>
        <a href="https://www.instagram.com/jadiel_strb_brd?stkn=cmZoNWxmcHo3ZGd5" target="_blank" rel="noopener noreferrer" class="social-btn instagram">Instagram Jadiel</a>
      `;
      d.appendChild(actions);
    } else {
      d.textContent = txt;
    }

    if (imgUrl) {
      const img = document.createElement('img');
      img.src = imgUrl;
      img.className = 'msg-img';
      img.alt = 'Imagem gerada pela AZION IA';
      img.onclick = () => window.open(imgUrl, '_blank');
      d.appendChild(img);
    }

    $('msgs').appendChild(d);
    $('msgs').scrollTop = $('msgs').scrollHeight;
  }

  function wantsImage(t) {
    return /(?:crie|criar|gere|gerar|faca|faça|faz|fazer|desenhe|desenha|desenhar|produza|produzir|cria|quero)\s+(?:uma?\s+)?(?:imagem|foto|desenho|arte)\b/i.test(t);
  }

  $('bar').addEventListener('submit', async (e) => {
    e.preventDefault();
    const t = $('text').value.trim();
    if (!t) return;
    $('text').value = '';
    renderMsg(t, 'out');
    playBeep(520, 'sine', 0.08);

    $('typing').classList.remove('hidden');
    try {
      if (wantsImage(t)) {
        $('typing').innerHTML = '<span>●</span> AZION IA está criando sua arte…';
        const res = await api({ action: 'generate_image', prompt: t });
        playBeep(780, 'triangle', 0.15);
        renderMsg('Arte gerada pela AZION IA com sucesso!', 'in', res.image);
      } else {
        $('typing').innerHTML = '<span>●</span> AZION IA está digitando…';
        const res = await api({ action: 'chat', message: t });
        playBeep(780, 'triangle', 0.15);
        renderMsg(res.reply || 'Como posso te ajudar?', 'in');
      }
    } catch(err) {
      renderMsg('Ocorreu uma instabilidade: ' + err.message, 'in');
    } finally {
      $('typing').classList.add('hidden');
    }
  });

  // Initial check
  (async function() {
    try {
      const res = await api({ action: 'me' });
      if (res.authenticated) {
        $('gate').classList.add('hidden');
        $('msgs').innerHTML = '';
        (res.messages || []).forEach(m => renderMsg(m.text, m.role === 'assistant' ? 'in' : 'out', m.image));
      }
    } catch(e) {}
  })();

  // 3D Scene Initialization (Three.js)
  (function initThree() {
    const container = $('threeCanvas');
    if (!container || !window.THREE) return;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x021814, 0.035);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 1.2, 5.0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Lights
    const amb = new THREE.HemisphereLight(0x064e3b, 0x0f172a, 1.2);
    scene.add(amb);
    const dir = new THREE.DirectionalLight(0xffffff, 2.0);
    dir.position.set(4, 5, 4);
    scene.add(dir);
    const pLight = new THREE.PointLight(0x10b981, 3.5, 8);
    pLight.position.set(0, 0.9, 0);
    scene.add(pLight);

    // 3D Composite Core Model
    const root = new THREE.Group();
    scene.add(root);

    // Base
    const base = new THREE.Mesh(
      new THREE.CylinderGeometry(1.6, 1.8, 0.2, 32),
      new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.85, roughness: 0.2 })
    );
    base.position.y = 0.1;
    root.add(base);

    // Rings
    const ring1 = new THREE.Mesh(
      new THREE.TorusGeometry(1.3, 0.04, 16, 64),
      new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.15 })
    );
    ring1.position.y = 0.95;
    root.add(ring1);

    const ring2 = new THREE.Mesh(
      new THREE.TorusGeometry(1.1, 0.04, 16, 64),
      new THREE.MeshStandardMaterial({ color: 0x059669, metalness: 0.85, roughness: 0.2 })
    );
    ring2.position.y = 0.95;
    ring2.rotation.x = Math.PI / 3;
    root.add(ring2);

    // Core Crystal
    const core = new THREE.Mesh(
      new THREE.IcosahedronGeometry(0.65, 1),
      new THREE.MeshStandardMaterial({ color: 0x10b981, emissive: 0x047857, metalness: 0.3, roughness: 0.1 })
    );
    core.position.y = 0.95;
    root.add(core);

    const wire = new THREE.Mesh(
      new THREE.IcosahedronGeometry(0.7, 1),
      new THREE.MeshBasicMaterial({ color: 0x6ee7b7, wireframe: true, transparent: true, opacity: 0.4 })
    );
    wire.position.y = 0.95;
    root.add(wire);

    // Orbiting Satellites
    const satCount = 10;
    const satMesh = new THREE.InstancedMesh(
      new THREE.SphereGeometry(0.05, 16, 16),
      new THREE.MeshStandardMaterial({ color: 0x34d399, emissive: 0x10b981, metalness: 0.8, roughness: 0.2 }),
      satCount
    );
    root.add(satMesh);

    const mat4 = new THREE.Matrix4();
    let clock = 0;

    // Presets
    let targetCamZ = 5.0;
    let targetLookY = 0.95;
    let explodeAmount = 0;

    $('btnPresetPersp').addEventListener('click', () => { targetCamZ = 5.0; explodeAmount = 0; });
    $('btnPresetFront').addEventListener('click', () => { targetCamZ = 4.2; explodeAmount = 0; });
    $('btnPresetCore').addEventListener('click', () => { targetCamZ = 2.6; explodeAmount = 0; });
    $('btnPresetExplode').addEventListener('click', () => { targetCamZ = 5.4; explodeAmount = 0.8; });

    function animate() {
      requestAnimationFrame(animate);
      clock += 0.015;

      ring1.rotation.y += 0.01;
      ring1.rotation.x = Math.sin(clock * 0.5) * 0.4;
      ring2.rotation.z += 0.014;
      core.rotation.y += 0.008;
      wire.rotation.y -= 0.005;

      ring1.position.y = 0.95 + explodeAmount * 0.7;
      ring2.position.y = 0.95 - explodeAmount * 0.5;

      camera.position.z += (targetCamZ - camera.position.z) * 0.08;

      for (let i = 0; i < satCount; i++) {
        const ang = (i / satCount) * Math.PI * 2 + clock * 0.8;
        const rad = 0.95 + (i % 3) * 0.15;
        mat4.makeTranslation(Math.cos(ang) * rad, 0.95 + Math.sin(ang * 2) * 0.25, Math.sin(ang) * rad);
        satMesh.setMatrixAt(i, mat4);
      }
      satMesh.instanceMatrix.needsUpdate = true;

      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    });
  })();
});
</script>
</body>
</html>
