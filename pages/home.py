"""
pages/home.py — Página inicial do Clube do Livro 104
"""

import streamlit as st


def render():
    st.markdown("""
    <div style='padding: 2rem 0 1rem'>
      <h1 style='font-size:clamp(1.6rem,4vw,2.2rem); margin-bottom:0.25rem'>
        Bem-vindo ao Clube do Livro 104! 📚
      </h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='
      background: #ffffff;
      border: 1px solid #dce6f7;
      border-left: 4px solid #f47c20;
      border-radius: 10px;
      padding: 1.75rem 2rem;
      font-size: 1rem;
      line-height: 1.8;
      color: #1a3a6b;
      margin-top: 1rem;
    '>
      <p>
        Este clube é formado por leitores e leitoras da <strong>CAIXA</strong>.
      </p>
      <p>
        Aqui você encontra todo o acervo deste clube que começou com um grupo no
        <strong>WhatsApp</strong> e hoje pode contar com participantes de toda a empresa
        espalhados por todo o Brasil.
      </p>
      <p style='margin-bottom:0'>
        Caso você tenha ebooks e queira colaborar, basta fazer o upload e deixar
        disponível para todos. 📖
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
        <div style='background:#e8f0fe; border-radius:10px; padding:1.25rem; text-align:center'>
          <div style='font-size:2rem'>🔍</div>
          <div style='font-weight:600; color:#0d2d5e; margin:0.5rem 0 0.25rem'>Buscar Livro</div>
          <div style='font-size:0.82rem; color:#5a7ab0'>
            Encontre um livro pelo título com busca em tempo real.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:#fff0e6; border-radius:10px; padding:1.25rem; text-align:center'>
          <div style='font-size:2rem'>📋</div>
          <div style='font-weight:600; color:#0d2d5e; margin:0.5rem 0 0.25rem'>Acervo Completo</div>
          <div style='font-size:0.82rem; color:#5a7ab0'>
            Veja todos os livros disponíveis em ordem alfabética.
          </div>
        </div>
        """, unsafe_allow_html=True)