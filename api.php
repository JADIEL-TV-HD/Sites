<?php
require_once __DIR__.'/config.php';
header('Content-Type: application/json; charset=utf-8');
if($_SERVER['REQUEST_METHOD']!=='POST'){http_response_code(405);echo json_encode(['ok'=>false,'error'=>'Método não permitido']);exit;}
$action=$_GET['action']??'';$body=json_decode(file_get_contents('php://input'),true)?:[];
if($action==='order'){
  $products=read_json('products.json',[]);$items=$body['items']??[];$byId=[];foreach($products as $p)$byId[$p['id']]=$p;
  if(!$body['name']||!filter_var($body['email'],FILTER_VALIDATE_EMAIL)||!$body['phone']||!$body['address']||!is_array($items)){http_response_code(422);echo json_encode(['ok'=>false,'error'=>'Dados do pedido inválidos']);exit;}
  $clean=[];$total=0;
  foreach($items as $i){$id=(string)($i['id']??'');$q=max(1,min(99,(int)($i['qty']??0)));if(!$q||!isset($byId[$id]))continue;$p=$byId[$id];if(empty($p['active']))continue;$line=$p['price']*$q;$total+=$line;$clean[]=['product_id'=>$id,'name'=>$p['name'],'qty'=>$q,'unit_price'=>$p['price'],'supplier'=>$p['supplier']??''];}
  if(!$clean){http_response_code(422);echo json_encode(['ok'=>false,'error'=>'Nenhum produto válido no pedido']);exit;}
  $orders=read_json('orders.json',[]);$id='JAD-'.date('Ymd').'-'.strtoupper(substr(bin2hex(random_bytes(4)),0,8));$orders[]=['id'=>$id,'created_at'=>date('c'),'customer'=>['name'=>trim($body['name']),'email'=>trim($body['email']),'phone'=>trim($body['phone']),'address'=>trim($body['address'])],'items'=>$clean,'total'=>$total,'payment_status'=>'pending','fulfillment_status'=>'new'];write_json('orders.json',$orders);echo json_encode(['ok'=>true,'order_id'=>$id,'message'=>'Pedido recebido. Aguarde a confirmação do pagamento e as instruções de envio.']);exit;
}
http_response_code(404);echo json_encode(['ok'=>false,'error'=>'Ação não encontrada']);