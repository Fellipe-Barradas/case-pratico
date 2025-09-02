# OptiMail

OptiMail é uma solução web para gerenciamento e classificação inteligente de e-mails. Permite analisar o conteúdo de e-mails (texto ou arquivos PDF/TXT), categorizá-los, visualizar, filtrar, paginar e deletar registros.

## Funcionalidades
- Envio de e-mails para análise (texto ou arquivo PDF/TXT)
- Classificação automática do tipo de e-mail
- Listagem de e-mails enviados
- Filtro por tipo de e-mail
- Paginação e seleção do tamanho da página
- Exclusão de e-mails
- Carrossel tutorial para novos usuários

## Tecnologias
- Backend: FastAPI, SQLModel, PyPDF2
- Frontend: HTML, TailwindCSS, JavaScript

## Como rodar o projeto

### Backend
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie o backend:
   ```bash
   python main.py
   ```
   O backend estará disponível em `http://localhost:8000`.

### Frontend
Abra o arquivo `frontend/index.html` em seu navegador.

## Endpoints principais
- `POST /analisar-email`: Analisa o conteúdo do e-mail (texto ou arquivo PDF/TXT)
- `GET /obter-emails`: Lista e-mails enviados, suporta paginação e filtro
- `GET /tipos-email`: Lista os tipos de e-mail disponíveis
- `DELETE /delete-email`: Deleta um e-mail pelo id

## Requisitos
- Python 3.11+
- Navegador moderno

## Observações
- Para análise de PDF, é necessário o pacote `PyPDF2`.
- O frontend consome os endpoints do backend via fetch.
- O carrossel tutorial aparece ao entrar no site e pode ser navegado ou fechado.

## Licença
MIT
