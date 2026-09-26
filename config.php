<?php
declare(strict_types=1);
session_start();
const APP_NAME='JADIEL IPTV';
const ADMIN_USER='1234';
const ADMIN_PASS='1234';
const DATA_DIR=__DIR__.'/data';
if(!is_dir(DATA_DIR)) @mkdir(DATA_DIR,0755,true);
function data_read(string $file,array $default=[]):array{$p=DATA_DIR.'/'.$file;if(!is_file($p))return $default;$d=json_decode((string)@file_get_contents($p),true);return is_array($d)?$d:$default;}
function data_write(string $file,array $data):bool{$p=DATA_DIR.'/'.$file;$f=@fopen($p,'c+');if(!$f)return false;flock($f,LOCK_EX);ftruncate($f,0);rewind($f);$ok=fwrite($f,json_encode($data,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));fflush($f);flock($f,LOCK_UN);fclose($f);return $ok!==false;}
function h($v):string{return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function logged():bool{return !empty($_SESSION['iptv_admin']);}
function require_admin():void{if(!logged()){header('Location: index.php');exit;}}
function flash(string $m):void{$_SESSION['flash']=$m;}
function get_flash():string{$m=$_SESSION['flash']??'';unset($_SESSION['flash']);return $m;}
