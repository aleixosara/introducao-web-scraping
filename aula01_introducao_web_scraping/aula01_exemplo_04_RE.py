import requests
import re

URL = "https://books.toscrape.com/"

print(f"Iniciando a requisição para: {URL}")

try:
    response = requests.get(URL, timeout=10) 
    response.raise_for_status()  
    print("Requisição bem-sucedida! Status Code:", response.status_code)
    html_content = response.text

except requests.exceptions.RequestException as e:
  
    print(f"Ocorreu um erro na requisição: {e}")
    
print("\n--- 2. Iniciando Parsing com Expressões Regulares (Regex) ---")

padrao = re.compile(
    r'title="([^"]+)".*?<p class="price_color">.£([\d.]+)</p>',
    re.DOTALL
)

matches = padrao.findall(html_content)

print(f"\n✅ Regex encontrou {len(matches)} correspondências.")
print("Amostra das 3 primeiras (o resultado é uma lista de tuplas):")
print(matches[:3])

livros_extraidos_regex = []
for match in matches:
    titulo = match[0]
    preco = float(match[1])
    livros_extraidos_regex.append({'titulo': titulo, 'preco': preco})

for livro in livros_extraidos_regex:
    print(livro)