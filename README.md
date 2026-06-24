# 📚 Clube do Livro 104 — Sistema de Acervo Digital

Sistema web para busca, listagem e futuramente upload de ebooks do **Clube do Livro 104**, grupo de leitores formado por colaboradores da Caixa Econômica Federal espalhados por todo o Brasil.

---

## 🎯 O que é

O Clube do Livro 104 nasceu como um grupo no WhatsApp e cresceu para reunir leitores de toda a empresa. Este sistema centraliza o acervo digital do clube — hospedado no Google Drive — e oferece uma interface web amigável para que qualquer participante possa encontrar e baixar os ebooks disponíveis, sem precisar navegar manualmente pelas pastas do Drive.

---

## ✨ Funcionalidades

| Módulo | Status | Descrição |
|---|---|---|
| 🏠 Página Inicial | ✅ Disponível | Boas-vindas e apresentação do clube |
| 🔍 Busca de Livros | ✅ Disponível | Busca por título com autocomplete e exibição de capa |
| 📋 Acervo Completo | ✅ Disponível | Listagem alfabética de todos os livros com download |
| 📤 Upload de Ebooks | 🔜 Em breve | Envio de novos livros direto para o Google Drive |

---

## 🗂️ Estrutura do Projeto

```
📁 Project_Clube_do_Livro_104/
│
├── app.py                  # Ponto de entrada — inicializa o Streamlit e o menu
├── drive_backend.py        # Módulo de integração com o Google Drive
│
├── pages/
│   ├── home.py             # Página inicial com mensagem de boas-vindas
│   ├── busca.py            # Página de busca por título
│   ├── acervo.py           # Página de acervo completo (relatório)
│   └── upload.py           # Página de upload (coming soon)
│
├── credentials.json        # Credenciais OAuth2 do Google Cloud (NÃO versionar)
├── token.json              # Token de sessão gerado automaticamente (NÃO versionar)
├── requirements.txt        # Dependências Python do projeto
├── limpa.sh                # Script para recriar o ambiente virtual do zero
└── README.md               # Este arquivo
```

---

## 🔧 Pré-requisitos

- Python 3.11 ou superior (recomendado)
- Conta Google com acesso à pasta compartilhada do acervo
- Projeto configurado no [Google Cloud Console](https://console.cloud.google.com)

---

## ⚙️ Configuração do Google Cloud

1. Acesse o [Google Cloud Console](https://console.cloud.google.com)
2. Crie ou selecione o projeto **busca-clube-do-livro**
3. Ative a **Google Drive API**
4. Em **APIs e Serviços → Credenciais**, crie um **ID do cliente OAuth 2.0**
   - Tipo: **Aplicativo de Computador** (para uso local)
   - Tipo: **Aplicativo da Web** (para deploy em servidor)
5. Baixe o arquivo `credentials.json` e coloque na raiz do projeto
6. Em **Tela de Consentimento OAuth**, adicione seu e-mail como usuário de teste

> ⚠️ **Nunca suba o `credentials.json` ou `token.json` para repositórios públicos.**

---

## 🚀 Instalação e Execução

### Primeira vez

```bash
# Clone ou copie os arquivos para a pasta do projeto
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

### Nas próximas vezes

```bash
source /Users/diogodcg/Documents/VSCode_Praticas/Project_Clube_do_Livro_104/env/bin/activate
streamlit run app.py
```

### Se o ambiente travar ou corromper

```bash
# Use o script de limpeza incluído no projeto
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

## 🗄️ Como funciona o acervo

O acervo é uma **pasta compartilhada no Google Drive**:
```
https://drive.google.com/drive/folders/1-dPWk5NKI_3BsECgS-7gSTQICHIzjvRf
```

O sistema navega recursivamente por todas as subpastas e lista arquivos nos seguintes formatos:

| Formato | Extensão |
|---|---|
| PDF | `.pdf` |
| EPUB | `.epub` |
| MOBI | `.mobi` |
| AZW / AZW3 | `.azw`, `.azw3` |
| DjVu | `.djvu` |
| FictionBook | `.fb2` |
| Texto | `.txt` |
| Compactado | `.zip` |

### Cache e performance

- O acervo é carregado **uma única vez por sessão** e armazenado em memória (`st.session_state`)
- A busca e a listagem são feitas **100% localmente**, sem novas requisições ao Drive
- As capas dos livros são buscadas na **Open Library** (base pública e gratuita) e também cacheadas por sessão

---

## 🔍 Módulo de Busca

- Filtragem em tempo real por qualquer parte do título
- Exibição de capa do livro (quando disponível na Open Library ou nos metadados do Drive)
- Informações extraídas automaticamente do nome do arquivo: título, autor, edição e ano
- Botões de **Download direto** e **Visualizar no navegador**

---

## 📋 Módulo de Acervo Completo

- Listagem de todos os livros em ordem alfabética
- Colunas: Título | Autor | Formato | Download | Visualizar
- Atualizado automaticamente conforme o Google Drive

---

## 📤 Módulo de Upload *(Em breve)*

Permitirá que qualquer participante envie ebooks diretamente para o Google Drive, sem precisar acessar a pasta manualmente. Formatos aceitos serão os mesmos já suportados pelo acervo.

> Requer ajuste de permissões de escrita no Google Cloud para o fluxo OAuth dos usuários.

---

## 🌐 Deploy (Futuro)

O sistema foi desenvolvido para rodar localmente, mas está preparado para ser publicado no **Streamlit Community Cloud**:

1. Subir o projeto para um repositório GitHub (sem `credentials.json` e `token.json`)
2. Configurar as credenciais nos **Secrets** do Streamlit Cloud
3. Trocar o fluxo OAuth de `run_local_server` para fluxo web
4. Cada usuário autenticaria com sua própria conta Google

---

## 👤 Autor

**Diogo Campos Gomes**
Profissional de negócios e agilidade | Mentor de transição de carreira
Brasília, DF — Brasil

---

## 📝 Histórico de Versões

| Versão | O que foi feito |
|---|---|
| v0.1 | Script CLI (`busca_livros.py`) com busca por terminal |
| v0.2 | Refatoração em módulos (`drive_backend.py` + `app.py`) |
| v0.3 | Frontend Streamlit com busca, capa e botões de download |
| v0.4 | Autocomplete em tempo real, cache em session_state |
| v0.5 | Design responsivo, paleta âmbar/escuro, botão de busca |
| v0.6 | Multipage com menu lateral, home, acervo e upload coming soon |

---

*Feito com ☕ e muito amor pelos livros — Clube do Livro 104*