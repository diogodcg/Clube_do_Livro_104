"""
pages/busca.py — Página de busca de livros por título
"""

import streamlit as st
from drive_backend import link_download, link_visualizar, buscar_capa_openlibrary


def render():
    st.markdown("<h2 style='margin-bottom:0.25rem'>🔍 Busca de Livro</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#5a7ab0; font-size:0.85rem; margin-bottom:1.25rem'>Digite o título ou parte dele para encontrar no acervo.</p>", unsafe_allow_html=True)

    acervo = st.session_state.get("acervo", [])

    termo = st.text_input(
        "Buscar",
        placeholder="ex: sapiens, hábitos, liderança…",
        label_visibility="collapsed",
    )

    if not termo or len(termo) < 2:
        st.markdown("""
        <div class='empty-state'>
          <div class='icon'>🔍</div>
          <p>Digite ao menos 2 letras para filtrar os títulos.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    termos = termo.lower().split()
    sugestoes = [m for m in acervo if all(t in m["nome"].lower() for t in termos)]

    if not sugestoes:
        st.markdown(f"""
        <div class='empty-state'>
          <div class='icon'>📭</div>
          <p>Nenhum livro encontrado para <strong>"{termo}"</strong>.<br>Tente outro termo.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    titulos = [m["titulo"] for m in sugestoes]

    if len(sugestoes) == 1:
        meta = sugestoes[0]
    else:
        st.markdown(
            f"<p style='font-size:0.8rem; color:#8aa3cc; margin:0.25rem 0 0.25rem'>"
            f"{len(sugestoes)} título(s) encontrado(s):</p>"
            f"<p style='font-size:0.78rem; color:#f47c20; margin:0 0 0.4rem'>▼ Clique abaixo para escolher o livro</p>",
            unsafe_allow_html=True,
        )
        escolha = st.selectbox("Selecione", options=titulos, label_visibility="collapsed")
        meta = next(m for m in sugestoes if m["titulo"] == escolha)

    # Capa
    capa_url = meta.get("thumbnail")
    if not capa_url:
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
        if meta["autor"]:  meta_parts.append(f"✍️ {meta['autor']}")
        if meta["edicao"]: meta_parts.append(f"📌 {meta['edicao']}")
        if meta["ano"]:    meta_parts.append(f"🗓️ {meta['ano']}")

        badges = f"<span class='badge'>{meta['ext']}</span>"

        st.markdown(f"""
        <div class='book-card'>
          <div class='book-title'>{meta['titulo']}</div>
          <div class='book-meta'>
            {'&nbsp;·&nbsp;'.join(meta_parts)}&nbsp;&nbsp;{badges}
          </div>
          <div style='font-size:0.72rem; color:#8aa3cc; margin-top:0.4rem'>📁 {meta['nome']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_d, col_v = st.columns(2)
        with col_d:
            st.link_button("⬇️ Download", url=link_download(meta["id"]), use_container_width=True)
        with col_v:
            st.link_button("👁️ Visualizar", url=link_visualizar(meta["id"]), use_container_width=True)