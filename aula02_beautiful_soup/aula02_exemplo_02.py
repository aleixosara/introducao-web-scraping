import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    sidebar = soup.find("div", class_="side_categories")
    category_tags = sidebar.find("ul").find_all("a")

    print("--- Categorias de Livros Encontradas ---\n")
    for tag in category_tags:
        nome_categoria = tag.text.strip()
        link_parcial = tag["href"]
        link_completo = URL + link_parcial
        print(f"Categoria: {nome_categoria} -> Link: {link_completo}")

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro: {e}")
