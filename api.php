<?php
header('Content-Type: application/json; charset=utf-8');
if($_SERVER['REQUEST_METHOD']!=='POST'){http_response_code(405);echo json_encode(['error'=>'Método não permitido']);exit;}
$in=json_decode(file_get_contents('php://input'),true);
if(isset($in['action'])&&$in['action']==='vote'){
 $f=__DIR__.'/data/poll_votes.json';$votes=is_file($f)?(json_decode(@file_get_contents($f),true)?:[]):[];$option=trim($in['option']??'');$key=hash('sha256',($_SERVER['REMOTE_ADDR']??'').'|'.date('Y-m-d').'|'.($in['poll']??''));
 if($option===''){http_response_code(400);echo json_encode(['error'=>'Opção inválida']);exit;}
 $votes[$key]=['option'=>$option,'at'=>date('c')];file_put_contents($f,json_encode($votes,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE),LOCK_EX);echo json_encode(['ok'=>true]);exit;
}
$url=trim($in['url']??'');
if(!filter_var($url,FILTER_VALIDATE_URL)||!preg_match('~^https?://~i',$url)){http_response_code(400);echo json_encode(['error'=>'Informe uma URL HTTP/HTTPS válida.']);exit;}
$p=parse_url($url);$host=$p['host']??'';$domain=preg_replace('/^www\./i','',$host);
if(!$domain){http_response_code(400);echo json_encode(['error'=>'Domínio inválido.']);exit;}
$dns=dns_get_record($domain,DNS_A|DNS_AAAA);$dnsOk=!empty($dns);$status=null;$server='';$title='';$final=$url;$https=(strtolower($p['scheme']??'')==='https');$tls=false;$err='';
$ch=curl_init($url);curl_setopt_array($ch,[CURLOPT_RETURNTRANSFER=>true,CURLOPT_FOLLOWLOCATION=>true,CURLOPT_MAXREDIRS=>5,CURLOPT_CONNECTTIMEOUT=>8,CURLOPT_TIMEOUT=>15,CURLOPT_USERAGENT=>'JADIEL-CHECK/1.0',CURLOPT_HEADER=>false, CURLOPT_SSL_VERIFYPEER=>true, CURLOPT_SSL_VERIFYHOST=>2]);
$html=curl_exec($ch);if($html!==false){$status=curl_getinfo($ch,CURLINFO_HTTP_CODE);$final=curl_getinfo($ch,CURLINFO_EFFECTIVE_URL)?:$url;$server=curl_getinfo($ch,CURLINFO_PRIMARY_IP)?:'';$tls=$https&&curl_getinfo($ch,CURLINFO_SSL_VERIFYRESULT)===0;if(preg_match('/<title[^>]*>(.*?)<\/title>/is',$html,$m))$title=trim(html_entity_decode(strip_tags($m[1]),ENT_QUOTES|ENT_HTML5,'UTF-8'));}else{$err=curl_error($ch);}curl_close($ch);
$cfgFile=__DIR__.'/data/settings.json';$cfg=is_file($cfgFile)?json_decode(@file_get_contents($cfgFile),true):[];$vtKey=trim($cfg['virustotal_api_key']??'');$rep=['status'=>'Não consultada','details'=>'Nenhuma chave de reputação foi configurada no gestor.'];$vt=[];
if($vtKey){$id=rtrim(strtr(base64_encode($url),'+/','-_'),'=');$ch=curl_init('https://www.virustotal.com/api/v3/urls/'.$id);curl_setopt_array($ch,[CURLOPT_RETURNTRANSFER=>true,CURLOPT_TIMEOUT=>12,CURLOPT_HTTPHEADER=>['accept: application/json','x-apikey: '.$vtKey]]);$body=curl_exec($ch);$code=curl_getinfo($ch,CURLINFO_HTTP_CODE);curl_close($ch);if($code===200&&$body){$j=json_decode($body,true);$a=$j['data']['attributes']??[];$st=$a['last_analysis_stats']??[];$mal=(int)($st['malicious']??0);$sus=(int)($st['suspicious']??0);$har=(int)($st['harmless']??0);$und=(int)($st['undetected']??0);$rep['status']=($mal>0?'Detecções encontradas':($sus>0?'Sinais suspeitos':'Sem detecções nas análises disponíveis'));$rep['details']="VirusTotal: {$mal} maliciosas, {$sus} suspeitas, {$har} benignas e {$und} não detectadas na última análise disponível."; }else{$rep['status']='Falha na consulta';$rep['details']='A consulta ao provedor de reputação não retornou um relatório válido.';}}
echo json_encode(['domain'=>$domain,'site'=>['title'=>$title?:$domain],'http'=>['status'=>$status,'server'=>$server,'final_url'=>$final,'error'=>$err],'dns'=>['resolved'=>$dnsOk,'records'=>$dns],'security'=>['https'=>$https,'tls'=>$tls],'reputation'=>$rep,'checked_at'=>date('d/m/Y H:i:s')],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
