import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://www.omelete.com.br/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36"
}


def extrair_titulos_materias(url):
    """
    Extrai títulos das matérias do Omelete e retorna uma lista de dicionários.
    """
    try:
        print(f"Buscando dados em: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        titulos = soup.find_all("h2", class_="card__title js-featured-title")

        dados_materias = []
        for t in titulos:
            titulo = t.text.strip()

            # tenta pegar o link sem quebrar o código
            link_tag = t.find_parent("a")
            link = link_tag.get("href") if link_tag and link_tag.has_attr("href") else None

            dados_materias.append({
                "titulo": titulo,
                "link": link
            })

        return dados_materias

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        return None


def salvar_em_json(dados, nome_arquivo):
    """
    Salva uma lista de dicionários em um arquivo JSON.
    """
    caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"✅ Dados salvos com sucesso no arquivo '{caminho_arquivo}'!")


if __name__ == "__main__":
    dados_extraidos = extrair_titulos_materias(URL)
    if dados_extraidos:
        print(f"\nForam extraídas {len(dados_extraidos)} matérias.")
        salvar_em_json(dados_extraidos, "materias_omelete.json")

        print("\n--- Algumas das matérias extraídas ---")
        for materia in dados_extraidos[:5]:
            print(materia)
