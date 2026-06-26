"""
pages/upload.py — Página de upload de ebooks (em breve)
"""

import streamlit as st


def render():
    st.markdown("<h2 style='margin-bottom:0.25rem'>📤 Upload de Ebooks</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div style='
      background: #ffffff;
      border: 1px solid #dce6f7;
      border-left: 4px solid #f47c20;
      border-radius: 10px;
      padding: 2.5rem 2rem;
      text-align: center;
      margin-top: 1.5rem;
    '>
      <div style='font-size:3rem; margin-bottom:1rem'>🚀</div>
      <h3 style='color:#0d2d5e; margin-bottom:0.5rem'>Em breve!</h3>
      <p style='color:#5a7ab0; font-size:0.95rem; max-width:500px; margin:0 auto; line-height:1.7'>
        Em breve você poderá enviar ebooks diretamente por aqui, sem precisar acessar o Google Drive.<br><br>
        Enquanto isso, continue utilizando o link abaixo para compartilhar o seu acervo digital:<br>
        <a href='https://drive.google.com/drive/folders/1-dPWk5NKI_3BsECgS-7gSTQICHIzjvRf' target='_blank' style='color:#f47c20; font-weight:600; text-decoration:none;'>Link do Google Drive 📚</a>
      </p>
    </div>
    """, unsafe_allow_html=True)