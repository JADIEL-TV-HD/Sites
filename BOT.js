// BOT.js — conversão segura do bot Python
// Requisitos: Node.js 18+, npm i node-telegram-bot-api dotenv qrcode
// Configure BOT_TOKEN e ADMIN_ID no ambiente. Nunca coloque tokens no código.

require('dotenv').config();
const TelegramBot = require('node-telegram-bot-api');
const QRCode = require('qrcode');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const TOKEN = process.env.BOT_TOKEN;
const ADMIN_ID = String(process.env.ADMIN_ID || '');
const MP_ACCESS_TOKEN = process.env.MP_ACCESS_TOKEN || '';
const LICENSE_PRICE = Number(process.env.LICENSE_PRICE || 25);
const LICENSE_DAYS = Number(process.env.LICENSE_DAYS || 30);
const DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
const DB_FILE = path.join(DATA_DIR, 'database.json');

if (!TOKEN) throw new Error('Defina BOT_TOKEN nas variáveis de ambiente.');
if (!ADMIN_ID) throw new Error('Defina ADMIN_ID nas variáveis de ambiente.');

fs.mkdirSync(DATA_DIR, { recursive: true });
const bot = new TelegramBot(TOKEN, { polling: true });
const now = () => Date.now();
const isAdmin = id => String(id) === ADMIN_ID;
const makeCode = (size = 8) => crypto.randomBytes(size).toString('hex').slice(0, size).toUpperCase();
const dateBR = value => value ? new Date(value).toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' }) : 'Nunca';

function loadDB() {
  try {
    const parsed = JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
    return {
      users: parsed.users || {}, coupons: parsed.coupons || {},
      affiliates: parsed.affiliates || {}, payments: parsed.payments || {}
    };
  } catch {
    return { users: {}, coupons: {}, affiliates: {}, payments: {} };
  }
}
const db = loadDB();
let saveTimer;
function saveDB() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    const temp = DB_FILE + '.tmp';
    fs.writeFileSync(temp, JSON.stringify(db, null, 2));
    fs.renameSync(temp, DB_FILE);
  }, 250);
}
function getUser(msg) {
  const id = String(msg.from.id);
  if (!db.users[id]) {
    db.users[id] = {
      id, first_name: msg.from.first_name || 'Usuário',
      username: msg.from.username || null, created_at: now(),
      license_until: 0, accounts: [], coupons_used: [], points: 0
    };
  } else {
    db.users[id].first_name = msg.from.first_name || db.users[id].first_name;
    db.users[id].username = msg.from.username || db.users[id].username;
  }
  saveDB();
  return db.users[id];
}
function licenseValid(user) {
  return Number(user.license_until || 0) > now();
}
function addLicense(user, days = LICENSE_DAYS) {
  const base = Math.max(now(), Number(user.license_until || 0));
  user.license_until = base + days * 86400000;
  saveDB();
}
function mainKeyboard() {
  return {
    inline_keyboard: [
      [{ text: '🔐 Minha licença', callback_data: 'license' }, { text: '💳 Comprar licença', callback_data: 'buy' }],
      [{ text: '🤝 Afiliado', callback_data: 'affiliate' }, { text: '🎟️ Resgatar cupom', callback_data: 'coupon_help' }],
      [{ text: '📋 Minhas contas', callback_data: 'accounts' }, { text: '❓ Ajuda', callback_data: 'help' }]
    ]
  };
}
async function safeSend(chatId, text, options = {}) {
  try { return await bot.sendMessage(chatId, text, options); }
  catch (err) { console.error('Falha ao enviar mensagem:', err.message); }
}
async function createPix(chatId, user) {
  if (!MP_ACCESS_TOKEN) {
    return safeSend(chatId, '⚠️ Pagamento automático não configurado. Fale com o suporte para pagamento manual.');
  }
  const body = {
    transaction_amount: LICENSE_PRICE,
    description: `Licença do bot por ${LICENSE_DAYS} dias`,
    payment_method_id: 'pix',
    payer: { email: `telegram${user.id}@example.com`, first_name: user.first_name || 'Cliente' },
    external_reference: String(user.id)
  };
  try {
    const response = await fetch('https://api.mercadopago.com/v1/payments', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${MP_ACCESS_TOKEN}`,
        'Content-Type': 'application/json',
        'X-Idempotency-Key': crypto.randomUUID()
      },
      body: JSON.stringify(body)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Mercado Pago recusou a solicitação');
    db.payments[String(data.id)] = { id: String(data.id), user_id: user.id, status: data.status, created_at: now() };
    saveDB();
    const pix = data.point_of_interaction?.transaction_data;
    if (!pix?.qr_code) return safeSend(chatId, 'Pagamento criado, mas o QR Code não foi retornado. Contate o suporte.');
    const qr = await QRCode.toBuffer(pix.qr_code, { type: 'png', width: 480, margin: 2 });
    await bot.sendPhoto(chatId, qr, { caption: `💳 PIX de R$ ${LICENSE_PRICE.toFixed(2)}\n\nApós pagar, use /verificar_pagamento ${data.id}` });
    await safeSend(chatId, '📋 PIX copia e cola:\n' + pix.qr_code);
  } catch (err) {
    console.error('Erro Mercado Pago:', err.message);
    safeSend(chatId, '❌ Não foi possível gerar o PIX agora. Tente novamente mais tarde.');
  }
}
async function checkPayment(chatId, paymentId, requesterId) {
  if (!MP_ACCESS_TOKEN) return safeSend(chatId, 'Pagamento automático não configurado.');
  const payment = db.payments[String(paymentId)];
  if (!payment || String(payment.user_id) !== String(requesterId)) return safeSend(chatId, 'Pagamento não encontrado para sua conta.');
  try {
    const response = await fetch(`https://api.mercadopago.com/v1/payments/${encodeURIComponent(paymentId)}`, {
      headers: { Authorization: `Bearer ${MP_ACCESS_TOKEN}` }
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Erro ao consultar pagamento');
    if (data.status === 'approved' && !payment.applied) {
      const user = db.users[String(requesterId)];
      addLicense(user);
      payment.applied = true;
      payment.status = 'approved';
      saveDB();
      return safeSend(chatId, `✅ Pagamento aprovado! Sua licença foi ativada até ${dateBR(user.license_until)}.`);
    }
    payment.status = data.status;
    saveDB();
    return safeSend(chatId, `ℹ️ Status do pagamento: ${data.status || 'desconhecido'}.`);
  } catch (err) {
    console.error('Consulta de pagamento:', err.message);
    return safeSend(chatId, '❌ Não consegui consultar esse pagamento. Tente novamente.');
  }
}
function affiliateLink(userId) {
  const username = process.env.BOT_USERNAME;
  if (!username) return 'Configure BOT_USERNAME para gerar links de convite.';
  const code = `ref_${userId}`;
  db.affiliates[code] ||= { owner_id: String(userId), clicks: 0, referred: [] };
  saveDB();
  return `https://t.me/${username}?start=${code}`;
}
function redeemCoupon(user, code) {
  code = String(code || '').trim().toUpperCase();
  const coupon = db.coupons[code];
  if (!coupon || coupon.expires_at && coupon.expires_at < now()) return '❌ Cupom inválido ou expirado.';
  if (user.coupons_used.includes(code)) return '⚠️ Você já utilizou esse cupom.';
  if (coupon.limit && coupon.used >= coupon.limit) return '❌ Esse cupom atingiu o limite de usos.';
  user.coupons_used.push(code);
  coupon.used = (coupon.used || 0) + 1;
  if (coupon.days) addLicense(user, coupon.days);
  saveDB();
  return `✅ Cupom aplicado! Benefício: ${coupon.days || 0} dia(s) de licença.`;
}

bot.onText(/^\/start(?:\s+(\S+))?/, async (msg, match) => {
  const user = getUser(msg);
  const ref = match?.[1];
  if (ref && ref.startsWith('ref_')) {
    const owner = ref.slice(4);
    const affiliate = db.affiliates[ref];
    if (affiliate && owner !== user.id && !affiliate.referred.includes(user.id)) {
      affiliate.referred.push(user.id);
      affiliate.clicks++;
      addLicense(db.users[owner] ||= { id: owner, first_name: 'Afiliado', coupons_used: [], accounts: [], license_until: 0 }, 3);
      addLicense(user, 3);
      saveDB();
      safeSend(owner, '🎉 Um novo usuário entrou pelo seu link. Bônus de 3 dias aplicado!');
    }
  }
  const status = licenseValid(user) ? `Ativa até: ${dateBR(user.license_until)}` : 'Sem licença ativa.';
  safeSend(msg.chat.id, `👋 Olá, ${user.first_name}!\n\n🤖 BOT — painel principal\n🔐 Licença: ${status}\n\nEscolha uma opção:`, { reply_markup: mainKeyboard() });
});
bot.onText(/^\/(menu|ajuda)(?:\s|$)/, msg => {
  getUser(msg);
  safeSend(msg.chat.id, '📌 Menu principal:', { reply_markup: mainKeyboard() });
});
bot.onText(/^\/minhascontas$/, msg => {
  const user = getUser(msg);
  safeSend(msg.chat.id, `📋 Contas cadastradas: ${(user.accounts || []).length}\nO gerenciamento de contas de operadoras não está habilitado nesta versão.`);
});
bot.onText(/^\/cupom(?:\s+(.+))?$/, (msg, match) => {
  const user = getUser(msg);
  if (!match?.[1]) return safeSend(msg.chat.id, 'Use: /cupom CODIGO');
  safeSend(msg.chat.id, redeemCoupon(user, match[1]));
});
bot.onText(/^\/comprar$/, msg => createPix(msg.chat.id, getUser(msg)));
bot.onText(/^\/verificar_pagamento\s+(\d+)$/, (msg, match) => checkPayment(msg.chat.id, match[1], msg.from.id));

bot.onText(/^\/estatisticas$/, msg => {
  if (!isAdmin(msg.from.id)) return;
  const users = Object.values(db.users);
  safeSend(msg.chat.id, `📊 PAINEL ADMIN\nUsuários: ${users.length}\nLicenças ativas: ${users.filter(licenseValid).length}\nCupons: ${Object.keys(db.coupons).length}\nPagamentos: ${Object.keys(db.payments).length}`);
});
bot.onText(/^\/gerar_cupom(?:\s+(\d+))?(?:\s+(\d+))?$/, (msg, match) => {
  if (!isAdmin(msg.from.id)) return;
  const days = Math.max(0, Number(match?.[1] || 3));
  const limit = Math.max(1, Number(match?.[2] || 1));
  const code = makeCode(8);
  db.coupons[code] = { days, limit, used: 0, created_at: now() };
  saveDB();
  safeSend(msg.chat.id, `🎟️ Cupom criado: ${code}\nDias: ${days}\nUsos máximos: ${limit}`);
});
bot.onText(/^\/confirmar_pagamento\s+(\d+)\s+(\d+)$/, (msg, match) => {
  if (!isAdmin(msg.from.id)) return;
  const [, userId, daysRaw] = match;
  const user = db.users[userId];
  if (!user) return safeSend(msg.chat.id, 'Usuário não encontrado.');
  addLicense(user, Math.max(1, Number(daysRaw)));
  safeSend(msg.chat.id, '✅ Licença confirmada manualmente.');
  safeSend(userId, `✅ Sua licença foi ativada por ${daysRaw} dia(s).`);
});
bot.onText(/^\/aviso\s+([\s\S]+)/, async (msg, match) => {
  if (!isAdmin(msg.from.id)) return;
  const ids = Object.keys(db.users);
  let sent = 0;
  for (const id of ids) {
    try { await bot.sendMessage(id, match[1]); sent++; } catch {}
  }
  safeSend(msg.chat.id, `📢 Aviso enviado para ${sent} usuário(s).`);
});
bot.onText(/^\/backup$/, msg => {
  if (!isAdmin(msg.from.id)) return;
  bot.sendDocument(msg.chat.id, Buffer.from(JSON.stringify(db, null, 2)), {}, { filename: 'backup-bot.json', contentType: 'application/json' });
});
bot.onText(/^\/ajuda_admin$/, msg => {
  if (!isAdmin(msg.from.id)) return;
  safeSend(msg.chat.id, [
    '🛠️ ADMIN',
    '/estatisticas — resumo do sistema',
    '/gerar_cupom [dias] [limite] — cria cupom',
    '/confirmar_pagamento ID_USUARIO DIAS — ativa licença',
    '/aviso TEXTO — envia comunicado',
    '/backup — exporta o banco JSON'
  ].join('\n'));
});

bot.on('callback_query', async query => {
  const chatId = query.message.chat.id;
  const user = getUser({ from: query.from, chat: query.message.chat });
  try {
    switch (query.data) {
      case 'license':
        await safeSend(chatId, licenseValid(user) ? `🔐 Licença ativa até ${dateBR(user.license_until)}.` : '🔒 Você não possui licença ativa.');
        break;
      case 'buy':
        await createPix(chatId, user);
        break;
      case 'affiliate':
        await safeSend(chatId, '🤝 Seu link de afiliado:\n' + affiliateLink(user.id));
        break;
      case 'coupon_help':
        await safeSend(chatId, '🎟️ Para resgatar, envie /cupom CODIGO');
        break;
      case 'accounts':
        await safeSend(chatId, `📋 Você possui ${(user.accounts || []).length} conta(s) cadastrada(s).\nO acesso às APIs de operadoras foi removido desta versão.`);
        break;
      case 'help':
        await safeSend(chatId, 'Use /start para abrir o painel, /comprar para gerar PIX e /cupom CODIGO para resgatar um cupom.');
        break;
    }
  } finally {
    bot.answerCallbackQuery(query.id).catch(() => {});
  }
});

bot.on('polling_error', err => console.error('Telegram polling:', err.message));
process.on('SIGINT', () => { saveDB(); bot.stopPolling(); process.exit(0); });
process.on('SIGTERM', () => { saveDB(); bot.stopPolling(); process.exit(0); });

console.log('🤖 BOT.js iniciado. Banco local:', DB_FILE);
