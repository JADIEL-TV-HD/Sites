# JADIEL IMG

Site de armazenamento e organização de imagens com interface premium, mobile-first e persistência local.

## Estrutura

- `index.html` — landing page + cadastro/login + área completa do usuário.
- `gestor.html` — painel visual de administração.
- Não utiliza MySQL, PostgreSQL ou qualquer banco SQL.
- Não depende de backend para o modo local.

## Armazenamento local

Os dados do modo local ficam no navegador usando `localStorage`.

As imagens são convertidas para Data URL e armazenadas junto dos dados locais. Isso permite testar o sistema diretamente em hospedagem estática.

### Recursos

- Cadastro e login local
- Galeria
- Upload múltiplo
- Arrastar e soltar
- Pesquisa
- Favoritos
- Álbuns
- Lixeira
- Perfil
- Dashboard
- Painel Gestor
- Limite local de armazenamento
- Interface responsiva
- Animações e microinterações
- Sem MySQL

## Observação

O armazenamento no navegador é específico do dispositivo/navegador e não é um armazenamento em nuvem. Limpar os dados do site ou trocar de navegador pode remover os dados locais. Para sincronização entre dispositivos seria necessário um serviço de armazenamento externo.

## Identidade visual

JADIEL IMG usa uma linguagem visual premium: fundo escuro, verde neon controlado, glassmorphism, iluminação ambiente, tipografia forte, cartões, microinterações e layout adaptativo para celular e desktop.
