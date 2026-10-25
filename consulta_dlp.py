"""
Consulta somente leitura (GET) da API DLP Invest:
  - /carteira   -> posição atual
  - /operacoes  -> operações

O token é lido do arquivo .env na mesma pasta deste script (variável DLP_TOKEN).
Se não existir, usa a variável de ambiente DLP_TOKEN. Nunca é impresso nem gravado.

Uso:
    pip install requests
    python consulta_dlp.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "https://users.dlpinvest.com.br"
ENDPOINTS = ["/carteira", "/operacoes"]  # somente posição e operações
TIMEOUT = 30
PASTA = Path(__file__).resolve().parent
OUTPUT_DIR = PASTA / "saida"


def ler_env(caminho: Path) -> dict:
    """Lê pares CHAVE=valor de um arquivo .env simples (sem dependências extras)."""
    valores = {}
    if not caminho.is_file():
        return valores
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        valores[chave.strip()] = valor.strip().strip('"').strip("'")
    return valores


def obter_token() -> str:
    token = ler_env(PASTA / ".env").get("DLP_TOKEN", "").strip()
    if not token:
        token = os.environ.get("DLP_TOKEN", "").strip()
    if not token:
        sys.exit("DLP_TOKEN não encontrado no arquivo .env nem na variável de ambiente.")
    return token


def consultar(path: str, token: str):
    # Apenas GET: nenhuma alteração é enviada à API.
    headers = {"Authorization": token}
    resp = requests.get(BASE_URL + path, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    token = obter_token()
    OUTPUT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    for path in ENDPOINTS:
        nome = path.strip("/")
        try:
            dados = consultar(path, token)
        except requests.HTTPError as e:
            print(f"[{path}] erro HTTP {e.response.status_code}")
            continue
        except requests.RequestException as e:
            print(f"[{path}] erro de conexão: {e.__class__.__name__}")
            continue

        arquivo = OUTPUT_DIR / f"{nome}_{stamp}.json"
        arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{path}] salvo em {arquivo}")


if __name__ == "__main__":
    main()
