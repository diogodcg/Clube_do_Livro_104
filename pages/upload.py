"""
pages/upload.py — Página de upload de ebooks para o Google Drive
"""

import streamlit as st
from drive_backend import fazer_upload, BOOK_EXTENSIONS

# Mapa de extensão para mimetype
MIMETYPES = {
    ".pdf"  : "application/pdf",
    ".epub" : "application/epub+zip",
    ".mobi" : "application/x-mobipocket-ebook",
    ".azw"  : "application/vnd.amazon.ebook",
    ".azw3" : "application/vnd.amazon.ebook",
    ".djvu" : "image/vnd.djvu",
    ".fb2"  : "application/x-fictionbook+xml",
    ".txt"  : "text/plain",
    ".zip"  : "application/zip",
}

def render():
    st.markdown("<h2 style='margin-bottom:0.25rem'>📤 Upload de Ebooks</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#5a7ab0; font-size:0.85rem; margin-bottom:1.5rem'>"
        "Contribua com o acervo do clube enviando um ebook abaixo.</p>",
        unsafe_allow_html=True,
    )

    # Extensões aceitas para exibição
    extensoes = ", ".join(sorted(BOOK_EXTENSIONS))

    st.markdown(f"""
    <div style='
        background:#ffffff; border:1px solid #dce6f7;
        border-left:4px solid #f47c20; border-radius:10px;
        padding:1rem 1.2rem; margin-bottom:1.25rem;
        font-size:0.82rem; color:#5a7ab0;
    '>
        📋 <strong>Formatos aceitos:</strong> {extensoes}
    </div>
    """, unsafe_allow_html=True)

    arquivo = st.file_uploader(
        "Selecione o ebook",
        type=[ext.lstrip(".") for ext in BOOK_EXTENSIONS],
        label_visibility="collapsed",
    )

    if arquivo is None:
        st.markdown("""
        <div class='empty-state'>
          <div class='icon'>📂</div>
          <p>Clique acima para selecionar um arquivo do seu dispositivo.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Informações do arquivo selecionado
    import os
    ext = os.path.splitext(arquivo.name)[1].lower()
    tamanho_mb = arquivo.size / (1024 * 1024)

    st.markdown(f"""
    <div style='
        background:#e8f0fe; border:1px solid #cdd8f0;
        border-radius:10px; padding:1rem 1.2rem; margin-bottom:1.25rem;
    '>
        <div style='font-weight:600; color:#0d2d5e; margin-bottom:0.25rem'>📄 {arquivo.name}</div>
        <div style='font-size:0.8rem; color:#5a7ab0'>
            Formato: <strong>{ext.lstrip(".").upper()}</strong>
            &nbsp;·&nbsp;
            Tamanho: <strong>{tamanho_mb:.1f} MB</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬆️ Enviar para o acervo", use_container_width=True):
        if "service_drive" not in st.session_state:
            from drive_backend import autenticar
            st.session_state.service_drive = autenticar()

        mimetype = MIMETYPES.get(ext, "application/octet-stream")

        with st.spinner(f"Enviando «{arquivo.name}» para o Google Drive…"):
            try:
                resultado = fazer_upload(
                    st.session_state.service_drive,
                    arquivo.name,
                    arquivo.read(),
                    mimetype,
                )
                # Invalida cache do acervo para incluir o novo livro
                if "acervo" in st.session_state:
                    del st.session_state["acervo"]

                st.success(f"✅ **{resultado['name']}** enviado com sucesso para o acervo!")
                st.markdown("""
                <div style='
                    background:#ffffff; border:1px solid #dce6f7;
                    border-left:4px solid #f47c20; border-radius:10px;
                    padding:1rem 1.2rem; font-size:0.88rem; color:#1a3a6b;
                    margin-top:0.75rem;
                '>
                    📚 O livro já está disponível no acervo para todos os membros do clube!
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erro ao enviar o arquivo: {e}")