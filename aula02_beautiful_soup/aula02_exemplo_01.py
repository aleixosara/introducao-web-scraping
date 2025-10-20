# Aula 2: Usando Beautiful Soup para extrair dados de um HTML.

import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

print(f"Buscando dados em: {URL}")

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    print("HTML analisado com sucesso!\n")
    print("--- DADOS EXTRAÍDOS ---")
    
    livros = soup.find_all("article", class_="product_pod")

    for livro in livros:
        titulo_tag = livro.find("h3").find("a")
        titulo = titulo_tag[
            "title"
        ]

        preco_tag = livro.find("p", class_="price_color")
        preco = preco_tag.text.strip()[1:]

        print(f"Título: {titulo}")
        print(f"Preço: {preco}")
        print("-" * 20)

    print(f"\nTotal de {len(livros)} livros encontrados na página.")


except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro na requisição: {e}")
except Exception as e:
    print(f"Ocorreu um erro ao processar os dados: {e}")
