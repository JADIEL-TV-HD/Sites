import telebot
from telebot import types
import requests
import json
import uuid
import time
import base64
import random
import string
import threading
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import concurrent.futures
import os
import qrcode
from io import BytesIO
import re
import pytz
import atexit

# PDF - importação com fallback seguro
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    PDF_DISPONIVEL = True
except ImportError:
    PDF_DISPONIVEL = False
    print("⚠️ reportlab não instalado - PDF não será gerado. Execute: pip install reportlab")

# ==============================================================================
# ⚙️ CONFIGURAÇÃO - VIVO, CLARO E TIM ENTERPRISE (LAYOUT FINAL)
# ==============================================================================
API_TOKEN = '8601115647:AAFPF6t9p3PVifPX3dkNh4F1276fe_fUGY8'
bot = telebot.TeleBot(API_TOKEN)

# SEU ID DE DONO (ADMIN)
ADMIN_ID = 7605369405 

# CANAL DE BACKUP
BACKUP_CHANNEL_ID = -1003566372959

# IMAGEM DE BOAS-VINDAS
START_IMAGE = "https://jadiel-internet-movel.is-best.net/analise/00.png" 

# UUID PATHS PARA CADA OPERADORA
UUID_PATH_VIVO = "39dd54c0-9ea1-4708-a9c5-5120810b3b72"
UUID_PATH_CLARO = "39dd54c0-9ea1-4708-a9c5-5120810b3b72"
UUID_PATH_TIM = "39dd54c0-9ea1-4708-a9c5-5120810b3b72"

# CONFIGURAÇÕES MERCADO PAGO
MP_ACCESS_TOKEN = "APP_USR-4289641562498463-021520-e378ae01ed7e34ce9b09640b1d037c79-1903970754"
MP_PUBLIC_KEY = "APP_USR-aad0c428-0c22-4ca0-958f-951f7aab639c"
VALOR_LICENCA = 25.00
DIAS_LICENCA = 30

# PONTOS POR VÍDEO
PONTOS_POR_VIDEO_VIVO = 10
PONTOS_POR_VIDEO_CLARO = 10
PONTOS_POR_VIDEO_TIM = 10

# ANTI-BAN
TEMPO_VIDEO_SEGUNDOS = 30

# AFILIADOS - BÔNUS
DIAS_BONUS_AFILIADO = 3

# URL base da API do Mercado Pago
MP_API_URL = "https://api.mercadopago.com/v1"

# LISTA DE ENDPOINTS PARA VIVO
ENDPOINTS_VIVO = [
    "99f9c90a-b13e-419a-b53d-f47f6f2dea35",
    "dbf70686-e31a-11ef-bb8e-0680334bb059",
    "afa4c2d9-0e23-4295-8802-d8df6ed24feb",
    "fb458184-caad-49ed-ba56-ef47a2b491b6",
    "d0397154-6b4c-43d8-9ccb-aaaf3e201edf",
    "2095ea80-2468-43e6-9736-fdeb703a8534",
    "46482b49-a6c5-4a20-bbbe-8f1c45d99c99",
    "5d54c2c3-16bd-4db9-a259-0c879c821873",
    "2b25a088-84ea-11ef-9082-0e639a16be05",
    "ce46818d-e31a-11ef-bb8e-0680334bb059",
    "f9077545-165c-4184-825a-a57459c131dc",
    "dcc45968-df87-403b-8c75-a8c021ec4c8c"
]

ENDPOINTS_CLARO = [
    "2b25a088-84ea-11ef-9082-0e639a16be05",
    "ce46818d-e31a-11ef-bb8e-0680334bb059",
    "f9077545-165c-4184-825a-a57459c131dc",
    "dcc45968-df87-403b-8c75-a8c021ec4c8c"
]

ENDPOINTS_TIM = [
    "bbdef37d-f5c4-4b19-9cfb-ed6e8f43fa2f"
]

HEADERS_FAST_VIVO = {
    "Host": "api.vivofree.com.br",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "X-CHANNEL": "WEB",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://vivofree.com.br",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://vivofree.com.br/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

HEADERS_LOGIN_VIVO = {
    "Host": "api.vivofree.com.br",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": '"Android"',
    "X-CONNECTIVITY": "true",
    "sec-ch-ua-mobile": "?1",
    "X-APP-VERSION": "3.1.10",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
    "X-CHANNEL": "WEB",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://vivofree.com.br",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://vivofree.com.br/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

HEADERS_FAST_CLARO = {
    "Host": "api.prezaofree.com.br",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "X-CHANNEL": "WEB",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://prezaofree.com.br",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://prezaofree.com.br/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

HEADERS_LOGIN_CLARO = {
    "Host": "api.prezaofree.com.br",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": '"Android"',
    "X-CONNECTIVITY": "true",
    "sec-ch-ua-mobile": "?1",
    "X-APP-VERSION": "3.1.10",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
    "X-CHANNEL": "WEB",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://prezaofree.com.br",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://prezaofree.com.br/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

HEADERS_FAST_TIM = {
    "Host": "api.timfun.com.br",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "X-CHANNEL": "WEB",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://timfun.com.br",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://timfun.com.br/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

HEADERS_LOGIN_TIM = {
    "Host": "api.timfun.com.br",
    "Connection": "keep-alive",
    "sec-ch-ua-platform": '"Android"',
    "X-CONNECTIVITY": "true",
    "sec-ch-ua-mobile": "?1",
    "X-APP-VERSION": "3.1.10",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
    "X-CHANNEL": "WEB",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://timfun.com.br",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://timfun.com.br/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# ==============================================================================
# 🛠️ UTILITÁRIOS
# ==============================================================================
def log_terminal(texto):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {texto}")

def get_saudacao():
    tz_brasilia = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz_brasilia)
    hora = agora.hour
    
    if hora < 12:
        return "☀️ Bom dia"
    elif hora < 18:
        return "🌤️ Boa tarde"
    else:
        return "🌙 Boa noite"

def formatar_data(dt):
    if dt is None:
        return "Nunca"
    if not dt.tzinfo:
        tz_brasilia = pytz.timezone('America/Sao_Paulo')
        dt = dt.astimezone(tz_brasilia)
    return dt.strftime("%d/%m/%Y às %H:%M")

def barra_progresso_ultra(atual, total):
    if total == 0:
        return "[░░░░░░░░░░░░░░░░░░░░] 0%"
    pct = atual / total
    cheios = int(20 * pct)
    return f"[{'█'*cheios}{'░'*(20-cheios)}] {int(pct*100)}%"

def extrair_dados_token(token):
    try:
        part = token.split('.')[1]
        part += "=" * ((4 - len(part) % 4) % 4)
        data = json.loads(base64.urlsafe_b64decode(part).decode())
        return data.get("X-WALLET-ID"), data.get("X-USER-ID")
    except: 
        return None, None

def gerar_codigo_cupom(tamanho=8):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(tamanho))

def gerar_qr_code_pix(pix_key):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(pix_key)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        return buffered
    except Exception as e:
        log_terminal(f"Erro ao gerar QR Code: {e}")
        return None

def base64_to_image(base64_string):
    try:
        if 'base64,' in base64_string:
            base64_string = base64_string.split('base64,')[1]
        image_data = base64.b64decode(base64_string)
        buffered = BytesIO(image_data)
        buffered.seek(0)
        return buffered
    except Exception as e:
        log_terminal(f"Erro ao converter base64 para imagem: {e}")
        return None

def get_base_url(operadora):
    if operadora == 'claro':
        return f"https://api.prezaofree.com.br/{UUID_PATH_CLARO}"
    elif operadora == 'tim':
        return f"https://api.timfun.com.br/{UUID_PATH_TIM}"
    else:
        return f"https://api.vivofree.com.br/{UUID_PATH_VIVO}"

def get_headers_fast(operadora):
    if operadora == 'claro':
        return HEADERS_FAST_CLARO.copy()
    elif operadora == 'tim':
        return HEADERS_FAST_TIM.copy()
    else:
        return HEADERS_FAST_VIVO.copy()

def get_headers_login(operadora):
    if operadora == 'claro':
        return HEADERS_LOGIN_CLARO.copy()
    elif operadora == 'tim':
        return HEADERS_LOGIN_TIM.copy()
    else:
        return HEADERS_LOGIN_VIVO.copy()

def get_endpoints(operadora):
    if operadora == 'claro':
        return ENDPOINTS_CLARO
    elif operadora == 'tim':
        return ENDPOINTS_TIM
    else:
        return ENDPOINTS_VIVO

def get_pontos_por_video(operadora):
    if operadora == 'claro':
        return PONTOS_POR_VIDEO_CLARO
    elif operadora == 'tim':
        return PONTOS_POR_VIDEO_TIM
    else:
        return PONTOS_POR_VIDEO_VIVO

# ==============================================================================
# 🔓 SISTEMA DE DESBANIMENTO DE NÚMEROS
# ==============================================================================
def api_desbanir_numero(telefone, operadora='vivo'):
    try:
        if not telefone.startswith('55'):
            if len(telefone) == 11:
                telefone = '55' + telefone
            elif len(telefone) == 9:
                telefone = '5511' + telefone
            else:
                return False, "Formato de telefone inválido"
        
        if operadora == 'claro':
            base_url = f"https://api.prezaofree.com.br/{UUID_PATH_CLARO}"
            headers = HEADERS_LOGIN_CLARO.copy()
        elif operadora == 'tim':
            base_url = f"https://api.timfun.com.br/{UUID_PATH_TIM}"
            headers = HEADERS_LOGIN_TIM.copy()
        else:
            base_url = f"https://api.vivofree.com.br/{UUID_PATH_VIVO}"
            headers = HEADERS_LOGIN_VIVO.copy()
        
        log_terminal(f"🔓 Tentando desbanir número: {telefone} ({operadora.upper()})")
        
        payload = {"msisdn": telefone}
        
        response = requests.post(
            f"{base_url}/pnde",
            json=payload,
            headers=headers,
            timeout=15
        )
        
        log_terminal(f"Status da requisição de SMS: {response.status_code}")
        
        if response.status_code == 200:
            return True, "✅ Número desbloqueado! Agora você pode solicitar um novo código SMS."
        elif response.status_code == 429:
            return False, "❌ Número temporariamente bloqueado por muitas tentativas. Aguarde algumas horas."
        elif response.status_code == 400:
            try:
                check_payload = {"msisdn": telefone, "verifyOnly": True}
                check_response = requests.post(
                    f"{base_url}/vapi/check",
                    json=check_payload,
                    headers=headers,
                    timeout=10
                )
                if check_response.status_code == 200:
                    return True, "✅ Número verificado e desbloqueado! Tente novamente o login."
                else:
                    return False, f"❌ Número bloqueado. Status: {check_response.status_code}"
            except Exception as e:
                return False, f"❌ Erro na verificação: {str(e)[:100]}"
        else:
            error_text = response.text[:200] if response.text else "Sem resposta detalhada"
            return False, f"❌ Erro ao desbanir. Status: {response.status_code} - {error_text}"
            
    except requests.exceptions.Timeout:
        return False, "❌ Timeout: Servidor não respondeu. Tente novamente mais tarde."
    except requests.exceptions.ConnectionError:
        return False, "❌ Erro de conexão. Verifique sua internet."
    except Exception as e:
        return False, f"❌ Erro inesperado: {str(e)[:200]}"

def api_resetar_conta(telefone, operadora='vivo'):
    try:
        if not telefone.startswith('55'):
            telefone = '55' + telefone
        
        if operadora == 'claro':
            base_url = f"https://api.prezaofree.com.br/{UUID_PATH_CLARO}"
            headers = HEADERS_LOGIN_CLARO.copy()
        elif operadora == 'tim':
            base_url = f"https://api.timfun.com.br/{UUID_PATH_TIM}"
            headers = HEADERS_LOGIN_TIM.copy()
        else:
            base_url = f"https://api.vivofree.com.br/{UUID_PATH_VIVO}"
            headers = HEADERS_LOGIN_VIVO.copy()
        
        log_terminal(f"🔄 Resetando conta: {telefone} ({operadora.upper()})")
        
        endpoints = [
            f"{base_url}/auth/reset",
            f"{base_url}/user/reset",
            f"{base_url}/account/unlock",
            f"{base_url}/block/remove"
        ]
        
        for endpoint in endpoints:
            try:
                payload = {
                    "msisdn": telefone,
                    "reason": "unblock_request",
                    "timestamp": int(time.time())
                }
                response = requests.post(
                    endpoint,
                    json=payload,
                    headers=headers,
                    timeout=10
                )
                if response.status_code in [200, 202, 204]:
                    log_terminal(f"✅ Endpoint {endpoint.split('/')[-1]} respondeu positivamente")
                    return True, "✅ Conta resetada com sucesso! Aguarde 5 minutos e tente novamente."
            except:
                continue
        
        sms_payload = {"msisdn": telefone, "force": True}
        response = requests.post(
            f"{base_url}/pnde/force",
            json=sms_payload,
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            return True, "✅ SMS forçado enviado! Verifique seu telefone."
        else:
            return False, "❌ Não foi possível resetar a conta. Entre em contato com o suporte da operadora."
            
    except Exception as e:
        return False, f"❌ Erro no reset: {str(e)[:200]}"
        
        # ==============================================================================
# 📁 SISTEMA DE PERSISTÊNCIA DE DADOS COM BACKUP E RESTAURAÇÃO AUTOMÁTICA
# ==============================================================================
class DataManager:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.data_dir = "/storage/emulated/0/bot"
        self.ensure_data_dir()
        
        self.user_db = {}
        self.cupons_db = {}
        self.username_to_id = {}
        self.last_broadcast_msgs = []
        self.last_media_msgs = []
        self.auto_farm_jobs = {}
        self.farm_status = {}
        self.pagamentos_pendentes = {}
        self.promocoes_ativas = {}
        self.afiliados_db = {}
        self.afiliado_codigo_to_user = {}
        self.backup_history = []
        self.backup_settings = {
            'auto_backup': True,
            'interval_hours': 24,
            'backup_time': "03:00",
            'last_auto_backup': None,
            'backup_job_id': None
        }
        
        self.last_json_send_time = time.time()
        self.min_interval = 60
        
        self._save_dirty = False
        self._save_thread = None
        self._save_lock = threading.Lock()
        self._save_write_lock = threading.Lock()
        
        self.local_data_exists = self.check_local_data_exists()
        self.load_all_data()
        
        if not self.local_data_exists or len(self.user_db) == 0:
            log_terminal("⚠️ Nenhum dado local encontrado. Tentando restaurar do canal...")
            if self.restaurar_ultimo_backup_do_canal():
                log_terminal("✅ Dados restaurados do canal com sucesso!")
            else:
                log_terminal("❌ Não foi possível restaurar dados do canal. Iniciando com dados vazios.")
        
        self.save_scheduler = BackgroundScheduler()
        self.save_scheduler.add_job(self.save_all_data, 'interval', minutes=5)
        self.save_scheduler.start()
    
    def check_local_data_exists(self):
        user_db_path = os.path.join(self.data_dir, 'user_db.json')
        return os.path.exists(user_db_path)
    
    def ensure_data_dir(self):
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir, exist_ok=True)
                log_terminal(f"✔️ Diretório criado: {self.data_dir}")
            backup_dir = os.path.join(self.data_dir, 'backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir, exist_ok=True)
                log_terminal(f"✔️ Diretório de backups criado: {backup_dir}")
            test_file = os.path.join(self.data_dir, 'test_permissions.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            log_terminal("✔️ Permissões de escrita OK")
        except Exception as e:
            log_terminal(f"❌ Erro ao criar diretório: {e}")
            self.data_dir = "bot_data"
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir, exist_ok=True)
            log_terminal(f"⚠️ Usando diretório fallback: {self.data_dir}")
    
    def buscar_ultimo_backup_no_canal(self):
        try:
            messages = self.bot.get_chat_history(BACKUP_CHANNEL_ID, limit=100)
            ultimo_backup = None
            ultima_data = None
            
            for message in messages:
                if message.document:
                    file_name = message.document.file_name
                    if file_name and file_name.startswith('backup_') and file_name.endswith('.json'):
                        msg_date = message.date
                        if ultima_data is None or msg_date > ultima_data:
                            ultima_data = msg_date
                            ultimo_backup = {
                                'message_id': message.message_id,
                                'file_id': message.document.file_id,
                                'file_name': file_name,
                                'date': msg_date,
                                'caption': message.caption
                            }
            return ultimo_backup
        except Exception as e:
            log_terminal(f"❌ Erro ao buscar backup no canal: {e}")
            return None
    
    def baixar_e_restaurar_backup(self, backup_info):
        try:
            log_terminal(f"📥 Baixando backup: {backup_info['file_name']}")
            file_info = self.bot.get_file(backup_info['file_id'])
            downloaded_file = self.bot.download_file(file_info.file_path)
            
            temp_path = os.path.join(self.data_dir, 'temp_backup.json')
            with open(temp_path, 'wb') as f:
                f.write(downloaded_file)
            
            log_terminal("📖 Lendo arquivo de backup...")
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            user_db_backup = backup_data.get('user_db', {})
            cupons_db_backup = backup_data.get('cupons_db', {})
            username_to_id_backup = backup_data.get('username_to_id', {})
            pagamentos_pendentes_backup = backup_data.get('pagamentos_pendentes', {})
            promocoes_ativas_backup = backup_data.get('promocoes_ativas', {})
            afiliados_backup = backup_data.get('afiliados_db', {})
            afiliado_codigo_backup = backup_data.get('afiliado_codigo_to_user', {})
            
            user_db_backup = self.deserialize_datetime(user_db_backup)
            cupons_db_backup = self.deserialize_datetime(cupons_db_backup)
            pagamentos_pendentes_backup = self.deserialize_datetime(pagamentos_pendentes_backup)
            promocoes_ativas_backup = self.deserialize_datetime(promocoes_ativas_backup)
            afiliados_backup = self.deserialize_datetime(afiliados_backup)
            
            self.user_db.clear()
            self.user_db.update(user_db_backup)
            self.cupons_db.clear()
            self.cupons_db.update(cupons_db_backup)
            self.username_to_id.clear()
            self.username_to_id.update(username_to_id_backup)
            self.pagamentos_pendentes.clear()
            self.pagamentos_pendentes.update(pagamentos_pendentes_backup)
            self.promocoes_ativas.clear()
            self.promocoes_ativas.update(promocoes_ativas_backup)
            self.afiliados_db.clear()
            self.afiliados_db.update(afiliados_backup)
            self.afiliado_codigo_to_user.clear()
            self.afiliado_codigo_to_user.update(afiliado_codigo_backup)
            
            self._save_now()
            os.remove(temp_path)
            
            log_terminal(f"✅ Backup restaurado com sucesso!")
            log_terminal(f"   👥 Usuários: {len(self.user_db)}")
            log_terminal(f"   🎫 Cupons: {len(self.cupons_db)}")
            log_terminal(f"   💰 Pagamentos: {len(self.pagamentos_pendentes)}")
            log_terminal(f"   🎉 Promoções: {len(self.promocoes_ativas)}")
            log_terminal(f"   🤝 Afiliados: {len(self.afiliados_db)}")
            return True
        except Exception as e:
            log_terminal(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def restaurar_ultimo_backup_do_canal(self):
        try:
            log_terminal("🔍 Buscando último backup no canal...")
            backup_info = self.buscar_ultimo_backup_no_canal()
            if not backup_info:
                log_terminal("❌ Nenhum backup encontrado no canal")
                return False
            
            log_terminal(f"📅 Último backup encontrado: {backup_info['file_name']}")
            log_terminal(f"   📅 Data: {backup_info['date']}")
            log_terminal(f"   📝 Legenda: {backup_info['caption']}")
            
            success = self.baixar_e_restaurar_backup(backup_info)
            
            if success:
                try:
                    self.bot.send_message(
                        ADMIN_ID,
                        f"🔄 BACKUP RESTAURADO AUTOMATICAMENTE\n\n"
                        f"📁 Arquivo: {backup_info['file_name']}\n"
                        f"📅 Data do backup: {backup_info['date']}\n"
                        f"👥 Usuários restaurados: {len(self.user_db)}\n"
                        f"🎫 Cupons: {len(self.cupons_db)}\n"
                        f"💰 Pagamentos: {len(self.pagamentos_pendentes)}\n"
                        f"🤝 Afiliados: {len(self.afiliados_db)}\n\n"
                        f"✅ Bot reiniciado com sucesso em nova VPS!"
                    )
                except:
                    pass
            return success
        except Exception as e:
            log_terminal(f"❌ Erro ao restaurar último backup: {e}")
            return False
    
    def restaurar_backup_manual(self, chat_id):
        try:
            backup_info = self.buscar_ultimo_backup_no_canal()
            if not backup_info:
                self.bot.send_message(chat_id, "❌ Nenhum backup encontrado no canal")
                return False
            
            self.bot.send_message(chat_id, f"🔄 Restaurando backup: {backup_info['file_name']}...")
            success = self.baixar_e_restaurar_backup(backup_info)
            
            if success:
                self.bot.send_message(
                    chat_id,
                    f"✅ BACKUP RESTAURADO COM SUCESSO!\n\n"
                    f"📁 Arquivo: {backup_info['file_name']}\n"
                    f"👥 Usuários: {len(self.user_db)}\n"
                    f"🎫 Cupons: {len(self.cupons_db)}\n"
                    f"💰 Pagamentos: {len(self.pagamentos_pendentes)}\n"
                    f"🎉 Promoções: {len(self.promocoes_ativas)}\n"
                    f"🤝 Afiliados: {len(self.afiliados_db)}"
                )
            else:
                self.bot.send_message(chat_id, "❌ Falha ao restaurar backup")
            return success
        except Exception as e:
            log_terminal(f"❌ Erro no restore manual: {e}")
            self.bot.send_message(chat_id, f"❌ Erro: {str(e)[:200]}")
            return False
    
    def send_all_json_to_channel(self, force_send=False, reason=""):
        try:
            if not self.bot or not BACKUP_CHANNEL_ID:
                return False
            
            now = time.time()
            if not force_send and (now - self.last_json_send_time) < self.min_interval:
                return False
            
            self.last_json_send_time = now
            
            self._save_now()
            
            arquivos_principais = [
                'user_db.json', 'cupons_db.json', 'username_to_id.json',
                'last_broadcast_msgs.json', 'last_media_msgs.json',
                'auto_farm_jobs.json', 'farm_status.json',
                'pagamentos_pendentes.json', 'promocoes_ativas.json',
                'afiliados_db.json', 'afiliado_codigo_to_user.json'
            ]
            
            tz_brasilia = pytz.timezone('America/Sao_Paulo')
            data_hora = datetime.now(tz_brasilia).strftime("%d/%m/%Y %H:%M:%S")
            
            mensagem_principal = f"📊 DADOS ATUALIZADOS - {data_hora}\n"
            mensagem_principal += f"📌 Motivo: {reason}\n\n"
            mensagem_principal += f"👥 Usuários: {len(self.user_db)}\n"
            mensagem_principal += f"🎫 Cupons: {len(self.cupons_db)}\n"
            mensagem_principal += f"💰 Pagamentos pendentes: {len(self.pagamentos_pendentes)}\n"
            mensagem_principal += f"🤖 Jobs automáticos: {len(self.auto_farm_jobs)}\n"
            mensagem_principal += f"🎉 Promoções ativas: {len(self.promocoes_ativas)}\n"
            mensagem_principal += f"🤝 Afiliados: {len(self.afiliados_db)}\n"
            
            usuarios_ativos = 0
            for user_id, user_data in self.user_db.items():
                if self.is_license_valid(user_id):
                    usuarios_ativos += 1
            
            mensagem_principal += f"✔️ Usuários ativos: {usuarios_ativos}\n\n"
            mensagem_principal += "📁 Arquivos enviados:"
            
            try:
                msg = self.bot.send_message(BACKUP_CHANNEL_ID, mensagem_principal)
            except Exception as e:
                log_terminal(f"❌ Erro ao enviar mensagem principal: {e}")
                return False
            
            for arquivo in arquivos_principais:
                filepath = os.path.join(self.data_dir, arquivo)
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'rb') as f:
                            self.bot.send_document(
                                BACKUP_CHANNEL_ID, f,
                                caption=f"📄 {arquivo} - {data_hora}",
                                visible_file_name=arquivo
                            )
                        time.sleep(0.3)
                    except Exception as e:
                        log_terminal(f"❌ Erro ao enviar {arquivo}: {e}")
            
            try:
                sucesso, backup_file, tamanho_kb = self.backup_data()
                if sucesso:
                    with open(backup_file, 'rb') as f:
                        self.bot.send_document(
                            BACKUP_CHANNEL_ID, f,
                            caption=f"💾 BACKUP COMPLETO - {data_hora} - {tamanho_kb:.2f} KB",
                            visible_file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        )
            except Exception as e:
                log_terminal(f"❌ Erro ao enviar backup completo: {e}")
            
            log_terminal(f"✔️ Dados enviados para o canal. Motivo: {reason}")
            return True
        except Exception as e:
            log_terminal(f"❌ Erro no envio de dados para o canal: {e}")
            return False
    
    def send_json_on_user_action(self, action_type, user_id=None):
        try:
            acoes_importantes = [
                "novo_usuario", "start_command", "farm_iniciado", "farm_concluido",
                "resgate_efetuado", "conta_adicionada", "conta_removida",
                "cupom_resgatado", "novo_pagamento", "pagamento_aprovado",
                "licenca_atualizada", "admin_add_user", "admin_gen_cupom",
                "menu_command", "minhas_contas", "admin_broadcast",
                "broadcast_enviado", "midia_enviada", "admin_estatisticas",
                "pagamento_expirado", "pagamento_manual_confirmado",
                "pagamento_cancelado", "cupom_excluido", "usuario_excluido",
                "aviso_excluido", "midia_excluida", "cupom_expirado",
                "cupom_gerado", "admin_add_dias", "promocao_criada",
                "promocao_excluida", "pagamento_promocao",
                "afiliado_criado", "afiliado_registrado", "backup_completo_restaurado"
            ]
            
            if action_type in acoes_importantes:
                motivos = {
                    "novo_usuario": "Novo usuário cadastrado",
                    "start_command": "Usuário iniciou o bot",
                    "farm_iniciado": "Início de coleta de pontos",
                    "farm_concluido": "Coleta de pontos concluída",
                    "resgate_efetuado": "Resgate na loja",
                    "conta_adicionada": "Nova conta adicionada",
                    "conta_removida": "Conta removida",
                    "cupom_resgatado": "Cupom resgatado",
                    "novo_pagamento": "Novo pagamento gerado",
                    "pagamento_aprovado": "Pagamento aprovado",
                    "licenca_atualizada": "Licença atualizada",
                    "admin_add_user": "Admin adicionou usuário",
                    "admin_gen_cupom": "Admin gerou cupom",
                    "menu_command": "Usuário acessou menu",
                    "minhas_contas": "Usuário viu contas",
                    "admin_broadcast": "Admin enviou broadcast",
                    "broadcast_enviado": "Broadcast enviado",
                    "midia_enviada": "Mídia enviada para todos",
                    "admin_estatisticas": "Admin viu estatísticas",
                    "pagamento_expirado": "Pagamento expirado",
                    "pagamento_manual_confirmado": "Pagamento confirmado manualmente",
                    "pagamento_cancelado": "Pagamento cancelado",
                    "cupom_excluido": "Cupom excluído",
                    "usuario_excluido": "Usuário excluído",
                    "aviso_excluido": "Aviso excluído",
                    "midia_excluida": "Mídia excluída",
                    "cupom_expirado": "Cupom expirado",
                    "cupom_gerado": "Cupom gerado",
                    "admin_add_dias": "Admin adicionou dias",
                    "promocao_criada": "Nova promoção criada",
                    "promocao_excluida": "Promoção excluída automaticamente",
                    "pagamento_promocao": "Pagamento de promoção gerado",
                    "afiliado_criado": "Novo afiliado cadastrado",
                    "afiliado_registrado": "Novo registro via afiliado",
                    "backup_completo_restaurado": "Backup completo restaurado"
                }
                
                motivo = motivos.get(action_type, f"Ação: {action_type}")
                if user_id:
                    motivo += f" (ID: {user_id})"
                
                threading.Thread(
                    target=self.send_all_json_to_channel,
                    args=(True, motivo)
                ).start()
                
                log_terminal(f"✔️ Envio de dados acionado: {motivo}")
        except Exception as e:
            log_terminal(f"❌ Erro no envio por ação: {e}")
    
    def serialize_datetime(self, obj):
        if isinstance(obj, datetime):
            return {'_type': 'datetime', 'value': obj.isoformat()}
        elif isinstance(obj, dict):
            return {k: self.serialize_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.serialize_datetime(item) for item in obj]
        else:
            return obj
    
    def deserialize_datetime(self, obj):
        if isinstance(obj, dict):
            if '_type' in obj and obj['_type'] == 'datetime':
                try:
                    return datetime.fromisoformat(obj['value'].replace('Z', '+00:00'))
                except:
                    for fmt in ('%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
                        try:
                            return datetime.strptime(obj['value'], fmt)
                        except:
                            continue
                    return datetime.now()
            return {k: self.deserialize_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.deserialize_datetime(item) for item in obj]
        else:
            return obj
    
    def save_to_file(self, filename, data):
        try:
            filepath = os.path.join(self.data_dir, filename)
            def json_serializer(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                raise TypeError(f"Type {type(obj)} not serializable")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, default=json_serializer, ensure_ascii=False, indent=2)
            log_terminal(f"✔️ Dados salvos em {filepath}")
            return True
        except Exception as e:
            log_terminal(f"❌ Erro ao salvar {filename}: {e}")
            return False
    
    def load_from_file(self, filename):
        try:
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                def convert_datetime(obj):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if isinstance(value, str):
                                try:
                                    if 'T' in value or ' ' in value:
                                        if '.' in value:
                                            obj[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                                        else:
                                            for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S'):
                                                try:
                                                    obj[key] = datetime.strptime(value, fmt)
                                                    break
                                                except:
                                                    continue
                                except:
                                    pass
                            elif isinstance(value, dict):
                                convert_datetime(value)
                            elif isinstance(value, list):
                                for item in value:
                                    if isinstance(item, dict):
                                        convert_datetime(item)
                        return obj
                    return obj
                
                data = convert_datetime(data)
                log_terminal(f"✔️ Dados carregados de {filepath}")
                return data
            else:
                log_terminal(f"📄 Arquivo {filename} não encontrado, criando novo")
                return self.get_default_data(filename)
        except Exception as e:
            log_terminal(f"❌ Erro ao carregar {filename}: {e}")
            return self.get_default_data(filename)
    
    def get_default_data(self, filename):
        defaults = {
            'user_db.json': {},
            'cupons_db.json': {},
            'username_to_id.json': {},
            'last_broadcast_msgs.json': [],
            'last_media_msgs.json': [],
            'auto_farm_jobs.json': {},
            'farm_status.json': {},
            'pagamentos_pendentes.json': {},
            'promocoes_ativas.json': {},
            'afiliados_db.json': {},
            'afiliado_codigo_to_user.json': {},
            'backup_history.json': [],
            'backup_settings.json': self.backup_settings
        }
        return defaults.get(filename, {})
    
    def save_all_data(self):
        """Agenda save em background (debounce 0.5s) — retorna imediatamente"""
        with self._save_lock:
            self._save_dirty = True
            if self._save_thread is None or not self._save_thread.is_alive():
                self._save_thread = threading.Thread(target=self._save_worker, daemon=True)
                self._save_thread.start()
    
    def _save_worker(self):
        """Worker que agrupa múltiplos cliques em um único save"""
        while True:
            time.sleep(0.5)
            with self._save_lock:
                if not self._save_dirty:
                    return
                self._save_dirty = False
            try:
                self._save_now()
            except Exception as e:
                log_terminal(f"❌ Erro no save em background: {e}")
    
    def _save_now(self):
        """Salva no disco de verdade (bloqueante) — usado pelo worker, atexit e operações críticas"""
        with self._save_write_lock:
            try:
                arquivos_principais = [
                    'user_db.json', 'cupons_db.json', 'username_to_id.json',
                    'last_broadcast_msgs.json', 'last_media_msgs.json',
                    'auto_farm_jobs.json', 'farm_status.json',
                    'pagamentos_pendentes.json', 'promocoes_ativas.json',
                    'afiliados_db.json', 'afiliado_codigo_to_user.json',
                    'backup_history.json', 'backup_settings.json'
                ]
                for arquivo in arquivos_principais:
                    attr_name = arquivo.replace('.json', '').replace('-', '_')
                    if hasattr(self, attr_name):
                        data = getattr(self, attr_name)
                        self.save_to_file(arquivo, data)
                log_terminal("💾 Dados salvos com sucesso!")
            except Exception as e:
                log_terminal(f"❌ Erro ao salvar dados: {e}")
    
    def load_all_data(self):
        try:
            log_terminal("📂 Carregando todos os dados do disco...")
            arquivos_principais = [
                'user_db.json', 'cupons_db.json', 'username_to_id.json',
                'last_broadcast_msgs.json', 'last_media_msgs.json',
                'auto_farm_jobs.json', 'farm_status.json',
                'pagamentos_pendentes.json', 'promocoes_ativas.json',
                'afiliados_db.json', 'afiliado_codigo_to_user.json',
                'backup_history.json', 'backup_settings.json'
            ]
            for arquivo in arquivos_principais:
                attr_name = arquivo.replace('.json', '').replace('-', '_')
                if hasattr(self, attr_name):
                    data = self.load_from_file(arquivo)
                    setattr(self, attr_name, data)
                    log_terminal(f"  ✔️ {arquivo}: {type(data)} carregado")
            
            self.ensure_data_structure()
            
            log_terminal(f"📊 Dados carregados: {len(self.user_db)} usuários")
            log_terminal(f"📊 Cupons: {len(self.cupons_db)} ativos")
            log_terminal(f"📊 Pagamentos: {len(self.pagamentos_pendentes)} pendentes")
            log_terminal(f"📊 Promoções ativas: {len(self.promocoes_ativas)}")
            log_terminal(f"📊 Afiliados: {len(self.afiliados_db)}")
        except Exception as e:
            log_terminal(f"❌ Erro ao carregar dados: {e}")
    
    def ensure_data_structure(self):
        log_terminal("🔧 Verificando estrutura de dados...")
        for chat_id in list(self.user_db.keys()):
            user = self.user_db[chat_id]
            estrutura_completa = {
                'contas': [], 'conta_ativa': 0,
                'config': {'auto_farm': False, 'notificacoes': True},
                'license_date': None,
                'first_seen': datetime.now(), 'last_seen': datetime.now(),
                'username': '', 'first_name': '', 'last_name': '',
                'language_code': 'pt', 'is_bot': False, 'is_premium': False,
                'added_by': None, 'status': 'active',
                'pontos_coletados': 0, 'total_farms': 0,
                'auto_farm_enabled': False, 'data_compra': None,
                'metodo_pagamento': None, 'ultima_coleta': None,
                'preferencias': {
                    'notificar_saldo': True,
                    'notificar_expira': True,
                    'modo_turbo': True
                }
            }
            for key, default_value in estrutura_completa.items():
                if key not in user:
                    user[key] = default_value
            
            for conta in user['contas']:
                estrutura_conta = {
                    'telefone': '', 'token': '', 'wallet': '',
                    'data_cadastro': datetime.now(), 'ultimo_login': datetime.now(),
                    'saldo': 0, 'validade_saldo': None, 'status': 'active',
                    'pais': 'BR', 'operadora': 'vivo', 'plano': '',
                    'pontos_hoje': 0, 'pontos_total': 0, 'resgates': [],
                    'ultima_atualizacao': datetime.now()
                }
                for key, default_value in estrutura_conta.items():
                    if key not in conta:
                        conta[key] = default_value
        
        for codigo, cupom in list(self.cupons_db.items()):
            if 'resgatado_por' not in cupom:
                cupom['resgatado_por'] = []
        
        for promo_id, promocao in list(self.promocoes_ativas.items()):
            estrutura_promocao = {
                'id': promo_id, 'preco': 0.0, 'dias': 0, 'horas_duracao': 24,
                'data_criacao': datetime.now(), 'mensagens': [], 'texto': '',
                'imagem': None, 'tipo': 'texto', 'job_id': None
            }
            for key, default_value in estrutura_promocao.items():
                if key not in promocao:
                    promocao[key] = default_value
        
        for afiliado_id, afiliado in list(self.afiliados_db.items()):
            estrutura_afiliado = {
                'user_id': afiliado_id, 'codigo': '', 'cliques': 0,
                'registros': 0, 'indicados': [], 'dias_ganhos': 0,
                'data_criacao': datetime.now()
            }
            for key, default_value in estrutura_afiliado.items():
                if key not in afiliado:
                    afiliado[key] = default_value
        
        log_terminal("✔️ Estrutura de dados verificada e corrigida")
    
    def get_user_complete_info(self, chat_id):
        if chat_id not in self.user_db:
            return None
        user = self.user_db[chat_id].copy()
        user['licenca_valida'] = self.is_license_valid(chat_id)
        user['dias_restantes'] = self.get_days_remaining(chat_id)
        user['total_contas'] = len(user.get('contas', []))
        user['tem_conta'] = user['total_contas'] > 0
        total_pontos = 0
        for conta in user.get('contas', []):
            total_pontos += conta.get('pontos_total', 0)
        user['pontos_total'] = total_pontos
        return user
    
    def is_license_valid(self, chat_id):
        if chat_id == ADMIN_ID:
            return True
        user = self.user_db.get(chat_id)
        if not user:
            return False
        license_date = user.get('license_date')
        if not license_date:
            return False
        return datetime.now() <= license_date
    
    def get_days_remaining(self, chat_id):
        if chat_id == ADMIN_ID:
            return 9999
        user = self.user_db.get(chat_id)
        if not user:
            return 0
        license_date = user.get('license_date')
        if not license_date or datetime.now() > license_date:
            return 0
        diferenca = license_date - datetime.now()
        return diferenca.days
    
    def get_user_statistics(self):
        stats = {
            'total_usuarios': len(self.user_db),
            'usuarios_ativos': 0, 'usuarios_com_contas': 0,
            'usuarios_com_licenca': 0, 'usuarios_novos_hoje': 0,
            'total_pontos': 0, 'total_afiliados': len(self.afiliados_db)
        }
        hoje = datetime.now().date()
        for user_id, user_data in self.user_db.items():
            if self.is_license_valid(user_id):
                stats['usuarios_ativos'] += 1
                stats['usuarios_com_licenca'] += 1
            if user_data.get('contas'):
                stats['usuarios_com_contas'] += 1
            first_seen = user_data.get('first_seen')
            if isinstance(first_seen, datetime) and first_seen.date() == hoje:
                stats['usuarios_novos_hoje'] += 1
            for conta in user_data.get('contas', []):
                stats['total_pontos'] += conta.get('pontos_total', 0)
        return stats
    
    def add_backup_history(self, backup_info):
        self.backup_history.append({
            'timestamp': datetime.now(),
            'info': backup_info,
            'arquivos': 10, 'tamanho_kb': 0
        })
        if len(self.backup_history) > 100:
            self.backup_history = self.backup_history[-100:]
        self.save_to_file('backup_history.json', self.backup_history)
    
    def backup_data(self):
        try:
            backup_dir = os.path.join(self.data_dir, 'backups')
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f'backup_{timestamp}.json')
            
            backup_data = {
                'timestamp': timestamp,
                'data_hora': datetime.now().isoformat(),
                'user_db': self.user_db,
                'cupons_db': self.cupons_db,
                'username_to_id': self.username_to_id,
                'last_broadcast_msgs': self.last_broadcast_msgs,
                'last_media_msgs': self.last_media_msgs,
                'auto_farm_jobs': self.auto_farm_jobs,
                'farm_status': self.farm_status,
                'pagamentos_pendentes': self.pagamentos_pendentes,
                'promocoes_ativas': self.promocoes_ativas,
                'afiliados_db': self.afiliados_db,
                'afiliado_codigo_to_user': self.afiliado_codigo_to_user,
                'backup_history': self.backup_history,
                'total_usuarios': len(self.user_db),
                'total_cupons': len(self.cupons_db),
                'total_pagamentos': len(self.pagamentos_pendentes),
                'total_promocoes': len(self.promocoes_ativas),
                'total_afiliados': len(self.afiliados_db)
            }
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, default=lambda obj: obj.isoformat() if isinstance(obj, datetime) else str(obj), ensure_ascii=False, indent=2)
            
            tamanho_kb = os.path.getsize(backup_file) / 1024
            self.add_backup_history({
                'filename': f'backup_{timestamp}.json',
                'tamanho_kb': round(tamanho_kb, 2),
                'arquivos': len(backup_data) - 4,
                'usuarios': len(self.user_db)
            })
            log_terminal(f"💾 Backup completo criado: {backup_file} ({tamanho_kb:.2f} KB)")
            return True, backup_file, tamanho_kb
        except Exception as e:
            log_terminal(f"❌ Erro ao criar backup: {e}")
            return False, None, 0

# Instanciar o gerenciador de dados
data_manager = DataManager(bot)

# Criar atalhos para as estruturas de dados
user_db = data_manager.user_db
cupons_db = data_manager.cupons_db
username_to_id = data_manager.username_to_id
last_broadcast_msgs = data_manager.last_broadcast_msgs
last_media_msgs = data_manager.last_media_msgs
auto_farm_jobs = data_manager.auto_farm_jobs
farm_status = data_manager.farm_status
pagamentos_pendentes = data_manager.pagamentos_pendentes
promocoes_ativas = data_manager.promocoes_ativas
afiliados_db = data_manager.afiliados_db
afiliado_codigo_to_user = data_manager.afiliado_codigo_to_user
backup_history = data_manager.backup_history

atexit.register(lambda: data_manager._save_now())

# ==============================================================================
# 🎭 ESTADOS DE USUÁRIO E ADMIN
# ==============================================================================
user_state = {}
admin_state = {}

scheduler = BackgroundScheduler()
scheduler.start()

# ==============================================================================
# 🛠️ MAIS UTILITÁRIOS
# ==============================================================================
def verificar_licenca(chat_id):
    if chat_id == ADMIN_ID: 
        return True 
    
    if chat_id not in user_db:
        user_db[chat_id] = {
            'contas': [], 'conta_ativa': 0,
            'config': {'auto_farm': False},
            'license_date': None,
            'first_seen': datetime.now()
        }
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("novo_usuario", chat_id)
        log_terminal(f"Usuário {chat_id} adicionado via verificação de licença")
    
    user = user_db.get(chat_id, {})
    validade = user.get('license_date')
    if not validade: 
        return False
    if datetime.now() > validade: 
        return False
    return True

def msg_licenca_expirada(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("💳 COMPRAR 30 DIAS - R$ 25,00", callback_data="comprar_licenca"))
    markup.add(types.InlineKeyboardButton("🥰 RENOVAR COM SUPORTE 🥰", url="https://t.me/JADIEL_TM"))
    bot.send_message(chat_id, "🚫 ACESSO BLOQUEADO\n\nSua licença expirou.\n\n🔓 Renove sua licença para continuar usando o bot.", reply_markup=markup)

def notificar_admin_novo_usuario(user_info):
    try:
        mensagem = f"🆕 NOVO USUÁRIO NO BOT!\n\n"
        mensagem += f"👤 Nome: {user_info.get('first_name', 'Não informado')}\n"
        mensagem += f"📛 Sobrenome: {user_info.get('last_name', 'Não informado')}\n"
        mensagem += f"📱 Username: @{user_info.get('username', 'Não informado')}\n"
        mensagem += f"🆔 ID: {user_info.get('id', 'Não informado')}\n"
        mensagem += f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        bot.send_message(ADMIN_ID, mensagem)
        log_terminal(f"Novo usuário: {user_info.get('first_name')} (@{user_info.get('username')})")
    except Exception as e:
        log_terminal(f"Erro ao notificar admin: {e}")

def criar_pagamento_mercadopago(chat_id, valor, descricao):
    try:
        headers = {
            "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": str(uuid.uuid4())
        }
        
        pagamento_data = {
            "transaction_amount": float(valor),
            "payment_method_id": "pix",
            "payer": {
                "email": "cliente@email.com",
                "first_name": "Cliente", "last_name": "Bot",
                "identification": {"type": "CPF", "number": "00000000000"}
            },
            "description": descricao,
            "notification_url": None,
            "external_reference": f"CHAT_{chat_id}_{int(time.time())}",
            "additional_info": {
                "items": [{
                    "id": "licenca",
                    "title": f"Licença {DIAS_LICENCA} dias",
                    "description": "Licença para uso do bot JADIEL MB",
                    "quantity": 1, "unit_price": float(valor)
                }],
                "payer": {
                    "first_name": "Cliente", "last_name": "Telegram",
                    "phone": {"area_code": "11", "number": "999999999"}
                }
            }
        }
        
        response = requests.post(
            f"{MP_API_URL}/payments",
            headers=headers, json=pagamento_data, timeout=30
        )
        
        if response.status_code == 201:
            pagamento_info = response.json()
            payment_id = str(pagamento_info["id"])
            status = pagamento_info["status"]
            
            if "point_of_interaction" in pagamento_info:
                pix_info = pagamento_info["point_of_interaction"]["transaction_data"]
                qr_code_base64 = pix_info.get("qr_code_base64")
                chave_pix = pix_info.get("pix_copypaste")
                if not chave_pix:
                    chave_pix = pix_info.get("qr_code", "")
                
                pagamento = {
                    'payment_id': payment_id,
                    'chat_id': chat_id,
                    'valor': valor, 'descricao': descricao,
                    'qr_code_base64': qr_code_base64,
                    'chave_pix': chave_pix,
                    'status': status,
                    'data_criacao': datetime.now(),
                    'data_expiracao': datetime.now() + timedelta(minutes=30),
                    'pago': False, 'dados_mp': pagamento_info
                }
                
                pagamentos_pendentes[payment_id] = pagamento
                data_manager.save_all_data()
                data_manager.send_json_on_user_action("novo_pagamento", chat_id)
                return pagamento
            else:
                log_terminal(f"❌ Pagamento criado mas sem dados PIX: {pagamento_info}")
                return None
        else:
            log_terminal(f"❌ Erro ao criar pagamento MP: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        log_terminal(f"❌ Erro ao criar pagamento Mercado Pago: {e}")
        return None

def verificar_pagamento(payment_id):
    try:
        if payment_id not in pagamentos_pendentes:
            return False, "Pagamento não encontrado"
        
        pagamento = pagamentos_pendentes[payment_id]
        
        if datetime.now() > pagamento['data_expiracao']:
            pagamento['status'] = 'expired'
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("pagamento_expirado", payment_id)
            return False, "Pagamento expirado"
        
        headers = {"Authorization": f"Bearer {MP_ACCESS_TOKEN}"}
        
        response = requests.get(
            f"{MP_API_URL}/payments/{payment_id}",
            headers=headers, timeout=10
        )
        
        if response.status_code == 200:
            pagamento_info = response.json()
            status = pagamento_info["status"]
            pagamento['status'] = status
            
            if status == "approved":
                pagamento['pago'] = True
                pagamento['data_pagamento'] = datetime.now()
                data_manager.save_all_data()
                data_manager.send_json_on_user_action("pagamento_aprovado", payment_id)
                return True, "Pagamento confirmado"
            elif status in ["pending", "in_process", "authorized"]:
                return False, "Aguardando pagamento"
            elif status in ["cancelled", "rejected", "refunded", "charged_back"]:
                pagamento['status'] = status
                data_manager.save_all_data()
                data_manager.send_json_on_user_action("pagamento_cancelado", payment_id)
                return False, f"Pagamento {status}"
            else:
                return False, f"Status: {status}"
        else:
            log_terminal(f"❌ Erro ao verificar pagamento: {response.status_code}")
            return False, "Erro ao verificar pagamento"
    except Exception as e:
        log_terminal(f"❌ Erro ao verificar pagamento: {e}")
        return False, f"Erro: {str(e)[:100]}"

def confirmar_pagamento_manual(payment_id):
    try:
        if payment_id not in pagamentos_pendentes:
            return False, "Pagamento não encontrado"
        
        pagamento = pagamentos_pendentes[payment_id]
        
        if datetime.now() > pagamento['data_expiracao']:
            return False, "Pagamento já expirou"
        
        pagamento['pago'] = True
        pagamento['status'] = 'approved'
        pagamento['data_pagamento'] = datetime.now()
        
        chat_id = pagamento['chat_id']
        
        if chat_id not in user_db:
            user_db[chat_id] = {
                'contas': [], 'conta_ativa': 0,
                'config': {'auto_farm': False},
                'license_date': None,
                'first_seen': datetime.now()
            }
        
        user = user_db[chat_id]
        validade_atual = user.get('license_date')
        
        if validade_atual and validade_atual > datetime.now():
            nova_validade = validade_atual + timedelta(days=DIAS_LICENCA)
        else:
            nova_validade = datetime.now() + timedelta(days=DIAS_LICENCA)
        
        user_db[chat_id]['license_date'] = nova_validade
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("pagamento_manual_confirmado", payment_id)
        log_terminal(f"Pagamento {payment_id} confirmado para chat_id {chat_id}")
        
        try:
            bot.send_message(chat_id, f"✔️ PAGAMENTO CONFIRMADO!\n\nSua licença foi renovada por {DIAS_LICENCA} dias!\nNova validade: {formatar_data(nova_validade)}\n\nObrigado pela confiança! 🎉")
        except:
            pass
        return True, "Pagamento confirmado com sucesso"
    except Exception as e:
        log_terminal(f"❌ Erro ao confirmar pagamento manual: {e}")
        return False, f"Erro: {str(e)}"

# ==============================================================================
# 🤝 SISTEMA DE AFILIADOS
# ==============================================================================
_bot_username_cache = None

def get_bot_username():
    global _bot_username_cache
    if _bot_username_cache is None:
        try:
            _bot_username_cache = bot.get_me().username
        except:
            _bot_username_cache = "jadiel_mb_vivo_vip_bot"
    return _bot_username_cache


def menu_afiliado():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(
        "🤝 SE AFILIE AQUI!",
        callback_data="afiliado_gerar_link",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "📊 PAINEL DE AFILIADOS",
        callback_data="afiliado_painel",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Voltar ao Menu",
        callback_data="back_home",
        style="success"
    ))
    return markup


def gerar_link_afiliado(chat_id):
    try:
        if chat_id in data_manager.afiliados_db:
            afiliado = data_manager.afiliados_db[chat_id]
            codigo = afiliado.get('codigo')
            if not codigo:
                codigo = gerar_codigo_cupom(8)
                while codigo in data_manager.afiliado_codigo_to_user:
                    codigo = gerar_codigo_cupom(8)
                afiliado['codigo'] = codigo
                data_manager.afiliado_codigo_to_user[codigo] = chat_id
                data_manager.save_all_data()
        else:
            codigo = gerar_codigo_cupom(8)
            while codigo in data_manager.afiliado_codigo_to_user:
                codigo = gerar_codigo_cupom(8)
            
            data_manager.afiliados_db[chat_id] = {
                'user_id': chat_id,
                'codigo': codigo,
                'cliques': 0,
                'registros': 0,
                'indicados': [],
                'dias_ganhos': 0,
                'data_criacao': datetime.now()
            }
            data_manager.afiliado_codigo_to_user[codigo] = chat_id
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("afiliado_criado", chat_id)
        
        bot_username = get_bot_username()
        link = f"https://t.me/{bot_username}?start={codigo}"
        return link, codigo
    except Exception as e:
        log_terminal(f"❌ Erro ao gerar link de afiliado: {e}")
        return None, None


def mostrar_painel_afiliado(chat_id):
    try:
        if chat_id not in data_manager.afiliados_db:
            bot.send_message(
                chat_id,
                "❌ Você ainda não é um afiliado!\n\nClique em *🤝 SE AFILIE AQUI!* para gerar seu link exclusivo.",
                parse_mode='Markdown'
            )
            return
        
        afiliado = data_manager.afiliados_db[chat_id]
        codigo = afiliado.get('codigo', '')
        cliques = afiliado.get('cliques', 0)
        registros = afiliado.get('registros', 0)
        dias_ganhos = afiliado.get('dias_ganhos', 0)
        data_criacao = afiliado.get('data_criacao', datetime.now())
        indicados = afiliado.get('indicados', [])
        
        taxa = (registros / cliques * 100) if cliques > 0 else 0
        
        msg = "📊 PAINEL DE AFILIADOS\n"
        msg += "━━━━━━━━━━━━━━━━\n"
        msg += f"🔗 Código: *{codigo}*\n"
        msg += f"📅 Afiliado desde: {formatar_data(data_criacao)}\n\n"
        msg += "📈 ESTATÍSTICAS REAIS:\n"
        msg += f"👆 Cliques no link: *{cliques}*\n"
        msg += f"👥 Registros: *{registros}*\n"
        msg += f"🎁 Dias ganhos: *{dias_ganhos}*\n"
        msg += f"📊 Taxa de conversão: *{taxa:.1f}%*\n\n"
        
        if indicados:
            msg += "👥 ÚLTIMOS INDICADOS:\n"
            for uid in indicados[-5:]:
                if uid in data_manager.user_db:
                    nome = data_manager.user_db[uid].get('first_name', 'Usuário')
                    username = data_manager.user_db[uid].get('username', '')
                    if username:
                        msg += f"• {nome} (@{username})\n"
                    else:
                        msg += f"• {nome}\n"
            if len(indicados) > 5:
                msg += f"... e mais {len(indicados) - 5} indicados\n"
            msg += "\n"
        
        msg += "💡 *Como funciona:*\n"
        msg += f"• Cada novo usuário que entrar pelo seu link = +{DIAS_BONUS_AFILIADO} dias grátis pra você e pra ele!\n"
        msg += "• Compartilhe seu link para ganhar cada vez mais!\n\n"
        msg += "🚀 Divulgue e lucre!"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            "🔗 COPIAR MEU LINK",
            callback_data="afiliado_copiar_link",
            style="success"
        ))
        markup.add(types.InlineKeyboardButton(
            "🔙 Voltar",
            callback_data="afiliado_menu",
            style="success"
        ))
        bot.send_message(chat_id, msg, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        log_terminal(f"❌ Erro ao mostrar painel de afiliado: {e}")
        bot.send_message(chat_id, f"❌ Erro ao carregar painel: {str(e)[:100]}")


def processar_afiliado(novo_user_id, codigo):
    try:
        codigo = codigo.strip().upper()
        
        if codigo not in data_manager.afiliado_codigo_to_user:
            log_terminal(f"⚠️ Código de afiliado inválido: {codigo}")
            return False
        
        afiliado_user_id = data_manager.afiliado_codigo_to_user[codigo]
        
        if afiliado_user_id == novo_user_id:
            log_terminal(f"⚠️ Auto-indicação bloqueada: {novo_user_id}")
            return False
        
        if afiliado_user_id not in data_manager.afiliados_db:
            log_terminal(f"⚠️ Registro de afiliado não encontrado: {afiliado_user_id}")
            return False
        
        afiliado = data_manager.afiliados_db[afiliado_user_id]
        
        if novo_user_id in afiliado.get('indicados', []):
            log_terminal(f"⚠️ Usuário {novo_user_id} já foi indicado")
            return False
        
        afiliado['registros'] = afiliado.get('registros', 0) + 1
        afiliado['indicados'].append(novo_user_id)
        afiliado['dias_ganhos'] = afiliado.get('dias_ganhos', 0) + DIAS_BONUS_AFILIADO
        
        agora = datetime.now()
        
        if afiliado_user_id in data_manager.user_db:
            ref_validade = data_manager.user_db[afiliado_user_id].get('license_date')
            if ref_validade and ref_validade > agora:
                data_manager.user_db[afiliado_user_id]['license_date'] = ref_validade + timedelta(days=DIAS_BONUS_AFILIADO)
            else:
                data_manager.user_db[afiliado_user_id]['license_date'] = agora + timedelta(days=DIAS_BONUS_AFILIADO)
        else:
            data_manager.user_db[afiliado_user_id] = {
                'contas': [], 'conta_ativa': 0,
                'config': {'auto_farm': False},
                'license_date': agora + timedelta(days=DIAS_BONUS_AFILIADO),
                'first_seen': agora
            }
        
        if novo_user_id not in data_manager.user_db:
            data_manager.user_db[novo_user_id] = {
                'contas': [], 'conta_ativa': 0,
                'config': {'auto_farm': False},
                'license_date': agora + timedelta(days=DIAS_BONUS_AFILIADO),
                'first_seen': agora
            }
        else:
            novo_validade = data_manager.user_db[novo_user_id].get('license_date')
            if novo_validade and novo_validade > agora:
                data_manager.user_db[novo_user_id]['license_date'] = novo_validade + timedelta(days=DIAS_BONUS_AFILIADO)
            else:
                data_manager.user_db[novo_user_id]['license_date'] = agora + timedelta(days=DIAS_BONUS_AFILIADO)
        
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("afiliado_registrado", novo_user_id)
        
        try:
            nova_val_ref = data_manager.user_db[afiliado_user_id].get('license_date')
            bot.send_message(
                afiliado_user_id,
                f"🎉 *PARABÉNS! ALGUÉM ENTROU PELO SEU LINK!*\n\n"
                f"🎁 Você ganhou *+{DIAS_BONUS_AFILIADO} DIAS* de licença grátis!\n"
                f"📅 Nova validade: *{formatar_data(nova_val_ref)}*\n\n"
                f"Continue divulgando para ganhar cada vez mais! 🚀",
                parse_mode='Markdown'
            )
        except Exception as e:
            log_terminal(f"⚠️ Não foi possível notificar afiliado: {e}")
        
        try:
            nova_val_novo = data_manager.user_db[novo_user_id].get('license_date')
            bot.send_message(
                novo_user_id,
                f"🎁 *BÔNUS DE AFILIADO ATIVADO!*\n\n"
                f"Você entrou pelo link de um afiliado e ganhou *+{DIAS_BONUS_AFILIADO} DIAS* de licença grátis!\n"
                f"📅 Sua validade: *{formatar_data(nova_val_novo)}*\n\n"
                f"Bem-vindo ao JADIEL MB VIP! 🚀",
                parse_mode='Markdown'
            )
        except Exception as e:
            log_terminal(f"⚠️ Não foi possível notificar novo usuário: {e}")
        
        log_terminal(f"✅ AFILIADO: {novo_user_id} registrado via {codigo} (dono: {afiliado_user_id})")
        return True
    except Exception as e:
        log_terminal(f"❌ Erro ao processar afiliado: {e}")
        return False

# ==============================================================================
# 📱 MENUS (LAYOUT VERTICAL)
# ==============================================================================
def menu_inicial_start():
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn_login = types.InlineKeyboardButton(
        "✔️FAZER LOGIN✔️",
        callback_data="login_start",
        style="success"
    )
    btn_sup = types.InlineKeyboardButton(
        "🥰 SUPORTE 🥰",
        url="https://t.me/JADIEL_TM",
        style="success"
    )

    markup.add(btn_login, btn_sup)
    return markup


def menu_operadora():
    markup = types.InlineKeyboardMarkup(row_width=3)

    markup.add(
        types.InlineKeyboardButton(
            "🟣 VIVO",
            callback_data="operator_vivo",
            style="success"
        ),
        types.InlineKeyboardButton(
            "🔴 CLARO",
            callback_data="operator_claro",
            style="success"
        ),
        types.InlineKeyboardButton(
            "🔵 TIM",
            callback_data="operator_tim",
            style="success"
        )
    )
    return markup


def menu_principal_logado():
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(types.InlineKeyboardButton(
        "🤩 COLETAR PONTOS\n\n✔️ATIVO✔️",
        callback_data="start_farm_turbo",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "💰 MEU SALDO\n\n✔️ATIVO✔️",
        callback_data="check_balance",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🛒 LOJA DE RESGATE\n\n✔️ATIVO✔️",
        callback_data="redeem_menu",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔒 MINHA LICENÇA\n\n✔️ATIVO✔️",
        callback_data="my_license",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "⚙️ CONFIGURAÇÕES",
        callback_data="config_menu",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🤝 AFILIADO",
        callback_data="afiliado_menu",
        style="success"
    ))

    return markup


def menu_configuracoes(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)

    user = user_db.get(chat_id, {})
    config = user.get('config', {})

    auto_status = (
        "✔️ ATIVADO"
        if config.get('auto_farm', False)
        else "❌ DESATIVADO"
    )

    markup.add(types.InlineKeyboardButton(
        f"🤖 BOT AUTOMÁTICO: {auto_status}",
        callback_data="toggle_auto_farm",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "📱 GERENCIAR CONTAS",
        callback_data="manage_accounts",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "➕ ADICIONAR CONTA",
        callback_data="add_new_account",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Voltar ao Menu",
        callback_data="back_home",
        style="success"
    ))

    return markup


def menu_gerenciar_contas(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)

    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)

    if not contas:
        markup.add(types.InlineKeyboardButton(
            "📭 Nenhuma conta cadastrada",
            callback_data="none"
        ))
    else:
        for idx, conta in enumerate(contas):
            telefone = conta.get('telefone', 'N/A')
            operadora = conta.get('operadora', 'vivo')
            status = " ✔️ ATIVA" if idx == conta_ativa else ""

            if operadora == 'vivo':
                icon = "🟣"
            elif operadora == 'claro':
                icon = "🔴"
            else:
                icon = "🔵"

            texto = f"{idx+1}. {icon} {telefone}{status}"

            markup.add(types.InlineKeyboardButton(
                texto,
                callback_data=f"select_account|{idx}"
            ))

        if len(contas) > 0:
            markup.add(types.InlineKeyboardButton(
                "🗑️ REMOVER CONTA ATIVA",
                callback_data="remove_account",
                style="success"
            ))

    markup.add(types.InlineKeyboardButton(
        "🔙 Voltar às Configurações",
        callback_data="config_menu",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Voltar ao Menu Principal",
        callback_data="back_home",
        style="success"
    ))

    return markup


def menu_comprar_licenca():
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(types.InlineKeyboardButton(
        "💳 PAGAR COM PIX - R$ 25,00",
        callback_data="gerar_pagamento_pix",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Voltar à Licença",
        callback_data="my_license",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Voltar ao Menu",
        callback_data="back_home",
        style="success"
    ))

    return markup


def menu_pagamento_pix(payment_id):
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(
        "✔️ JÁ PAGUEI",
        callback_data=f"verificar_pagamento|{payment_id}",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔄 GERAR NOVO PIX",
        callback_data="gerar_pagamento_pix",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Cancelar",
        callback_data="my_license",
        style="success"
    ))

    return markup


def menu_pagamento_promocao(payment_id, promo_id):
    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(types.InlineKeyboardButton(
        "✔️ JÁ PAGUEI",
        callback_data=f"verificar_pagamento_promo|{payment_id}|{promo_id}",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔄 GERAR NOVO PIX",
        callback_data=f"promo_pagar|{promo_id}",
        style="success"
    ))
    markup.add(types.InlineKeyboardButton(
        "🔙 Cancelar",
        callback_data="my_license",
        style="success"
    ))

    return markup
    
def show_menu_with_image(chat_id, is_logged=False):
    saudacao = get_saudacao()
    
    nome = (user_db.get(chat_id, {}).get('first_name') or '').strip()
    if not nome:
        try:
            chat = bot.get_chat(chat_id)
            nome = chat.first_name or 'Usuário'
            if chat_id in user_db:
                user_db[chat_id]['first_name'] = nome
        except:
            nome = 'Usuário'
    
    tz_brasilia = pytz.timezone('America/Sao_Paulo')
    hora_atual = datetime.now(tz_brasilia).strftime("%H:%M")
    
    if is_logged and chat_id in user_db and user_db[chat_id].get('contas'):
        legenda = f"{saudacao}, {nome}! 👋\n🕐 Horário: {hora_atual}\n\n✔️ Você está logado!\n\n⚠️Atenção, verifique se o sistema do bot está funcionando corretamente na sua operadora. Caso não esteja, fale com o suporte\n\n🥰SUPORTE: @JADIEL_TM\n\n👇 Escolha uma opção:"
        markup = menu_principal_logado()
    else:
        legenda = f"{saudacao}, {nome}! 👋\n🕐 Horário: {hora_atual}\n\n🤖 Bem-vindo ao JADIEL MB VIP\n\n⚠️Atenção: pra usar esse serviço, você precisa ter um chip dessas operadoras abaixo\n\n🟣VIVO🟣\n\n🔴CLARO🔴\n\n🔵TIM🔵\n\n👇 Escolha uma opção:"
        markup = menu_inicial_start()
    
    try:
        bot.send_photo(chat_id, START_IMAGE, caption=legenda, reply_markup=markup, parse_mode='HTML')
    except:
        bot.send_message(chat_id, legenda, reply_markup=markup)

# ==============================================================================
# 🌐 API VIVO - COLETA COM ANTI-BAN (30s POR VÍDEO)
# ==============================================================================
def api_executar_farm_vivo(chat_id, is_auto=False):
    if not verificar_licenca(chat_id): 
        if not is_auto: 
            msg_licenca_expirada(chat_id)
        return
    
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        if not is_auto: 
            bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    operadora = conta.get('operadora', 'vivo')
    
    if operadora != 'vivo':
        api_executar_farm_generico(chat_id, is_auto)
        return
    
    base_url = get_base_url(operadora)
    headers = get_headers_fast(operadora)
    endpoints = get_endpoints(operadora)
    wallet = conta.get('wallet')
    token = conta.get('token')
    telefone = conta.get('telefone', 'N/A')
    
    if not is_auto:
        msg_status = bot.send_message(chat_id, f"🚀 INICIANDO COLETA VIVO!\n\n📱 Conta: {telefone}\n📡 Operadora: 🟣 VIVO\n🛡️ Modo anti-ban ATIVO ({TEMPO_VIDEO_SEGUNDOS}s por vídeo)\n⚡ Isso pode levar vários minutos...")
        farm_status[chat_id] = {'msg_id': msg_status.message_id, 'progress': 0, 'total': 0}
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("farm_iniciado", chat_id)
    else:
        msg_status = None
    
    log_terminal(f"FARM VIVO: {telefone} - {len(endpoints)} endpoints - {TEMPO_VIDEO_SEGUNDOS}s/vídeo")
    
    payload = {
        "userId": wallet,
        "contextInfo": {
            "os": "WEB", 
            "brand": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", 
            "manufacturer": "Linux armv81",
            "osVersion": "Linux armv81", 
            "battery": "74",
            "X-APP-ID": "akross_rewardapps", 
            "X-APP-VERSION": "3.1.10"
        }
    }
    
    headers["X-AUTHORIZATION"] = token
    
    todas_campanhas = []
    if not is_auto:
        bot.edit_message_text("⚡ Buscando missões Vivo...", chat_id, msg_status.message_id)
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        def coletar_endpoint_vivo(zone_id):
            try:
                endpoint_url = f"{base_url}/adserver/campaign/v3/{zone_id}?size=100"
                resp = session.post(endpoint_url, json=payload, timeout=5)
                if resp.status_code == 204:
                    return []
                data = resp.json()
                request_id = data.get('requestId')
                campanhas = data.get('campaigns', [])
                for campanha in campanhas:
                    campanha['requestId'] = request_id
                    campanha['zone_id'] = zone_id
                return campanhas
            except Exception as e:
                log_terminal(f"Erro no endpoint {zone_id}: {e}")
                return []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(coletar_endpoint_vivo, zone_id) for zone_id in endpoints]
            for future in concurrent.futures.as_completed(futures):
                campanhas = future.result()
                if campanhas:
                    todas_campanhas.extend(campanhas)
    
    if not todas_campanhas:
        if not is_auto:
            bot.edit_message_text("📶 Servidor vivo.\n\n⚠️Atenção, aperta novamente no botão Coletar Pontos pra ver se você consegue coletar mais pontos.\n\n⚠️ Se caso não conseguir coletar os pontos, tente mais tarde, tente.\n\n⚠️ Você pode tentar 1, 2, 3, 4, 5 vezes, apertando no botão Coletar Pontos para ver se coleta novamente.\n\n✔️ Verifique, no aplicativo da sua operadora, se você já concluiu todas as missões. Se sim, então é por isso que você recebeu essa mensagem da Vivo.\n\n✔️ Qualquer dúvida, fale com o suporte.\n\n🥰 SUPORTE @JADIEL_TM", chat_id, msg_status.message_id)
        return
    
    total_videos = sum(len(camp.get('mainData', {}).get('media', [])) for camp in todas_campanhas)
    
    if total_videos == 0:
        if not is_auto:
            bot.edit_message_text("❌ Nenhum vídeo disponível nas missões encontradas.", chat_id, msg_status.message_id)
        return
    
    farm_status[chat_id]['total'] = total_videos
    data_manager.save_all_data()
    
    tempo_estimado_min = (total_videos * TEMPO_VIDEO_SEGUNDOS) / 60
    
    if not is_auto:
        bot.edit_message_text(
            f"🎯 {total_videos} missões encontradas na Vivo!\n"
            f"🛡️ Anti-ban ATIVO: {TEMPO_VIDEO_SEGUNDOS}s por vídeo\n"
            f"⏱️ Tempo estimado: ~{tempo_estimado_min:.1f} minutos\n"
            f"⚡ Iniciando coleta...",
            chat_id, msg_status.message_id
        )
    
    videos_processados = 0
    inicio = time.time()
    
    for campanha in todas_campanhas:
        uuid_camp = campanha.get('campaignUuid')
        request_id = campanha.get('requestId')
        videos = campanha.get('mainData', {}).get('media', [])
        
        for video in videos:
            uuid_media = video.get('uuid')
            
            try:
                requests.post(
                    f"{base_url}/adserver/tracker",
                    params={"e": "impression", "c": uuid_camp, "u": wallet, 
                           "requestId": request_id, "m": uuid_media},
                    headers=headers,
                    timeout=2
                )
            except:
                pass
            
            if not is_auto:
                for seg in range(TEMPO_VIDEO_SEGUNDOS):
                    time.sleep(1)
                    if seg in [5, 10, 15, 20, 25]:
                        try:
                            bot.edit_message_text(
                                f"🎬 ASSISTINDO VÍDEO...\n"
                                f"📡 Operadora: 🟣 VIVO\n"
                                f"🎬 Vídeo {videos_processados + 1}/{total_videos}\n"
                                f"⏱️ {seg}/{TEMPO_VIDEO_SEGUNDOS} segundos\n\n"
                                f"🛡️ Modo anti-ban ativo\n"
                                f"⚠️ Não feche o bot",
                                chat_id, msg_status.message_id
                            )
                        except:
                            pass
            else:
                time.sleep(TEMPO_VIDEO_SEGUNDOS)
            
            try:
                requests.post(
                    f"{base_url}/adserver/tracker",
                    params={"e": "complete", "c": uuid_camp, "u": wallet, 
                           "requestId": request_id, "m": uuid_media},
                    headers=headers,
                    timeout=2
                )
            except:
                pass
            
            videos_processados += 1
            
            if not is_auto:
                progresso = barra_progresso_ultra(videos_processados, total_videos)
                tempo_decorrido = time.time() - inicio
                
                if videos_processados > 0:
                    tempo_medio = tempo_decorrido / videos_processados
                    tempo_restante = tempo_medio * (total_videos - videos_processados)
                else:
                    tempo_restante = 0
                
                status_msg = (
                    f"🚀 COLETANDO PONTOS VIVO!\n"
                    f"📡 Operadora: 🟣 VIVO\n"
                    f"{progresso}\n"
                    f"📊 {videos_processados}/{total_videos} vídeos\n"
                    f"⏱️ Decorrido: {tempo_decorrido/60:.1f} min\n"
                    f"⏳ Restante: {tempo_restante/60:.1f} min"
                )
                
                try:
                    bot.edit_message_text(status_msg, chat_id, msg_status.message_id)
                except:
                    pass
        
        try:
            requests.post(
                f"{base_url}/adserver/tracker",
                params={"e": "conversion", "c": uuid_camp, "u": wallet, "requestId": request_id},
                headers=headers, timeout=2
            )
        except:
            pass
    
    fim = time.time()
    tempo_total = fim - inicio
    
    pontos_coletados = videos_processados * get_pontos_por_video(operadora)
    
    if chat_id in user_db:
        user = user_db[chat_id]
        if len(user['contas']) > conta_ativa:
            conta_atual = user['contas'][conta_ativa]
            pontos_atuais = conta_atual.get('pontos_total', 0)
            conta_atual['pontos_total'] = pontos_atuais + pontos_coletados
            conta_atual['pontos_hoje'] = pontos_coletados
            conta_atual['ultima_atualizacao'] = datetime.now()
            user_db[chat_id]['pontos_coletados'] = user.get('pontos_coletados', 0) + pontos_coletados
            user_db[chat_id]['total_farms'] = user.get('total_farms', 0) + 1
            user_db[chat_id]['ultima_coleta'] = datetime.now()
            data_manager.save_all_data()
    
    if not is_auto:
        try:
            progresso_final = barra_progresso_ultra(total_videos, total_videos)
            relatorio = (
                f"✔️ COLETA VIVO COMPLETA!\n\n"
                f"📱 Conta: {telefone}\n"
                f"📡 Operadora: 🟣 VIVO\n"
                f"🎯 Missões: {videos_processados}\n"
                f"💰 Pontos coletados: {pontos_coletados}\n"
                f"⏱️ Tempo total: {tempo_total/60:.1f} minutos\n"
                f"🛡️ Modo anti-ban respeitado\n"
                f"{progresso_final}\n\n"
                f"🎉 Pontos coletados com sucesso!\n\n"
                f"Dobre esses pontos, apertando novamente no botão 'Coletar Pontos'. 🔁✨"
            )
            bot.edit_message_text(relatorio, chat_id, msg_status.message_id)
            time.sleep(0.5)
            api_ver_saldo(chat_id)
        except Exception as e:
            bot.send_message(chat_id, f"✔️ Coleta Vivo completa! {videos_processados} missões ({pontos_coletados} pontos) em {tempo_total/60:.1f}min")
    else:
        log_terminal(f"FARM AUTO VIVO: {videos_processados} missões ({pontos_coletados} pontos) em {tempo_total/60:.1f}min")
    
    if chat_id in farm_status:
        del farm_status[chat_id]
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("farm_concluido", chat_id)

def api_executar_farm_generico(chat_id, is_auto=False):
    if not verificar_licenca(chat_id): 
        if not is_auto: 
            msg_licenca_expirada(chat_id)
        return
    
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        if not is_auto: 
            bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    operadora = conta.get('operadora', 'claro')
    
    if operadora == 'tim':
        api_executar_farm_tim_especial(chat_id, is_auto)
        return
    
    base_url = get_base_url(operadora)
    headers = get_headers_fast(operadora)
    endpoints = get_endpoints(operadora)
    wallet = conta.get('wallet')
    token = conta.get('token')
    telefone = conta.get('telefone', 'N/A')
    
    operadora_nome = "🔴 CLARO" if operadora == 'claro' else "📱 DESCONHECIDA"
    operadora_icon = "🔴" if operadora == 'claro' else "📱"
    
    if not is_auto:
        msg_status = bot.send_message(chat_id, f"🚀 INICIANDO COLETA {operadora_nome}!\n\n📱 Conta: {telefone}\n📡 Operadora: {operadora_nome}\n🛡️ Anti-ban: {TEMPO_VIDEO_SEGUNDOS}s/vídeo\n⚡ Isso pode levar vários minutos...")
        farm_status[chat_id] = {'msg_id': msg_status.message_id, 'progress': 0, 'total': 0}
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("farm_iniciado", chat_id)
    else:
        msg_status = None
    
    log_terminal(f"FARM {operadora.upper()}: {telefone} - {len(endpoints)} endpoints - {TEMPO_VIDEO_SEGUNDOS}s/vídeo")
    
    payload = {
        "userId": wallet,
        "contextInfo": {
            "os": "WEB", 
            "brand": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", 
            "manufacturer": "Linux armv81",
            "osVersion": "Linux armv81", 
            "battery": "74",
            "X-APP-ID": "akross_rewardapps", 
            "X-APP-VERSION": "3.1.10"
        }
    }
    
    headers["X-AUTHORIZATION"] = token
    
    todas_campanhas = []
    if not is_auto:
        bot.edit_message_text("⚡ Buscando missões...", chat_id, msg_status.message_id)
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        def coletar_endpoint(zone_id):
            try:
                endpoint_url = f"{base_url}/adserver/campaign/v3/{zone_id}?size=100"
                resp = session.post(endpoint_url, json=payload, timeout=5)
                if resp.status_code == 204:
                    return []
                data = resp.json()
                request_id = data.get('requestId')
                campanhas = data.get('campaigns', [])
                for campanha in campanhas:
                    campanha['requestId'] = request_id
                    campanha['zone_id'] = zone_id
                return campanhas
            except:
                return []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(coletar_endpoint, zone_id) for zone_id in endpoints]
            for future in concurrent.futures.as_completed(futures):
                campanhas = future.result()
                todas_campanhas.extend(campanhas)
    
    if not todas_campanhas:
        if not is_auto:
            bot.edit_message_text("❌ Nenhuma missão disponível.", chat_id, msg_status.message_id)
        return
    
    total_videos = sum(len(camp.get('mainData', {}).get('media', [])) for camp in todas_campanhas)
    
    if total_videos == 0:
        if not is_auto:
            bot.edit_message_text("❌ Nenhuma missão disponível.", chat_id, msg_status.message_id)
        return
    
    farm_status[chat_id]['total'] = total_videos
    data_manager.save_all_data()
    
    tempo_estimado_min = (total_videos * TEMPO_VIDEO_SEGUNDOS) / 60
    
    if not is_auto:
        bot.edit_message_text(
            f"🎯 {total_videos} missões encontradas!\n"
            f"🛡️ Anti-ban ATIVO: {TEMPO_VIDEO_SEGUNDOS}s por vídeo\n"
            f"⏱️ Tempo estimado: ~{tempo_estimado_min:.1f} minutos\n"
            f"⚡ Iniciando coleta...",
            chat_id, msg_status.message_id
        )
    
    videos_processados = 0
    inicio = time.time()
    
    for campanha in todas_campanhas:
        uuid_camp = campanha.get('campaignUuid')
        request_id = campanha.get('requestId')
        videos = campanha.get('mainData', {}).get('media', [])
        
        for video in videos:
            uuid_media = video.get('uuid')
            
            try:
                requests.post(
                    f"{base_url}/adserver/tracker",
                    params={"e": "impression", "c": uuid_camp, "u": wallet, 
                           "requestId": request_id, "m": uuid_media},
                    headers=headers, timeout=2
                )
            except:
                pass
            
            if not is_auto:
                for seg in range(TEMPO_VIDEO_SEGUNDOS):
                    time.sleep(1)
                    if seg in [5, 10, 15, 20, 25]:
                        try:
                            bot.edit_message_text(
                                f"🎬 ASSISTINDO VÍDEO...\n"
                                f"📡 Operadora: {operadora_nome}\n"
                                f"🎬 Vídeo {videos_processados + 1}/{total_videos}\n"
                                f"⏱️ {seg}/{TEMPO_VIDEO_SEGUNDOS} segundos\n\n"
                                f"🛡️ Modo anti-ban ativo",
                                chat_id, msg_status.message_id
                            )
                        except:
                            pass
            else:
                time.sleep(TEMPO_VIDEO_SEGUNDOS)
            
            try:
                requests.post(
                    f"{base_url}/adserver/tracker",
                    params={"e": "complete", "c": uuid_camp, "u": wallet, 
                           "requestId": request_id, "m": uuid_media},
                    headers=headers, timeout=2
                )
            except:
                pass
            
            videos_processados += 1
            
            if not is_auto:
                progresso = barra_progresso_ultra(videos_processados, total_videos)
                tempo_decorrido = time.time() - inicio
                
                if videos_processados > 0:
                    tempo_medio = tempo_decorrido / videos_processados
                    tempo_restante = tempo_medio * (total_videos - videos_processados)
                else:
                    tempo_restante = 0
                
                status_msg = (
                    f"🚀 COLETANDO PONTOS {operadora_nome}!\n"
                    f"📡 Operadora: {operadora_nome}\n"
                    f"{progresso}\n"
                    f"📊 {videos_processados}/{total_videos} vídeos\n"
                    f"⏱️ Decorrido: {tempo_decorrido/60:.1f} min\n"
                    f"⏳ Restante: {tempo_restante/60:.1f} min"
                )
                
                try:
                    bot.edit_message_text(status_msg, chat_id, msg_status.message_id)
                except:
                    pass
        
        try:
            requests.post(
                f"{base_url}/adserver/tracker",
                params={"e": "conversion", "c": uuid_camp, "u": wallet, "requestId": request_id},
                headers=headers, timeout=2
            )
        except:
            pass
    
    fim = time.time()
    tempo_total = fim - inicio
    pontos_coletados = videos_processados * get_pontos_por_video(operadora)
    
    if chat_id in user_db:
        user = user_db[chat_id]
        if len(user['contas']) > conta_ativa:
            conta_atual = user['contas'][conta_ativa]
            pontos_atuais = conta_atual.get('pontos_total', 0)
            conta_atual['pontos_total'] = pontos_atuais + pontos_coletados
            conta_atual['pontos_hoje'] = pontos_coletados
            conta_atual['ultima_atualizacao'] = datetime.now()
            user_db[chat_id]['pontos_coletados'] = user.get('pontos_coletados', 0) + pontos_coletados
            user_db[chat_id]['total_farms'] = user.get('total_farms', 0) + 1
            user_db[chat_id]['ultima_coleta'] = datetime.now()
            data_manager.save_all_data()
    
    if not is_auto:
        try:
            progresso_final = barra_progresso_ultra(total_videos, total_videos)
            relatorio = (
                f"✔️ COLETA {operadora_nome} COMPLETA!\n\n"
                f"📱 Conta: {telefone}\n"
                f"📡 Operadora: {operadora_nome}\n"
                f"🎯 Missões: {videos_processados}\n"
                f"💰 Pontos coletados: {pontos_coletados}\n"
                f"⏱️ Tempo total: {tempo_total/60:.1f} minutos\n"
                f"🛡️ Modo anti-ban respeitado\n"
                f"{progresso_final}\n\n"
                f"🎉 Pontos coletados com sucesso!"
            )
            bot.edit_message_text(relatorio, chat_id, msg_status.message_id)
            time.sleep(0.5)
            api_ver_saldo(chat_id)
        except Exception as e:
            bot.send_message(chat_id, f"✔️ Coleta completa! {videos_processados} missões ({pontos_coletados} pontos) em {tempo_total/60:.1f}min")
    else:
        log_terminal(f"FARM AUTO {operadora.upper()}: {videos_processados} missões ({pontos_coletados} pontos) em {tempo_total/60:.1f}min")
    
    if chat_id in farm_status:
        del farm_status[chat_id]
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("farm_concluido", chat_id)

def api_executar_farm(chat_id, is_auto=False):
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        if not is_auto: 
            bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    operadora = conta.get('operadora', 'vivo')
    
    if operadora == 'vivo':
        api_executar_farm_vivo(chat_id, is_auto)
    elif operadora == 'tim':
        api_executar_farm_tim_especial(chat_id, is_auto)
    else:
        api_executar_farm_generico(chat_id, is_auto)

# ==============================================================================
# 🌐 API TIM ESPECIAL COM ANTI-BAN
# ==============================================================================
def api_executar_farm_tim_especial(chat_id, is_auto=False):
    if not verificar_licenca(chat_id): 
        if not is_auto: 
            msg_licenca_expirada(chat_id)
        return
    
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        if not is_auto: 
            bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    
    if conta.get('operadora') != 'tim':
        if not is_auto:
            bot.send_message(chat_id, "❌ Esta função é apenas para contas TIM.")
        return
    
    base_url = get_base_url('tim')
    headers = get_headers_fast('tim')
    wallet = conta.get('wallet')
    token = conta.get('token')
    telefone = conta.get('telefone', 'N/A')
    
    if not is_auto:
        msg_status = bot.send_message(chat_id, f"🚀 INICIANDO COLETA TIM!\n\n📱 Conta: {telefone}\n📡 Operadora: 🔵 TIM\n🛡️ Anti-ban: {TEMPO_VIDEO_SEGUNDOS}s/vídeo\n⚡ Isso pode levar vários minutos...")
        farm_status[chat_id] = {'msg_id': msg_status.message_id, 'progress': 0, 'total': 0}
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("farm_iniciado", chat_id)
    else:
        msg_status = None
    
    log_terminal(f"FARM TIM: {telefone} - {TEMPO_VIDEO_SEGUNDOS}s/vídeo")
    
    ZONE_UUID_TIM = "bbdef37d-f5c4-4b19-9cfb-ed6e8f43fa2f"
    
    payload = {
        "userId": wallet,
        "contextInfo": {
            "os": "WEB", 
            "brand": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", 
            "manufacturer": "Linux armv81",
            "osVersion": "Linux armv81", 
            "battery": "74",
            "X-APP-ID": "akross_rewardapps", 
            "X-APP-VERSION": "3.1.10"
        }
    }
    
    headers["X-AUTHORIZATION"] = token
    
    todas_campanhas = []
    if not is_auto:
        bot.edit_message_text("⚡ Buscando missões TIM...", chat_id, msg_status.message_id)
    
    try:
        endpoint_url = f"{base_url}/adserver/campaign/v3/{ZONE_UUID_TIM}?size=100"
        resp = requests.post(endpoint_url, json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            request_id = data.get('requestId')
            campanhas = data.get('campaigns', [])
            for campanha in campanhas:
                campanha['requestId'] = request_id
                campanha['zone_id'] = ZONE_UUID_TIM
            todas_campanhas.extend(campanhas)
            log_terminal(f"TIM: {len(campanhas)} campanhas encontradas")
        else:
            log_terminal(f"TIM: Erro {resp.status_code}")
            if not is_auto:
                bot.edit_message_text("❌ Erro ao buscar missões da TIM.", chat_id, msg_status.message_id)
            return
    except Exception as e:
        log_terminal(f"Erro na coleta TIM: {e}")
        if not is_auto:
            bot.edit_message_text("❌ Erro de conexão com a TIM.", chat_id, msg_status.message_id)
        return
    
    if not todas_campanhas:
        if not is_auto:
            bot.edit_message_text("📶 Servidor vivo.\n\n⚠️Atenção, aperta novamente no botão Coletar Pontos pra ver se você consegue coletar mais pontos.\n\n⚠️ Se caso não conseguir coletar os pontos, tente mais tarde, tente.\n\n⚠️ Você pode tentar 1, 2, 3, 4, 5 vezes, apertando no botão Coletar Pontos para ver se coleta novamente.\n\n✔️ Verifique, no aplicativo da sua operadora, se você já concluiu todas as missões. Se sim, então é por isso que você recebeu essa mensagem da Vivo.\n\n✔️ Qualquer dúvida, fale com o suporte.\n\n🥰 SUPORTE @JADIEL_TM", chat_id, msg_status.message_id)
        return
    
    total_videos = sum(len(camp.get('mainData', {}).get('media', [])) for camp in todas_campanhas)
    
    if total_videos == 0:
        if not is_auto:
            bot.edit_message_text("📶 Servidor tim.\n\n⚠️Atenção, aperta novamente no botão Coletar Pontos pra ver se você consegue coletar mais pontos.\n\n⚠️ Se caso não conseguir coletar os pontos, tente mais tarde, tente.\n\n⚠️ Você pode tentar 1, 2, 3, 4, 5 vezes, apertando no botão Coletar Pontos para ver se coleta novamente.\n\n✔️ Verifique, no aplicativo da sua operadora, se você já concluiu todas as missões. Se sim, então é por isso que você recebeu essa mensagem da tim.\n\n✔️ Qualquer dúvida, fale com o suporte.\n\n🥰 SUPORTE JADIEL_TM", chat_id, msg_status.message_id)
        return
    
    farm_status[chat_id]['total'] = total_videos
    data_manager.save_all_data()
    
    tempo_estimado_min = (total_videos * TEMPO_VIDEO_SEGUNDOS) / 60
    
    if not is_auto:
        bot.edit_message_text(
            f"🎯 {total_videos} missões TIM encontradas!\n"
            f"🛡️ Anti-ban ATIVO: {TEMPO_VIDEO_SEGUNDOS}s por vídeo\n"
            f"⏱️ Tempo estimado: ~{tempo_estimado_min:.1f} minutos\n"
            f"⚡ Iniciando coleta...",
            chat_id, msg_status.message_id
        )
    
    videos_processados = 0
    inicio = time.time()
    
    for campanha in todas_campanhas:
        uuid_camp = campanha.get('campaignUuid')
        request_id = campanha.get('requestId')
        videos = campanha.get('mainData', {}).get('media', [])
        
        for video in videos:
            uuid_media = video.get('uuid')
            
            try:
                requests.post(
                    f"{base_url}/adserver/tracker",
                    params={"e": "impression", "c": uuid_camp, "u": wallet, 
                           "requestId": request_id, "m": uuid_media},
                    headers=headers, timeout=2
                )
            except:
                pass
            
            if not is_auto:
                for seg in range(TEMPO_VIDEO_SEGUNDOS):
                    time.sleep(1)
                    if seg in [5, 10, 15, 20, 25]:
                        try:
                            bot.edit_message_text(
                                f"🎬 ASSISTINDO VÍDEO...\n"
                                f"📡 Operadora: 🔵 TIM\n"
                                f"🎬 Vídeo {videos_processados + 1}/{total_videos}\n"
                                f"⏱️ {seg}/{TEMPO_VIDEO_SEGUNDOS} segundos\n\n"
                                f"🛡️ Modo anti-ban ativo",
                                chat_id, msg_status.message_id
                            )
                        except:
                            pass
            else:
                time.sleep(TEMPO_VIDEO_SEGUNDOS)
            
            try:
                requests.post(
                    f"{base_url}/adserver/tracker",
                    params={"e": "complete", "c": uuid_camp, "u": wallet, 
                           "requestId": request_id, "m": uuid_media},
                    headers=headers, timeout=2
                )
            except:
                pass
            
            videos_processados += 1
            
            if not is_auto:
                progresso = barra_progresso_ultra(videos_processados, total_videos)
                tempo_decorrido = time.time() - inicio
                
                if videos_processados > 0:
                    tempo_medio = tempo_decorrido / videos_processados
                    tempo_restante = tempo_medio * (total_videos - videos_processados)
                else:
                    tempo_restante = 0
                
                status_msg = (
                    f"🚀 COLETANDO PONTOS TIM!\n"
                    f"📡 Operadora: 🔵 TIM\n"
                    f"{progresso}\n"
                    f"📊 {videos_processados}/{total_videos} vídeos\n"
                    f"⏱️ Decorrido: {tempo_decorrido/60:.1f} min\n"
                    f"⏳ Restante: {tempo_restante/60:.1f} min"
                )
                
                try:
                    bot.edit_message_text(status_msg, chat_id, msg_status.message_id)
                except:
                    pass
        
        try:
            requests.post(
                f"{base_url}/adserver/tracker",
                params={"e": "conversion", "c": uuid_camp, "u": wallet, "requestId": request_id},
                headers=headers, timeout=2
            )
        except:
            pass
    
    fim = time.time()
    tempo_total = fim - inicio
    pontos_coletados = videos_processados * get_pontos_por_video('tim')
    
    if chat_id in user_db:
        user = user_db[chat_id]
        if len(user['contas']) > conta_ativa:
            conta_atual = user['contas'][conta_ativa]
            pontos_atuais = conta_atual.get('pontos_total', 0)
            conta_atual['pontos_total'] = pontos_atuais + pontos_coletados
            conta_atual['pontos_hoje'] = pontos_coletados
            conta_atual['ultima_atualizacao'] = datetime.now()
            user_db[chat_id]['pontos_coletados'] = user.get('pontos_coletados', 0) + pontos_coletados
            user_db[chat_id]['total_farms'] = user.get('total_farms', 0) + 1
            user_db[chat_id]['ultima_coleta'] = datetime.now()
            data_manager.save_all_data()
    
    if not is_auto:
        try:
            progresso_final = barra_progresso_ultra(total_videos, total_videos)
            relatorio = (
                f"✔️ COLETA TIM COMPLETA!\n\n"
                f"📱 Conta: {telefone}\n"
                f"📡 Operadora: 🔵 TIM\n"
                f"🎯 Missões: {videos_processados}\n"
                f"💰 Pontos coletados: {pontos_coletados}\n"
                f"⏱️ Tempo total: {tempo_total/60:.1f} minutos\n"
                f"🛡️ Modo anti-ban respeitado\n"
                f"{progresso_final}\n\n"
                f"🎉 Pontos coletados com sucesso!"
            )
            bot.edit_message_text(relatorio, chat_id, msg_status.message_id)
            time.sleep(0.5)
            api_ver_saldo(chat_id)
        except Exception as e:
            bot.send_message(chat_id, f"✔️ Coleta TIM completa! {videos_processados} missões ({pontos_coletados} pontos) em {tempo_total/60:.1f}min")
    else:
        log_terminal(f"FARM AUTO TIM: {videos_processados} missões ({pontos_coletados} pontos) em {tempo_total/60:.1f}min")
    
    if chat_id in farm_status:
        del farm_status[chat_id]
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("farm_concluido", chat_id)

def api_ver_saldo(chat_id):
    if not verificar_licenca(chat_id): 
        return msg_licenca_expirada(chat_id)
    
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    operadora = conta.get('operadora', 'vivo')
    base_url = get_base_url(operadora)
    headers = get_headers_fast(operadora)
    token = conta.get('token')
    telefone = conta.get('telefone', 'N/A')
    
    try:
        headers["X-AUTHORIZATION"] = token
        
        operadora_nome = {'vivo': 'VIVO', 'claro': 'CLARO', 'tim': 'TIM'}.get(operadora, operadora)
        operadora_icon = {'vivo': '🟣', 'claro': '🔴', 'tim': '🔵'}.get(operadora, '📱')
        
        r = requests.get(f"{base_url}/hmld", headers=headers, timeout=5)
        if r.status_code == 200:
            d = r.json().get('wallet', {})
            
            pontos_total = conta.get('pontos_total', 0)
            pontos_hoje = conta.get('pontos_hoje', 0)
            
            msg = (
                f"💰 SALDO {operadora_nome}\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📱 Conta: {telefone}\n"
                f"📡 Operadora: {operadora_icon} {operadora_nome}\n"
                f"💎 Pontos atuais: {d.get('balance', 0)}\n"
                f"📈 Pontos hoje: {pontos_hoje}\n"
                f"🏆 Pontos totais: {pontos_total}\n"
                f"📅 Validade: {d.get('expirationDate', '').split('T')[0] if d.get('expirationDate') else 'Não informada'}"
            )
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(chat_id, msg, reply_markup=markup)
        else:
            pontos_total = conta.get('pontos_total', 0)
            pontos_hoje = conta.get('pontos_hoje', 0)
            
            msg = (
                f"💰 SALDO {operadora_nome}\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📱 Conta: {telefone}\n"
                f"📡 Operadora: {operadora_icon} {operadora_nome}\n"
                f"⚠️ Não foi possível obter saldo atual\n"
                f"📈 Pontos hoje: {pontos_hoje}\n"
                f"🏆 Pontos totais: {pontos_total}"
            )
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔄 Tentar novamente", callback_data="check_balance"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(chat_id, msg, reply_markup=markup)
    except Exception as e:
        pontos_total = conta.get('pontos_total', 0)
        pontos_hoje = conta.get('pontos_hoje', 0)
        
        error_msg = (
            f"💰 SALDO {operadora_nome.upper()}\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"📱 Conta: {telefone}\n"
            f"📡 Operadora: {operadora_icon} {operadora_nome}\n"
            f"⚠️ Erro ao verificar saldo: {str(e)[:100]}\n"
            f"📈 Pontos hoje: {pontos_hoje}\n"
            f"🏆 Pontos totais: {pontos_total}"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔄 Tentar novamente", callback_data="check_balance"))
        markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
        bot.send_message(chat_id, error_msg, reply_markup=markup)

def api_abrir_loja(chat_id):
    if not verificar_licenca(chat_id): 
        return msg_licenca_expirada(chat_id)
    
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    operadora = conta.get('operadora', 'vivo')
    base_url = get_base_url(operadora)
    headers = get_headers_fast(operadora)
    token = conta.get('token')
    
    try:
        headers["X-AUTHORIZATION"] = token
        r = requests.get(f"{base_url}/przl/v2", headers=headers, timeout=5)
        if r.status_code == 200:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for pkg in r.json().get('packages', []):
                bt_txt = f"📦 {pkg['name']} — 💎 {pkg['price']}"
                bt_dat = f"confirm_buy|{pkg['id']}|{pkg['price']}|{pkg['name']}"
                markup.add(types.InlineKeyboardButton(bt_txt, callback_data=bt_dat))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(chat_id, "🎁 Loja de Resgate:", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"❌ Erro ao abrir loja: {str(e)[:100]}")

def api_comprar(chat_id, pkg_id, nome):
    if not verificar_licenca(chat_id): 
        return msg_licenca_expirada(chat_id)
    
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        bot.send_message(chat_id, "❌ Nenhuma conta cadastrada.")
        return
    
    conta = contas[conta_ativa]
    operadora = conta.get('operadora', 'vivo')
    base_url = get_base_url(operadora)
    headers = get_headers_fast(operadora)
    token = conta.get('token')
    
    msg = bot.send_message(chat_id, f"💳 Comprando {nome}...")
    try:
        headers["X-AUTHORIZATION"] = token
        r = requests.post(f"{base_url}/wtdr", 
                         json={"packageId": int(pkg_id), "destinationMsisdn": None}, 
                         headers=headers, timeout=10)
        
        if r.status_code == 200 and r.json().get("code") == "SUCCESS":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.edit_message_text(f"✔️ SUCESSO! {nome} resgatado.", chat_id, msg.message_id, reply_markup=markup)
            data_manager.send_json_on_user_action("resgate_efetuado", chat_id)
            api_ver_saldo(chat_id)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.edit_message_text(f"❌ Erro na compra: {r.text[:100]}", chat_id, msg.message_id, reply_markup=markup)
    except Exception as e:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
        bot.edit_message_text(f"❌ Erro: {str(e)[:100]}", chat_id, msg.message_id, reply_markup=markup)

# ==============================================================================
# 🤖 FUNÇÕES DE CONFIGURAÇÃO
# ==============================================================================
def toggle_auto_farm(chat_id):
    user = user_db.get(chat_id, {})
    
    if chat_id not in user_db:
        user_db[chat_id] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
        data_manager.save_all_data()
    
    config = user_db[chat_id].setdefault('config', {'auto_farm': False})
    config['auto_farm'] = not config.get('auto_farm', False)
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("auto_farm_toggle", chat_id)
    
    if chat_id in auto_farm_jobs:
        try:
            scheduler.remove_job(auto_farm_jobs[chat_id])
            del auto_farm_jobs[chat_id]
            data_manager.save_all_data()
        except:
            pass
    
    if config['auto_farm']:
        contas = user_db[chat_id].get('contas', [])
        if not contas:
            config['auto_farm'] = False
            data_manager.save_all_data()
            bot.send_message(chat_id, "❌ Não é possível ativar o farm automático sem contas cadastradas.")
            return False
        
        job = scheduler.add_job(
            lambda: auto_farm_task(chat_id),
            'cron', hour=0, minute=10,
            id=f'auto_farm_{chat_id}'
        )
        auto_farm_jobs[chat_id] = job.id
        data_manager.save_all_data()
        bot.send_message(chat_id, "✔️ Bot automático ATIVADO!\n\n🤖 O bot irá coletar pontos automaticamente todos os dias às 00:10.")
        return True
    else:
        bot.send_message(chat_id, "❌ Bot automático DESATIVADO!")
        return False

def auto_farm_task(chat_id):
    log_terminal(f"Executando bot automático para chat_id: {chat_id}")
    try:
        api_executar_farm(chat_id, is_auto=True)
    except Exception as e:
        log_terminal(f"Erro no farm automático: {e}")

def adicionar_conta(chat_id, telefone, token, wallet, operadora='vivo'):
    if chat_id not in user_db:
        user_db[chat_id] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
    
    contas = user_db[chat_id].get('contas', [])
    
    for conta in contas:
        if conta.get('telefone') == telefone and conta.get('operadora') == operadora:
            return False, "Esta conta já está cadastrada!"
    
    nova_conta = {
        'telefone': telefone,
        'token': token,
        'wallet': wallet,
        'operadora': operadora,
        'data_cadastro': datetime.now(),
        'pontos_total': 0,
        'pontos_hoje': 0
    }
    
    contas.append(nova_conta)
    user_db[chat_id]['contas'] = contas
    
    if len(contas) == 1:
        user_db[chat_id]['conta_ativa'] = 0
    
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("conta_adicionada", chat_id)
    return True, f"Conta {operadora.upper()} adicionada com sucesso!"

def remover_conta_ativa(chat_id):
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    if not contas:
        return False, "Nenhuma conta para remover!", False
    
    conta_removida = contas.pop(conta_ativa)
    operadora = conta_removida.get('operadora', 'vivo')
    
    if conta_ativa >= len(contas):
        user_db[chat_id]['conta_ativa'] = max(0, len(contas) - 1)
    
    user_db[chat_id]['contas'] = contas
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("conta_removida", chat_id)
    
    if len(contas) == 0:
        return True, f"✅ Conta {conta_removida.get('telefone')} ({operadora.upper()}) removida com sucesso!\n\n🚪 Você não possui mais contas cadastradas.\n\n👉 Faça login novamente para continuar usando o bot.", True
    
    return True, f"✅ Conta {conta_removida.get('telefone')} ({operadora.upper()}) removida com sucesso!", False

def selecionar_conta(chat_id, indice):
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    
    if not contas:
        return False, "Nenhuma conta cadastrada!"
    if indice < 0 or indice >= len(contas):
        return False, "Índice inválido!"
    
    user_db[chat_id]['conta_ativa'] = indice
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("conta_selecionada", chat_id)
    
    conta = contas[indice]
    operadora = conta.get('operadora', 'vivo')
    return True, f"Conta {conta.get('telefone')} ({operadora.upper()}) selecionada como ativa!"

def verificar_cupom_valido(codigo, chat_id):
    if codigo not in cupons_db:
        return False, "Cupom inválido ou inexistente!"
    
    cupom = cupons_db[codigo]
    resgatado_por = cupom.get('resgatado_por', [])
    
    if chat_id in resgatado_por:
        return False, "Você já resgatou este cupom anteriormente!"
    
    if len(resgatado_por) >= cupom['limite']:
        if len(resgatado_por) >= cupom['limite']:
            del cupons_db[codigo]
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("cupom_expirado", codigo)
        return False, "Este cupom atingiu o limite máximo de resgates!"
    
    return True, cupom

# ==============================================================================
# 💰 SISTEMA DE PAGAMENTO PIX REAL
# ==============================================================================
def gerar_pagamento_pix(chat_id):
    try:
        descricao = f"Licença {DIAS_LICENCA} dias - JADIEL MB"
        pagamento = criar_pagamento_mercadopago(chat_id, VALOR_LICENCA, descricao)
        
        if not pagamento:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔄 TENTAR NOVAMENTE", callback_data="gerar_pagamento_pix"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar à Licença", callback_data="my_license"))
            bot.send_message(chat_id, "❌ Erro ao gerar pagamento. Tente novamente ou entre em contato com o suporte: @JADIEL_TM", reply_markup=markup)
            return
        
        payment_id = pagamento['payment_id']
        qr_code_base64 = pagamento.get('qr_code_base64')
        chave_pix = pagamento.get('chave_pix', '')
        data_expiracao = pagamento['data_expiracao']
        
        mensagem = (
            f"💰 PAGAMENTO PIX - R$ {VALOR_LICENCA:.2f}\n\n"
            f"📅 Validade: {DIAS_LICENCA} dias\n"
            f"⏰ Expira: {data_expiracao.strftime('%d/%m/%Y às %H:%M')}\n"
            f"🆔 ID do pagamento: `{payment_id}`\n\n"
        )
        
        if qr_code_base64:
            qr_image = base64_to_image(qr_code_base64)
            if qr_image:
                mensagem += "📱 Escaneie o QR Code abaixo com seu app de banco:\n\n"
                mensagem += f"📋 Chave PIX (copia e cola):\n`{chave_pix}`\n\n⚠️ Após o pagamento, clique em 'JÁ PAGUEI' para confirmar."
                bot.send_photo(chat_id, qr_image, caption=mensagem, parse_mode='Markdown', reply_markup=menu_pagamento_pix(payment_id))
            else:
                mensagem += f"📋 Chave PIX (copia e cola):\n`{chave_pix}`\n\n⚠️ Após o pagamento, clique em 'JÁ PAGUEI' para confirmar."
                bot.send_message(chat_id, mensagem, parse_mode='Markdown', reply_markup=menu_pagamento_pix(payment_id))
        else:
            mensagem += f"📋 Chave PIX (copia e cola):\n`{chave_pix}`\n\n⚠️ Após o pagamento, clique em 'JÁ PAGUEI' para confirmar."
            bot.send_message(chat_id, mensagem, parse_mode='Markdown', reply_markup=menu_pagamento_pix(payment_id))
        
        log_terminal(f"Pagamento PIX gerado para chat_id {chat_id}: {payment_id}")
    except Exception as e:
        log_terminal(f"❌ Erro ao gerar pagamento PIX: {e}")
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔄 TENTAR NOVAMENTE", callback_data="gerar_pagamento_pix"))
        markup.add(types.InlineKeyboardButton("🔙 Voltar à Licença", callback_data="my_license"))
        bot.send_message(chat_id, f"❌ Erro ao gerar pagamento: {str(e)[:100]}\n\nTente novamente ou entre em contato com o suporte: @JADIEL_TM", reply_markup=markup)

def gerar_pagamento_pix_promocional(chat_id, valor, dias, promo_id):
    try:
        descricao = f"Licença Promoção {dias} dias - JADIEL MB VIP"
        pagamento = criar_pagamento_mercadopago(chat_id, valor, descricao)
        
        if not pagamento:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🔄 TENTAR NOVAMENTE", callback_data=f"promo_pagar|{promo_id}"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(chat_id, "❌ Erro ao gerar pagamento. Tente novamente ou entre em contato com o suporte: @JADIEL_TM", reply_markup=markup)
            return
        
        payment_id = pagamento['payment_id']
        qr_code_base64 = pagamento.get('qr_code_base64')
        chave_pix = pagamento.get('chave_pix', '')
        data_expiracao = pagamento['data_expiracao']
        
        mensagem = (
            f"💰 PAGAMENTO PIX PROMOCIONAL - R$ {valor:.2f}\n\n"
            f"📅 Validade: {dias} dias\n"
            f"⏰ Expira: {data_expiracao.strftime('%d/%m/%Y às %H:%M')}\n"
            f"🆔 ID do pagamento: `{payment_id}`\n"
            f"🎁 Promoção VIP ativa!\n\n"
        )
        
        if qr_code_base64:
            qr_image = base64_to_image(qr_code_base64)
            if qr_image:
                mensagem += "📱 Escaneie o QR Code abaixo com seu app de banco:\n\n"
                mensagem += f"📋 Chave PIX (copia e cola):\n`{chave_pix}`\n\n⚠️ Após o pagamento, clique em 'JÁ PAGUEI' para confirmar."
                bot.send_photo(chat_id, qr_image, caption=mensagem, parse_mode='Markdown', reply_markup=menu_pagamento_promocao(payment_id, promo_id))
            else:
                mensagem += f"📋 Chave PIX (copia e cola):\n`{chave_pix}`\n\n⚠️ Após o pagamento, clique em 'JÁ PAGUEI' para confirmar."
                bot.send_message(chat_id, mensagem, parse_mode='Markdown', reply_markup=menu_pagamento_promocao(payment_id, promo_id))
        else:
            mensagem += f"📋 Chave PIX (copia e cola):\n`{chave_pix}`\n\n⚠️ Após o pagamento, clique em 'JÁ PAGUEI' para confirmar."
            bot.send_message(chat_id, mensagem, parse_mode='Markdown', reply_markup=menu_pagamento_promocao(payment_id, promo_id))
        
        log_terminal(f"Pagamento PIX promocional gerado para chat_id {chat_id}: {payment_id} - Promoção: {promo_id}")
        data_manager.send_json_on_user_action("pagamento_promocao", chat_id)
    except Exception as e:
        log_terminal(f"❌ Erro ao gerar pagamento PIX promocional: {e}")
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔄 TENTAR NOVAMENTE", callback_data=f"promo_pagar|{promo_id}"))
        markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
        bot.send_message(chat_id, f"❌ Erro ao gerar pagamento: {str(e)[:100]}\n\nTente novamente ou entre em contato com o suporte: @JADIEL_TM", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("verificar_pagamento|"))
def verificar_pagamento_pix_callback(call):
    try:
        payment_id = call.data.split("|")[1]
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id, "🔍 Verificando pagamento...")
        sucesso, mensagem = verificar_pagamento(payment_id)
        
        if sucesso:
            if chat_id not in user_db:
                user_db[chat_id] = {
                    'contas': [], 'conta_ativa': 0,
                    'config': {'auto_farm': False},
                    'license_date': None,
                    'first_seen': datetime.now()
                }
            
            user = user_db[chat_id]
            validade_atual = user.get('license_date')
            
            if validade_atual and validade_atual > datetime.now():
                nova_validade = validade_atual + timedelta(days=DIAS_LICENCA)
            else:
                nova_validade = datetime.now() + timedelta(days=DIAS_LICENCA)
            
            user_db[chat_id]['license_date'] = nova_validade
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("licenca_atualizada", chat_id)
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🎉 ACESSAR BOT", callback_data="back_home"))
            
            try:
                bot.edit_message_caption(
                    chat_id=chat_id, message_id=call.message.message_id,
                    caption=f"✔️ PAGAMENTO CONFIRMADO!\n\nSua licença foi renovada por {DIAS_LICENCA} dias!\n📅 Nova validade: {formatar_data(nova_validade)}\n🎉 Obrigado pela confiança!\n\nAgora você pode continuar usando o bot normalmente.",
                    reply_markup=markup
                )
            except:
                bot.send_message(chat_id, f"✔️ PAGAMENTO CONFIRMADO!\n\nSua licença foi renovada por {DIAS_LICENCA} dias!\n📅 Nova validade: {formatar_data(nova_validade)}\n🎉 Obrigado pela confiança!\n\nAgora você pode continuar usando o bot normalmente.", reply_markup=markup)
        else:
            try:
                bot.edit_message_caption(
                    chat_id=chat_id, message_id=call.message.message_id,
                    caption=f"❌ {mensagem}\n\n⚠️ Se você já realizou o pagamento, aguarde alguns minutos e tente novamente.\n⏰ O pagamento pode levar alguns minutos para ser processado.\n🔍 Se o problema persistir, entre em contato com o suporte: @JADIEL_TM",
                    reply_markup=menu_pagamento_pix(payment_id)
                )
            except:
                bot.send_message(chat_id, f"❌ {mensagem}\n\n⚠️ Se você já realizou o pagamento, aguarde alguns minutos e tente novamente.\n⏰ O pagamento pode levar alguns minutos para ser processado.\n🔍 Se o problema persistir, entre em contato com o suporte: @JADIEL_TM", reply_markup=menu_pagamento_pix(payment_id))
    except Exception as e:
        log_terminal(f"❌ Erro ao verificar pagamento PIX: {e}")
        try:
            bot.send_message(call.message.chat.id, f"❌ Erro ao verificar pagamento: {str(e)[:100]}\n\nTente novamente ou entre em contato com o suporte: @JADIEL_TM", reply_markup=menu_pagamento_pix(payment_id))
        except:
            pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("verificar_pagamento_promo|"))
def verificar_pagamento_promo_callback(call):
    try:
        _, payment_id, promo_id = call.data.split("|")
        chat_id = call.message.chat.id
        bot.answer_callback_query(call.id, "🔍 Verificando pagamento...")
        sucesso, mensagem = verificar_pagamento(payment_id)
        
        if sucesso:
            if chat_id not in user_db:
                user_db[chat_id] = {
                    'contas': [], 'conta_ativa': 0,
                    'config': {'auto_farm': False},
                    'license_date': None,
                    'first_seen': datetime.now()
                }
            
            user = user_db[chat_id]
            validade_atual = user.get('license_date')
            
            dias = DIAS_LICENCA
            if promo_id in promocoes_ativas:
                dias = promocoes_ativas[promo_id]['dias']
            
            if validade_atual and validade_atual > datetime.now():
                nova_validade = validade_atual + timedelta(days=dias)
            else:
                nova_validade = datetime.now() + timedelta(days=dias)
            
            user_db[chat_id]['license_date'] = nova_validade
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("licenca_atualizada_promo", chat_id)
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🎉 ACESSAR BOT", callback_data="back_home"))
            
            try:
                bot.edit_message_caption(
                    chat_id=chat_id, message_id=call.message.message_id,
                    caption=f"✔️ PAGAMENTO CONFIRMADO!\n\n🎁 PROMOÇÃO VIP ATIVADA!\nSua licença foi renovada por {dias} dias!\n📅 Nova validade: {formatar_data(nova_validade)}\n🎉 Obrigado pela confiança!\n\nAgora você pode continuar usando o bot normalmente.",
                    reply_markup=markup
                )
            except:
                bot.send_message(chat_id, f"✔️ PAGAMENTO CONFIRMADO!\n\n🎁 PROMOÇÃO VIP ATIVADA!\nSua licença foi renovada por {dias} dias!\n📅 Nova validade: {formatar_data(nova_validade)}\n🎉 Obrigado pela confiança!\n\nAgora você pode continuar usando o bot normalmente.", reply_markup=markup)
        else:
            try:
                bot.edit_message_caption(
                    chat_id=chat_id, message_id=call.message.message_id,
                    caption=f"❌ {mensagem}\n\n⚠️ Se você já realizou o pagamento, aguarde alguns minutos e tente novamente.\n⏰ O pagamento pode levar alguns minutos para ser processado.\n🔍 Se o problema persistir, entre em contato com o suporte: @JADIEL_TM",
                    reply_markup=menu_pagamento_promocao(payment_id, promo_id)
                )
            except:
                bot.send_message(chat_id, f"❌ {mensagem}\n\n⚠️ Se você já realizou o pagamento, aguarde alguns minutos e tente novamente.\n⏰ O pagamento pode levar alguns minutos para ser processado.\n🔍 Se o problema persistir, entre em contato com o suporte: @JADIEL_TM", reply_markup=menu_pagamento_promocao(payment_id, promo_id))
    except Exception as e:
        log_terminal(f"❌ Erro ao verificar pagamento promo: {e}")
        try:
            bot.send_message(call.message.chat.id, f"❌ Erro ao verificar pagamento: {str(e)[:100]}\n\nTente novamente ou entre em contato com o suporte: @JADIEL_TM", reply_markup=menu_pagamento_promocao(payment_id, promo_id))
        except:
            pass

# ==============================================================================
# 🤖 FUNÇÃO PARA ENVIAR MÍDIA PARA TODOS
# ==============================================================================
def enviar_midia_para_todos(chat_id, tipo, conteudo=None, file_id=None):
    try:
        total_usuarios = len(user_db)
        enviados = 0
        falhas = 0
        
        log_terminal(f"🚀 ENVIANDO {tipo.upper()} PARA {total_usuarios} USUÁRIOS")
        msg_status = bot.send_message(chat_id, f"📤 Enviando {tipo} para {total_usuarios} usuários...")
        last_media_msgs.clear()
        
        for cid in list(user_db.keys()):
            try:
                if cid == chat_id:
                    continue
                
                if tipo == 'texto':
                    m = bot.send_message(cid, f"📢 MENSAGEM IMPORTANTE 📢\n\n{conteudo}\n\n— Equipe JADIEL MB")
                    last_media_msgs.append((cid, m.message_id))
                elif tipo == 'imagem':
                    m = bot.send_photo(cid, file_id, caption=conteudo if conteudo else "")
                    last_media_msgs.append((cid, m.message_id))
                elif tipo == 'video':
                    m = bot.send_video(cid, file_id, caption=conteudo if conteudo else "")
                    last_media_msgs.append((cid, m.message_id))
                
                enviados += 1
                if enviados % 10 == 0:
                    log_terminal(f"📊 Progresso: {enviados}/{total_usuarios} enviados")
                time.sleep(0.05)
            except Exception as e:
                falhas += 1
                log_terminal(f"❌ Erro ao enviar para {cid}: {e}")
        
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("midia_enviada", chat_id)
        
        resultado = f"✔️ {tipo.upper()} ENVIADO COM SUCESSO!\n\n📊 Estatísticas:\n✔️ Enviados: {enviados}\n❌ Falhas: {falhas}\n👥 Total de usuários: {total_usuarios}"
        bot.edit_message_text(resultado, chat_id, msg_status.message_id)
        log_terminal(resultado)
        return True
    except Exception as e:
        log_terminal(f"❌ Erro geral em enviar_midia_para_todos: {e}")
        bot.send_message(chat_id, f"❌ Erro ao enviar {tipo}: {str(e)[:100]}")
        return False

# ==============================================================================
# 🎉 SISTEMA DE PROMOÇÃO VIP
# ==============================================================================
def enviar_promocao_para_todos(admin_chat_id, promo_id, preco, dias, horas_duracao, texto=None, imagem=None):
    mensagens_enviadas = []
    total_usuarios = len(user_db)
    enviados = 0
    falhas = 0
    
    log_terminal(f"🚀 ENVIANDO PROMOÇÃO VIP {promo_id} PARA {total_usuarios} USUÁRIOS")
    
    for chat_id in list(user_db.keys()):
        try:
            if chat_id == admin_chat_id:
                continue
            
            if imagem:
                legenda = texto if texto else ""
                legenda += f"\n\n💰 PREÇO PROMOCIONAL: R$ {preco:.2f}\n📅 DIAS: {dias}\n⏰ PROMOÇÃO VÁLIDA POR: {horas_duracao} HORAS\n\n🎁 NÃO PERCA ESTA OPORTUNIDADE!"
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(f"💳 PAGAR R$ {preco:.2f} - {dias} DIAS", callback_data=f"promo_pagar|{promo_id}"))
                m = bot.send_photo(chat_id, imagem, caption=legenda, reply_markup=markup)
            else:
                mensagem = texto if texto else ""
                mensagem += f"\n\n💰 PREÇO PROMOCIONAL: R$ {preco:.2f}\n📅 DIAS: {dias}\n⏰ PROMOÇÃO VÁLIDA POR: {horas_duracao} HORAS\n\n🎁 NÃO PERCA ESTA OPORTUNIDADE!"
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(f"💳 PAGAR R$ {preco:.2f} - {dias} DIAS", callback_data=f"promo_pagar|{promo_id}"))
                m = bot.send_message(chat_id, mensagem, reply_markup=markup)
            
            mensagens_enviadas.append((chat_id, m.message_id))
            enviados += 1
            time.sleep(0.05)
        except Exception as e:
            falhas += 1
            log_terminal(f"❌ Erro ao enviar promoção para {chat_id}: {e}")
    
    log_terminal(f"📊 Promoção {promo_id}: {enviados} enviados, {falhas} falhas")
    return mensagens_enviadas

def agendar_exclusao_promocao(promo_id, horas_duracao):
    try:
        job_id = f"excluir_promo_{promo_id}"
        scheduler.add_job(
            excluir_promocao, 'date',
            run_date=datetime.now() + timedelta(hours=horas_duracao),
            args=[promo_id], id=job_id
        )
        log_terminal(f"⏰ Exclusão da promoção {promo_id} agendada para {horas_duracao} horas")
        return job_id
    except Exception as e:
        log_terminal(f"❌ Erro ao agendar exclusão da promoção: {e}")
        return None

def excluir_promocao(promo_id):
    try:
        if promo_id not in promocoes_ativas:
            log_terminal(f"❌ Promoção {promo_id} não encontrada para exclusão")
            return
        
        promocao = promocoes_ativas[promo_id]
        mensagens = promocao.get('mensagens', [])
        
        excluidos = 0
        falhas = 0
        
        for chat_id, message_id in mensagens:
            try:
                bot.delete_message(chat_id, message_id)
                excluidos += 1
            except Exception as e:
                falhas += 1
                log_terminal(f"❌ Erro ao excluir mensagem da promoção {promo_id} para {chat_id}: {e}")
        
        job_id = f"excluir_promo_{promo_id}"
        try:
            scheduler.remove_job(job_id)
        except:
            pass
        
        del promocoes_ativas[promo_id]
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("promocao_excluida", promo_id)
        log_terminal(f"🗑️ Promoção {promo_id} excluída: {excluidos} mensagens removidas, {falhas} falhas")
        return True
    except Exception as e:
        log_terminal(f"❌ Erro ao excluir promoção {promo_id}: {e}")
        return False

def recriar_agendamentos_promocoes():
    try:
        log_terminal("🔄 Recriando agendamentos de promoções...")
        for promo_id, promocao in list(promocoes_ativas.items()):
            try:
                data_criacao = promocao.get('data_criacao', datetime.now())
                horas_duracao = promocao.get('horas_duracao', 24)
                tempo_decorrido = (datetime.now() - data_criacao).total_seconds() / 3600
                tempo_restante = horas_duracao - tempo_decorrido
                
                if tempo_restante > 0:
                    agendar_exclusao_promocao(promo_id, tempo_restante)
                    log_terminal(f"  ✔️ Promoção {promo_id}: {tempo_restante:.1f}h restantes")
                else:
                    excluir_promocao(promo_id)
                    log_terminal(f"  🗑️ Promoção {promo_id} expirada, excluindo...")
            except Exception as e:
                log_terminal(f"  ❌ Erro ao processar promoção {promo_id}: {e}")
        log_terminal(f"✔️ {len(promocoes_ativas)} promoções processadas")
    except Exception as e:
        log_terminal(f"❌ Erro ao recriar agendamentos de promoções: {e}")
        
        # ==============================================================================
# 📊 COMANDO PARA VERIFICAR ARMAZENAMENTO
# ==============================================================================
@bot.message_handler(commands=['armazenamento'])
def comando_armazenamento(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        data_dir = data_manager.data_dir
        if not os.path.exists(data_dir):
            bot.reply_to(message, f"❌ Diretório não existe: {data_dir}")
            return
        
        arquivos = []
        tamanho_total = 0
        
        for filename in os.listdir(data_dir):
            filepath = os.path.join(data_dir, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath) / 1024
                arquivos.append(f"• {filename}: {size:.2f} KB")
                tamanho_total += size
        
        backup_dir = os.path.join(data_dir, 'backups')
        backups = []
        if os.path.exists(backup_dir):
            for filename in os.listdir(backup_dir):
                filepath = os.path.join(backup_dir, filename)
                if os.path.isfile(filepath):
                    size = os.path.getsize(filepath) / 1024
                    backups.append(f"• {filename}: {size:.2f} KB")
                    tamanho_total += size
        
        mensagem = f"📁 ARMAZENAMENTO DO BOT\n\n📂 Diretório: {data_dir}\n💾 Tamanho total: {tamanho_total:.2f} KB\n\n"
        if arquivos:
            mensagem += "📄 ARQUIVOS PRINCIPAIS:\n" + "\n".join(arquivos) + "\n\n"
        if backups:
            mensagem += "💾 BACKUPS:\n" + "\n".join(backups[:10])
            if len(backups) > 10:
                mensagem += f"\n... e mais {len(backups) - 10} backups"
        bot.reply_to(message, mensagem)
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao verificar armazenamento: {str(e)[:100]}")

# ==============================================================================
# 🔄 COMANDO /backup_completo (RESTAURAÇÃO TOTAL)
# ==============================================================================
@bot.message_handler(commands=['backup_completo'])
def comando_backup_completo(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        admin_state[message.chat.id] = {'step': 'wait_backup_completo'}
        bot.reply_to(
            message,
            "🔄 *BACKUP COMPLETO*\n\n"
            "📤 Por favor, envie o arquivo `.json` de backup completo.\n\n"
            "⚠️ *ATENÇÃO:* O bot irá restaurar TODOS os dados do arquivo enviado, incluindo:\n"
            "• 👥 Usuários e suas licenças\n"
            "• 📱 Contas cadastradas\n"
            "• 🎫 Cupons\n"
            "• 💰 Pagamentos\n"
            "• 🎉 Promoções\n"
            "• 🤝 Afiliados e códigos\n"
            "• ⚙️ Configurações\n"
            "• 📢 Histórico de broadcast/mídia\n\n"
            "📁 Nome esperado: `backup_completo.json`\n\n"
            "❌ Para cancelar, digite: *cancelar*",
            parse_mode='Markdown'
        )
        log_terminal(f"🔄 Admin iniciou /backup_completo")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)[:200]}")


@bot.message_handler(content_types=['document'], func=lambda m: m.chat.id == ADMIN_ID and m.chat.id in admin_state and admin_state[m.chat.id] is not None and admin_state[m.chat.id].get('step') == 'wait_backup_completo')
def handle_backup_completo_file(message):
    chat_id = message.chat.id
    try:
        if not message.document.file_name.endswith('.json'):
            bot.reply_to(message, "❌ O arquivo deve ser um JSON (.json)")
            return
        
        bot.reply_to(message, f"📥 Baixando backup completo: {message.document.file_name}...")
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        backup_data = json.loads(downloaded_file.decode('utf-8'))
        
        bot.reply_to(message, "🔄 Restaurando dados...")
        
        restaurados = []
        
        if 'user_db' in backup_data:
            new_user_db = data_manager.deserialize_datetime(backup_data['user_db'])
            data_manager.user_db.clear()
            data_manager.user_db.update(new_user_db)
            restaurados.append(f"👥 Usuários: {len(data_manager.user_db)}")
        
        if 'cupons_db' in backup_data:
            new_cupons = data_manager.deserialize_datetime(backup_data['cupons_db'])
            data_manager.cupons_db.clear()
            data_manager.cupons_db.update(new_cupons)
            restaurados.append(f"🎫 Cupons: {len(data_manager.cupons_db)}")
        
        if 'username_to_id' in backup_data:
            data_manager.username_to_id.clear()
            data_manager.username_to_id.update(backup_data['username_to_id'])
            restaurados.append(f"📛 Usernames: {len(data_manager.username_to_id)}")
        
        if 'pagamentos_pendentes' in backup_data:
            new_pagamentos = data_manager.deserialize_datetime(backup_data['pagamentos_pendentes'])
            data_manager.pagamentos_pendentes.clear()
            data_manager.pagamentos_pendentes.update(new_pagamentos)
            restaurados.append(f"💰 Pagamentos: {len(data_manager.pagamentos_pendentes)}")
        
        if 'promocoes_ativas' in backup_data:
            new_promocoes = data_manager.deserialize_datetime(backup_data['promocoes_ativas'])
            data_manager.promocoes_ativas.clear()
            data_manager.promocoes_ativas.update(new_promocoes)
            restaurados.append(f"🎉 Promoções: {len(data_manager.promocoes_ativas)}")
        
        if 'afiliados_db' in backup_data:
            new_afiliados = data_manager.deserialize_datetime(backup_data['afiliados_db'])
            data_manager.afiliados_db.clear()
            data_manager.afiliados_db.update(new_afiliados)
            restaurados.append(f"🤝 Afiliados: {len(data_manager.afiliados_db)}")
        
        if 'afiliado_codigo_to_user' in backup_data:
            data_manager.afiliado_codigo_to_user.clear()
            data_manager.afiliado_codigo_to_user.update(backup_data['afiliado_codigo_to_user'])
            restaurados.append(f"🔗 Códigos de afiliado: {len(data_manager.afiliado_codigo_to_user)}")
        
        if 'auto_farm_jobs' in backup_data:
            data_manager.auto_farm_jobs.clear()
            data_manager.auto_farm_jobs.update(backup_data['auto_farm_jobs'])
            restaurados.append(f"🤖 Jobs automáticos: {len(data_manager.auto_farm_jobs)}")
        
        if 'last_broadcast_msgs' in backup_data:
            data_manager.last_broadcast_msgs.clear()
            data_manager.last_broadcast_msgs.extend(backup_data['last_broadcast_msgs'])
            restaurados.append(f"📢 Broadcasts: {len(data_manager.last_broadcast_msgs)}")
        
        if 'last_media_msgs' in backup_data:
            data_manager.last_media_msgs.clear()
            data_manager.last_media_msgs.extend(backup_data['last_media_msgs'])
            restaurados.append(f"🎬 Mídias: {len(data_manager.last_media_msgs)}")
        
        data_manager.save_all_data()
        data_manager.send_all_json_to_channel(force_send=True, reason="Backup completo restaurado manualmente")
        
        admin_state.pop(chat_id, None)
        
        relatorio = "✅ *BACKUP COMPLETO RESTAURADO COM SUCESSO!*\n\n"
        relatorio += "📊 *Dados restaurados:*\n"
        for item in restaurados:
            relatorio += f"✔️ {item}\n"
        relatorio += "\n💾 Todos os dados foram salvos localmente.\n"
        relatorio += "📤 Backup enviado para o canal de backups.\n\n"
        relatorio += "🎉 O bot está funcionando com os dados restaurados!"
        
        bot.reply_to(message, relatorio, parse_mode='Markdown')
        
        log_terminal(f"✅ BACKUP COMPLETO RESTAURADO:")
        for item in restaurados:
            log_terminal(f"   {item}")
        
        data_manager.send_json_on_user_action("backup_completo_restaurado", chat_id)
        
    except json.JSONDecodeError:
        bot.reply_to(message, "❌ Arquivo JSON inválido! Verifique se o arquivo está no formato correto.")
        admin_state.pop(chat_id, None)
    except Exception as e:
        log_terminal(f"❌ Erro ao restaurar backup completo: {e}")
        bot.reply_to(message, f"❌ Erro ao restaurar backup: {str(e)[:300]}")
        admin_state.pop(chat_id, None)


# ==============================================================================
# 📋 COMANDOS DE ADMIN PARA BACKUP E RESTAURAÇÃO
# ==============================================================================
@bot.message_handler(commands=['enviar_dados_agora'])
def enviar_dados_agora(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        bot.reply_to(message, "📤 Enviando dados para o canal...")
        data_manager.send_all_json_to_channel(force_send=True, reason="Comando manual do admin")
        bot.reply_to(message, "✔️ Dados enviados com sucesso para o canal!")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar dados: {str(e)[:100]}")

@bot.message_handler(commands=['restaurar_backup'])
def comando_restaurar_backup(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        bot.reply_to(message, "🔄 Restaurando backup do canal...")
        if data_manager.restaurar_backup_manual(chat_id=message.chat.id):
            bot.reply_to(message, "✅ Backup restaurado com sucesso!")
        else:
            bot.reply_to(message, "❌ Falha ao restaurar backup.")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao restaurar backup: {str(e)[:100]}")

# ==============================================================================
# 📤 COMANDOS PARA ENVIAR ARQUIVOS MANUALMENTE
# ==============================================================================
@bot.message_handler(commands=['enviar_json'])
def enviar_json_manual(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        if not message.document:
            bot.reply_to(message, "❌ Por favor, envie um arquivo JSON como documento.")
            return
        file_name = message.document.file_name
        if not file_name.endswith('.json'):
            bot.reply_to(message, "❌ O arquivo deve ser um JSON (.json)")
            return
        bot.reply_to(message, f"📥 Baixando {file_name}...")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join(data_manager.data_dir, file_name)
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        bot.reply_to(message, f"✅ Arquivo {file_name} salvo em:\n{file_path}")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)[:200]}")

@bot.message_handler(commands=['listar_json'])
def listar_json_disponiveis(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        data_dir = data_manager.data_dir
        json_files = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                size_kb = os.path.getsize(file_path) / 1024
                json_files.append(f"• {filename} ({size_kb:.2f} KB)")
        if not json_files:
            bot.reply_to(message, "📭 Nenhum arquivo JSON encontrado.")
            return
        mensagem = "📄 ARQUIVOS JSON DISPONÍVEIS:\n\n" + "\n".join(json_files) + f"\n\n📁 Diretório: {data_dir}"
        bot.reply_to(message, mensagem)
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)[:200]}")

@bot.message_handler(commands=['carregar_json'])
def carregar_json_especifico(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        partes = message.text.split()
        if len(partes) < 2:
            bot.reply_to(message, "❌ Use: /carregar_json nome_arquivo.json\n\nExemplo: /carregar_json user_db.json")
            return
        file_name = partes[1].strip()
        if not file_name.endswith('.json'):
            file_name += '.json'
        file_path = os.path.join(data_manager.data_dir, file_name)
        if not os.path.exists(file_path):
            bot.reply_to(message, f"❌ Arquivo {file_name} não encontrado.")
            return
        bot.reply_to(message, f"📖 Carregando {file_name}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if file_name == 'user_db.json':
            new_data = data_manager.deserialize_datetime(data)
            data_manager.user_db.clear()
            data_manager.user_db.update(new_data)
            bot.reply_to(message, f"✅ user_db.json carregado! {len(data_manager.user_db)} usuários")
        elif file_name == 'cupons_db.json':
            new_data = data_manager.deserialize_datetime(data)
            data_manager.cupons_db.clear()
            data_manager.cupons_db.update(new_data)
            bot.reply_to(message, f"✅ cupons_db.json carregado! {len(data_manager.cupons_db)} cupons")
        elif file_name == 'pagamentos_pendentes.json':
            new_data = data_manager.deserialize_datetime(data)
            data_manager.pagamentos_pendentes.clear()
            data_manager.pagamentos_pendentes.update(new_data)
            bot.reply_to(message, f"✅ pagamentos_pendentes.json carregado! {len(data_manager.pagamentos_pendentes)} pagamentos")
        elif file_name == 'promocoes_ativas.json':
            new_data = data_manager.deserialize_datetime(data)
            data_manager.promocoes_ativas.clear()
            data_manager.promocoes_ativas.update(new_data)
            bot.reply_to(message, f"✅ promocoes_ativas.json carregado! {len(data_manager.promocoes_ativas)} promoções")
        elif file_name == 'afiliados_db.json':
            new_data = data_manager.deserialize_datetime(data)
            data_manager.afiliados_db.clear()
            data_manager.afiliados_db.update(new_data)
            bot.reply_to(message, f"✅ afiliados_db.json carregado! {len(data_manager.afiliados_db)} afiliados")
        else:
            bot.reply_to(message, f"✅ {file_name} carregado, mas não atribuído a nenhum banco de dados específico.")
        data_manager.save_all_data()
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao carregar JSON: {str(e)[:200]}")

@bot.message_handler(commands=['forcar_restauracao'])
def forcar_restauracao(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        bot.reply_to(message, "🔄 FORÇANDO RESTAURAÇÃO DO CANAL...")
        try:
            messages = bot.get_chat_history(BACKUP_CHANNEL_ID, limit=200)
            arquivos_encontrados = []
            for msg in messages:
                if msg.document and msg.document.file_name and msg.document.file_name.endswith('.json'):
                    arquivos_encontrados.append({
                        'file_id': msg.document.file_id,
                        'file_name': msg.document.file_name,
                        'date': msg.date, 'message_id': msg.message_id
                    })
            if not arquivos_encontrados:
                bot.reply_to(message, "❌ Nenhum arquivo JSON encontrado no canal.")
                return
            bot.reply_to(message, f"📊 Encontrados {len(arquivos_encontrados)} arquivos JSON no canal.")
            for arquivo in arquivos_encontrados:
                try:
                    bot.reply_to(message, f"📥 Baixando {arquivo['file_name']}...")
                    file_info = bot.get_file(arquivo['file_id'])
                    downloaded_file = bot.download_file(file_info.file_path)
                    file_path = os.path.join(data_manager.data_dir, arquivo['file_name'])
                    with open(file_path, 'wb') as f:
                        f.write(downloaded_file)
                    bot.reply_to(message, f"✅ {arquivo['file_name']} salvo!")
                except Exception as e:
                    bot.reply_to(message, f"❌ Erro ao baixar {arquivo['file_name']}: {str(e)[:100]}")
            
            bot.reply_to(message, "🔄 Carregando todos os dados...")
            data_manager.load_all_data()
            bot.reply_to(message, f"✅ RESTAURAÇÃO COMPLETA!\n\n👥 Usuários: {len(data_manager.user_db)}\n🎫 Cupons: {len(data_manager.cupons_db)}\n💰 Pagamentos: {len(data_manager.pagamentos_pendentes)}\n🎉 Promoções: {len(data_manager.promocoes_ativas)}\n🤝 Afiliados: {len(data_manager.afiliados_db)}")
        except Exception as e:
            bot.reply_to(message, f"❌ Erro ao buscar histórico do canal: {str(e)[:200]}")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro na restauração forçada: {str(e)[:200]}")

@bot.message_handler(commands=['enviar_todos_arquivos'])
def enviar_todos_arquivos(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        data_dir = data_manager.data_dir
        arquivos_enviados = 0
        bot.reply_to(message, f"📤 Enviando todos os arquivos de {data_dir} para o canal...")
        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        bot.send_document(
                            BACKUP_CHANNEL_ID, f,
                            caption=f"📄 {filename} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                            visible_file_name=filename
                        )
                    arquivos_enviados += 1
                    time.sleep(0.5)
                except Exception as e:
                    bot.reply_to(message, f"❌ Erro ao enviar {filename}: {str(e)[:100]}")
        bot.reply_to(message, f"✅ {arquivos_enviados} arquivos enviados para o canal!")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)[:200]}")

# ==============================================================================
# 🔐 COMANDOS PARA LICENÇAS
# ==============================================================================
@bot.message_handler(commands=['verificar_licencas'])
def verificar_licencas_comando(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        total_usuarios = len(user_db)
        licencas_validas = 0
        licencas_expiradas = 0
        sem_licenca = 0
        
        relatorio = "📋 RELATÓRIO DE LICENÇAS\n\n"
        
        for user_id, user_data in user_db.items():
            if data_manager.is_license_valid(user_id):
                licencas_validas += 1
                license_date = user_data.get('license_date')
                if license_date:
                    dias_restantes = (license_date - datetime.now()).days
                    username = user_data.get('username', 'N/A')
                    first_name = user_data.get('first_name', 'N/A')
                    relatorio += f"✅ ID: {user_id} | @{username} | {first_name}\n   📅 Validade: {formatar_data(license_date)} | Dias restantes: {dias_restantes}\n\n"
            else:
                if user_data.get('license_date'):
                    licencas_expiradas += 1
                else:
                    sem_licenca += 1
        
        relatorio += f"📊 RESUMO:\n👥 Total de usuários: {total_usuarios}\n✅ Licenças válidas: {licencas_validas}\n❌ Licenças expiradas: {licencas_expiradas}\n📭 Sem licença: {sem_licenca}\n"
        
        if len(relatorio) > 4000:
            partes = [relatorio[i:i+4000] for i in range(0, len(relatorio), 4000)]
            for i, parte in enumerate(partes):
                bot.reply_to(message, f"📋 Parte {i+1}/{len(partes)}\n\n{parte}")
        else:
            bot.reply_to(message, relatorio)
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao verificar licenças: {str(e)[:200]}")

# ⚡ FUNÇÃO AUXILIAR: obtém nome completo com fallback
def _obter_nome_usuario(user_id):
    user_data = user_db.get(user_id, {})
    first_name = (user_data.get('first_name') or '').strip()
    last_name = (user_data.get('last_name') or '').strip()
    username = (user_data.get('username') or '').strip()
    
    if first_name or last_name or username:
        nome_completo = (first_name + ' ' + last_name).strip() or first_name or 'Sem nome'
        return {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'nome_completo': nome_completo
        }
    
    try:
        chat = bot.get_chat(user_id)
        first_name = (chat.first_name or '').strip()
        last_name = (chat.last_name or '').strip()
        username = (chat.username or '').strip()
        if user_id in user_db:
            user_db[user_id]['first_name'] = first_name
            user_db[user_id]['last_name'] = last_name
            user_db[user_id]['username'] = username
    except Exception:
        pass
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'nome_completo': (first_name + ' ' + last_name).strip() or first_name or 'Sem nome'
    }


# ==============================================================================
# 📄 SISTEMA DE BACKUP DE LICENÇAS + PDF (CHAMADO NO /start)
# ==============================================================================
_last_start_backup_time = 0
_start_backup_lock = threading.Lock()


def gerar_backup_licencas_completo():
    """Gera backup completo de licenças com TODAS as informações corretas"""
    backup_licencas = {}
    for user_id, user_data in user_db.items():
        license_date = user_data.get('license_date')
        if not license_date:
            continue
        
        nomes = _obter_nome_usuario(user_id)
        
        licenca_valida = False
        try:
            licenca_valida = data_manager.is_license_valid(user_id)
        except:
            pass
        
        dias_restantes = 0
        try:
            dias_restantes = data_manager.get_days_remaining(user_id)
        except:
            pass
        
        contas_info = []
        for conta in user_data.get('contas', []):
            contas_info.append({
                'telefone': conta.get('telefone', ''),
                'operadora': conta.get('operadora', ''),
                'pontos_total': conta.get('pontos_total', 0)
            })
        
        backup_licencas[str(user_id)] = {
            'user_id': user_id,
            'first_name': nomes['first_name'],
            'last_name': nomes['last_name'],
            'username': nomes['username'],
            'nome_completo': nomes['nome_completo'],
            'license_date': license_date,
            'dias_restantes': dias_restantes,
            'licenca_valida': licenca_valida,
            'first_seen': user_data.get('first_seen'),
            'status': user_data.get('status', 'active'),
            'total_contas': len(contas_info),
            'total_pontos': user_data.get('pontos_coletados', 0),
            'total_farms': user_data.get('total_farms', 0),
            'contas': contas_info
        }
    return backup_licencas


def gerar_pdf_licencas(backup_licencas):
    """Gera PDF com o relatório de licenças"""
    if not PDF_DISPONIVEL:
        return None
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            topMargin=1.5 * cm, bottomMargin=1.5 * cm,
            leftMargin=1 * cm, rightMargin=1 * cm
        )
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle', parent=styles['Heading1'],
            fontSize=16, alignment=1, spaceAfter=10,
            textColor=colors.HexColor('#1a237e')
        )
        subtitle_style = ParagraphStyle(
            'Subtitle', parent=styles['Normal'],
            fontSize=10, alignment=1, spaceAfter=15
        )
        
        elements = []
        elements.append(Paragraph("RELATÓRIO DE LICENÇAS - JADIEL MB VIP", title_style))
        elements.append(Paragraph(
            f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')} | "
            f"Total: {len(backup_licencas)} licenças",
            subtitle_style
        ))
        elements.append(Spacer(1, 0.3 * cm))
        
        total_ativas = sum(1 for v in backup_licencas.values() if v.get('licenca_valida'))
        total_expiradas = len(backup_licencas) - total_ativas
        
        stats_data = [
            ['Ativas', 'Expiradas', 'Total'],
            [str(total_ativas), str(total_expiradas), str(len(backup_licencas))]
        ]
        stats_table = Table(stats_data, colWidths=[5 * cm, 5 * cm, 5 * cm])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(stats_table)
        elements.append(Spacer(1, 0.5 * cm))
        
        def sort_key(item):
            ld = item[1].get('license_date')
            if isinstance(ld, datetime):
                return ld
            return datetime.max
        
        items_ordenados = sorted(backup_licencas.items(), key=sort_key)
        
        header = ['#', 'Nome Completo', 'Username', 'ID', 'Validade', 'Dias', 'Status']
        data = [header]
        
        for idx, (uid, info) in enumerate(items_ordenados, 1):
            nome = info.get('nome_completo', 'Sem nome')
            if not nome or nome == 'Sem nome':
                nome = info.get('first_name', '') or 'Não informado'
            username = info.get('username', '')
            username_str = f"@{username}" if username else "—"
            ld = info.get('license_date')
            if isinstance(ld, datetime):
                validade_str = ld.strftime('%d/%m/%Y %H:%M')
            else:
                validade_str = '—'
            dias = info.get('dias_restantes', 0)
            status = '✅ Ativa' if info.get('licenca_valida') else '❌ Expirada'
            nome_display = nome if len(nome) <= 25 else nome[:22] + '...'
            data.append([str(idx), nome_display, username_str, str(uid),
                         validade_str, str(dias), status])
        
        col_widths = [0.8 * cm, 5 * cm, 3 * cm, 2.5 * cm, 3 * cm, 1.2 * cm, 2.2 * cm]
        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    except Exception as e:
        log_terminal(f"❌ Erro ao gerar PDF de licenças: {e}")
        return None


def enviar_todos_backups_ao_start():
    """Envia TODOS os JSONs + backup_licencas.json + licenca.pdf para o canal"""
    try:
        log_terminal("📤 [/start] Enviando backups completos para o canal...")
        data_manager._save_now()
        
        backup_licencas = gerar_backup_licencas_completo()
        
        licencas_file = os.path.join(data_manager.data_dir, 'backup_licencas.json')
        with open(licencas_file, 'w', encoding='utf-8') as f:
            json.dump(
                backup_licencas, f,
                default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o),
                ensure_ascii=False, indent=2
            )
        
        data_manager.send_all_json_to_channel(
            force_send=True,
            reason="Usuário executou /start - backup automático"
        )
        
        tz_brasilia = pytz.timezone('America/Sao_Paulo')
        data_hora = datetime.now(tz_brasilia).strftime("%d/%m/%Y às %H:%M:%S")
        
        time.sleep(0.5)
        try:
            with open(licencas_file, 'rb') as f:
                bot.send_document(
                    BACKUP_CHANNEL_ID, f,
                    caption=(
                        f"🔐 BACKUP DE LICENÇAS COMPLETO\n"
                        f"📅 {data_hora}\n"
                        f"📊 Total: {len(backup_licencas)} licenças\n"
                        f"✅ Ativas: {sum(1 for v in backup_licencas.values() if v.get('licenca_valida'))}\n"
                        f"❌ Expiradas: {sum(1 for v in backup_licencas.values() if not v.get('licenca_valida'))}"
                    ),
                    visible_file_name='backup_licencas.json'
                )
        except Exception as e:
            log_terminal(f"❌ Erro ao enviar backup_licencas.json: {e}")
        
        if PDF_DISPONIVEL:
            time.sleep(0.5)
            try:
                pdf_buffer = gerar_pdf_licencas(backup_licencas)
                if pdf_buffer:
                    bot.send_document(
                        BACKUP_CHANNEL_ID, pdf_buffer,
                        caption=(
                            f"📄 RELATÓRIO DE LICENÇAS (PDF)\n"
                            f"📅 {data_hora}\n"
                            f"📊 Total: {len(backup_licencas)} licenças"
                        ),
                        visible_file_name='licenca.pdf'
                    )
                    log_terminal("✅ PDF licenca.pdf enviado para o canal")
            except Exception as e:
                log_terminal(f"❌ Erro ao enviar PDF: {e}")
        else:
            log_terminal("⚠️ reportlab não instalado - PDF não gerado")
        
        log_terminal("✅ [/start] Todos os backups enviados para o canal")
    except Exception as e:
        log_terminal(f"❌ Erro no envio de backups do /start: {e}")


def _backup_ao_start_rate_limited():
    """Rate-limit de 10s para evitar spam no canal"""
    global _last_start_backup_time
    with _start_backup_lock:
        agora = time.time()
        if agora - _last_start_backup_time < 10:
            log_terminal("⏱️ [/start] Backup recente - aguardando cooldown de 10s")
            return
        _last_start_backup_time = agora
    try:
        enviar_todos_backups_ao_start()
    except Exception as e:
        log_terminal(f"❌ Erro no worker de backup do /start: {e}")


@bot.message_handler(commands=['backup_licencas'])
def backup_licencas_comando(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        bot.reply_to(message, "💾 Gerando backup completo de licenças (JSON + PDF)...")
        backup_licencas = gerar_backup_licencas_completo()
        
        backup_file = os.path.join(data_manager.data_dir, 'backup_licencas.json')
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(
                backup_licencas, f,
                default=lambda obj: obj.isoformat() if isinstance(obj, datetime) else str(obj),
                ensure_ascii=False, indent=2
            )
        
        with open(backup_file, 'rb') as f:
            bot.send_document(
                BACKUP_CHANNEL_ID, f,
                caption=(
                    f"🔐 BACKUP DE LICENÇAS - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"📊 {len(backup_licencas)} licenças salvas"
                ),
                visible_file_name=f"backup_licencas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
        
        if PDF_DISPONIVEL:
            pdf_buffer = gerar_pdf_licencas(backup_licencas)
            if pdf_buffer:
                bot.send_document(
                    BACKUP_CHANNEL_ID, pdf_buffer,
                    caption=(
                        f"📄 RELATÓRIO DE LICENÇAS (PDF) - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                        f"📊 {len(backup_licencas)} licenças"
                    ),
                    visible_file_name='licenca.pdf'
                )
        
        bot.reply_to(
            message,
            f"✅ Backup de {len(backup_licencas)} licenças concluído!\n\n"
            f"📤 JSON e PDF enviados para o canal."
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Erro no backup de licenças: {str(e)[:200]}")

@bot.message_handler(commands=['forcar_save'])
def forcar_save_comando(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        bot.reply_to(message, "💾 Salvando todos os dados...")
        data_manager._save_now()
        data_manager.send_all_json_to_channel(force_send=True, reason="Forçado pelo admin")
        bot.reply_to(message, f"✅ Dados salvados com sucesso!\n\n👥 Usuários: {len(user_db)}\n🎫 Cupons: {len(cupons_db)}\n💰 Pagamentos: {len(pagamentos_pendentes)}\n🤝 Afiliados: {len(afiliados_db)}\n🔐 Licenças ativas: {sum(1 for uid in user_db if data_manager.is_license_valid(uid))}")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao forçar save: {str(e)[:200]}")

@bot.message_handler(commands=['restaurar_manual'])
def restaurar_manual_comando(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📤 Baixar JSONs do Canal", callback_data="manual_baixar_jsons"),
        types.InlineKeyboardButton("🔄 Carregar Local", callback_data="manual_carregar_local"),
        types.InlineKeyboardButton("👥 user_db.json", callback_data="manual_restaurar_userdb"),
        types.InlineKeyboardButton("🎫 cupons_db.json", callback_data="manual_restaurar_cuponsdb"),
        types.InlineKeyboardButton("💰 pagamentos.json", callback_data="manual_restaurar_pagamentos"),
        types.InlineKeyboardButton("🤝 afiliados.json", callback_data="manual_restaurar_afiliados"),
        types.InlineKeyboardButton("📊 Verificar Status", callback_data="manual_verificar_status"),
        types.InlineKeyboardButton("❌ Cancelar", callback_data="manual_cancelar")
    )
    bot.reply_to(message, "🔄 MENU DE RESTAURAÇÃO MANUAL\n\nSelecione uma opção:", reply_markup=markup)

@bot.message_handler(commands=['restaurar_licencas_emergencia'])
def restaurar_licencas_emergencia(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        bot.reply_to(message, "📤 Por favor, envie o arquivo 'backup_licencas.json' como documento.")
        admin_state[message.chat.id] = {'step': 'esperando_arquivo_licencas', 'comando': 'restaurar_licencas'}
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)[:200]}")

@bot.message_handler(commands=['teste_datas'])
def teste_datas_comando(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        user_id = message.from_user.id
        if user_id in user_db:
            license_date = user_db[user_id].get('license_date')
            serialized = data_manager.serialize_datetime(license_date)
            deserialized = data_manager.deserialize_datetime(serialized)
            bot.reply_to(message, f"🧪 TESTE DE DATAS\n\nOriginal: {license_date}\nSerializado: {serialized}\nDeserializado: {deserialized}\nTipos: {type(license_date)} -> {type(deserialized)}")
        else:
            bot.reply_to(message, "❌ Usuário não encontrado no banco de dados.")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro no teste: {str(e)[:200]}")

@bot.message_handler(content_types=['document'], func=lambda m: m.chat.id in admin_state and admin_state[m.chat.id] is not None and admin_state[m.chat.id].get('step') == 'esperando_arquivo_licencas')
def handle_arquivo_licencas(message):
    chat_id = message.chat.id
    try:
        if not message.document.file_name.endswith('.json'):
            bot.reply_to(message, "❌ O arquivo deve ser um JSON (.json)")
            admin_state.pop(chat_id, None)
            return
        bot.reply_to(message, f"📥 Baixando {message.document.file_name}...")
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        data = json.loads(downloaded_file.decode('utf-8'))
        
        licencas_restauradas = 0
        licencas_falhas = 0
        
        for user_id_str, licenca_info in data.items():
            try:
                user_id = int(user_id_str)
                license_date_str = licenca_info.get('license_date')
                if license_date_str:
                    license_date = None
                    try:
                        if 'T' in license_date_str:
                            license_date = datetime.fromisoformat(license_date_str.replace('Z', '+00:00'))
                        else:
                            for fmt in ('%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
                                try:
                                    license_date = datetime.strptime(license_date_str, fmt)
                                    break
                                except:
                                    continue
                    except:
                        license_date = datetime.now() + timedelta(days=30)
                    
                    if user_id not in user_db:
                        user_db[user_id] = {
                            'contas': [], 'conta_ativa': 0,
                            'config': {'auto_farm': False},
                            'license_date': license_date,
                            'first_seen': datetime.now()
                        }
                    else:
                        user_db[user_id]['license_date'] = license_date
                    licencas_restauradas += 1
            except Exception as e:
                licencas_falhas += 1
                log_terminal(f"Erro ao restaurar licença {user_id_str}: {e}")
        
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("licencas_restauradas_emergencia", chat_id)
        admin_state.pop(chat_id, None)
        bot.reply_to(message, f"✅ LICENÇAS RESTAURADAS!\n\n📊 Estatísticas:\n✔️ Licenças restauradas: {licencas_restauradas}\n❌ Falhas: {licencas_falhas}\n👥 Total no banco: {len(user_db)}\n\n💾 Dados salvos e enviados para o canal.")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao processar arquivo: {str(e)[:200]}")
        admin_state.pop(chat_id, None)

# ==============================================================================
# 📱 COMANDOS PARA DESBANIMENTO
# ==============================================================================
@bot.message_handler(commands=['desbanir'])
def comando_desbanir(message):
    chat_id = message.chat.id
    if not verificar_licenca(chat_id):
        msg_licenca_expirada(chat_id)
        return
    try:
        user = user_db.get(chat_id, {})
        contas = user.get('contas', [])
        
        if not contas:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🟣 VIVO", callback_data="desbanir_vivo"),
                types.InlineKeyboardButton("🔴 CLARO", callback_data="desbanir_claro"),
                types.InlineKeyboardButton("🔵 TIM", callback_data="desbanir_tim")
            )
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(chat_id, "🔓 DESBANIR NÚMERO\n\nSeu número foi bloqueado/baneado?\n\nSelecione a operadora do número que deseja desbanir:", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for idx, conta in enumerate(contas):
                telefone = conta.get('telefone', 'N/A')
                operadora = conta.get('operadora', 'vivo')
                if operadora == 'vivo':
                    icon = "🟣"
                elif operadora == 'claro':
                    icon = "🔴"
                else:
                    icon = "🔵"
                texto = f"{icon} {telefone} - Desbanir"
                markup.add(types.InlineKeyboardButton(texto, callback_data=f"desbanir_conta|{idx}"))
            markup.add(types.InlineKeyboardButton("➕ Outro Número", callback_data="desbanir_outro"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(chat_id, "🔓 DESBANIR NÚMERO\n\nSelecione a conta que deseja desbanir ou adicione outro número:", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"❌ Erro: {str(e)[:100]}")

@bot.message_handler(commands=['admin_desbanir'])
def admin_desbanir(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    try:
        partes = message.text.split()
        if len(partes) < 3:
            bot.reply_to(message, "❌ Use: /admin_desbanir NUMERO OPERADORA\n\nExemplos:\n/admin_desbanir 11999999999 vivo\n/admin_desbanir 11988888888 claro\n/admin_desbanir 11977777777 tim\n\n📱 O número deve ter 11 dígitos (com DDD)")
            return
        telefone = partes[1].strip()
        operadora = partes[2].strip().lower()
        if operadora not in ['vivo', 'claro', 'tim']:
            bot.reply_to(message, "❌ Operadora inválida! Use: vivo, claro ou tim")
            return
        if len(telefone) != 11 or not telefone.isdigit():
            bot.reply_to(message, "❌ Número inválido! Use 11 dígitos com DDD")
            return
        
        msg_status = bot.reply_to(message, f"🔓 Processando desbanimento...\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}")
        sucesso, mensagem = api_desbanir_numero(telefone, operadora)
        if not sucesso:
            sucesso, mensagem = api_resetar_conta(telefone, operadora)
        
        try:
            bot.edit_message_text(
                f"🔓 RESULTADO DO DESBANIMENTO\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}\n\n{mensagem}\n\n⚠️ Se ainda tiver problemas:\n1. Aguarde 1 hora e tente novamente\n2. Entre em contato com a operadora\n3. Use outro número se possível",
                chat_id=message.chat.id, message_id=msg_status.message_id
            )
        except:
            bot.send_message(message.chat.id, f"🔓 RESULTADO DO DESBANIMENTO\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}\n\n{mensagem}")
        
        log_terminal(f"ADMIN DESBANIMENTO: {telefone} ({operadora}) - Sucesso: {sucesso}")
    except Exception as e:
        bot.reply_to(message, f"❌ Erro no desbanimento: {str(e)[:200]}")

@bot.message_handler(commands=['admin_reset_massivo'])
def admin_reset_massivo(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    admin_state[message.chat.id] = {'step': 'admin_wait_reset_numbers'}
    bot.reply_to(message, "🔄 RESET MASSIVO DE NÚMEROS\n\nEnvie uma lista de números no formato:\n\n11999999999 vivo\n11988888888 claro\n11977777777 tim\n\n⚠️ Um número por linha\n⚠️ Inclua a operadora após o número\n⚠️ Máximo: 10 números por vez\n\nOu digite 'cancelar' para cancelar.")

@bot.message_handler(commands=['ajuda_desbanir'])
def ajuda_desbanir(message):
    chat_id = message.chat.id
    ajuda_texto = (
        "🔓 AJUDA - DESBANIR NÚMERO\n\n"
        "📌 O que é desbanimento?\n"
        "É o processo de remover bloqueios que impedem seu número de fazer login no app da operadora.\n\n"
        "📌 Quando preciso desbanir?\n"
        "• Quando recebe 'número bloqueado'\n"
        "• Quando não recebe o código SMS\n"
        "• Quando é redirecionado para suporte\n"
        "• Quando o app diz 'conta suspensa'\n\n"
        "📌 Como usar:\n"
        "1. Use /desbanir para seu próprio número\n"
        "2. Selecione sua operadora\n"
        "3. Digite seu número com DDD\n"
        "4. Aguarde o processamento\n\n"
        "📌 Dicas importantes:\n"
        "• Aguarde 1 hora após tentativas falhas\n"
        "• Verifique se o número está ativo\n"
        "• Use apenas números da operadora correta\n"
        "• Entre em contato com a operadora se persistir\n\n"
        "📌 Comandos:\n"
        "/desbanir - Para seu próprio número\n"
        "/admin_desbanir NUMERO OPERADORA - (Apenas admin)\n\n"
        "🥰 SUPORTE: @JADIEL_TM"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔓 DESBANIR MEU NÚMERO", callback_data="desbanir_start"))
    markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
    bot.send_message(chat_id, ajuda_texto, reply_markup=markup)

# ==============================================================================
# 🤖 HANDLERS PRINCIPAIS
# ==============================================================================
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    user = message.from_user
    
    afiliado_code = None
    partes = message.text.split()
    if len(partes) > 1:
        afiliado_code = partes[1].strip().upper()
    
    is_new_user = chat_id not in data_manager.user_db
    
    if user.username:
        data_manager.username_to_id[user.username.lower()] = chat_id
        data_manager.save_all_data()
    
    if chat_id not in data_manager.user_db:
        data_manager.user_db[chat_id] = {
            'contas': [], 'conta_ativa': 0,
            'config': {'auto_farm': False},
            'license_date': None,
            'first_seen': datetime.now(),
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'pontos_coletados': 0, 'total_farms': 0
        }
        log_terminal(f"✔️ Novo usuário registrado: {user.first_name} (@{user.username}) ID: {chat_id}")
    else:
        data_manager.user_db[chat_id].update({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("start_command", chat_id)
    notificar_admin_novo_usuario({
        'id': user.id, 'first_name': user.first_name,
        'last_name': user.last_name, 'username': user.username
    })
    
    if afiliado_code:
        try:
            if afiliado_code in data_manager.afiliado_codigo_to_user:
                owner_id = data_manager.afiliado_codigo_to_user[afiliado_code]
                if owner_id != chat_id and owner_id in data_manager.afiliados_db:
                    data_manager.afiliados_db[owner_id]['cliques'] = data_manager.afiliados_db[owner_id].get('cliques', 0) + 1
                    data_manager.save_all_data()
                    log_terminal(f"👆 Clique registrado: afiliado {owner_id} via {afiliado_code}")
        except Exception as e:
            log_terminal(f"⚠️ Erro ao registrar clique de afiliado: {e}")
        
        if is_new_user:
            try:
                processar_afiliado(chat_id, afiliado_code)
            except Exception as e:
                log_terminal(f"⚠️ Erro ao processar afiliado: {e}")
    
    if chat_id in user_state:
        del user_state[chat_id]
    
    # ✅ NOVA LINHA — Envia TODOS os backups (JSONs + backup_licencas.json + licenca.pdf) para o canal
    threading.Thread(target=_backup_ao_start_rate_limited, daemon=True).start()
    
    if data_manager.user_db[chat_id].get('contas'):
        show_menu_with_image(chat_id, is_logged=True)
    else:
        show_menu_with_image(chat_id, is_logged=False)

@bot.message_handler(commands=['menu'])
def menu_command(message):
    chat_id = message.chat.id
    if chat_id in user_state:
        del user_state[chat_id]
    data_manager.send_json_on_user_action("menu_command", chat_id)
    if chat_id in user_db and user_db[chat_id].get('contas'):
        show_menu_with_image(chat_id, is_logged=True)
    else:
        show_menu_with_image(chat_id, is_logged=False)

@bot.message_handler(commands=['minhascontas'])
def minhas_contas_command(message):
    chat_id = message.chat.id
    user = user_db.get(chat_id, {})
    contas = user.get('contas', [])
    conta_ativa = user.get('conta_ativa', 0)
    
    data_manager.send_json_on_user_action("minhas_contas", chat_id)
    
    if not contas:
        bot.send_message(chat_id, "📭 Você não tem nenhuma conta cadastrada.")
        return
    
    msg = "📱 SUAS CONTAS CADASTRADAS:\n\n"
    for idx, conta in enumerate(contas):
        telefone = conta.get('telefone', 'N/A')
        operadora = conta.get('operadora', 'vivo')
        pontos_total = conta.get('pontos_total', 0)
        status = "✔️ ATIVA" if idx == conta_ativa else ""
        if operadora == 'vivo':
            icon = "🟣"
        elif operadora == 'claro':
            icon = "🔴"
        else:
            icon = "🔵"
        msg += f"{idx+1}. {icon} {telefone}\n   Pontos: {pontos_total} {status}\n\n"
    
    pontos_totais_usuario = user.get('pontos_coletados', 0)
    total_farms = user.get('total_farms', 0)
    msg += f"🏆 PONTOS TOTAIS: {pontos_totais_usuario}\n🔄 Coletas realizadas: {total_farms}\n📊 Total de contas: {len(contas)}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("⚙️ CONFIGURAÇÕES", callback_data="config_menu"))
    markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
    bot.send_message(chat_id, msg, reply_markup=markup)

@bot.message_handler(commands=['cupom'])
def user_redeem_cupom(message):
    data_manager.send_json_on_user_action("cupom_command", message.chat.id)
    try:
        codigo = message.text.split()[1].strip().upper()
    except:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
        return bot.reply_to(message, "❌ Use: /cupom CODIGO\n\nExemplo: /cupom ABC12345", reply_markup=markup)
    
    valido, resultado = verificar_cupom_valido(codigo, message.chat.id)
    
    if not valido:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
        bot.reply_to(message, f"❌ {resultado}", reply_markup=markup)
        return
    
    cupom = resultado
    dias = cupom['dias']
    
    if 'resgatado_por' not in cupom:
        cupom['resgatado_por'] = []
    
    if message.chat.id not in cupom['resgatado_por']:
        cupom['resgatado_por'].append(message.chat.id)
    
    cupom['usos'] = len(cupom['resgatado_por'])
    
    if len(cupom['resgatado_por']) >= cupom['limite']:
        del cupons_db[codigo]
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("cupom_expirado", codigo)
    else:
        cupons_db[codigo] = cupom
        data_manager.save_all_data()
    
    novo = datetime.now() + timedelta(days=dias)
    if message.chat.id not in user_db:
        user_db[message.chat.id] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
    
    if user_db[message.chat.id].get('license_date') and user_db[message.chat.id]['license_date'] > datetime.now():
        novo = user_db[message.chat.id]['license_date'] + timedelta(days=dias)
    
    user_db[message.chat.id]['license_date'] = novo
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("cupom_resgatado", message.chat.id)
    
    resgates_restantes = cupom['limite'] - len(cupom['resgatado_por'])
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
    
    mensagem_resposta = f"✔️ CUPOM ATIVADO COM SUCESSO!\n\n📅 Dias adicionados: {dias}\n🕒 Validade atualizada\n👤 Você resgatou este cupom pela 1ª vez\n"
    
    if codigo in cupons_db:
        mensagem_resposta += f"🎉 Resgates restantes: {resgates_restantes}"
    else:
        mensagem_resposta += "⚠️ Este cupom esgotou todos os resgates disponíveis"
    
    bot.reply_to(message, mensagem_resposta, reply_markup=markup)

# ==============================================================================
# 🎉 COMANDO /promo_vip (ADMIN ONLY)
# ==============================================================================
@bot.message_handler(commands=['promo_vip'])
def admin_promo_vip(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_promo_vip", message.chat.id)
    admin_state[message.chat.id] = {'step': 'promo_wait_price'}
    bot.reply_to(message, "💰 Qual o preço da promoção VIP? (Em reais, ex: 5.00 para R$ 5,00)")

# ==============================================================================
# 🤖 COMANDOS DE ADMINISTRADOR
# ==============================================================================
@bot.message_handler(commands=['JADIEL07'])
def admin_add_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_add_user", message.chat.id)
    try:
        partes = message.text.split()
        if len(partes) < 2:
            bot.reply_to(message, "❌ Use: /JADIEL07 @usuario ou ID")
            return
        user_input = partes[1].strip()
        target_id = None
        if user_input.startswith("@"):
            username = user_input[1:].lower()
            target_id = username_to_id.get(username)
            if not target_id:
                bot.reply_to(message, f"❌ Usuário @{username} não encontrado!")
                return
        elif user_input.isdigit():
            target_id = int(user_input)
        else:
            bot.reply_to(message, "❌ Formato inválido! Use @usuario ou ID numérico.")
            return
        admin_state[message.chat.id] = {'step': 'adm_wait_days', 'target': target_id}
        bot.reply_to(message, f"👤 Usuário identificado!\n🆔 ID: {target_id}\n\n📅 Quantos dias deseja adicionar?")
    except Exception as e:
        log_terminal(f"Erro no comando JADIEL07: {e}")
        bot.reply_to(message, "❌ Erro ao processar comando!")

@bot.message_handler(commands=['JADIEL07_CUPOM_GERAR'])
def admin_gen_cupom(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_gen_cupom", message.chat.id)
    admin_state[message.chat.id] = {'step': 'adm_wait_cupom_days'}
    bot.reply_to(message, "🎫 GERADOR DE CUPOM\n\n📅 Quantos dias de validade para o cupom?\n\nExemplo: 30")

@bot.message_handler(commands=['excluir_cupom'])
def admin_del_cupom(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_del_cupom", message.chat.id)
    try:
        codigo = message.text.split()[1].strip().upper()
        if codigo in cupons_db:
            del cupons_db[codigo]
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("cupom_excluido", codigo)
            bot.reply_to(message, f"✔️ Cupom {codigo} deletado com sucesso!")
        else:
            bot.reply_to(message, f"❌ Cupom {codigo} não existe!")
    except:
        bot.reply_to(message, "❌ Use: /excluir_cupom CODIGO\n\nExemplo: /excluir_cupom ABC12345")

@bot.message_handler(commands=['excluir_usuario'])
def admin_del_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_del_user", message.chat.id)
    try:
        user_input = message.text.split()[1].strip()
        target_id = None
        if user_input.startswith("@"):
            username = user_input[1:].lower()
            target_id = username_to_id.get(username)
        elif user_input.isdigit():
            target_id = int(user_input)
        
        if target_id and target_id in user_db:
            user_db[target_id]['license_date'] = datetime.now() - timedelta(days=1)
            if target_id in auto_farm_jobs:
                try:
                    scheduler.remove_job(auto_farm_jobs[target_id])
                    del auto_farm_jobs[target_id]
                except:
                    pass
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("usuario_excluido", target_id)
            bot.reply_to(message, f"✔️ LICENÇA REVOGADA!\n\n🆔 ID do usuário: {target_id}")
        else:
            bot.reply_to(message, "❌ Usuário não encontrado!")
    except:
        bot.reply_to(message, "❌ Use: /excluir_usuario @usuario ou ID\n\nExemplo: /excluir_usuario @username")

@bot.message_handler(commands=['aviso'])
def admin_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_broadcast", message.chat.id)
    try:
        conteudo = message.text.replace("/aviso", "", 1).strip()
        if not conteudo:
            bot.reply_to(message, "❌ Digite a mensagem do aviso!\n\nExemplo: /aviso Manutenção programada para amanhã.")
            return
        
        last_broadcast_msgs.clear()
        total_usuarios = len(user_db)
        enviados = 0
        falhas = 0
        msg_status = bot.reply_to(message, f"📢 Enviando aviso para {total_usuarios} usuários...")
        
        for cid in list(user_db.keys()):
            try:
                if cid == message.chat.id:
                    continue
                m = bot.send_message(cid, f"📢 AVISO IMPORTANTE 📢\n\n{conteudo}\n\n— SUPORTE: @JADIEL_TM")
                last_broadcast_msgs.append((cid, m.message_id))
                enviados += 1
                time.sleep(0.05)
            except Exception as e:
                falhas += 1
                log_terminal(f"Erro ao enviar para {cid}: {e}")
        
        data_manager.save_all_data()
        data_manager.send_json_on_user_action("broadcast_enviado", message.chat.id)
        bot.edit_message_text(f"✔️ AVISO ENVIADO COM SUCESSO!\n\n📊 Estatísticas:\n✔️ Enviados: {enviados}\n❌ Falhas: {falhas}\n👥 Total de usuários: {total_usuarios}", message.chat.id, msg_status.message_id)
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao enviar aviso: {str(e)[:100]}")

@bot.message_handler(commands=['excluir_aviso'])
def del_aviso(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("del_aviso", message.chat.id)
    if not last_broadcast_msgs:
        bot.reply_to(message, "❌ Nenhum aviso recente para excluir!")
        return
    excluidos = 0
    falhas = 0
    for cid, mid in last_broadcast_msgs:
        try:
            bot.delete_message(cid, mid)
            excluidos += 1
        except:
            falhas += 1
    last_broadcast_msgs.clear()
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("aviso_excluido", message.chat.id)
    bot.reply_to(message, f"✔️ ÚLTIMO AVISO EXCLUÍDO!\n\n🗑️ Mensagens excluídas: {excluidos}\n⚠️ Falhas: {falhas}")

@bot.message_handler(commands=['enviar_midia'])
def admin_enviar_midia(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_enviar_midia", message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📝 TEXTO", callback_data="enviar_texto"))
    markup.add(types.InlineKeyboardButton("🖼️ IMAGEM", callback_data="enviar_imagem"))
    markup.add(types.InlineKeyboardButton("🎬 VÍDEO", callback_data="enviar_video"))
    markup.add(types.InlineKeyboardButton("❌ CANCELAR", callback_data="cancelar_envio"))
    bot.reply_to(message, "📤 ENVIAR MÍDIA PARA TODOS OS USUÁRIOS\n\nSelecione o tipo de mídia que deseja enviar:", reply_markup=markup)

@bot.message_handler(commands=['excluir_midia'])
def admin_excluir_midia(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_excluir_midia", message.chat.id)
    if not last_media_msgs:
        bot.reply_to(message, "❌ Nenhuma mídia recente para excluir!")
        return
    excluidos = 0
    falhas = 0
    for cid, mid in last_media_msgs:
        try:
            bot.delete_message(cid, mid)
            excluidos += 1
        except:
            falhas += 1
    last_media_msgs.clear()
    data_manager.save_all_data()
    data_manager.send_json_on_user_action("midia_excluida", message.chat.id)
    bot.reply_to(message, f"✔️ ÚLTIMA MÍDIA EXCLUÍDA!\n\n🗑️ Mensagens excluídas: {excluidos}\n⚠️ Falhas: {falhas}")

@bot.message_handler(commands=['estatisticas'])
def admin_estatisticas(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_estatisticas", message.chat.id)
    stats = data_manager.get_user_statistics()
    total_usuarios = len(user_db)
    usuarios_com_login = sum(1 for u in user_db.values() if u.get('contas'))
    usuarios_com_licenca = sum(1 for u in user_db.values() if u.get('license_date') and u['license_date'] > datetime.now())
    pagamentos_pendentes_count = sum(1 for p in pagamentos_pendentes.values() if p['status'] == 'pending')
    pagamentos_aprovados_count = sum(1 for p in pagamentos_pendentes.values() if p.get('pago', False))
    
    contas_vivo = 0
    contas_claro = 0
    contas_tim = 0
    for user in user_db.values():
        for conta in user.get('contas', []):
            if conta.get('operadora') == 'claro':
                contas_claro += 1
            elif conta.get('operadora') == 'tim':
                contas_tim += 1
            else:
                contas_vivo += 1
    
    cupons_info = ""
    if cupons_db:
        for codigo, cupom in list(cupons_db.items())[:5]:
            resgates = len(cupom.get('resgatado_por', []))
            limite = cupom.get('limite', 0)
            dias = cupom.get('dias', 0)
            cupons_info += f"• {codigo}: {resgates}/{limite} resgates - {dias} dias\n"
    
    usuarios_recentes = []
    for cid, data in list(user_db.items())[-10:]:
        nome = data.get('first_name', 'Sem nome')
        username = f"@{data.get('username')}" if data.get('username') else "Sem username"
        data_registro = data.get('first_seen', datetime.now()).strftime("%d/%m %H:%M")
        usuarios_recentes.append(f"• {nome} ({username}) - {data_registro}")
    
    pontos_totais = 0
    for user in user_db.values():
        pontos_totais += user.get('pontos_coletados', 0)
    
    total_cliques_afiliados = sum(a.get('cliques', 0) for a in afiliados_db.values())
    total_registros_afiliados = sum(a.get('registros', 0) for a in afiliados_db.values())
    total_dias_afiliados = sum(a.get('dias_ganhos', 0) for a in afiliados_db.values())
    
    mensagem = f"📊 ESTATÍSTICAS DO BOT\n\n"
    mensagem += f"👥 Total de usuários: {total_usuarios}\n"
    mensagem += f"✔️ Com login: {usuarios_com_login}\n"
    mensagem += f"🔐 Com licença ativa: {usuarios_com_licenca}\n"
    mensagem += f"🤖 Farm automático ativo: {len(auto_farm_jobs)}\n"
    mensagem += f"🎫 Cupons ativos: {len(cupons_db)}\n"
    mensagem += f"💰 Pagamentos pendentes: {pagamentos_pendentes_count}\n"
    mensagem += f"✔️ Pagamentos aprovados: {pagamentos_aprovados_count}\n"
    mensagem += f"🎉 Promoções ativas: {len(promocoes_ativas)}\n"
    mensagem += f"🤝 Afiliados cadastrados: {len(afiliados_db)}\n"
    mensagem += f"👆 Total de cliques em afiliados: {total_cliques_afiliados}\n"
    mensagem += f"👥 Total de registros por afiliados: {total_registros_afiliados}\n"
    mensagem += f"🎁 Dias distribuídos por afiliados: {total_dias_afiliados}\n"
    mensagem += f"🟣 Contas Vivo: {contas_vivo}\n"
    mensagem += f"🔴 Contas Claro: {contas_claro}\n"
    mensagem += f"🔵 Contas TIM: {contas_tim}\n"
    mensagem += f"💰 Pontos totais coletados: {pontos_totais}\n\n"
    mensagem += f"📈 ESTATÍSTICAS AVANÇADAS:\n"
    mensagem += f"• Usuários ativos: {stats['usuarios_ativos']}\n"
    mensagem += f"• Usuários novos hoje: {stats['usuarios_novos_hoje']}\n"
    mensagem += f"• Total de pontos: {stats['total_pontos']}\n\n"
    
    if cupons_info:
        mensagem += "🎫 CUPONS ATIVOS (top 5):\n" + cupons_info + "\n"
    
    mensagem += "📈 ÚLTIMOS 10 USUÁRIOS:\n" + "\n".join(usuarios_recentes)
    bot.reply_to(message, mensagem)

@bot.message_handler(commands=['confirmar_pagamento'])
def admin_confirmar_pagamento(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Comando restrito ao administrador!")
        return
    data_manager.send_json_on_user_action("admin_confirmar_pagamento", message.chat.id)
    try:
        payment_id = message.text.split()[1].strip()
        sucesso, mensagem = confirmar_pagamento_manual(payment_id)
        if sucesso:
            bot.reply_to(message, f"✔️ PAGAMENTO CONFIRMADO!\n\n{mensagem}")
        else:
            bot.reply_to(message, f"❌ ERRO AO CONFIRMAR PAGAMENTO:\n\n{mensagem}")
    except:
        if not pagamentos_pendentes:
            bot.reply_to(message, "❌ Nenhum pagamento pendente encontrado.")
            return
        mensagem = "📋 PAGAMENTOS PENDENTES:\n\n"
        for pid, pagamento in list(pagamentos_pendentes.items())[:20]:
            chat_id = pagamento['chat_id']
            valor = pagamento['valor']
            status = pagamento['status']
            data_criacao = pagamento['data_criacao'].strftime("%d/%m %H:%M")
            expiracao = pagamento['data_expiracao'].strftime("%H:%M")
            mensagem += f"🆔 {pid}\n👤 Chat ID: {chat_id}\n💰 R$ {valor:.2f}\n📅 {data_criacao} (expira {expiracao})\n📊 Status: {status}\n\n"
        mensagem += f"\nTotal: {len(pagamentos_pendentes)} pagamentos\n\nPara confirmar um pagamento, use:\n/confirmar_pagamento PAYMENT_ID"
        bot.reply_to(message, mensagem)

# ==============================================================================
# 🤖 HANDLER DE RESPOSTAS DO ADMIN
# ==============================================================================
@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.chat.id in admin_state and admin_state[m.chat.id] is not None)
def admin_response_handler(message):
    chat_id = message.chat.id
    if chat_id not in admin_state or admin_state[chat_id] is None:
        return
    
    step = admin_state[chat_id].get('step')
    
    if step == 'wait_backup_completo':
        texto = message.text.strip().lower() if message.text else ''
        if texto == 'cancelar':
            admin_state.pop(chat_id, None)
            bot.reply_to(message, "❌ Backup completo cancelado.")
        else:
            bot.reply_to(message, "📎 Por favor, envie o arquivo `.json` como documento.\n\nOu digite *cancelar* para cancelar.", parse_mode='Markdown')
        return
    
    if step == 'adm_wait_days':
        try:
            dias = int(message.text)
            tid = admin_state[chat_id]['target']
            if tid not in user_db:
                user_db[tid] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
            if user_db[tid].get('license_date') and user_db[tid]['license_date'] > datetime.now():
                user_db[tid]['license_date'] = user_db[tid]['license_date'] + timedelta(days=dias)
            else:
                user_db[tid]['license_date'] = datetime.now() + timedelta(days=dias)
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("admin_add_dias", tid)
            try:
                bot.send_message(tid, f"🎉 PARABÉNS!\n\nSua licença foi renovada em {dias} dias!\nNova validade: {formatar_data(user_db[tid]['license_date'])}")
            except:
                pass
            bot.reply_to(message, f"✔️ LICENÇA ATUALIZADA!\n\n🆔 ID do usuário: {tid}\n📅 Dias adicionados: {dias}\n🕒 Nova validade: {formatar_data(user_db[tid]['license_date'])}")
            admin_state[chat_id] = None
        except ValueError:
            bot.reply_to(message, "❌ Erro: Digite um número válido para os dias. Exemplo: 30")
    
    elif step == 'adm_wait_cupom_days':
        try:
            dias = int(message.text)
            admin_state[chat_id] = {'step': 'adm_wait_cupom_limite', 'dias': dias}
            bot.reply_to(message, f"📅 Dias definidos: {dias}\n\n👥 Qual o limite de pessoas que podem resgatar este cupom?\n\nExemplo: 10")
        except ValueError:
            bot.reply_to(message, "❌ Erro: Digite um número válido para os dias. Exemplo: 30")
    
    elif step == 'adm_wait_cupom_limite':
        try:
            limite = int(message.text)
            dias = admin_state[chat_id]['dias']
            c = gerar_codigo_cupom()
            cupons_db[c] = {
                'dias': dias, 'limite': limite, 'usos': 0,
                'resgatado_por': [], 'criado_em': datetime.now(),
                'resgates_realizados': 0
            }
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("cupom_gerado", c)
            mensagem_cupom = (
                "<b>🟣 CUPOM OPERADORA VIVO 🟣</b>\n\n"
                f"🔖 <b>CUPOM</b>: <code>{c}</code>\n"
                f"✔️ <b>VÁLIDO</b>: {dias} DIAS\n"
                f"👥 <b>LIMITE</b>: {limite} PESSOAS (1 vez por pessoa)\n\n"
                "📲 Onde você consegue usar esse cupom da operadora Vivo?\n"
                "<i>Você só consegue usar no bot do Telegram.</i>\n\n"
                "🤖 <b>Link do bot</b>: https://t.me/jadiel_mb_vivo_vip_bot\n"
                "🛠️ <b>Suporte</b>: https://t.me/JADIEL_TM"
            )
            bot.reply_to(message, mensagem_cupom, parse_mode='HTML')
            admin_state[chat_id] = None
        except ValueError:
            bot.reply_to(message, "❌ Erro: Digite um número válido para o limite. Exemplo: 30")
    
    elif step == 'adm_wait_midia_text':
        texto = message.text
        admin_state[chat_id]['tipo'] = 'texto'
        admin_state[chat_id]['conteudo'] = texto
        admin_state[chat_id]['step'] = 'adm_wait_midia_confirm'
        preview = f"📝 PREVIEW DO TEXTO:\n\n{texto}\n\n━━━━━━━━━━━━━━━━\n👥 Destinatários: {len(user_db)} usuários\n\nDeseja enviar agora?"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✔️ SIM, ENVIAR", callback_data="confirmar_envio"),
            types.InlineKeyboardButton("❌ NÃO, CANCELAR", callback_data="cancelar_envio")
        )
        bot.reply_to(message, preview, reply_markup=markup)
    
    elif step == 'promo_wait_price':
        try:
            preco = float(message.text)
            if preco <= 0:
                bot.reply_to(message, "❌ O preço deve ser maior que zero. Tente novamente.")
                return
            admin_state[chat_id] = {'step': 'promo_wait_days', 'preco': preco}
            bot.reply_to(message, f"💰 Preço definido: R$ {preco:.2f}\n\n📅 Quantos dias de licença para esta promoção?")
        except ValueError:
            bot.reply_to(message, "❌ Valor inválido. Digite um número, ex: 5.00")
    
    elif step == 'promo_wait_days':
        try:
            dias = int(message.text)
            if dias <= 0:
                bot.reply_to(message, "❌ Os dias devem ser maiores que zero. Tente novamente.")
                return
            preco = admin_state[chat_id]['preco']
            admin_state[chat_id] = {'step': 'promo_wait_hours', 'preco': preco, 'dias': dias}
            bot.reply_to(message, f"📅 Dias definidos: {dias}\n\n⏰ Por quantas horas a promoção ficará ativa?")
        except ValueError:
            bot.reply_to(message, "❌ Valor inválido. Digite um número inteiro de dias.")
    
    elif step == 'promo_wait_hours':
        try:
            horas = int(message.text)
            if horas <= 0:
                bot.reply_to(message, "❌ As horas devem ser maiores que zero. Tente novamente.")
                return
            preco = admin_state[chat_id]['preco']
            dias = admin_state[chat_id]['dias']
            admin_state[chat_id] = {'step': 'promo_wait_media_type', 'preco': preco, 'dias': dias, 'horas': horas}
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📝 Apenas Texto", callback_data="promo_media_text"),
                types.InlineKeyboardButton("🖼️ Imagem com Legenda", callback_data="promo_media_image")
            )
            bot.reply_to(message, f"⏰ Duração definida: {horas} horas\n\n📤 Como deseja enviar a promoção?", reply_markup=markup)
        except ValueError:
            bot.reply_to(message, "❌ Valor inválido. Digite um número inteiro de horas.")
    
    elif step == 'promo_wait_text':
        try:
            texto = message.text
            if not texto.strip():
                bot.reply_to(message, "❌ O texto não pode estar vazio. Tente novamente.")
                return
            preco = admin_state[chat_id]['preco']
            dias = admin_state[chat_id]['dias']
            horas = admin_state[chat_id]['horas']
            promo_id = str(uuid.uuid4())[:8]
            mensagens_enviadas = enviar_promocao_para_todos(chat_id, promo_id, preco, dias, horas, texto=texto)
            promocao = {
                'id': promo_id, 'preco': preco, 'dias': dias,
                'horas_duracao': horas, 'data_criacao': datetime.now(),
                'mensagens': mensagens_enviadas, 'texto': texto,
                'imagem': None, 'tipo': 'texto'
            }
            promocoes_ativas[promo_id] = promocao
            job_id = agendar_exclusao_promocao(promo_id, horas)
            if job_id:
                promocao['job_id'] = job_id
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("promocao_criada", promo_id)
            admin_state[chat_id] = None
            bot.reply_to(message, f"🎉 PROMOÇÃO VIP ENVIADA COM SUCESSO!\n\n💰 Preço: R$ {preco:.2f}\n📅 Dias: {dias}\n⏰ Duração: {horas} horas\n🆔 ID da promoção: {promo_id}\n👥 Enviada para: {len(mensagens_enviadas)} usuários\n\n⚠️ A promoção será excluída automaticamente após {horas} horas.")
        except Exception as e:
            log_terminal(f"❌ Erro ao criar promoção: {e}")
            bot.reply_to(message, f"❌ Erro ao criar promoção: {str(e)[:100]}")
    
    elif step == 'admin_wait_reset_numbers':
        texto = message.text.strip().lower()
        if texto == 'cancelar':
            admin_state.pop(chat_id, None)
            bot.reply_to(message, "❌ Reset massivo cancelado.")
            return
        linhas = texto.split('\n')
        resultados = []
        processados = 0
        msg_status = bot.reply_to(message, "🔄 Processando números...")
        for linha in linhas[:10]:
            partes = linha.strip().split()
            if len(partes) >= 2:
                telefone = partes[0]
                operadora = partes[1].lower()
                if operadora in ['vivo', 'claro', 'tim'] and len(telefone) == 11 and telefone.isdigit():
                    sucesso, mensagem = api_desbanir_numero(telefone, operadora)
                    if not sucesso:
                        sucesso, mensagem = api_resetar_conta(telefone, operadora)
                    resultados.append(f"{telefone} ({operadora}): {'✅' if sucesso else '❌'} - {mensagem[:50]}")
                    processados += 1
                    time.sleep(1)
        admin_state.pop(chat_id, None)
        relatorio = f"📊 RESET MASSIVO CONCLUÍDO\n\n🔢 Números processados: {processados}\n\n📋 Resultados:\n" + "\n".join(resultados[:20])
        if len(resultados) > 20:
            relatorio += f"\n\n... e mais {len(resultados) - 20} resultados"
        try:
            bot.edit_message_text(relatorio, chat_id=chat_id, message_id=msg_status.message_id)
        except:
            bot.send_message(chat_id, relatorio)
        log_terminal(f"RESET MASSIVO: {processados} números processados")

@bot.message_handler(content_types=['photo', 'video'], func=lambda m: m.chat.id == ADMIN_ID and m.chat.id in admin_state and admin_state[m.chat.id] is not None)
def admin_media_handler(message):
    chat_id = message.chat.id
    if chat_id not in admin_state or admin_state[chat_id] is None:
        return
    
    step = admin_state[chat_id].get('step')
    
    if step == 'adm_wait_midia_image' and message.photo:
        file_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ""
        admin_state[chat_id]['tipo'] = 'imagem'
        admin_state[chat_id]['file_id'] = file_id
        admin_state[chat_id]['conteudo'] = caption
        admin_state[chat_id]['step'] = 'adm_wait_midia_confirm'
        preview = f"🖼️ PREVIEW DA IMAGEM\n\nLegenda: {caption if caption else '(Sem legenda)'}\n\n━━━━━━━━━━━━━━━━\n👥 Destinatários: {len(user_db)} usuários\n\nDeseja enviar agora?"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✔️ SIM, ENVIAR", callback_data="confirmar_envio"),
            types.InlineKeyboardButton("❌ NÃO, CANCELAR", callback_data="cancelar_envio")
        )
        bot.reply_to(message, preview, reply_markup=markup)
    
    elif step == 'adm_wait_midia_video' and message.video:
        file_id = message.video.file_id
        caption = message.caption if message.caption else ""
        admin_state[chat_id]['tipo'] = 'video'
        admin_state[chat_id]['file_id'] = file_id
        admin_state[chat_id]['conteudo'] = caption
        admin_state[chat_id]['step'] = 'adm_wait_midia_confirm'
        preview = f"🎬 PREVIEW DO VÍDEO\n\nLegenda: {caption if caption else '(Sem legenda)'}\n\n━━━━━━━━━━━━━━━━\n👥 Destinatários: {len(user_db)} usuários\n\nDeseja enviar agora?"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✔️ SIM, ENVIAR", callback_data="confirmar_envio"),
            types.InlineKeyboardButton("❌ NÃO, CANCELAR", callback_data="cancelar_envio")
        )
        bot.reply_to(message, preview, reply_markup=markup)
    
    elif step == 'promo_wait_image' and message.photo:
        try:
            file_id = message.photo[-1].file_id
            caption = message.caption if message.caption else ""
            preco = admin_state[chat_id]['preco']
            dias = admin_state[chat_id]['dias']
            horas = admin_state[chat_id]['horas']
            promo_id = str(uuid.uuid4())[:8]
            mensagens_enviadas = enviar_promocao_para_todos(chat_id, promo_id, preco, dias, horas, imagem=file_id, texto=caption)
            promocao = {
                'id': promo_id, 'preco': preco, 'dias': dias,
                'horas_duracao': horas, 'data_criacao': datetime.now(),
                'mensagens': mensagens_enviadas, 'texto': caption,
                'imagem': file_id, 'tipo': 'imagem'
            }
            promocoes_ativas[promo_id] = promocao
            job_id = agendar_exclusao_promocao(promo_id, horas)
            if job_id:
                promocao['job_id'] = job_id
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("promocao_criada", promo_id)
            admin_state[chat_id] = None
            bot.reply_to(message, f"🎉 PROMOÇÃO VIP ENVIADA COM SUCESSO!\n\n💰 Preço: R$ {preco:.2f}\n📅 Dias: {dias}\n⏰ Duração: {horas} horas\n🆔 ID da promoção: {promo_id}\n👥 Enviada para: {len(mensagens_enviadas)} usuários\n\n⚠️ A promoção será excluída automaticamente após {horas} horas.")
        except Exception as e:
            log_terminal(f"❌ Erro ao criar promoção com imagem: {e}")
            bot.reply_to(message, f"❌ Erro ao criar promoção: {str(e)[:100]}")

# ==============================================================================
# 🤖 HANDLER DE FLUXO DE ADIÇÃO DE CONTA
# ==============================================================================
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    
    if chat_id == ADMIN_ID and chat_id in admin_state and admin_state[chat_id] is not None:
        return
    
    if message.text and message.text.startswith('/'):
        show_menu_with_image(chat_id, is_logged=(chat_id in user_db and user_db[chat_id].get('contas')))
        return
    
    if chat_id in user_state and user_state[chat_id].get('step'):
        step = user_state[chat_id]['step']
        
        if step == 'add_account_telefone':
            operator = user_state[chat_id].get('operator', 'vivo')
            tel = ''.join(filter(str.isdigit, message.text))
            
            if len(tel) < 10 or len(tel) > 11:
                bot.reply_to(message, "❌ Número inválido. Digite o número com DDD (10 ou 11 dígitos, ex: 11999999999).")
                return
            
            if not tel.startswith('55'):
                tel = '55' + tel
            
            user_state[chat_id]['temp_telefone'] = tel
            user_state[chat_id]['step'] = 'add_account_codigo'
            
            msg_envio = bot.reply_to(message, "📨 Enviando SMS...")
            try:
                base_url = get_base_url(operator)
                headers = get_headers_login(operator)
                payload = {"msisdn": tel}
                response = requests.post(f"{base_url}/pnde", json=payload, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    bot.edit_message_text("✔️ Código SMS enviado!\n\nDigite o código de 6 números abaixo:", chat_id, msg_envio.message_id)
                else:
                    error_msg = f"❌ Erro ao enviar SMS. Status: {response.status_code}"
                    if response.text:
                        try:
                            error_json = response.json()
                            error_msg += f"\nDetalhes: {json.dumps(error_json, indent=2, ensure_ascii=False)[:500]}"
                        except:
                            error_msg += f"\nResposta: {response.text[:500]}"
                    bot.edit_message_text(error_msg, chat_id, msg_envio.message_id)
                    user_state[chat_id]['step'] = 'add_account_telefone'
            except requests.exceptions.Timeout:
                bot.edit_message_text("❌ Timeout: O servidor demorou muito para responder. Tente novamente.", chat_id, msg_envio.message_id)
                user_state[chat_id]['step'] = 'add_account_telefone'
            except requests.exceptions.ConnectionError:
                bot.edit_message_text("❌ Erro de conexão: Não foi possível conectar ao servidor. Verifique sua internet.", chat_id, msg_envio.message_id)
                user_state[chat_id]['step'] = 'add_account_telefone'
            except Exception as e:
                bot.edit_message_text(f"❌ Erro de conexão: {str(e)[:500]}", chat_id, msg_envio.message_id)
                user_state[chat_id]['step'] = 'add_account_telefone'
        
        elif step == 'add_account_codigo':
            code = message.text.strip()
            tel = user_state[chat_id].get('temp_telefone', '')
            operator = user_state[chat_id].get('operator', 'vivo')
            
            if not tel:
                bot.reply_to(message, "❌ Sessão expirada. Por favor, inicie o processo novamente.")
                user_state.pop(chat_id, None)
                return
            
            msg = bot.send_message(chat_id, "🔐 Validando código...")
            
            try:
                base_url = get_base_url(operator)
                headers = get_headers_login(operator)
                headers["X-USER-ID"] = tel
                headers["X-PINCODE"] = code
                payload = {"msisdn": tel, "code": code}
                response = requests.post(f"{base_url}/vapi", json=payload, headers=headers, timeout=15)
                token = response.headers.get('X-AUTHORIZATION')
                
                log_terminal(f"Resposta da API {operator}: Status {response.status_code}")
                if response.status_code != 200:
                    log_terminal(f"Erro resposta: {response.text[:500]}")
                
                if token:
                    wallet, _ = extrair_dados_token(token)
                    if wallet:
                        telefone_formatado = tel[2:] if tel.startswith('55') else tel
                        success, msg_result = adicionar_conta(chat_id, telefone_formatado, token, wallet, operator)
                        
                        if success:
                            user = user_db[chat_id]
                            contas = user.get('contas', [])
                            if len(contas) == 1 and chat_id != ADMIN_ID:
                                if not user_db[chat_id].get('license_date'):
                                    user_db[chat_id]['license_date'] = datetime.now() + timedelta(days=2)
                                    data_manager.save_all_data()
                                    msg_result += "\n🎁 Você ganhou 2 dias de teste grátis!"
                            
                            bot.delete_message(chat_id, msg.message_id)
                            saudacao = get_saudacao()
                            nome = message.from_user.first_name
                            legenda = f"{saudacao}, {nome}! 👋\n\n✔️ {msg_result}\n\n👇 Escolha uma opção:"
                            
                            try:
                                bot.send_photo(chat_id, START_IMAGE, caption=legenda, reply_markup=menu_principal_logado(), parse_mode='HTML')
                            except:
                                bot.send_message(chat_id, legenda, reply_markup=menu_principal_logado())
                        else:
                            bot.edit_message_text(f"❌ {msg_result}", chat_id, msg.message_id)
                    else:
                        markup = types.InlineKeyboardMarkup(row_width=1)
                        markup.add(types.InlineKeyboardButton(f"{'🟣' if operator == 'vivo' else '🔴' if operator == 'claro' else '🔵'} TENTAR NOVAMENTE", callback_data=f"operator_{operator}"))
                        markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
                        bot.edit_message_text("❌ Erro ao extrair dados da conta.", chat_id, msg.message_id, reply_markup=markup)
                else:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    markup.add(types.InlineKeyboardButton(f"{'🟣' if operator == 'vivo' else '🔴' if operator == 'claro' else '🔵'} TENTAR NOVAMENTE", callback_data=f"operator_{operator}"))
                    markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
                    
                    error_msg = "❌ Código incorreto ou expirado. Tente novamente."
                    if response.text:
                        try:
                            error_data = response.json()
                            error_msg += f"\n\nDetalhes: {json.dumps(error_data, indent=2, ensure_ascii=False)[:400]}"
                        except:
                            error_msg += f"\n\nResposta: {response.text[:400]}"
                    
                    bot.edit_message_text(error_msg, chat_id, msg.message_id, reply_markup=markup)
                
                if chat_id in user_state:
                    del user_state[chat_id]
            except requests.exceptions.Timeout:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(f"{'🟣' if operator == 'vivo' else '🔴' if operator == 'claro' else '🔵'} TENTAR NOVAMENTE", callback_data=f"operator_{operator}"))
                markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
                bot.edit_message_text("❌ Timeout: O servidor demorou muito para responder. Tente novamente.", chat_id, msg.message_id, reply_markup=markup)
                if chat_id in user_state:
                    del user_state[chat_id]
            except requests.exceptions.ConnectionError:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(f"{'🟣' if operator == 'vivo' else '🔴' if operator == 'claro' else '🔵'} TENTAR NOVAMENTE", callback_data=f"operator_{operator}"))
                markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
                bot.edit_message_text("❌ Erro de conexão: Não foi possível conectar ao servidor. Verifique sua internet.", chat_id, msg.message_id, reply_markup=markup)
                if chat_id in user_state:
                    del user_state[chat_id]
            except Exception as e:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(f"{'🟣' if operator == 'vivo' else '🔴' if operator == 'claro' else '🔵'} TENTAR NOVAMENTE", callback_data=f"operator_{operator}"))
                markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
                bot.edit_message_text(f"❌ Erro: {str(e)[:500]}", chat_id, msg.message_id, reply_markup=markup)
                if chat_id in user_state:
                    del user_state[chat_id]
    
    elif chat_id in user_state and user_state[chat_id].get('step', '').startswith('desbanir_'):
        texto = message.text.strip().lower()
        
        if texto == 'cancelar':
            user_state.pop(chat_id, None)
            bot.send_message(chat_id, "❌ Desbanimento cancelado.")
            show_menu_with_image(chat_id, is_logged=(chat_id in user_db and user_db[chat_id].get('contas')))
            return
        
        step = user_state[chat_id]['step']
        
        if step == 'desbanir_wait_number':
            telefone = ''.join(filter(str.isdigit, texto))
            operadora = user_state[chat_id]['operadora']
            
            if len(telefone) != 11:
                bot.reply_to(message, "❌ Número inválido! Use 11 dígitos com DDD (ex: 11999999999)")
                return
            
            msg_status = bot.reply_to(message, f"🔓 PROCESSANDO DESBANIMENTO...\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}\n\n⏳ Isso pode levar alguns segundos...")
            
            sucesso, mensagem = api_desbanir_numero(telefone, operadora)
            if not sucesso:
                sucesso, mensagem = api_resetar_conta(telefone, operadora)
            
            try:
                bot.edit_message_text(
                    f"🔓 RESULTADO DO DESBANIMENTO\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}\n\n{mensagem}\n\n🔄 Agora você pode:\n1. Tentar fazer login novamente\n2. Aguardar 1 hora se ainda não funcionar\n3. Entrar em contato com o suporte\n\n🥰 SUPORTE: @JADIEL_TM",
                    chat_id=chat_id, message_id=msg_status.message_id
                )
            except:
                bot.send_message(chat_id, f"🔓 RESULTADO DO DESBANIMENTO\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}\n\n{mensagem}")
            
            user_state.pop(chat_id, None)
            log_terminal(f"DESBANIMENTO: {chat_id} - {telefone} ({operadora}) - Sucesso: {sucesso}")
    
    else:
        show_menu_with_image(chat_id, is_logged=(chat_id in user_db and user_db[chat_id].get('contas')))

# ==============================================================================
# 🤖 HANDLERS DE CALLBACK
# ==============================================================================
@bot.callback_query_handler(func=lambda call: True)
def callback_manager(call):
    cid = call.message.chat.id
    
    try:
        if call.data == "start_farm_turbo":
            user = user_db.get(cid, {})
            contas = user.get('contas', [])
            conta_ativa = user.get('conta_ativa', 0)
            
            if contas:
                conta = contas[conta_ativa]
                operadora = conta.get('operadora', 'vivo')
                if operadora == 'vivo':
                    bot.answer_callback_query(call.id, "⚡ Iniciando coleta Vivo")
                elif operadora == 'tim':
                    bot.answer_callback_query(call.id, "⚡ Iniciando coleta TIM")
                else:
                    bot.answer_callback_query(call.id, "⚡ Iniciando coleta")
            else:
                bot.answer_callback_query(call.id, "⚡ Iniciando coleta")
            
            def farm_thread():
                try:
                    api_executar_farm(cid)
                except Exception as e:
                    log_terminal(f"Erro no farm: {e}")
                    bot.send_message(cid, f"❌ Erro durante a coleta: {str(e)[:100]}")
            
            thread = threading.Thread(target=farm_thread)
            thread.start()
        
        elif call.data == "login_start":
            if cid not in user_db:
                user_db[cid] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
                data_manager.save_all_data()
            bot.send_message(cid, "📡 Selecione a operadora da conta que deseja adicionar:", reply_markup=menu_operadora())
        
        elif call.data == "operator_vivo":
            if cid not in user_db:
                user_db[cid] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
                data_manager.save_all_data()
            user_state[cid] = {'step': 'add_account_telefone', 'operator': 'vivo'}
            bot.send_message(cid, "📲 ADICIONAR CONTA VIVO\n\nPor favor, digite o número com DDD (ex: 11999999999):\n\n⚠️ Use apenas números da Vivo")
        
        elif call.data == "operator_claro":
            if cid not in user_db:
                user_db[cid] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
                data_manager.save_all_data()
            user_state[cid] = {'step': 'add_account_telefone', 'operator': 'claro'}
            bot.send_message(cid, "📲 ADICIONAR CONTA CLARO\n\nPor favor, digite o número com DDD (ex: 11999999999):\n\n⚠️ Use apenas números da Claro")
        
        elif call.data == "operator_tim":
            if cid not in user_db:
                user_db[cid] = {'contas': [], 'conta_ativa': 0, 'config': {'auto_farm': False}}
                data_manager.save_all_data()
            user_state[cid] = {'step': 'add_account_telefone', 'operator': 'tim'}
            bot.send_message(cid, "📲 ADICIONAR CONTA TIM\n\nPor favor, digite o número com DDD (ex: 11999999999):\n\n⚠️ Use apenas números da TIM")
        
        elif call.data == "my_license":
            user = user_db.get(cid, {})
            validade = user.get('license_date')
            contas = user.get('contas', [])
            conta_ativa = user.get('conta_ativa', 0)
            
            if contas:
                telefone = contas[conta_ativa].get('telefone', 'Não logado')
                operadora = contas[conta_ativa].get('operadora', 'vivo')
                pontos_total = contas[conta_ativa].get('pontos_total', 0)
            else:
                telefone = 'Não logado'
                operadora = ''
                pontos_total = 0
            
            status_lic = "❌ Expirada"
            data_fmt = "--/--/--"
            
            if validade and validade > datetime.now():
                status_lic = "✔️ Ativa"
                data_fmt = formatar_data(validade)
            
            if operadora == 'vivo':
                icon = "🟣"; nome_op = "VIVO"
            elif operadora == 'claro':
                icon = "🔴"; nome_op = "CLARO"
            elif operadora == 'tim':
                icon = "🔵"; nome_op = "TIM"
            else:
                icon = "📱"; nome_op = ""
            
            msg = (
                f"🔒 SUA LICENÇA\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"👤 Usuário: {call.from_user.first_name}\n"
                f"📱 Telefone: {telefone}\n"
                f"📡 Operadora: {icon} {nome_op}\n"
                f"🏆 Pontos totais: {pontos_total}\n"
                f"📅 Validade: {data_fmt}\n"
                f"📊 Status: {status_lic}\n\n"
                f"💡 Dicas:\n"
                f"• Use /cupom CODIGO para resgatar cupons\n"
                f"• Compre 30 dias por apenas R$ 25,00\n"
                f"• Suporte: @JADIEL_TM"
            )
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("💳 COMPRAR 30 DIAS - R$ 25,00", callback_data="comprar_licenca"))
            markup.add(types.InlineKeyboardButton("⚙️ CONFIGURAÇÕES", callback_data="config_menu"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.send_message(cid, msg, reply_markup=markup)
        
        elif call.data == "comprar_licenca":
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("💳 PAGAR COM PIX - R$ 25,00", callback_data="gerar_pagamento_pix"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar à Licença", callback_data="my_license"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            msg = (
                "💰 COMPRAR LICENÇA\n"
                "━━━━━━━━━━━━━━━━\n"
                f"📅 Duração: {DIAS_LICENCA} dias\n"
                f"💵 Valor: R$ {VALOR_LICENCA:.2f}\n"
                f"💳 Forma de pagamento: PIX\n\n"
                f"✔️ Vantagens:\n"
                f"• Acesso completo ao bot\n"
                f"• Coleta automática diária\n"
                f"• Suporte prioritário\n\n"
                f"Clique no botão abaixo para gerar o PIX:"
            )
            bot.send_message(cid, msg, reply_markup=markup)
        
        elif call.data == "gerar_pagamento_pix":
            bot.answer_callback_query(call.id, "Gerando pagamento PIX...")
            gerar_pagamento_pix(cid)
        
        elif call.data.startswith("promo_pagar|"):
            promo_id = call.data.split("|")[1]
            if promo_id in promocoes_ativas:
                promocao = promocoes_ativas[promo_id]
                preco = promocao['preco']
                dias = promocao['dias']
                bot.answer_callback_query(call.id, f"Gerando pagamento promocional...")
                gerar_pagamento_pix_promocional(cid, preco, dias, promo_id)
            else:
                bot.answer_callback_query(call.id, "❌ Esta promoção não está mais disponível.")
        
        elif call.data.startswith("verificar_pagamento|"):
            pass
        
        elif call.data == "afiliado_menu":
            msg = (
                "🤝 SEJA UM AFILIADO!\n\n"
                "🚀 DIVULGUE O BOT E GANHE 3 DIAS GRÁTIS, "
                "VOCÊ E QUEM ENTRAR ATRAVÉS DO SEU LINK! 🎁💰"
            )
            try:
                bot.edit_message_text(msg, cid, call.message.message_id, reply_markup=menu_afiliado())
            except:
                bot.send_message(cid, msg, reply_markup=menu_afiliado())
        
        elif call.data == "afiliado_gerar_link":
            try:
                link, codigo = gerar_link_afiliado(cid)
                if not link:
                    bot.answer_callback_query(call.id, "❌ Erro ao gerar link")
                    return
                
                msg = (
                    "🤝 *SEU LINK DE AFILIADO EXCLUSIVO!*\n\n"
                    f"🔗 *Link:*\n`{link}`\n\n"
                    f"🔑 *Código:* `{codigo}`\n\n"
                    "━━━━━━━━━━━━━━━━\n"
                    "🎁 *COMO FUNCIONA:*\n"
                    f"• Cada novo usuário que entrar pelo seu link = *+{DIAS_BONUS_AFILIADO} dias grátis* pra você e pra ele!\n"
                    "• Só vale para *novos usuários*\n"
                    "• Compartilhe nas suas redes sociais\n\n"
                    "🚀 *COMECE A DIVULGAR AGORA!*"
                )
                
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(
                    "📊 VER MEU PAINEL",
                    callback_data="afiliado_painel",
                    style="success"
                ))
                markup.add(types.InlineKeyboardButton(
                    "🔙 Voltar",
                    callback_data="afiliado_menu",
                    style="success"
                ))
                
                bot.send_message(cid, msg, parse_mode='Markdown', reply_markup=markup)
                bot.answer_callback_query(call.id, "✅ Link gerado com sucesso!")
            except Exception as e:
                log_terminal(f"❌ Erro ao gerar link de afiliado: {e}")
                bot.answer_callback_query(call.id, f"❌ Erro: {str(e)[:50]}")
        
        elif call.data == "afiliado_painel":
            bot.answer_callback_query(call.id, "📊 Carregando painel...")
            mostrar_painel_afiliado(cid)
        
        elif call.data == "afiliado_copiar_link":
            try:
                if cid in data_manager.afiliados_db:
                    codigo = data_manager.afiliados_db[cid].get('codigo', '')
                    bot_username = get_bot_username()
                    link = f"https://t.me/{bot_username}?start={codigo}"
                    bot.send_message(
                        cid,
                        f"🔗 *SEU LINK DE AFILIADO:*\n\n`{link}`\n\n"
                        "👆 *Copie o link acima e compartilhe!*\n\n"
                        "💡 *Dica:* Envie para amigos, grupos e redes sociais para ganhar mais!",
                        parse_mode='Markdown'
                    )
                    bot.answer_callback_query(call.id, "✅ Link enviado!")
                else:
                    bot.answer_callback_query(call.id, "❌ Você ainda não tem um link. Clique em SE AFILIE AQUI!")
            except Exception as e:
                log_terminal(f"❌ Erro ao copiar link de afiliado: {e}")
                bot.answer_callback_query(call.id, "❌ Erro ao copiar link")
        
        elif call.data == "config_menu":
            if cid in user_db and user_db[cid].get('contas'):
                try:
                    bot.edit_message_text("⚙️ CONFIGURAÇÕES DO BOT", cid, call.message.message_id, reply_markup=menu_configuracoes(cid))
                except:
                    bot.send_message(cid, "⚙️ CONFIGURAÇÕES DO BOT", reply_markup=menu_configuracoes(cid))
            else:
                bot.send_message(cid, "⚠️ Primeiro faça login para acessar as configurações.")
        
        elif call.data == "toggle_auto_farm":
            success = toggle_auto_farm(cid)
            if success is not None:
                try:
                    bot.edit_message_text("⚙️ CONFIGURAÇÕES DO BOT", cid, call.message.message_id, reply_markup=menu_configuracoes(cid))
                except:
                    bot.send_message(cid, "⚙️ CONFIGURAÇÕES DO BOT", reply_markup=menu_configuracoes(cid))
        
        elif call.data == "manage_accounts":
            try:
                bot.edit_message_text("📱 GERENCIAR CONTAS", cid, call.message.message_id, reply_markup=menu_gerenciar_contas(cid))
            except:
                bot.send_message(cid, "📱 GERENCIAR CONTAS", reply_markup=menu_gerenciar_contas(cid))
        
        elif call.data == "add_new_account":
            bot.send_message(cid, "📡 Selecione a operadora da conta que deseja adicionar:", reply_markup=menu_operadora())
        
        elif call.data == "remove_account":
            success, message, sem_contas = remover_conta_ativa(cid)
            
            if success and sem_contas:
                try:
                    bot.delete_message(cid, call.message.message_id)
                except:
                    pass
                bot.send_message(cid, message)
                if cid in user_state:
                    del user_state[cid]
                show_menu_with_image(cid, is_logged=False)
            else:
                bot.send_message(cid, message)
                try:
                    bot.edit_message_text("📱 GERENCIAR CONTAS", cid, call.message.message_id, reply_markup=menu_gerenciar_contas(cid))
                except:
                    bot.send_message(cid, "📱 GERENCIAR CONTAS", reply_markup=menu_gerenciar_contas(cid))
        
        elif call.data.startswith("select_account|"):
            try:
                indice = int(call.data.split("|")[1])
                success, message = selecionar_conta(cid, indice)
                bot.send_message(cid, message)
                try:
                    bot.edit_message_text("📱 GERENCIAR CONTAS", cid, call.message.message_id, reply_markup=menu_gerenciar_contas(cid))
                except:
                    bot.send_message(cid, "📱 GERENCIAR CONTAS", reply_markup=menu_gerenciar_contas(cid))
            except:
                bot.send_message(cid, "❌ Erro ao selecionar conta.")
        
        elif call.data == "back_home":
            try:
                bot.delete_message(cid, call.message.message_id)
            except:
                pass
            if cid in user_state:
                del user_state[cid]
            if cid in user_db and user_db[cid].get('contas'):
                show_menu_with_image(cid, is_logged=True)
            else:
                show_menu_with_image(cid, is_logged=False)
        
        elif call.data == "check_balance": 
            api_ver_saldo(cid)
        elif call.data == "redeem_menu": 
            api_abrir_loja(cid)
        elif call.data.startswith("confirm_buy"):
            _, pid, pr, nm = call.data.split("|")
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("✔️ CONFIRMAR", callback_data=f"do_buy|{pid}|{nm}"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar à Loja", callback_data="redeem_menu"))
            markup.add(types.InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_home"))
            bot.edit_message_text(f"⚠️ Confirmar resgate de {nm} por {pr} pontos?", cid, call.message.message_id, reply_markup=markup)
        elif call.data.startswith("do_buy"):
            _, pid, nm = call.data.split("|")
            api_comprar(cid, pid, nm)
        
        elif call.data == "enviar_texto":
            if cid == ADMIN_ID:
                admin_state[cid] = {'step': 'adm_wait_midia_text'}
                bot.edit_message_text("📝 ENVIAR TEXTO\n\nDigite o texto que deseja enviar para todos os usuários:", cid, call.message.message_id)
        
        elif call.data == "enviar_imagem":
            if cid == ADMIN_ID:
                admin_state[cid] = {'step': 'adm_wait_midia_image'}
                bot.edit_message_text("🖼️ ENVIAR IMAGEM\n\nEnvie a imagem que deseja enviar para todos os usuários.\n\nVocê pode adicionar uma legenda opcional.", cid, call.message.message_id)
        
        elif call.data == "enviar_video":
            if cid == ADMIN_ID:
                admin_state[cid] = {'step': 'adm_wait_midia_video'}
                bot.edit_message_text("🎬 ENVIAR VÍDEO\n\nEnvie o vídeo que deseja enviar para todos os usuários.\n\nVocê pode adicionar uma legenda opcional.", cid, call.message.message_id)
        
        elif call.data == "confirmar_envio":
            if cid == ADMIN_ID and cid in admin_state and admin_state[cid] is not None:
                estado = admin_state[cid]
                if estado.get('step') == 'adm_wait_midia_confirm':
                    tipo = estado.get('tipo', 'texto')
                    conteudo = estado.get('conteudo', '')
                    file_id = estado.get('file_id', None)
                    sucesso = enviar_midia_para_todos(cid, tipo, conteudo, file_id)
                    if sucesso:
                        bot.edit_message_text(f"✔️ {tipo.upper()} ENVIADO COM SUCESSO PARA TODOS OS USUÁRIOS!", cid, call.message.message_id)
                    else:
                        bot.edit_message_text("❌ Erro ao enviar mídia.", cid, call.message.message_id)
                    admin_state[cid] = None
        
        elif call.data == "cancelar_envio":
            if cid == ADMIN_ID:
                admin_state[cid] = None
                bot.edit_message_text("❌ ENVIO DE MÍDIA CANCELADO", cid, call.message.message_id)
        
        elif call.data == "promo_media_text":
            if cid == ADMIN_ID and cid in admin_state and admin_state[cid].get('step') == 'promo_wait_media_type':
                admin_state[cid]['step'] = 'promo_wait_text'
                bot.edit_message_text("📝 Digite o texto da promoção VIP:", cid, call.message.message_id)
        
        elif call.data == "promo_media_image":
            if cid == ADMIN_ID and cid in admin_state and admin_state[cid].get('step') == 'promo_wait_media_type':
                admin_state[cid]['step'] = 'promo_wait_image'
                bot.edit_message_text("🖼️ Envie a imagem da promoção VIP (com legenda opcional):", cid, call.message.message_id)
        
        elif call.data == "desbanir_start":
            comando_desbanir(call.message)
        
        elif call.data == "desbanir_vivo":
            user_state[cid] = {'step': 'desbanir_wait_number', 'operadora': 'vivo'}
            bot.send_message(cid, "🟣 DESBANIR NÚMERO VIVO\n\nDigite o número com DDD (11 dígitos):\n\nExemplo: 11999999999\n\n⚠️ Use apenas números Vivo\n⚠️ Digite 'cancelar' para cancelar")
        
        elif call.data == "desbanir_claro":
            user_state[cid] = {'step': 'desbanir_wait_number', 'operadora': 'claro'}
            bot.send_message(cid, "🔴 DESBANIR NÚMERO CLARO\n\nDigite o número com DDD (11 dígitos):\n\nExemplo: 11999999999\n\n⚠️ Use apenas números Claro\n⚠️ Digite 'cancelar' para cancelar")
        
        elif call.data == "desbanir_tim":
            user_state[cid] = {'step': 'desbanir_wait_number', 'operadora': 'tim'}
            bot.send_message(cid, "🔵 DESBANIR NÚMERO TIM\n\nDigite o número com DDD (11 dígitos):\n\nExemplo: 11999999999\n\n⚠️ Use apenas números TIM\n⚠️ Digite 'cancelar' para cancelar")
        
        elif call.data.startswith("desbanir_conta|"):
            idx = int(call.data.split("|")[1])
            user = user_db.get(cid, {})
            contas = user.get('contas', [])
            
            if idx < len(contas):
                conta = contas[idx]
                telefone = conta.get('telefone', '')
                operadora = conta.get('operadora', 'vivo')
                
                bot.answer_callback_query(call.id, "🔓 Processando desbanimento...")
                msg_status = bot.send_message(cid, f"🔓 DESBANINDO SUA CONTA...\n\n📱 Número: {telefone}\n📡 Operadora: {operadora.upper()}\n\n⏳ Aguarde alguns segundos...")
                
                sucesso, mensagem = api_desbanir_numero(telefone, operadora)
                if not sucesso:
                    sucesso, mensagem = api_resetar_conta(telefone, operadora)
                
                try:
                    bot.edit_message_text(
                        f"🔓 RESULTADO DO DESBANIMENTO\n\n📱 Sua conta: {telefone}\n📡 Operadora: {operadora.upper()}\n\n{mensagem}\n\n🔄 Agora tente fazer login novamente:\n1. Vá para Configurações\n2. Adicione a conta novamente\n3. Use o mesmo número\n\n⚠️ Se não funcionar, aguarde 1 hora e tente novamente",
                        chat_id=cid, message_id=msg_status.message_id
                    )
                except:
                    bot.send_message(cid, f"🔓 RESULTADO DO DESBANIMENTO\n\n📱 Sua conta: {telefone}\n📡 Operadora: {operadora.upper()}\n\n{mensagem}")
                
                log_terminal(f"DESBANIMENTO CONTA: {cid} - {telefone} ({operadora})")
        
        elif call.data == "desbanir_outro":
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🟣 VIVO", callback_data="desbanir_vivo"),
                types.InlineKeyboardButton("🔴 CLARO", callback_data="desbanir_claro"),
                types.InlineKeyboardButton("🔵 TIM", callback_data="desbanir_tim")
            )
            markup.add(types.InlineKeyboardButton("🔙 Voltar", callback_data="desbanir_back"))
            try:
                bot.edit_message_text("🔓 DESBANIR OUTRO NÚMERO\n\nSelecione a operadora do número:", chat_id=cid, message_id=call.message.message_id, reply_markup=markup)
            except:
                bot.send_message(cid, "🔓 DESBANIR OUTRO NÚMERO\n\nSelecione a operadora do número:", reply_markup=markup)
        
        elif call.data == "desbanir_back":
            comando_desbanir(call.message)
        
        elif call.data == "manual_baixar_jsons":
            if cid == ADMIN_ID:
                bot.answer_callback_query(call.id, "Baixando JSONs do canal...")
                arquivos = []
                try:
                    messages = bot.get_chat_history(BACKUP_CHANNEL_ID, limit=100)
                    for msg in messages:
                        if msg.document and msg.document.file_name:
                            arquivos.append(msg.document.file_name)
                    bot.send_message(cid, f"📊 Encontrados {len(arquivos)} arquivos no canal.\n\n" + "\n".join(arquivos[:20]) + ("\n\n..." if len(arquivos) > 20 else ""))
                except Exception as e:
                    bot.send_message(cid, f"❌ Erro: {str(e)[:200]}")
        
        elif call.data == "manual_restaurar_userdb":
            if cid == ADMIN_ID:
                bot.answer_callback_query(call.id, "Restaurando user_db.json...")
                try:
                    messages = bot.get_chat_history(BACKUP_CHANNEL_ID, limit=100)
                    user_db_msg = None
                    for msg in messages:
                        if msg.document and msg.document.file_name == 'user_db.json':
                            user_db_msg = msg
                            break
                    if user_db_msg:
                        file_info = bot.get_file(user_db_msg.document.file_id)
                        downloaded_file = bot.download_file(file_info.file_path)
                        file_path = os.path.join(data_manager.data_dir, 'user_db.json')
                        with open(file_path, 'wb') as f:
                            f.write(downloaded_file)
                        new_data = data_manager.load_from_file('user_db.json')
                        data_manager.user_db.clear()
                        data_manager.user_db.update(new_data)
                        data_manager.save_all_data()
                        bot.send_message(cid, f"✅ user_db.json restaurado!\n\n👥 {len(data_manager.user_db)} usuários carregados\n🔐 Licenças restauradas: {sum(1 for u in data_manager.user_db.values() if u.get('license_date'))}")
                    else:
                        bot.send_message(cid, "❌ user_db.json não encontrado no canal.")
                except Exception as e:
                    bot.send_message(cid, f"❌ Erro: {str(e)[:200]}")
        
        elif call.data == "manual_restaurar_afiliados":
            if cid == ADMIN_ID:
                bot.answer_callback_query(call.id, "Restaurando afiliados_db.json...")
                try:
                    messages = bot.get_chat_history(BACKUP_CHANNEL_ID, limit=100)
                    afiliados_msg = None
                    for msg in messages:
                        if msg.document and msg.document.file_name == 'afiliados_db.json':
                            afiliados_msg = msg
                            break
                    if afiliados_msg:
                        file_info = bot.get_file(afiliados_msg.document.file_id)
                        downloaded_file = bot.download_file(file_info.file_path)
                        file_path = os.path.join(data_manager.data_dir, 'afiliados_db.json')
                        with open(file_path, 'wb') as f:
                            f.write(downloaded_file)
                        new_data = data_manager.load_from_file('afiliados_db.json')
                        data_manager.afiliados_db.clear()
                        data_manager.afiliados_db.update(new_data)
                        data_manager.save_all_data()
                        bot.send_message(cid, f"✅ afiliados_db.json restaurado!\n\n🤝 {len(data_manager.afiliados_db)} afiliados carregados")
                    else:
                        bot.send_message(cid, "❌ afiliados_db.json não encontrado no canal.")
                except Exception as e:
                    bot.send_message(cid, f"❌ Erro: {str(e)[:200]}")
        
        elif call.data == "manual_verificar_status":
            if cid == ADMIN_ID:
                bot.answer_callback_query(call.id, "Verificando status...")
                status_msg = f"📊 STATUS DO SISTEMA\n\n👥 Usuários: {len(data_manager.user_db)}\n🎫 Cupons: {len(data_manager.cupons_db)}\n💰 Pagamentos: {len(data_manager.pagamentos_pendentes)}\n🎉 Promoções: {len(data_manager.promocoes_ativas)}\n🤝 Afiliados: {len(data_manager.afiliados_db)}\n🔐 Licenças ativas: {sum(1 for uid in data_manager.user_db if data_manager.is_license_valid(uid))}"
                bot.send_message(cid, status_msg)
        
        elif call.data == "manual_cancelar":
            if cid == ADMIN_ID:
                bot.answer_callback_query(call.id, "Cancelado")
                bot.edit_message_text("❌ Restauração manual cancelada.", cid, call.message.message_id)
    
    except Exception as e:
        log_terminal(f"Erro no callback: {e}")

# ==============================================================================
# 📢 INICIALIZAÇÃO DO BOT
# ==============================================================================
def limpar_pagamentos_expirados():
    try:
        removidos = 0
        agora = datetime.now()
        for payment_id in list(pagamentos_pendentes.keys()):
            pagamento = pagamentos_pendentes[payment_id]
            if agora > pagamento['data_expiracao'] and not pagamento.get('pago', False):
                del pagamentos_pendentes[payment_id]
                removidos += 1
        if removidos > 0:
            data_manager.save_all_data()
            data_manager.send_json_on_user_action("pagamentos_expirados_limpos", None)
            log_terminal(f"🧹 {removidos} pagamentos expirados removidos")
    except Exception as e:
        log_terminal(f"Erro ao limpar pagamentos expirados: {e}")

scheduler.add_job(limpar_pagamentos_expirados, 'interval', minutes=5)
recriar_agendamentos_promocoes()

# ⚡ OTIMIZAÇÃO: Pré-carregar username do bot
try:
    _bot_username_cache = bot.get_me().username
    log_terminal(f"⚡ Bot username pré-carregado: @{_bot_username_cache}")
except Exception:
    pass

print("=" * 60)
print("🤖 BOT VIVO, CLARO E TIM ENTERPRISE - ANTI-BAN ATIVO")
print("=" * 60)
print(f"🛡️ ANTI-BAN: {TEMPO_VIDEO_SEGUNDOS} segundos por vídeo (3 operadoras)")
print("")
print("⚡ OTIMIZAÇÕES ATIVAS:")
print("   ✅ Save em background (não bloqueia)")
print("   ✅ Cache de first_name (menu instantâneo)")
print("   ✅ Username pré-carregado no boot")
print("   ✅ atexit save ao encerrar")
print("")
print("✅ SISTEMA DE LICENÇAS CORRIGIDO!")
print("💾 Sistema de serialização/deserialização de datas funcionando")
print("🔐 Licenças serão salvas e restauradas corretamente")
print("")
print("📤 Sistema de backup/restauração completo:")
print("   - Comandos para enviar arquivos JSON manualmente")
print("   - Comandos para restaurar licenças de emergência")
print("   - Sistema automático de backup no canal")
print("")
print("🔓 SISTEMA DE DESBANIMENTO ATIVADO!")
print("   Comandos:")
print("   /desbanir - Para usuários desbanirem seus próprios números")
print("   /admin_desbanir NUMERO OPERADORA - Para admin desbanir qualquer número")
print("   /admin_reset_massivo - Reset em massa (apenas admin)")
print("   /ajuda_desbanir - Ajuda sobre o sistema de desbanimento")
print("")
print("💳 SISTEMA DE PAGAMENTO PIX REAL ATIVADO!")
print(f"💰 Valor da licença: R$ {VALOR_LICENCA:.2f} por {DIAS_LICENCA} dias")
print("")
print("🎉 SISTEMA DE PROMOÇÃO VIP ATIVADO!")
print(f"   Comando: /promo_vip (somente admin)")
print("")
print("🤝 SISTEMA DE AFILIADOS ATIVADO!")
print(f"   🎁 Bônus: +{DIAS_BONUS_AFILIADO} dias para quem divulga e quem entra pelo link")
print(f"   📊 Painel com estatísticas reais (cliques, registros, dias ganhos)")
print(f"   🔗 Botão AFILIADO no menu principal (verde)")
print("")
print("🔄 COMANDO /backup_completo ATIVADO!")
print("   📤 Admin envia arquivo JSON e restaura TUDO")
print("   💾 Usuários, licenças, afiliados, cupons, pagamentos, promoções")
print("")
print("🔄 SISTEMA DE REMOÇÃO DE CONTA ATUALIZADO!")
print("   ✅ Permite remover a última conta")
print("   ✅ Volta automaticamente à tela inicial de login")
print("")
print("📄 NOVO: BACKUP AUTOMÁTICO NO /start!")
print("   ✅ Todos os JSONs enviados ao canal a cada /start")
print("   ✅ backup_licencas.json com nomes corretos")
print("   ✅ licenca.pdf com relatório organizado")
if PDF_DISPONIVEL:
    print("   ✅ PDF (reportlab) ativo")
else:
    print("   ⚠️ PDF desativado - instale: pip install reportlab")
print("")
print("🕐 HORÁRIO BRASIL:")
tz_brasilia = pytz.timezone('America/Sao_Paulo')
hora_brasil = datetime.now(tz_brasilia).strftime("%H:%M:%S")
print(f"   📅 Horário atual: {hora_brasil}")
print("")
print("📱 SISTEMA DE COLETA COM ANTI-BAN:")
print(f"   🟣 Vivo: {PONTOS_POR_VIDEO_VIVO} pts/vídeo - {TEMPO_VIDEO_SEGUNDOS}s por vídeo")
print(f"   🔴 Claro: {PONTOS_POR_VIDEO_CLARO} pts/vídeo - {TEMPO_VIDEO_SEGUNDOS}s por vídeo")
print(f"   🔵 TIM: {PONTOS_POR_VIDEO_TIM} pts/vídeo - {TEMPO_VIDEO_SEGUNDOS}s por vídeo")
print("")
print("📊 ESTATÍSTICAS ATUAIS:")
print(f"   💾 Usuários carregados: {len(user_db)}")
print(f"   🎫 Cupons ativos: {len(cupons_db)}")
print(f"   💰 Pagamentos pendentes: {len(pagamentos_pendentes)}")
print(f"   🎉 Promoções ativas: {len(promocoes_ativas)}")
print(f"   🤝 Afiliados: {len(afiliados_db)}")
print(f"   🔐 Licenças ativas: {sum(1 for uid in user_db if data_manager.is_license_valid(uid))}")
print(f"   💰 Pontos totais coletados: {sum(user.get('pontos_coletados', 0) for user in user_db.values())}")
print("")
print("=" * 60)

log_terminal("🤖 BOT INICIADO COM SUCESSO!")
log_terminal(f"👑 ADMIN ID: {ADMIN_ID}")
log_terminal(f"🛡️ ANTI-BAN: {TEMPO_VIDEO_SEGUNDOS}s por vídeo")
log_terminal(f"📁 Dados carregados: {len(user_db)} usuários")
log_terminal(f"💰 Pagamentos pendentes: {len(pagamentos_pendentes)}")
log_terminal(f"🎫 Cupons ativos: {len(cupons_db)}")
log_terminal(f"🎉 Promoções ativas: {len(promocoes_ativas)}")
log_terminal(f"🤝 Afiliados: {len(afiliados_db)}")
log_terminal(f"💰 Pontos totais: {sum(user.get('pontos_coletados', 0) for user in user_db.values())}")
log_terminal("📍 Aguardando comandos...")

data_manager._save_now()

try:
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
except Exception as e:
    log_terminal(f"❌ Erro no polling: {e}")
    data_manager._save_now()
    data_manager.send_all_json_to_channel(force_send=True, reason="Reinicialização do bot")
    time.sleep(5)
    log_terminal("🔄 Reiniciando bot...")