# AZION IA — Atendimento profissional

Atendimento por texto com visual inspirado no WhatsApp, PHP + JSON, sem MySQL.

## Acesso por e-mail

O visitante primeiro escolhe SIM ou NÃO para indicar se já possui conta. O AZION envia um código de verificação por e-mail. Somente após a validação o atendimento é liberado.

SIM: informa e-mail e valida o código.
NÃO: informa nome, e-mail e telefone opcional, depois valida o código.

## Configuração

Edite config.php no servidor e informe a chave Gemini, a senha do administrador e a senha de app do Gmail do endereço inovatechinsights@gmail.com.

Não publique credenciais reais no GitHub.

## Arquivos

index.php = experiência do cliente e chat AZION IA.
admin.php = painel administrativo separado.
api.php = autenticação, verificação por e-mail, IA e administração.
data.json = dados em JSON.
config.php = configurações do servidor.

## Segurança

Código expira em 10 minutos, é armazenado com hash e possui limite de tentativas. O chat usa sessão autenticada e não aceita ID de conversa enviado livremente pelo cliente.

Requer PHP com cURL, sockets SSL e permissão de escrita no data.json.
