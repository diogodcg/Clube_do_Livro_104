#!/bin/bash
# ── Recria o ambiente virtual e sobe o Clube do Livro ────────────────────────

PASTA="/Users/diogodcg/Documents/VSCode_Praticas/Project_Clube_do_Livro_104"

echo "🗑️  Removendo ambiente antigo..."
rm -rf "$PASTA/env"

echo "🐍  Criando ambiente novo..."
python3 -m venv "$PASTA/env"

echo "⚡  Ativando ambiente..."
source "$PASTA/env/bin/activate"

echo "📦  Instalando dependências..."
pip install --quiet streamlit google-api-python-client google-auth-httplib2 google-auth-oauthlib requests

echo "🚀  Subindo o app..."
streamlit run "$PASTA/app.py"