"""
pages/upload.py — Página de upload de ebooks para o Google Drive
"""

import os
import streamlit as st
from drive_backend import (
    fazer_upload,
    BOOK_EXTENSIONS,
    verificar_duplicata,
    extrair_metadados,
)

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


def _enviar(service, nome, conteudo, mimetype):
    """Executa o upload e atualiza o estado da sessão."""
    with st.spinner(f"Enviando «{nome}» para o Google Drive…"):
        try:
            resultado = fazer_upload(service, nome, conteudo, mimetype)

            if "acervo" in st.session_state:
                del st.session_state["acervo"]
            st.session_state.pop("duplicata_detectada", None)

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


def render():
    st.markdown("<h2 style='margin-bottom:0.25rem'>📤 Upload de Ebooks</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#5a7ab0; font-size:0.85rem; margin-bottom:1.5rem'>"
        "Contribua com o acervo do clube enviando um ebook abaixo.</p>",
        unsafe_allow_html=True,
    )

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
        st.session_state.pop("duplicata_detectada", None)
        st.markdown("""
        <div class='empty-state'>
          <div class='icon'>📂</div>
          <p>Clique acima para selecionar um arquivo do seu dispositivo.</p>
        </div>
        """, unsafe_allow_html=True)
        return

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

    if "service_drive" not in st.session_state:
        from drive_backend import autenticar
        st.session_state.service_drive = autenticar()

    mimetype = MIMETYPES.get(ext, "application/octet-stream")
    conteudo = arquivo.getvalue()  # lê uma vez, reutiliza depois

    # ── Se já detectamos duplicata nesta sessão, mostra o aviso e as opções ──
    if st.session_state.get("duplicata_detectada"):
        dup = st.session_state.duplicata_detectada
        livro = dup["livro"]

        if dup["tipo"] == "hash":
            st.warning(
                f"⚠️ Este **arquivo já existe** no acervo, com o nome:\n\n"
                f"📖 **{livro['titulo']}**  ·  `{livro['nome']}`"
            )
        else:
            st.warning(
                f"⚠️ Encontramos um livro **parecido** no acervo "
                f"(similaridade {dup['score']}%):\n\n"
                f"📖 **{livro['titulo']}**" +
                (f"  ·  ✍️ {livro['autor']}" if livro.get("autor") else "")
            )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancelar envio", use_container_width=True):
                st.session_state.pop("duplicata_detectada", None)
                st.rerun()
        with col2:
            if st.button("✅ Enviar mesmo assim", use_container_width=True):
                _enviar(st.session_state.service_drive, arquivo.name, conteudo, mimetype)
        return

    # ── Botão principal: verifica duplicata antes de liberar o envio ────────
    if st.button("⬆️ Enviar para o acervo", use_container_width=True):
        meta_novo = extrair_metadados({"name": arquivo.name})
        acervo = st.session_state.get("acervo", [])

        with st.spinner("Verificando se este livro já está no acervo…"):
            resultado = verificar_duplicata(conteudo, meta_novo["titulo"], acervo)

        if resultado["tipo"]:
            st.session_state.duplicata_detectada = resultado
            st.rerun()
        else:
            _enviar(st.session_state.service_drive, arquivo.name, conteudo, mimetype)