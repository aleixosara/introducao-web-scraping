import requests

SITES_PARA_VERIFICAR = [
    "https://google.com",
    "https://github.com",
    "https://books.toscrape.com/",
    "https://httpbin.org/status/404",  # Um site que sempre retorna 404 (Não Encontrado)
    "https://endereco-que-nao-existe.com.br",  # Um site que não existe
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

print("--- Iniciando Verificador de Status de Sites ---\n")

for site in SITES_PARA_VERIFICAR:
    try:
        # Usamos `head` pois é mais rápido, não baixa o corpo da página
        # `allow_redirects=True` permite seguir redirecionamentos (ex: http para https)
        response = requests.head(site, headers=HEADERS, timeout=5, allow_redirects=True)

        # `raise_for_status()` vai gerar um erro para status 4xx ou 5xx
        response.raise_for_status()
        print(f"✅ {site} - Status: {response.status_code} (OK)")
    except requests.exceptions.RequestException as e:
        # Captura erros de conexão, timeout, status de erro (4xx, 5xx), etc.
        print(f"❌ {site} - Erro: {e}")
