<?php
declare(strict_types=1);header('Content-Type: application/json; charset=utf-8');header('Cache-Control: no-store');require_once __DIR__.'/../config.php';
if($_SERVER['REQUEST_METHOD']!=='POST'){http_response_code(405);echo json_encode(['error'=>'Método não permitido.']);exit;}
$i=json_decode(file_get_contents('php://input')?:'{}',true);$m=trim((string)($i['message']??''));$h=is_array($i['history']??null)?$i['history']:[];
if($m===''){http_response_code(400);echo json_encode(['error'=>'Digite uma pergunta.']);exit;}
if(GEMINI_API_KEY==='COLOQUE_SUA_CHAVE_AQUI'){http_response_code(500);echo json_encode(['error'=>'Coloque sua chave Gemini em config.php.']);exit;}
$c=[];foreach(array_slice($h,-10) as $a){$r=($a['role']??'')==='model'?'model':'user';$t=trim((string)($a['text']??''));if($t!=='')$c[]=['role'=>$r,'parts'=>[['text'=>$t]]];}$c[]=['role'=>'user','parts'=>[['text'=>$m]]];
$body=['contents'=>$c];$url='https://generativelanguage.googleapis.com/v1beta/models/'.rawurlencode(GEMINI_MODEL).':generateContent';
$ch=curl_init($url);curl_setopt_array($ch,[CURLOPT_POST=>true,CURLOPT_RETURNTRANSFER=>true,CURLOPT_HTTPHEADER=>['Content-Type: application/json','X-goog-api-key: '.GEMINI_API_KEY],CURLOPT_POSTFIELDS=>json_encode($body,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),CURLOPT_TIMEOUT=>45]);$res=curl_exec($ch);$code=(int)curl_getinfo($ch,CURLINFO_HTTP_CODE);$err=curl_error($ch);curl_close($ch);
if($res===false){http_response_code(502);echo json_encode(['error'=>'Falha de conexão: '.$err]);exit;}$d=json_decode($res,true);if($code<200||$code>=300){http_response_code(502);echo json_encode(['error'=>$d['error']['message']??'Erro retornado pelo Gemini'],JSON_UNESCAPED_UNICODE);exit;}
$out='';foreach(($d['candidates'][0]['content']['parts']??[]) as $p)if(isset($p['text']))$out.=$p['text'];echo json_encode(['reply'=>$out?:'Não recebi uma resposta.'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);