
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.config.config import HEADERS


class ComandoPlay:
    def __init__(self):
        self.result = list()
        self.deal = requests.Session()
        self.deal.headers = HEADERS

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
        result = []
        soup = html
        itens = soup.select(".item-container .item")
        if not itens:
            print("[ERRO] Verifique os selectores")
            return []

        for item in itens:
            try:
                image = item.find("img")["data-src"]
                link = urlparse(item.find("a")["href"]).path # # Extrai o caminho da URL
                genero = item.find("span", attrs={"class":"genre"}).text.strip()
                title = item.find("h2", attrs={"class":"movie-title"}).text.strip()
                rank = item.find("div", attrs={"class":"imdb-rating"}).text.strip()
                data_movie = item.find("span", attrs={"class":"movie-date"}).text.strip()
                description = item.find("p", attrs={"class":"movie-description"}).text.strip()

                result.append({
                    "title": title, "description": description,
                    "data-movie": data_movie, "category": genero,
                    "link": link, "image": image, "rank": rank
                })

            except AttributeError:
                print("[EXCEPT] Erro ao extrair informações de um item.")
                continue
        
        self.result = result.copy()
        return result
    
    def extract_movie(self, html: BeautifulSoup) -> list:
        soup = html
        multi_element = soup.find(class_="multi")

        link = multi_element.find_all("a")
        return link[0]["href"]
