<?php
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
$base=__DIR__.'/data';
if(!is_dir($base)) @mkdir($base,0755,true);
$ht=$base.'/.htaccess';
if(!file_exists($ht)) @file_put_contents($ht,"Require all denied\nDeny from all\n");
function out(array $x):never{echo json_encode($x,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);exit;}
function safe(string $s):string{$s=preg_replace('/[^a-zA-Z0-9_\- ]/u','',$s)??'';return trim(mb_substr($s,0,60));}
function validFiles($f):array{
  if(!is_array($f)) return [];
  $r=[];
  foreach(['html','css','js'] as $k){
    if(isset($f[$k]) && is_string($f[$k])) $r[$k]=mb_substr($f[$k],0,500000);
  }
  return $r;
}
$method=$_SERVER['REQUEST_METHOD']??'GET';
if($method==='GET'){
  $action=$_GET['action']??'list';
  if($action==='list'){
    $items=[];
    foreach(glob($base.'/*.json')?:[] as $f){$j=json_decode((string)@file_get_contents($f),true);if(is_array($j)&&isset($j['name']))$items[]=$j['name'];}
    sort($items,SORT_NATURAL|SORT_FLAG_CASE);out(['ok'=>true,'projects'=>$items]);
  }
  if($action==='load'){
    $name=safe((string)($_GET['name']??''));if($name==='')out(['ok'=>false,'error'=>'Nome inválido']);
    $file=$base.'/'.hash('sha256',$name).'.json';if(!is_file($file))out(['ok'=>false,'error'=>'Projeto não encontrado']);
    $j=json_decode((string)file_get_contents($file),true);if(!is_array($j))out(['ok'=>false,'error'=>'Projeto inválido']);
    out(['ok'=>true,'name'=>$j['name'],'files'=>validFiles($j['files']??[])]);
  }
  out(['ok'=>false,'error'=>'Ação inválida']);
}
if($method==='POST'){
  $body=json_decode((string)file_get_contents('php://input'),true);
  if(!is_array($body))out(['ok'=>false,'error'=>'JSON inválido']);
  if(($body['action']??'')==='save'){
    $name=safe((string)($body['name']??'Meu projeto'));if($name==='')$name='Meu projeto';
    $files=validFiles($body['files']??[]);if(!$files)out(['ok'=>false,'error'=>'Nenhum código recebido']);
    $data=['name'=>$name,'updated_at'=>date('c'),'files'=>$files];
    $file=$base.'/'.hash('sha256',$name).'.json';
    if(@file_put_contents($file,json_encode($data,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),LOCK_EX)===false)out(['ok'=>false,'error'=>'Não foi possível gravar. Verifique a permissão da pasta data.']);
    out(['ok'=>true]);
  }
  out(['ok'=>false,'error'=>'Ação inválida']);
}
out(['ok'=>false,'error'=>'Método não permitido']);