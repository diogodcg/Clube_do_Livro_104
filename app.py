"""
app.py — Clube do Livro 104
Ponto de entrada do sistema. Inicializa o Streamlit e carrega o acervo.
Execute com: streamlit run app.py
"""

import streamlit as st
from drive_backend import autenticar, listar_arquivos, extrair_metadados

# ── configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clube do Livro 104",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── estilos globais ───────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=Inter:wght@400;500;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ── sidebar ── */
  [data-testid="stSidebar"] {
    background-color: #0d2d5e !important;
  }
  [data-testid="stSidebar"] * {
    color: #e8f0fe !important;
  }
  [data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem !important;
    padding: 0.4rem 0 !important;
    cursor: pointer !important;
  }
  [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 0.5rem !important;
  }
  [data-testid="stSidebar"] hr {
    border-color: #1a4a8a !important;
  }

  /* ── fundo geral ── */
  .stApp { background-color: #f5f7fa; }
  .block-container {
    padding-top: 1.5rem !important;
    max-width: 820px !important;
  }

  /* ── tipografia ── */
  h1, h2, h3 {
    font-family: 'Lora', serif !important;
    color: #0d2d5e !important;
  }

  /* ── botões de link ── */
  .stLinkButton a {
    background: #0d2d5e !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 7px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: background 0.2s !important;
  }
  .stLinkButton a:hover {
    background: #f47c20 !important;
  }

  /* ── botões normais ── */
  .stButton > button {
    background: #0d2d5e !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 500 !important;
    transition: background 0.2s !important;
  }
  .stButton > button:hover {
    background: #f47c20 !important;
    color: #ffffff !important;
  }

  /* ── inputs ── */
  .stTextInput > div > div > input {
    font-family: 'Lora', serif !important;
    font-size: 1rem !important;
    border: 1.5px solid #cdd8f0 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    color: #0d2d5e !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #f47c20 !important;
    box-shadow: 0 0 0 2px rgba(244,124,32,0.15) !important;
  }

  /* ── selectbox ── */
  div[data-baseweb="select"] > div {
    border: 1.5px solid #cdd8f0 !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    color: #0d2d5e !important;
  }

  /* ── cards ── */
  .book-card {
    background: #ffffff;
    border: 1px solid #dce6f7;
    border-left: 4px solid #f47c20;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    transition: box-shadow 0.2s;
  }
  .book-card:hover {
    box-shadow: 0 2px 12px rgba(13,45,94,0.10);
  }
  .book-title {
    font-family: 'Lora', serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #0d2d5e;
    margin-bottom: 0.25rem;
  }
  .book-meta {
    font-size: 0.8rem;
    color: #5a7ab0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: center;
  }
  .badge {
    display: inline-block;
    background: #e8f0fe;
    color: #0d2d5e;
    border-radius: 4px;
    padding: 1px 7px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.04em;
  }
  .badge-orange {
    background: #fff0e6;
    color: #f47c20;
  }

  /* ── empty state ── */
  .empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #8aa3cc;
  }
  .empty-state .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
  .empty-state p { font-size: 0.9rem; margin: 0; color: #8aa3cc; }

  /* ── placeholder de capa ── */
  .cover-placeholder {
    width: 90px; height: 128px;
    background: #e8f0fe;
    border: 1px solid #cdd8f0;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
  }

  /* ── responsivo ── */
  @media (max-width: 640px) {
    .block-container { padding: 1rem 0.5rem !important; }
    .book-card { padding: 0.75rem; }
    .cover-placeholder { width: 65px; height: 92px; font-size: 1.5rem; }
  }

  /* ── esconde elementos padrão ── */
  #MainMenu, footer { visibility: hidden; }

  /* ── esconde menu de páginas nativo do Streamlit ── */
  [data-testid="stSidebarNav"] { display: none !important; }

  /* ── rodapé customizado ── */
  .cl-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #0d2d5e;
    color: #a0bce8;
    text-align: center;
    font-size: 0.72rem;
    padding: 0.5rem 1rem;
    letter-spacing: 0.03em;
    z-index: 999;
  }
</style>
""", unsafe_allow_html=True)

# ── autenticação por senha ───────────────────────────────────────────────────
def tela_login():
    st.markdown("""
    <div style='
      max-width: 380px;
      margin: 5rem auto 0;
      background: #ffffff;
      border: 1px solid #dce6f7;
      border-top: 4px solid #f47c20;
      border-radius: 12px;
      padding: 2.5rem 2rem;
      text-align: center;
    '>
      <div style='font-size:2.5rem; margin-bottom:0.75rem'>📚</div>
      <div style='font-family:Lora,serif; font-size:1.3rem; font-weight:600;
                  color:#0d2d5e; margin-bottom:0.25rem'>Clube do Livro 104</div>
      <div style='font-size:0.82rem; color:#8aa3cc; margin-bottom:1.5rem'>
        Acesso restrito aos membros do clube
      </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        senha = st.text_input("Senha", type="password", placeholder="Digite a senha do clube",
                               label_visibility="collapsed")
        entrar = st.button("Entrar", use_container_width=True)

        if entrar or senha:
            senha_correta = st.secrets.get("acesso", {}).get("senha", "")
            if senha == senha_correta:
                st.session_state.autenticado = True
                st.rerun()
            elif senha:
                st.error("Senha incorreta. Tente novamente.")

    st.stop()

if not st.session_state.get("autenticado", False):
    tela_login()

# ── carrega acervo uma vez na sessão ─────────────────────────────────────────
if "acervo" not in st.session_state:
    with st.spinner("Conectando ao Google Drive e carregando acervo…"):
        try:
            service = autenticar()
            arquivos = listar_arquivos(service)
            st.session_state.acervo = [extrair_metadados(a) for a in arquivos]
        except Exception as e:
            st.error(f"Erro ao conectar ao Google Drive: {e}")
            st.stop()

# ── menu lateral ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem'>
      <span style='font-size:2.5rem'>📚</span>
      <div style='font-family:Lora,serif; font-size:1.1rem; font-weight:600;
                  color:#ffffff; margin-top:0.3rem; line-height:1.3'>
        Clube do Livro 104
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)

    pagina = st.radio(
        "Navegação",
        options=["🏠  Início", "🔍  Busca de Livro", "📋  Acervo Completo", "📤  Upload de Ebooks"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='margin:0.75rem 0'>", unsafe_allow_html=True)
    total = len(st.session_state.get("acervo", []))
    st.markdown(
        f"<div style='font-size:0.75rem; color:#a0bce8; text-align:center'>"
        f"📖 {total} livros no acervo</div>",
        unsafe_allow_html=True,
    )

# ── roteamento de páginas ─────────────────────────────────────────────────────
if "Início" in pagina:
    from pages.home import render
    render()
elif "Busca" in pagina:
    from pages.busca import render
    render()
elif "Acervo" in pagina:
    from pages.acervo import render
    render()
elif "Upload" in pagina:
    from pages.upload import render
    render()

# ── rodapé ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='cl-footer'>
  Desenvolvido por <strong style='color:#ffffff'>Diogo Campos Gomes</strong>
  &nbsp;·&nbsp; Todos os direitos reservados
</div>
""", unsafe_allow_html=True)