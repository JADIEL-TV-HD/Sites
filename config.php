<?php
if(session_status()!==PHP_SESSION_ACTIVE) session_start();
define('STORE_NAME','JADIEL SHOP');
define('ADMIN_EMAIL','admin@jadielshop.local');
// Troque este hash por outro gerado com password_hash() antes de publicar.
define('ADMIN_PASSWORD_HASH','$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llCq7hV5WvQq9jZ9q7M6');
define('PIX_KEY','');
define('DATA_DIR',__DIR__.'/data');
if(!is_dir(DATA_DIR)) @mkdir(DATA_DIR,0755,true);
function read_json($file,$default=[]){$path=DATA_DIR.'/'.$file;if(!is_file($path))return $default;$raw=@file_get_contents($path);$data=json_decode($raw,true);return is_array($data)?$data:$default;}
function write_json($file,$data){$path=DATA_DIR.'/'.$file;$fp=@fopen($path,'c+');if(!$fp)return false;flock($fp,LOCK_EX);ftruncate($fp,0);rewind($fp);$ok=fwrite($fp,json_encode($data,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));fflush($fp);flock($fp,LOCK_UN);fclose($fp);return $ok!==false;}
function e($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function admin(){return !empty($_SESSION['admin']);}
