"""
pages/acervo.py — Listagem completa do acervo em ordem alfabética
"""

import streamlit as st
from drive_backend import link_download, link_visualizar


def render():
    st.markdown("<h2 style='margin-bottom:0.25rem'>📋 Acervo Completo</h2>", unsafe_allow_html=True)

    acervo = st.session_state.get("acervo", [])
    ordenado = sorted(acervo, key=lambda m: m["titulo"].lower())

    st.markdown(
        f"<p style='color:#5a7ab0; font-size:0.85rem; margin-bottom:1.25rem'>"
        f"{len(ordenado)} livros disponíveis · ordenados alfabeticamente</p>",
        unsafe_allow_html=True,
    )

    # Filtro rápido
    filtro = st.text_input(
        "Filtrar lista",
        placeholder="Filtrar por título ou autor…",
        label_visibility="collapsed",
    )

    if filtro:
        termos = filtro.lower().split()
        ordenado = [
            m for m in ordenado
            if all(t in m["titulo"].lower() or (m["autor"] or "").lower().__contains__(t) for t in termos)
        ]
        st.markdown(
            f"<p style='font-size:0.78rem; color:#8aa3cc; margin-bottom:0.75rem'>"
            f"{len(ordenado)} resultado(s) para <strong>{filtro}</strong></p>",
            unsafe_allow_html=True,
        )

    if not ordenado:
        st.markdown("""
        <div class='empty-state'>
          <div class='icon'>📭</div>
          <p>Nenhum livro encontrado com esse filtro.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Cabeçalho da tabela
    st.markdown("""
    <div style='
      display:grid;
      grid-template-columns: 3fr 2fr 80px 80px;
      gap:0.5rem;
      padding: 0.5rem 1rem;
      font-size:0.75rem;
      font-weight:600;
      color:#5a7ab0;
      letter-spacing:0.05em;
      text-transform:uppercase;
      border-bottom: 2px solid #dce6f7;
      margin-bottom:0.25rem;
    '>
      <div>Título</div>
      <div>Autor</div>
      <div style='text-align:center'>Formato</div>
      <div style='text-align:center'>Ações</div>
    </div>
    """, unsafe_allow_html=True)

    for m in ordenado:
        col_titulo, col_autor, col_fmt, col_acoes = st.columns([3, 2, 0.8, 1.2], gap="small")

        with col_titulo:
            st.markdown(
                f"<div style='font-size:0.88rem; font-weight:600; color:#0d2d5e; "
                f"padding:0.6rem 0; line-height:1.3'>{m['titulo']}</div>",
                unsafe_allow_html=True,
            )
        with col_autor:
            autor = m["autor"] or "—"
            st.markdown(
                f"<div style='font-size:0.82rem; color:#5a7ab0; padding:0.6rem 0'>{autor}</div>",
                unsafe_allow_html=True,
            )
        with col_fmt:
            st.markdown(
                f"<div style='text-align:center; padding:0.5rem 0'>"
                f"<span class='badge'>{m['ext']}</span></div>",
                unsafe_allow_html=True,
            )
        with col_acoes:
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("⬇️", url=link_download(m["id"]), use_container_width=True, help="Download")
            with c2:
                st.link_button("👁️", url=link_visualizar(m["id"]), use_container_width=True, help="Visualizar")

        st.markdown("<hr style='margin:0; border-color:#f0f4fb'>", unsafe_allow_html=True)