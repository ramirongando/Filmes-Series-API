
from typing import Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.config.config import HEADERS



def debug(content):
    with open("index.html", "wt") as file:
        file.write(content)
        file.close()

class ComandoPlay:
    def __init__(self):
        self.filmes = list()
        self.series = list()
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
        
        self.filmes = result.copy()
        return result
    
    def extract_movie(self, html: BeautifulSoup) -> list:
        soup = html
        result = []
        multi_element = soup.find(class_="multi")
        link = multi_element.find_all("a") if multi_element else []

        def safe_text(selector, attr=None, index=0):
            try:
                if attr:
                    return soup.find(selector[0], selector[1])[attr].strip()
                elif isinstance(selector, tuple):
                    return soup.find(selector[0], selector[1]).text.strip()
                elif selector.startswith("select:"):
                    sel = soup.select(selector[7:])
                    return sel[index].text.strip() if len(sel) > index else ""
            except (AttributeError, IndexError, TypeError):
                return ""

        result.append({
            "image": safe_text(("img", {"itemprop": "image"}), attr="src"),
            "title": safe_text(("h1", {"itemprop": "name"})),
            "movie-data": safe_text("select:span:nth-child(2) > a"),
            "category": safe_text("select:span:nth-child(3) > a"),
            "duration": safe_text(("span", {"itemprop": "duration"})),
            "description": safe_text(("p", {"class": "movie-description"})),
            "video": link[0]["href"] if link else ""
        })

        return result


class AssistirBiz(ComandoPlay):
    def extract_series(self, html: BeautifulSoup) -> list:
        """Extrai informações de séries da página HTML"""
        result = []
        soup = html
        itens = soup.select("div.catalog > div > div > div")
        if not itens:
            print("[ERRO] Verifique os selectores")
            return []
        
        for item in itens:
            try:
                title = item.find("h3", attrs={"class": "card__title"}).text.strip()
                category = item.select("span > a:nth-child(1)")[0].text.strip()
                serie_data = item.select("span > a:nth-child(2)")[0].text.strip()
                rank = item.find("span", attrs={"class": "card__rate"}).text.strip()
                link = item.select("div.card__cover > a")[0]["href"]
                img_tag = item.find("img")
                image = img_tag.get("src", "")
                if not image or "poster_default" in image or "_filter(blur)" in image:
                    image = img_tag.get("data-src", "https://assistir.biz/assets/img/poster_default.jpg")

                result.append({
                    "title": title, "data-serie": serie_data, 
                    "category": category, "link": link, 
                    "image": image, "rank": rank
                })

            except AttributeError:
                print("[EXCEPT] Erro ao extrair informações de um item.")
                continue

        self.series = result.copy()
        return result


