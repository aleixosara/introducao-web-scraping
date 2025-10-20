import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def extrair_detalhes_primeiro_livro():
    """
    Encontra o primeiro livro na página principal, segue seu link e
    extrai informações detalhadas da página do produto.
    """
    try:
        print(f"Acessando a página principal: {BASE_URL}")
        response_main = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response_main.raise_for_status()
        soup_main = BeautifulSoup(response_main.text, "lxml")

        primeiro_livro_tag = soup_main.find("h3").find("a")
        link_parcial = primeiro_livro_tag["href"]

        url_detalhes = BASE_URL  + link_parcial.replace("../", "")

        print(f"Acessando a página de detalhes: {url_detalhes}")
        response_details = requests.get(url_detalhes, headers=HEADERS, timeout=10)
        response_details.raise_for_status()
        soup_details = BeautifulSoup(response_details.text, "lxml")

        titulo = soup_details.find("h1").text
        descricao = (
            soup_details.find("article", class_="product_page")
            .find("p", recursive=False)
            .text
        )
        
        upc = soup_details.find("th", string="UPC").find_next_sibling("td").text

        dados_detalhados = {
            "titulo": titulo,
            "upc": upc,
            "descricao": descricao.strip(),
        }
        return dados_detalhados

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")
        return None


if __name__ == "__main__":
    detalhes = extrair_detalhes_primeiro_livro()
    if detalhes:
        print("\n--- Detalhes Extraídos ---")
        print(json.dumps(detalhes, indent=2, ensure_ascii=False))
