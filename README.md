# 📚 Clube do Livro 104 — Sistema de Acervo Digital

Sistema web para busca, listagem e futuramente upload de ebooks do **Clube do Livro 104**, grupo de leitores formado por colaboradores da Caixa Econômica Federal espalhados por todo o Brasil.

🌐 **Acesse em:** https://clubedolivro104.streamlit.app

---

## 🎯 O que é

O Clube do Livro 104 nasceu como um grupo no WhatsApp e cresceu para reunir leitores de toda a empresa. Este sistema centraliza o acervo digital do clube — hospedado no Google Drive — e oferece uma interface web amigável para que qualquer participante possa encontrar e baixar os ebooks disponíveis, sem precisar navegar manualmente pelas pastas do Drive.

---

## ✨ Funcionalidades

| Módulo | Status | Descrição |
|---|---|---|
| 🔐 Login por senha | ✅ Disponível | Acesso restrito aos membros do clube |
| 🏠 Página Inicial | ✅ Disponível | Boas-vindas e apresentação do clube |
| 🔍 Busca de Livros | ✅ Disponível | Busca por título com autocomplete e exibição de capa |
| 📋 Acervo Completo | ✅ Disponível | Listagem alfabética de todos os livros com download |
| 📤 Upload de Ebooks | 🔜 Em breve | Envio de novos livros direto para o Google Drive |

---

## 🗂️ Estrutura do Projeto

```
📁 Project_Clube_do_Livro_104/
│
├── app.py                  # Ponto de entrada — menu lateral, login, roteamento
├── drive_backend.py        # Módulo de integração com o Google Drive
│
├── pages/
│   ├── home.py             # Página inicial com mensagem de boas-vindas
│   ├── busca.py            # Página de busca por título com autocomplete
│   ├── acervo.py           # Página de acervo completo em ordem alfabética
│   └── upload.py           # Página de upload (coming soon)
│
├── credentials.json        # Credenciais OAuth2 do Google Cloud (NÃO versionar)
├── token.json              # Token de sessão gerado automaticamente (NÃO versionar)
├── requirements.txt        # Dependências Python do projeto
├── limpa.sh                # Script para recriar o ambiente virtual do zero
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Este arquivo
```

> ⚠️ `credentials.json` e `token.json` estão no `.gitignore` e **nunca devem ser versionados**.

---

## 🔧 Pré-requisitos

- Python 3.11 ou superior
- Conta Google com acesso à pasta compartilhada do acervo
- Projeto configurado no [Google Cloud Console](https://console.cloud.google.com)

---

## ⚙️ Configuração do Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Projeto: **busca-clube-do-livro**
3. Ative a **Google Drive API**
4. Crie um **ID do cliente OAuth 2.0** do tipo **Aplicativo da Web**
5. Adicione o URI de redirecionamento: `https://clubedolivro104.streamlit.app/oauth2callback`
6. Baixe o `credentials.json` e coloque na raiz do projeto
7. Adicione seu e-mail como usuário de teste na Tela de Consentimento OAuth

---

## 🚀 Instalação e Execução Local

```bash
# Entre na pasta do projeto
cd /Users/diogodcg/Documents/VSCode_Praticas/Project_Clube_do_Livro_104

# Crie o ambiente virtual
python3 -m venv env

# Ative o ambiente
source env/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Rode o app
streamlit run app.py
```

### Se o ambiente travar ou corromper

```bash
./limpa.sh
```

---

## 📦 Dependências

```
streamlit>=1.35.0
google-api-python-client>=2.120.0
google-auth-httplib2>=0.2.0
google-auth-oauthlib>=1.2.0
requests>=2.31.0
```

---

## 🔐 Secrets do Streamlit Cloud

O arquivo `.streamlit/secrets.toml` (local) ou os Secrets do Streamlit Cloud devem conter:

```toml
[acesso]
senha = "suasenhaaqui"

[google]
credentials = """{ conteúdo do credentials.json }"""
token = """{ conteúdo do token.json }"""
```

> ⚠️ O `token.json` tem prazo de validade. Quando expirar, gere um novo localmente e atualize nos Secrets do Streamlit Cloud.

---

## 🗄️ Como funciona o acervo

Pasta compartilhada no Google Drive:
```
https://drive.google.com/drive/folders/1-dPWk5NKI_3BsECgS-7gSTQICHIzjvRf
```

Formatos suportados: `.pdf`, `.epub`, `.mobi`, `.azw`, `.azw3`, `.djvu`, `.fb2`, `.txt`, `.zip`

### Cache e performance

- Acervo carregado **uma única vez por sessão** via `st.session_state`
- Busca e listagem feitas **100% em memória**, zero requisições ao Drive durante uso
- Capas buscadas na **Open Library** e cacheadas por sessão

---

## 🎨 Design

- Paleta **azul marinho** (`#0d2d5e`) e **laranja** (`#f47c20`)
- Fontes: **Lora** (títulos) + **Inter** (interface)
- Layout responsivo — sidebar fecha automaticamente ao navegar no celular
- Rodapé fixo: *Desenvolvido por Diogo Campos Gomes*

---

## 📝 Histórico de Versões

| Versão | O que foi feito |
|---|---|
| v0.1 | Script CLI (`busca_livros.py`) com busca por terminal |
| v0.2 | Refatoração em módulos (`drive_backend.py` + `app.py`) |
| v0.3 | Frontend Streamlit com busca, capa e botões de download |
| v0.4 | Autocomplete em tempo real, cache em `session_state` |
| v0.5 | Design responsivo, paleta azul/laranja |
| v0.6 | Multipage com menu lateral, home, acervo e upload coming soon |
| v0.7 | GitHub, `.gitignore`, README completo |
| v0.8 | Deploy em produção no Streamlit Cloud |
| v0.9 | Login por senha para membros do clube |
| v1.0 | Sidebar fecha automaticamente no celular |

---

## 👤 Autor

**Diogo Campos Gomes**
Profissional de negócios e agilidade | Mentor de transição de carreira
Brasília, DF — Brasil
[github.com/diogodcg](https://github.com/diogodcg)

---

*Feito com ☕ e muito amor pelos livros — Clube do Livro 104*