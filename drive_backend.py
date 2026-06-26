"""
drive_backend.py
Módulo de acesso ao Google Drive — usado pelo CLI e pelo frontend Streamlit.
"""

import os
import re
import requests

# Lê as credenciais dos Secrets do Streamlit
import streamlit as st
import json

credentials_info = json.loads(st.secrets["google"]["credentials"])
flow = Flow.from_client_config(credentials_info, SCOPES, redirect_uri=...)

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── constantes ────────────────────────────────────────────────────────────────
FOLDER_ID        = "1-dPWk5NKI_3BsECgS-7gSTQICHIzjvRf"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"
SCOPES           = ["https://www.googleapis.com/auth/drive.readonly"]
BOOK_EXTENSIONS  = {".pdf", ".epub", ".mobi", ".azw", ".azw3", ".djvu", ".fb2", ".txt", ".zip"}

# ── autenticação ──────────────────────────────────────────────────────────────
def autenticar():
    """Autentica via OAuth2 e retorna o service do Drive."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Produção: lê dos Secrets do Streamlit Cloud
            if "google" in st.secrets:
                credentials_info = json.loads(st.secrets["google"]["credentials"])
                flow = Flow.from_client_config(
                    credentials_info,
                    SCOPES,
                    redirect_uri="https://clubedolivro104.streamlit.app/oauth2callback"
                )
                creds = flow.run_local_server(port=0)
            # Local: lê do arquivo credentials.json
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)

# ── listagem recursiva ────────────────────────────────────────────────────────
def listar_arquivos(service, folder_id=FOLDER_ID):
    """Retorna todos os livros (recursivo em subpastas)."""
    arquivos = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"

    while True:
        resp = service.files().list(
            q=query,
            pageSize=1000,
            fields=(
                "nextPageToken, files("
                "id, name, mimeType, description, "
                "properties, appProperties, thumbnailLink, hasThumbnail"
                ")"
            ),
            pageToken=page_token,
        ).execute()

        for item in resp.get("files", []):
            if item["mimeType"] == "application/vnd.google-apps.folder":
                arquivos.extend(listar_arquivos(service, item["id"]))
            else:
                ext = os.path.splitext(item["name"])[1].lower()
                if ext in BOOK_EXTENSIONS:
                    arquivos.append(item)

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return arquivos

# ── metadados ─────────────────────────────────────────────────────────────────
def extrair_metadados(arquivo):
    nome = arquivo["name"]
    nome_sem_ext, ext = os.path.splitext(nome)
    titulo = nome_sem_ext
    autor = edicao = ano = None

    m_ano = re.search(r"\((\d{4})\)", nome_sem_ext)
    if m_ano:
        ano = m_ano.group(1)
        nome_sem_ext = nome_sem_ext.replace(m_ano.group(0), "").strip()

    m_ed = re.search(
        r"(\d+[\wªº°.]*\s*(?:ed(?:ição|ition|\.)?|vol(?:ume|\.)?|v\.))",
        nome_sem_ext, re.IGNORECASE,
    )
    if m_ed:
        edicao = m_ed.group(1).strip()

    if " - " in nome_sem_ext:
        partes = [p.strip() for p in nome_sem_ext.split(" - ", 1)]
        if len(partes[0]) < len(partes[1]):
            autor, titulo = partes
        else:
            titulo, autor = partes

    props = {**arquivo.get("properties", {}), **arquivo.get("appProperties", {})}
    if props.get("author"):  autor  = props["author"]
    if props.get("title"):   titulo = props["title"]
    if props.get("edition"): edicao = props["edition"]

    # Thumbnail: usa o link do Drive se existir
    thumbnail = arquivo.get("thumbnailLink") or None

    return {
        "id"       : arquivo["id"],
        "nome"     : arquivo["name"],
        "titulo"   : titulo.strip(" -"),
        "autor"    : autor,
        "edicao"   : edicao,
        "ano"      : ano,
        "ext"      : ext.lstrip(".").upper(),
        "thumbnail": thumbnail,
    }

# ── busca ─────────────────────────────────────────────────────────────────────
def buscar(todos: list, termo: str) -> list:
    """Filtra a lista de arquivos pelo termo digitado (todas as palavras)."""
    termos = termo.lower().split()
    return [
        extrair_metadados(a)
        for a in todos
        if all(t in a["name"].lower() for t in termos)
    ]

# ── links ─────────────────────────────────────────────────────────────────────
def link_download(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def link_visualizar(file_id: str) -> str:
    return f"https://drive.google.com/file/d/{file_id}/view"

# ── thumbnail via Open Library (fallback público) ─────────────────────────────
def buscar_capa_openlibrary(titulo: str, autor: str = None):
    """
    Tenta encontrar a capa do livro na Open Library.
    Retorna URL da imagem ou None.
    """
    try:
        q = titulo
        if autor:
            q += f" {autor}"
        resp = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": q, "limit": 1, "fields": "cover_i,title"},
            timeout=5,
        )
        data = resp.json()
        docs = data.get("docs", [])
        if docs and docs[0].get("cover_i"):
            cover_id = docs[0]["cover_i"]
            return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    except Exception:
        pass
    return None
