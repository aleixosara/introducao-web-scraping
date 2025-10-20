import requests

URL = "https://books.toscrape.com/"

print(f"Iniciando a requisição para: {URL}")

try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()  # Isso vai gerar um erro se o status não for 2xx (sucesso)

    print("Requisição bem-sucedida! Status Code:", response.status_code)

    print("\n--- Detalhes da Resposta ---")
    print(dir(response))
    print("\nCabeçalhos da Resposta:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")        
        #input("Pressione Enter para continuar ...")
    print("-" * 30)
    
    print("\nConteúdo da página (primeiros 500 caracteres):")
    print(response.text[:1000])  # Mostra os primeiros 1000 caracteres do HTML
    print("-" * 30)

    # Fazendo uma pausa antes de salvar, pressinte Enter para continuar
    input("Pressione Enter para salvar o conteúdo HTML em 'pagina.html'...")

    # Salvando o conteúdo da página em um arquivo HTML
    with open("pagina.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("O conteúdo HTML foi salvo no arquivo 'pagina.html'.")

except requests.exceptions.RequestException as e:
    # Captura qualquer erro que possa ocorrer durante a requisição (ex: sem internet, URL errada)
    print(f"Ocorreu um erro na requisição: {e}")
