<?php
require __DIR__.'/config.php';
ini_set('display_errors','0');
header('Content-Type: application/json; charset=utf-8');
register_shutdown_function(function(){
  $e=error_get_last();
  if($e && in_array($e['type'],[E_ERROR,E_PARSE,E_CORE_ERROR,E_COMPILE_ERROR],true)){
    if(!headers_sent())header('Content-Type: application/json; charset=utf-8');
    http_response_code(500);
    echo json_encode(['error'=>'Erro interno no servidor. Verifique a configuração do AZION IA.'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  }
});
set_exception_handler(function($e){
  http_response_code(500);
  echo json_encode(['error'=>'Erro interno no servidor. Verifique a configuração do AZION IA.'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  exit;
});
function out($x,$s=200){http_response_code($s);echo json_encode($x,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);exit;}
function ip(){return $_SERVER['REMOTE_ADDR']??'unknown';}
function rate($key,$limit,$window=RATE_LIMIT_WINDOW){
  $tmp=function_exists('sys_get_temp_dir')?sys_get_temp_dir():__DIR__;
  $f=$tmp.'/azion_rl_'.hash('sha256',$key);$now=time();
  $x=json_decode(@file_get_contents($f),true)?:['t'=>$now,'n'=>0];
  if($now-$x['t']>$window)$x=['t'=>$now,'n'=>0];
  $x['n']++;@file_put_contents($f,json_encode($x),LOCK_EX);
  if($x['n']>$limit)out(['error'=>'Muitas tentativas. Aguarde alguns minutos e tente novamente.'],429);
}
function csrf(){if(empty($_SESSION['csrf']))$_SESSION['csrf']=bin2hex(random_bytes(32));return $_SESSION['csrf'];}
function require_csrf($token){if(!hash_equals(csrf(),(string)$token))out(['error'=>'Sessão de segurança inválida. Recarregue a página.'],403);}
function clean($x,$n=4000){$x=trim((string)$x);return function_exists('mb_substr')?mb_substr($x,0,$n):substr($x,0,$n);}
function plain_ai($x){return trim(str_replace(['**','__','`','*'],'',$x));}
function client_banned($client){return !empty($client['banned']);}
function db(){
  $x=json_decode(@file_get_contents(DATA_FILE),true);
  return is_array($x)?$x:['knowledge'=>[],'clients'=>[],'conversations'=>[],'verifications'=>[]];
}
function save($d){
  $json=json_encode($d,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT);
  return $json!==false&&@file_put_contents(DATA_FILE,$json,LOCK_EX)!==false;
}
function email_ok($e){return filter_var($e,FILTER_VALIDATE_EMAIL)!==false;}

function smtp_send($to,$code){
  if(!function_exists('stream_socket_client')||!function_exists('stream_socket_enable_crypto'))return false;
  $pwd=str_replace(' ','',trim(SMTP_APP_PASSWORD));
  if(!$pwd||substr($pwd,0,5)==='COLE_')return false;
  $fp=@stream_socket_client('tcp://'.SMTP_HOST.':'.SMTP_PORT,$errno,$errstr,20);
  if(!$fp)return false;
  stream_set_timeout($fp,20);
  $read=function()use($fp){
    $out='';
    while(($line=fgets($fp,4096))!==false){$out.=$line;if(strlen($line)<4||$line[3]===' ')break;}
    return $out;
  };
  $expect=function($codes)use($read){
    $r=$read();
    foreach((array)$codes as $code)if(substr($r,0,strlen((string)$code))===(string)$code)return true;
    return false;
  };
  $send=function($s)use($fp){return @fwrite($fp,$s."\r\n")!==false;};
  if(!$expect(220)){fclose($fp);return false;}
  $send('EHLO azion.local');if(!$expect(250)){fclose($fp);return false;}
  $send('STARTTLS');if(!$expect(220)){fclose($fp);return false;}
  if(!@stream_socket_enable_crypto($fp,true,STREAM_CRYPTO_METHOD_TLS_CLIENT)){fclose($fp);return false;}
  $send('EHLO azion.local');if(!$expect(250)){fclose($fp);return false;}
  $send('AUTH LOGIN');if(!$expect(334)){fclose($fp);return false;}
  $send(base64_encode(SMTP_USER));if(!$expect(334)){fclose($fp);return false;}
  $send(base64_encode($pwd));if(!$expect(235)){fclose($fp);return false;}
  $send('MAIL FROM:<'.SMTP_USER.'>');if(!$expect(250)){fclose($fp);return false;}
  $send('RCPT TO:<'.$to.'>');if(!$expect([250,251])){fclose($fp);return false;}
  $send('DATA');if(!$expect(354)){fclose($fp);return false;}
  $body="From: ".MAIL_FROM_NAME." <".SMTP_USER.">\r\n".
        "To: <".$to.">\r\n".
        "Subject: Seu código de verificação • AZION IA\r\n".
        "MIME-Version: 1.0\r\n".
        "Content-Type: text/html; charset=UTF-8\r\n\r\n".
        "<!doctype html><html><body style='margin:0;padding:0;background:#f2f6f5;font-family:Arial,Helvetica,sans-serif;color:#17332f'><table width='100%' cellpadding='0' cellspacing='0' style='background:#f2f6f5;padding:36px 12px'><tr><td align='center'><table width='100%' cellpadding='0' cellspacing='0' style='max-width:560px;background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.10)'><tr><td style='background:#075e54;padding:30px;text-align:center;color:#fff'><div style='font-size:28px;font-weight:800'>AZION IA</div><div style='margin-top:7px;font-size:14px'>Atendimento inteligente e seguro</div></td></tr><tr><td style='padding:34px 32px;text-align:center'><div style='font-size:15px;color:#60716d;margin-bottom:10px'>Seu código de verificação é</div><div style='display:inline-block;background:#edf8f4;border:1px solid #cceee2;border-radius:16px;padding:18px 26px;font-size:38px;font-weight:800;letter-spacing:9px;color:#075e54'>".$code."</div><p style='font-size:15px;line-height:1.6;color:#52635f;margin:24px 0 8px'>Digite este código no AZION IA para confirmar seu e-mail e continuar.</p><p style='font-size:13px;color:#8a9995;margin:0'>Este código expira em ".(int)(CODE_TTL/60)." minutos.</p></td></tr><tr><td style='padding:20px 32px;background:#f8faf9;text-align:center;font-size:12px;color:#7b8985;line-height:1.6'>Se você não solicitou este código, ignore este e-mail.<br>Nunca compartilhe seu código com ninguém.<br><strong style='color:#075e54'>AZION IA • JADIEL</strong></td></tr></table></td></tr></table></body></html>\r\n";
  $body=preg_replace('/^\./m','..',$body);
  $send($body.'.');if(!$expect(250)){fclose($fp);return false;}
  $send('QUIT');$read();fclose($fp);return true;
}
function code_send($to,$code){
  if(smtp_send($to,$code))return true;
  if(!function_exists('mail'))return false;
  $subject='Seu código de verificação • AZION IA';
  $headers="From: ".MAIL_FROM_NAME." <".SMTP_USER.">\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=UTF-8\r\n";
  $html="<!doctype html><html><body style='margin:0;padding:0;background:#f2f6f5;font-family:Arial,Helvetica,sans-serif;color:#17332f'><table width='100%' cellpadding='0' cellspacing='0' style='background:#f2f6f5;padding:36px 12px'><tr><td align='center'><table width='100%' cellpadding='0' cellspacing='0' style='max-width:560px;background:#fff;border-radius:24px;overflow:hidden'><tr><td style='background:#075e54;padding:30px;text-align:center;color:#fff'><div style='font-size:28px;font-weight:800'>AZION IA</div><div style='margin-top:7px;font-size:14px'>Atendimento inteligente e seguro</div></td></tr><tr><td style='padding:34px 32px;text-align:center'><div style='font-size:15px;color:#60716d;margin-bottom:10px'>Seu código de verificação é</div><div style='display:inline-block;background:#edf8f4;border:1px solid #cceee2;border-radius:16px;padding:18px 26px;font-size:38px;font-weight:800;letter-spacing:9px;color:#075e54'>".$code."</div><p style='font-size:15px;line-height:1.6;color:#52635f;margin:24px 0 8px'>Digite este código no AZION IA para confirmar seu e-mail e continuar.</p><p style='font-size:13px;color:#8a9995'>Este código expira em ".(int)(CODE_TTL/60)." minutos.</p></td></tr><tr><td style='padding:20px 32px;background:#f8faf9;text-align:center;font-size:12px;color:#7b8985;line-height:1.6'>Se você não solicitou este código, ignore este e-mail.<br>Nunca compartilhe seu código com ninguém.<br><strong style='color:#075e54'>AZION IA • JADIEL</strong></td></tr></table></td></tr></table></body></html>";
  return @mail($to,$subject,$html,$headers);
}
function create_code($d,$email,$client=[]){
  $code=(string)random_int(100000,999999);
  $d['verifications'][]=['id'=>bin2hex(random_bytes(8)),'email'=>$email,'hash'=>password_hash($code,PASSWORD_DEFAULT),'client'=>$client,'expires'=>time()+CODE_TTL,'attempts'=>0,'used'=>false];
  while(count($d['verifications'])>100)$d['verifications']=array_slice($d['verifications'],-100);
  if(!code_send($email,$code))return [false,$d];
  save($d);return [true,$d];
}
function groq_http($url,$payload,$timeout=60){
  $json=is_string($payload)?$payload:json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  if($json===false)return [0,false,'Não foi possível preparar a solicitação.'];
  $token=trim((string)GROQ_API_KEY);
  if($token===''||strpos($token,'COLE_')===0)return [0,false,'O token da Groq ainda não foi configurado no servidor.'];
  $headers=['Content-Type: application/json','Authorization: Bearer '.$token];
  if(function_exists('curl_init')){
    $ch=curl_init($url);
    curl_setopt_array($ch,[CURLOPT_POST=>1,CURLOPT_RETURNTRANSFER=>1,CURLOPT_CONNECTTIMEOUT=>15,CURLOPT_TIMEOUT=>$timeout,CURLOPT_HTTPHEADER=>$headers,CURLOPT_POSTFIELDS=>$json]);
    $body=curl_exec($ch);$status=(int)curl_getinfo($ch,CURLINFO_HTTP_CODE);$err=curl_error($ch);curl_close($ch);
    if($body!==false)return [$status,$body,''];
    return [0,false,$err?:'Falha na conexão HTTPS.'];
  }
  $ctx=stream_context_create(['http'=>['method'=>'POST','header'=>implode("\r\n",$headers)."\r\n",'content'=>$json,'timeout'=>$timeout,'ignore_errors'=>true]]);
  $body=@file_get_contents($url,false,$ctx);$status=0;
  if(isset($http_response_header[0])&&preg_match('/\s(\d{3})\s/',$http_response_header[0],$m))$status=(int)$m[1];
  if($body!==false)return [$status,$body,''];
  return [0,false,'A hospedagem não conseguiu conectar à API da Groq.'];
}
function generate_image_groq($prompt){
  return ['error'=>'A API da Groq usada pela AZION IA gera respostas de texto, mas não cria arquivos de imagem. A geração de imagens exige outro serviço de IA.'];
}
function groq_chat($history,$knowledge,$client){
  $token=trim((string)GROQ_API_KEY);
  if($token===''||strpos($token,'COLE_')===0)return ['error'=>'O token da Groq ainda não foi configurado no servidor.'];
  $kb='';foreach($knowledge as $k)$kb.="\n### ".clean($k['title'],200)."\n".clean($k['content'],7000);
  $sys="Você é AZION IA, uma assistente de inteligência artificial avançada, competente, confiável, profissional e natural. Seu objetivo é entender o que a pessoa realmente precisa e entregar a melhor resposta possível. Você pode pesquisar na web em tempo real usando a ferramenta browser_search disponibilizada pela Groq.\\n\\nCOMPORTAMENTO E INTELIGÊNCIA:\\n- Responda em português brasileiro por padrão; acompanhe o idioma do usuário quando ele escrever em outro idioma. Entenda gírias, abreviações, erros de digitação e mensagens curtas pelo contexto.\\n- Identifique a intenção e responda diretamente. Use o histórico recente para manter continuidade e não faça a pessoa repetir informações já fornecidas.\\n- Explique assuntos complexos de forma organizada, com exemplos concretos e etapas práticas. Em programação, ofereça soluções coerentes, código funcional quando solicitado e indique onde aplicar mudanças.\\n- Em matemática, confira os cálculos. Diferencie fatos de estimativas. Se não souber ou não tiver dados suficientes, diga isso com honestidade e faça uma pergunta objetiva quando necessário.\\n- PESQUISA NA WEB EM TEMPO REAL: para notícias, acontecimentos de hoje, resultados esportivos, preços, versões atuais, leis/regras recentes, pessoas/empresas atuais ou quando o usuário pedir para pesquisar/buscar na internet, use a ferramenta browser_search. Baseie a resposta nos resultados retornados, priorize fontes confiáveis e recentes, informe datas quando relevante e inclua URLs das fontes quando disponíveis. Se a busca falhar ou não trouxer dados suficientes, diga isso claramente. Para perguntas estáveis e simples, responda diretamente sem pesquisar desnecessariamente. Não afirme que pesquisou se a ferramenta não foi usada. Não invente notícias, fontes, funcionalidades ou resultados.\\n- Seja conversacional, educada e útil, sem repetir a pergunta, sem respostas genéricas e sem excesso de formalidade. Ajuste o tamanho da resposta à necessidade.\\n- Use títulos e listas quando ajudarem, mas não mostre asteriscos ou marcação Markdown crua.\\n- Nunca solicite nem revele senhas, tokens, códigos de verificação ou dados financeiros sensíveis. Proteja a privacidade.\\n- Esta integração usa a API de conversa da Groq e não possui geração de imagens habilitada. Não finja que criou arquivos de imagem nem prometa ferramentas indisponíveis.\\n\\nIDENTIDADE E REDES SOCIAIS — REGRA IMPORTANTE:\\n- JADIEL é o desenvolvedor e proprietário oficial da AZION IA e responsável pela JDL PROGRAMING. Não invente outras informações biográficas.\\n- SOMENTE quando a pessoa perguntar quem é o dono, criador ou desenvolvedor da AZION IA, quem é JADIEL, quem criou o sistema, ou fizer pergunta claramente relacionada ao responsável pela AZION IA/JDL PROGRAMING, responda com essa informação e inclua os dois links oficiais: Telegram https://t.me/JADIEL_TM e Instagram https://www.instagram.com/jadiel_strb_brd?stkn=cmZoNWxmcHo3ZGd5.\\n- Não ofereça nem mencione esses links em respostas comuns, saudações, dúvidas técnicas ou assuntos sem relação com o dono/desenvolvedor. Não transforme perguntas comuns em divulgação.\\n- Data e hora do servidor: ".date('d/m/Y H:i:s')." (fuso America/Bahia).\\nCLIENTE: ".json_encode($client,JSON_UNESCAPED_UNICODE)."\\nBASE DE CONHECIMENTO:\\n".$kb;
  $messages=[['role'=>'system','content'=>$sys]];
  foreach(array_slice($history,-12) as $m)$messages[]=['role'=>$m['role']==='assistant'?'assistant':'user','content'=>clean($m['text'],8000)];
  $payload=['model'=>GROQ_CHAT_MODEL,'messages'=>$messages,'temperature'=>0.25,'max_tokens'=>1800,'stream'=>false,'tools'=>[['type'=>'browser_search']],'tool_choice'=>'auto'];
  [$status,$body,$err]=groq_http('https://api.groq.com/openai/v1/chat/completions',$payload,60);
  $j=json_decode($body?:'',true);
  if($status>=200&&$status<300){
    $text=$j['choices'][0]['message']['content']??'';
    if(is_array($text))$text=json_encode($text,JSON_UNESCAPED_UNICODE);
    if(trim((string)$text)!=='')return ['text'=>plain_ai($text)];
  }
  if($status===401||$status===403)return ['error'=>'A Groq recusou o token. Confira se ele está correto e ativo.'];
  if($status===402)return ['error'=>'A Groq informou que a conta não pode processar esta solicitação. Confira o painel da Groq.'];
  if($status===429)return ['error'=>'A Groq atingiu o limite de solicitações ou tokens da conta. Aguarde e tente novamente.'];
  if($status===404)return ['error'=>'O modelo de conversa configurado não está disponível.'];
  return ['error'=>'Não foi possível obter uma resposta da Groq neste momento'.($status?' (HTTP '.$status.')':'').'. Tente novamente em instantes.'];
}
$d=db();
$raw=file_get_contents('php://input');
$in=json_decode($raw?:'',true);
if(!is_array($in))$in=is_array($_POST)?$_POST:[];
$a=isset($in['action'])?(string)$in['action']:'';

if($a==='request_code'){
  rate('code:'.ip().':'.strtolower(clean($in['email']??'',160)),5,900);
  $email=strtolower(clean($in['email']??'',160));$mode=$in['mode']??'existing';
  if(!email_ok($email))out(['error'=>'Informe um e-mail válido.'],422);
  $client=['name'=>clean($in['name']??'',100),'email'=>$email,'phone'=>clean($in['phone']??'',40),'banned'=>false];
  if($mode==='existing'){
    $found=null;foreach($d['clients'] as $c)if(strtolower($c['email']??'')===$email){$found=$c;break;}
    if(!$found)out(['error'=>'Não encontrei uma conta com esse e-mail. Escolha NÃO para criar sua conta.'],404);
    $client=$found;
  }
  [$ok,$d]=create_code($d,$email,$client);
  if(!$ok)out(['error'=>'Não foi possível enviar o código. Verifique a configuração de e-mail no servidor.'],500);
  $_SESSION['verify_email']=$email;out(['ok'=>1,'message'=>'Código enviado para o e-mail informado.']);
}
if($a==='verify_code'){
  rate('verify:'.ip(),12,600);
  $email=strtolower(clean($in['email']??$_SESSION['verify_email']??'',160));$code=clean($in['code']??'',10);
  $idx=-1;foreach($d['verifications'] as $i=>$v)if(!$v['used']&&$v['email']===$email)$idx=$i;
  if($idx<0)out(['error'=>'Código não encontrado. Solicite um novo código.'],400);
  $v=$d['verifications'][$idx];
  if(time()>$v['expires'])out(['error'=>'Código expirado. Solicite outro código.'],400);
  if($v['attempts']>=MAX_CODE_ATTEMPTS)out(['error'=>'Limite de tentativas atingido. Solicite outro código.'],429);
  if(!password_verify($code,$v['hash'])){$d['verifications'][$idx]['attempts']++;save($d);out(['error'=>'Código incorreto.'],401);}
  $d['verifications'][$idx]['used']=true;$client=$v['client'];
  $existing=-1;foreach($d['clients'] as $i=>$c)if(strtolower($c['email']??'')===$email)$existing=$i;
  if($existing>=0)$client=$d['clients'][$existing];else{$client['id']='u_'.bin2hex(random_bytes(8));$client['created_at']=date('c');$d['clients'][]=$client;}
  $cid='c_'.bin2hex(random_bytes(8));$c=['id'=>$cid,'client'=>$client,'status'=>'ia','messages'=>[['role'=>'assistant','text'=>'Olá, '.($client['name']?:'seja bem-vindo').'! Eu sou a AZION IA. Como posso ajudar?','time'=>date('c')]],'updated_at'=>date('c')];
  $d['conversations'][]=$c;save($d);session_regenerate_id(true);$_SESSION['azion_client']=$client['id'];$_SESSION['azion_cid']=$cid;unset($_SESSION['verify_email']);
  out(['ok'=>1,'id'=>$cid,'messages'=>$c['messages']]);
}
if($a==='me'){
  if(empty($_SESSION['azion_client'])||empty($_SESSION['azion_cid']))out(['authenticated'=>false]);
  foreach($d['conversations'] as $cv)if(($cv['id']??'')===$_SESSION['azion_cid']&&($cv['client']['id']??'')===$_SESSION['azion_client']){
    if(!empty($cv['client']['banned'])){session_destroy();out(['authenticated'=>false,'banned'=>true],403);}
    out(['authenticated'=>true,'id'=>$cv['id'],'messages'=>$cv['messages']]);
  }
  session_destroy();out(['authenticated'=>false]);
}
if($a==='generate_image'){
  rate('image:'.ip(),5,300);
  if(empty($_SESSION['azion_client']))out(['error'=>'Faça a verificação por e-mail para acessar o AZION IA.'],401);
  $prompt=clean($in['prompt']??'',1200);
  if($prompt==='')out(['error'=>'Descreva a imagem que deseja criar.'],422);
  $r=generate_image_groq($prompt);
  if(isset($r['error']))out(['error'=>$r['error']],502);
  out(['ok'=>1,'image'=>$r['image'],'prompt'=>$r['prompt']]);
}
if($a==='chat'){
  rate('chat:'.ip(),60,60);
  if(empty($_SESSION['azion_client']))out(['error'=>'Faça a verificação por e-mail para acessar o AZION IA.'],401);
  $text=clean($in['message']??'',4000);$cid=$_SESSION['azion_cid'];
  foreach($d['conversations'] as &$c)if($c['id']===$cid&&($c['client']['id']??'')===$_SESSION['azion_client']){
    if(client_banned($c['client']))out(['reply'=>'Seu acesso ao AZION IA foi banido. Não é possível continuar este atendimento.'],403);
    if($c['status']!=='ia')out(['reply'=>'Seu atendimento está com um atendente humano. Aguarde uma resposta.']);
    $c['messages'][]=['role'=>'user','text'=>$text,'time'=>date('c')];$r=groq_chat($c['messages'],$d['knowledge'],$c['client']);
    if(isset($r['error']))out(['error'=>$r['error']],502);
    $c['messages'][]=['role'=>'assistant','text'=>$r['text'],'time'=>date('c')];$c['updated_at']=date('c');save($d);out(['reply'=>$r['text']]);
  }
  out(['error'=>'Atendimento não encontrado.'],404);
}
if($a==='login'){
  rate('admin:'.ip(),8,900);
  if(($in['user']??'')===ADMIN_USER&&($in['pass']??'')===ADMIN_PASSWORD){session_regenerate_id(true);$_SESSION['admin']=1;out(['ok'=>1,'csrf'=>csrf()]);}
  out(['error'=>'Login inválido.'],401);
}
if(empty($_SESSION['admin']))out(['error'=>'Não autorizado.'],401);
if($_SERVER['REQUEST_METHOD']==='POST'&&$a!=='login')require_csrf($in['csrf']??'');
if($a==='list')out(['conversations'=>$d['conversations'],'csrf'=>csrf()]);
if($a==='clients')out(['clients'=>$d['clients'],'csrf'=>csrf()]);
if($a==='ban'||$a==='unban'){
  $id=clean($in['id']??'',80);$found=false;
  foreach($d['clients'] as &$cl)if(($cl['id']??'')===$id){$cl['banned']=$a==='ban';$found=true;}
  if(!$found)out(['error'=>'Conta não encontrada.'],404);
  foreach($d['conversations'] as &$cv)if(($cv['client']['id']??'')===$id)$cv['client']['banned']=$a==='ban';
  save($d);out(['ok'=>1,'banned'=>$a==='ban']);
}
if($a==='knowledge'){if($_SERVER['REQUEST_METHOD']==='POST'){$d['knowledge']=$in['knowledge']??[];save($d);}out(['knowledge'=>$d['knowledge']]);}
if($a==='take'){foreach($d['conversations'] as &$c)if($c['id']===$in['id'])$c['status']='human';save($d);out(['ok'=>1]);}
if($a==='reply'){foreach($d['conversations'] as &$c)if($c['id']===$in['id']){$c['status']='human';$c['messages'][]=['role'=>'human','text'=>clean($in['message']??''),'time'=>date('c')];}save($d);out(['ok'=>1]);}
out(['error'=>'Ação inválida.'],400);
