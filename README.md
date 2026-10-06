# Agente de Atendimento IA — InfinityFree

Site de atendimento por texto, visual inspirado no WhatsApp, PHP + JSON e sem MySQL.

## Configuração
1. Envie o conteúdo do repositório para o htdocs da InfinityFree.
2. Edite config.php.
3. Substitua COLE_SUA_CHAVE_GEMINI_AQUI pela sua chave Gemini.
4. Acesse /admin.php.
5. Login inicial: admin
6. Senha inicial: Admin@12345
7. Cadastre os sistemas, procedimentos e respostas na Base de conhecimento.

## Arquivos principais
- index.php — atendimento do cliente
- admin.php — painel administrativo
- api.php — cadastro, chat, IA e administração
- data.json — clientes, conversas e conhecimento
- config.php — configuração da API

## Segurança
Troque a senha inicial antes de publicar. Não coloque senhas, tokens ou códigos de segurança dos clientes na base de conhecimento. Use HTTPS e revise a política de privacidade/LGPD antes de produção.

Requer PHP com cURL e permissão de escrita no data.json.