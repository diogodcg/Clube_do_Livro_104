"""
app.py  —  Clube do Livro · Frontend Streamlit
Execute com:  streamlit run app.py
"""

import streamlit as st
from drive_backend import (
    autenticar,
    listar_arquivos,
    extrair_metadados,
    link_download,
    link_visualizar,
    buscar_capa_openlibrary,
)

# ── página ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Clube do Livro",
    page_icon="📚",
    layout="centered",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .cl-header {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 2rem 0 0.25rem;
  }
  .cl-header h1 {
    font-family: 'Lora', serif;
    font-size: clamp(1.6rem, 4vw, 2.2rem);
    font-weight: 600; color: #f0e6d3; margin: 0; line-height: 1.1;
  }
  .cl-subtitle { font-size: 0.85rem; color: #8a7f72; margin-bottom: 1.5rem; letter-spacing: 0.03em; }
  .cl-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: #1e1a15; border: 1px solid #3a3228; border-radius: 999px;
    padding: 0.3rem 0.9rem; font-size: 0.8rem; color: #c9a96e; margin-bottom: 1.75rem;
  }
  .stTextInput > label {
    font-size: 0.8rem !important; font-weight: 500 !important;
    color: #8a7f72 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important;
  }
  .stTextInput > div > div > input {
    font-family: 'Lora', serif !important; font-size: 1.05rem !important;
    background: #1a1612 !important; border: 1px solid #3a3228 !important;
    border-radius: 8px !important; color: #f0e6d3 !important; padding: 0.65rem 1rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #c9a96e !important; box-shadow: 0 0 0 2px rgba(201,169,110,0.15) !important;
  }
  .stSelectbox > label {
    font-size: 0.8rem !important; color: #8a7f72 !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
  }
  div[data-baseweb="select"] > div {
    background: #1a1612 !important; border: 1px solid #3a3228 !important;
    border-radius: 8px !important; color: #f0e6d3 !important;
  }
  .book-card {
    background: #1a1612; border: 1px solid #2e2820; border-radius: 12px;
    padding: 1.1rem 1.2rem 1rem; margin-bottom: 1rem; transition: border-color 0.2s;
  }
  .book-card:hover { border-color: #c9a96e44; }
  .book-title {
    font-family: 'Lora', serif; font-size: clamp(0.95rem, 2.5vw, 1.1rem);
    font-weight: 600; color: #f0e6d3; margin-bottom: 0.35rem; line-height: 1.3;
  }
  .book-meta {
    font-size: 0.8rem; color: #8a7f72;
    display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-bottom: 0.75rem;
  }
  .book-meta span { color: #a89880; }
  .badge {
    display: inline-block; background: #2a2218; color: #c9a96e;
    border: 1px solid #3a3228; border-radius: 4px;
    padding: 1px 7px; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.05em;
  }
  /* botão lupa */
  div[data-testid="stButton"] button {
    background: #2a2218 !important;
    border: 1px solid #3a3228 !important;
    color: #c9a96e !important;
    border-radius: 8px !important;
    font-size: 1.1rem !important;
    height: 2.75rem !important;
    width: 100% !important;
    padding: 0 !important;
    transition: background 0.2s, border-color 0.2s !important;
  }
  div[data-testid="stButton"] button:hover {
    background: #332b1e !important;
    border-color: #c9a96e !important;
  }

  .stLinkButton a {
    background: #2a2218 !important; border: 1px solid #3a3228 !important;
    color: #c9a96e !important; border-radius: 7px !important;
    font-size: 0.82rem !important; font-weight: 500 !important;
  }
  .stLinkButton a:hover { background: #332b1e !important; border-color: #c9a96e !important; }
  .cover-placeholder {
    width: 90px; height: 128px; background: #2a2218; border: 1px solid #3a3228;
    border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 2rem;
  }
  .empty-state { text-align: center; padding: 2.5rem 1rem; color: #5a5248; }
  .empty-state .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
  .empty-state p { font-size: 0.9rem; margin: 0; }

  @media (max-width: 640px) {
    .cl-header h1 { font-size: 1.5rem; }
    .book-card { padding: 0.85rem; }
    .cover-placeholder { width: 70px; height: 100px; font-size: 1.5rem; }
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 0 !important; max-width: 780px !important; }
</style>
""", unsafe_allow_html=True)

# ── header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cl-header">
  <span style="font-size:2rem">📚</span>
  <h1>Clube do Livro</h1>
</div>
<p class="cl-subtitle">Acervo compartilhado · Google Drive</p>
""", unsafe_allow_html=True)

# ── carrega acervo UMA VEZ na sessão ─────────────────────────────────────────
# st.session_state garante que não recarrega a cada interação do usuário
if "acervo" not in st.session_state:
    with st.spinner("Carregando acervo do Google Drive… (só na primeira vez)"):
        try:
            service = autenticar()
            arquivos = listar_arquivos(service)
            st.session_state.acervo = [extrair_metadados(a) for a in arquivos]
        except Exception as e:
            st.error(f"Erro ao conectar ao Google Drive: {e}")
            st.stop()

acervo = st.session_state.acervo

st.markdown(
    f'<div class="cl-badge">📖 &nbsp;<strong>{len(acervo)}</strong> livros no acervo</div>',
    unsafe_allow_html=True,
)

# ── busca local (zero requisições ao Drive) ───────────────────────────────────
col_input, col_btn = st.columns([9, 1], gap="small")
with col_input:
    termo = st.text_input(
        "Título",
        placeholder="Digite para filtrar… ex: sapiens, hábitos, liderança",
        label_visibility="collapsed",
        key="campo_busca",
    )
with col_btn:
    st.markdown("<div style='height:0rem'></div>", unsafe_allow_html=True)
    buscar_clicado = st.button("🔍", use_container_width=True, help="Buscar")

if not termo or len(termo) < 2:
    st.markdown(
        '<div class="empty-state"><div class="icon">🔍</div>'
        '<p>Digite ao menos 2 letras para filtrar os títulos.</p></div>',
        unsafe_allow_html=True,
    )
    st.stop()

# Filtra 100% em memória — instantâneo
termos = termo.lower().split()
sugestoes = [
    m for m in acervo
    if all(t in m["nome"].lower() for t in termos)
]

if not sugestoes:
    st.markdown(
        '<div class="empty-state"><div class="icon">📭</div>'
        f'<p>Nenhum livro encontrado para <strong>"{termo}"</strong>.<br>'
        'Tente outro termo.</p></div>',
        unsafe_allow_html=True,
    )
    st.stop()

# ── dropdown de seleção ───────────────────────────────────────────────────────
titulos = [m["titulo"] for m in sugestoes]

if len(sugestoes) == 1:
    meta = sugestoes[0]
else:
    st.markdown(
        f"<p style='font-size:0.8rem;color:#5a5248;margin:0.25rem 0 0.5rem'>"
        f"{len(sugestoes)} título(s) encontrado(s) — selecione um:</p>",
        unsafe_allow_html=True,
    )
    escolha = st.selectbox("Selecione", options=titulos, label_visibility="collapsed")
    meta = next(m for m in sugestoes if m["titulo"] == escolha)

# ── card do livro selecionado ─────────────────────────────────────────────────
capa_url = meta.get("thumbnail")
if not capa_url:
    # Busca capa na Open Library só quando o livro é selecionado
    cache_key = f"capa_{meta['id']}"
    if cache_key not in st.session_state:
        with st.spinner("Buscando capa…"):
            st.session_state[cache_key] = buscar_capa_openlibrary(meta["titulo"], meta.get("autor"))
    capa_url = st.session_state[cache_key]

col_img, col_info = st.columns([1, 3], gap="medium")

with col_img:
    if capa_url:
        st.image(capa_url, width=100)
    else:
        st.markdown('<div class="cover-placeholder">📄</div>', unsafe_allow_html=True)

with col_info:
    meta_parts = []
    if meta["autor"]:  meta_parts.append(f"<span>✍️ {meta['autor']}</span>")
    if meta["edicao"]: meta_parts.append(f"<span>📌 {meta['edicao']}</span>")
    if meta["ano"]:    meta_parts.append(f"<span>🗓️ {meta['ano']}</span>")
    meta_parts.append(f"<span class='badge'>{meta['ext']}</span>")

    st.markdown(f"""
    <div class="book-card">
      <div class="book-title">{meta['titulo']}</div>
      <div class="book-meta">{'&nbsp;·&nbsp;'.join(meta_parts)}</div>
      <div style="font-size:0.72rem;color:#4a4540;margin-top:-0.3rem">📁 {meta['nome']}</div>
    </div>
    """, unsafe_allow_html=True)

    col_d, col_v = st.columns(2)
    with col_d:
        st.link_button("⬇️ Download", url=link_download(meta["id"]), use_container_width=True)
    with col_v:
        st.link_button("👁️ Visualizar", url=link_visualizar(meta["id"]), use_container_width=True)