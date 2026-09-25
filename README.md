# JADIEL IMG

Plataforma de armazenamento e gerenciamento de imagens.

## Arquivos principais

- `index.html`: experiência pública e área do usuário.
- `gestor.html`: painel administrativo.
- `api/`: backend a ser conectado.
- `database/schema.sql`: modelo de dados.

## Importante sobre segurança

GitHub Pages é hospedagem estática. Ele não executa PHP/Node no servidor e não deve ser usado como armazenamento privado de imagens ou como banco de dados.

O frontend foi preparado para consumir uma API externa. Configure:

`localStorage.setItem('JADIEL_IMG_API','https://SEU-BACKEND.example')`

e, para o gestor:

`localStorage.setItem('JADIEL_IMG_ADMIN_API','https://SEU-BACKEND.example')`

Em produção, use HTTPS, autenticação no servidor, hash de senha, autorização por usuário, proteção CSRF quando aplicável, rate limiting, validação MIME/tamanho e armazenamento privado de objetos.

O modo sem API existente é apenas uma demonstração local no navegador e **não representa armazenamento seguro em produção**.