
from typing import Optional

import requests
from bs4 import BeautifulSoup

from src.util import util
from src.config.config import URL_S, URL_PLAY



def debug(content):
    with open("index.html", "wt") as file:
        file.write(content)
        file.close()

class ComandoPlay:
    def __init__(self):
        self.filmes = list()
        self.series = list()
        self.deal = requests.Session()
        self.deal.headers.update({"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"})

    @staticmethod
    def soup(content: str) -> BeautifulSoup:
        """Retorna um objeto BeautifulSoup para análise do HTML"""
        return BeautifulSoup(content, "html.parser")

    # region - Requests Server
    def fetch_page(self, url: str, params: dict=None) -> Optional[str]:
        """Faz requisição para a página e retorna o HTML se bem sucedida"""
        try:
            response = self.deal.get(url, params=params)
            response.raise_for_status()
            return response.text
        except requests.RequestException as error:
            print(f"[!] Erro ao acessar {url}: {error}")
            return None
        
    def extract_itens(self, html: BeautifulSoup) -> list:
        """Extrai informações de filmes/séries da página HTML"""
        soup = html
        itens = soup.select(".item-container .item")
        if not itens:
            print("[ERRO] Verifique os selectores")
            return []
        result = util.result_filmes(itens)
        self.filmes = result.copy()
        return result
    
    def extract_movie(self, html: BeautifulSoup) -> list:
        soup = html
        result = util.result_movie(soup)
        return result


class AssistirBiz:
    def __init__(self):
        self.series = list()
        self.deal = requests.Session()
        self.deal.headers.update({"upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"})

    @staticmethod
    def soup(content: str) -> BeautifulSoup:
        """Retorna um objeto BeautifulSoup para análise do HTML"""
        return BeautifulSoup(content, "html.parser")

    # region - Requests Server
    def fetch_page(self, url: str, params: dict=None) -> Optional[str]:
        """Faz requisição para a página e retorna o HTML se bem sucedida"""
        try:
            response = self.deal.get(url, params=params)
            response.raise_for_status()
            return response.text
        except requests.RequestException as error:
            # print(f"[!] Erro ao acessar {url}: {error}")
            return None

    def extract_series(self, html: BeautifulSoup) -> list:
        """Extrai informações de séries da página HTML"""
        soup = html
        itens = soup.select("div.catalog > div > div > div")
        if not itens:
            print("[ERRO] Verifique os selectores")
            return []
        result = util.result_series(itens)
        self.series = result.copy()
        return result

    def extract_temporadas(self, html: BeautifulSoup) -> list:
        soup = html
        result = util.result_temporadas(soup)
        return result

    def extract_episodes(self, html: BeautifulSoup) -> list:
        soup = html
        epsodios_result = util.result_episodes(soup)
        return epsodios_result

    def get_ep_link_video(self, id_video):
        """Busca o link do vídeo de uma série pelo ID."""
        url = f"{URL_S}/getepisodio"
        data = {"id": id_video}
        headers = {"origin": URL_S, "x-requested-with": "XMLHttpRequest","content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

        try:
            res = self.deal.post(url, data=data, headers=headers)
            if "tá fazendo o quê aqui?" in res.text:
                return [{"error": "não achou o link"}]
            json_data = res.json()
            link = f"{URL_PLAY}/{id_video}/{json_data['token']}"
            return link
        except Exception as e:
            return [{"error": str(e)}]
