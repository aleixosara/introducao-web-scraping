from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}


def extrair_titulos_materias(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    titulos = soup.find_all("h2", class_="card__title js-featured-title")

    dados_materias = []
    for t in titulos:
        titulo = t.text.strip()
        link_tag = t.find_parent("a")
        link = link_tag.get("href") if link_tag and link_tag.has_attr("href") else None
        dados_materias.append({"titulo": titulo, "link": link})
    return dados_materias


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extrair', methods=['POST'])
def extrair():
    url = request.form.get('url')
    if not url:
        return jsonify({"erro": "URL não fornecida"}), 400

    try:
        dados = extrair_titulos_materias(url)
        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route('/salvar', methods=['POST'])
def salvar():
    dados = request.json
    caminho = os.path.join(os.getcwd(), "materias_omelete.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return jsonify({"mensagem": f"Dados salvos em {caminho}"})


if __name__ == '__main__':
    app.run(debug=True)
