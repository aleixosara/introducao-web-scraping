import requests

URL = "https://books.toscrape.com/"

print(f"Iniciando a requisição para: {URL}")

try:
    response = requests.get(URL, timeout=10) 
    response.raise_for_status()  
    print("Requisição bem-sucedida! Status Code:", response.status_code)
    html_content = response.text

except requests.exceptions.RequestException as e:
  
    print(f"Ocorreu um erro na requisição: {e}")

print("\n--- 1. Iniciando Parsing 'na Mão' ---")
print("Objetivo: Extrair o título e o preço de cada livro.")

livros_extraidos_manual = []
cursor = 0
while True:
    inicio_bloco = html_content.find('<article class="product_pod">', cursor)
    
    if inicio_bloco == -1:
        break
    
    fim_bloco = html_content.find('</article>', inicio_bloco)
    
    html_livro = html_content[inicio_bloco:fim_bloco]
    
    marcador_titulo = 'title="'
    inicio_titulo = html_livro.find(marcador_titulo) + len(marcador_titulo)
    fim_titulo = html_livro.find('">', inicio_titulo)
    titulo = html_livro[inicio_titulo:fim_titulo]
    
    marcador_preco = '<p class="price_color">Â£'
    inicio_preco = html_livro.find(marcador_preco) + len(marcador_preco)
    fim_preco = html_livro.find('</p>', inicio_preco)
    preco_str = html_livro[inicio_preco:fim_preco]

    dados = {'titulo': titulo, 'preco': preco_str}
    print(titulo, preco_str)

    livros_extraidos_manual.append(dados)
    
    cursor = fim_bloco

print(f"\n✅ Foram extraídos {len(livros_extraidos_manual)} livros manualmente.")

for livro in livros_extraidos_manual:
    print(livro)

