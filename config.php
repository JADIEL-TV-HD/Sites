<?php
const GEMINI_API_KEYS=[
 'COLE_SUA_CHAVE_GEMINI_01',
 'COLE_SUA_CHAVE_GEMINI_02',
 'COLE_SUA_CHAVE_GEMINI_03',
 'COLE_SUA_CHAVE_GEMINI_04',
 'COLE_SUA_CHAVE_GEMINI_05',
 'COLE_SUA_CHAVE_GEMINI_06',
 'COLE_SUA_CHAVE_GEMINI_07',
 'COLE_SUA_CHAVE_GEMINI_08',
 'COLE_SUA_CHAVE_GEMINI_09',
 'COLE_SUA_CHAVE_GEMINI_10'
];
const GEMINI_MODEL='gemini-2.5-flash';
const ADMIN_USER='admin';
const ADMIN_PASSWORD='TROQUE_ESTA_SENHA';
const DATA_FILE=__DIR__.'/data.json';
const SMTP_HOST='smtp.gmail.com';
const SMTP_PORT=587;
const SMTP_USER='inovatechinsights@gmail.com';
const SMTP_APP_PASSWORD='COLE_AQUI_A_SENHA_DE_APP_DO_GMAIL';
const MAIL_FROM_NAME='AZION IA';
const CODE_TTL=600;
const MAX_CODE_ATTEMPTS=5;
const RATE_LIMIT_WINDOW=300;
date_default_timezone_set('America/Bahia');

if(session_status()===PHP_SESSION_NONE){
 session_name('AZIONSESSID');
 session_set_cookie_params(['lifetime'=>2592000,'path'=>'/','secure'=>!empty($_SERVER['HTTPS'])&&$_SERVER['HTTPS']!=='off','httponly'=>true,'samesite'=>'Lax']);
 session_start();
}
header_remove('X-Powered-By');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('Referrer-Policy: strict-origin-when-cross-origin');
header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
header("Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'; form-action 'self';");
if(!empty($_SERVER['HTTPS'])&&$_SERVER['HTTPS']!=='off') header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
