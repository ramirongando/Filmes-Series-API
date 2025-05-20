
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
                title = item.find("h3", attrs={"class": "card__title"})
                category_sel = item.select("span > a:nth-child(1)")
                serie_data_sel = item.select("span > a:nth-child(2)")
                rank = item.find("span", attrs={"class": "card__rate"})
                link_sel = item.select("div.card__cover > a")
                img_tag = item.find("img")

                title = title.text.strip() if title else ""
                category = category_sel[0].text.strip() if len(category_sel) > 0 else ""
                serie_data = serie_data_sel[0].text.strip() if len(serie_data_sel) > 0 else ""
                rank = rank.text.strip() if rank else ""
                link = link_sel[0]["href"] if len(link_sel) > 0 and "href" in link_sel[0].attrs else ""

                img_tag = item.find("img")
                image = img_tag.get("src", "")
                if not image or "poster_default" in image or "_filter(blur)" in image:
                    image = img_tag.get("data-src", "https://assistir.biz/assets/img/poster_default.jpg")

                result.append({
                    "title": title,
                    "data-serie": serie_data,
                    "category": category,
                    "link": link,
                    "image": image,
                    "rank": rank
                })

            except AttributeError:
                print("[EXCEPT] Erro ao extrair informações de um item.")
                continue

        self.series = result.copy()
        return result

    def extract_serie(self, html: BeautifulSoup) -> list:
        soup = html
        result = []

        card = soup.find("div", attrs={"class": "card card--details card--series"})
        
        title = soup.find("h1", attrs={"class": "section__title"})
        title = title.text.strip() if title else ""

        category = card.select_one("div > ul > li:nth-child(1) > a")
        category = category.text.strip() if category else ""

        serie_data = card.select_one("div > ul > li:nth-child(2)")
        serie_data = serie_data.text.strip().split(":")[-1].strip() if serie_data else ""

        status = card.select_one("div > ul > li:nth-child(5) > span")
        status = status.text.strip() if status else ""

        description_tag = card.select_one("div.card__description.card__description--details")
        description = description_tag.text.strip() if description_tag else ""

        img_tag = card.find("img")
        image = img_tag.get("src", "") if img_tag else ""
        if not image or "poster_default" in image or "_filter(blur)" in image:
            image = img_tag.get("data-src", "https://assistir.biz/assets/img/poster_default.jpg") if img_tag else "https://assistir.biz/assets/img/poster_default.jpg"

        # Extrair temporadas
        temporadas = soup.select("section.section.section--details > div > div > div.container > div > div")

        temporadas_result = []
        for index, temporada in enumerate(temporadas):
            if index != 0:
                name = temporada.find("div", attrs={"class": "card__content"}).text.strip()
                link_sel = temporada.select("div.card__cover > a")
                link = link_sel[0]["href"] if len(link_sel) > 0 and "href" in link_sel[0].attrs else ""

                _tag = temporada.find("img")
                img = _tag.get("src", "") if _tag else ""
                if not img or "poster_default" in img or "_filter(blur)" in img:
                    img = _tag.get("data-src", "https://assistir.biz/assets/img/poster_default.jpg") if _tag else "https://assistir.biz/assets/img/poster_default.jpg"


                temporadas_result.append({
                    "season": name,
                    "image": img,
                    "link": link
                })

        result.append({
            "title": title,
            "data": serie_data,
            "status": status,
            "category": category,
            "image": image,
            "description": description,
            "seasons": temporadas_result
        })

        return result
