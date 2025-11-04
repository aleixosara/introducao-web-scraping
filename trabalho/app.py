from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import json
import os

app = Flask(__name__)

URL_BASE = "https://www.omelete.com.br/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def extrair_titulos_materias(url):
    """
    Extrai títulos e links das matérias do Omelete.
    """
    try:
        print(f"🔍 Buscando dados em: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Tenta localizar os títulos (padrão atual do Omelete)
        titulos = soup.find_all("h2", class_="card__title js-featured-title")
        if not titulos:
            titulos = soup.find_all("h2", class_="title")

        dados_materias = []
        for t in titulos:
            titulo = t.get_text(strip=True)

            # Busca o link completo
            link_tag = t.find_parent("a")
            link = link_tag.get("href") if link_tag and link_tag.has_attr("href") else None
            if link:
                link = urljoin(url, link)  # Corrige links relativos

            dados_materias.append({
                "titulo": titulo,
                "link": link
            })

        print(f"✅ {len(dados_materias)} matérias extraídas.")
        return dados_materias

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        return None


def salvar_em_json(dados, nome_arquivo):
    """
    Salva as matérias extraídas em um arquivo JSON.
    """
    caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return caminho_arquivo


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extrair", methods=["POST"])
def extrair():
    url = request.form.get("url", URL_BASE)
    dados = extrair_titulos_materias(url)

    if not dados:
        return jsonify({"erro": "Não foi possível extrair as matérias."})
    return jsonify(dados)


@app.route("/salvar", methods=["POST"])
def salvar():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"mensagem": "Nenhum dado recebido."}), 400

        caminho = salvar_em_json(dados, "materias_omelete.json")
        return jsonify({"mensagem": f"✅ Dados salvos com sucesso em '{caminho}'!"})
    except Exception as e:
        return jsonify({"mensagem": f"❌ Erro ao salvar: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
