
from urllib.parse import urlparse
from src.config.config import IMG


def result_filmes(itens):
    result = []
    for item in itens:
        try:
            image = item.find("img")["data-src"]
            link = urlparse(item.find("a")["href"]).path # Extrai o caminho da URL
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
    
    return result

def safe_text(soup, selector, attr=None, index=0):
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

def result_movie(soup):
    multi_element = soup.find(class_="multi")
    link = multi_element.find_all("a") if multi_element else []

    return [{
        "image": safe_text(soup, ("img", {"itemprop": "image"}), attr="src"),
        "title": safe_text(soup, ("h1", {"itemprop": "name"})),
        "movie-data": safe_text(soup, "select:span:nth-child(2) > a"),
        "category": safe_text(soup, "select:span:nth-child(3) > a"),
        "duration": safe_text(soup, ("span", {"itemprop": "duration"})),
        "description": safe_text(soup, ("p", {"class": "movie-description"})),
        "video": link[0]["href"] if link else ""
    }]

def result_series(itens):
    result = []
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
                image = img_tag.get("data-src", IMG)

            result.append({
                "title": title,
                "data-serie": serie_data,
                "category": category,
                "link": link,
                "image": image,
                "rank": rank
            })

        except AttributeError:
            # print("[EXCEPT] Erro ao extrair informações de um item.")
            continue
    return result

def result_temporadas(soup):
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
        image = img_tag.get("data-src", IMG)

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
                img = _tag.get("data-src", IMG)


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
        "seasons": temporadas_result,
        "total": index
    })
    return result

def result_episodes(soup):
    epsodios_result= []
        
    for tr in soup.select("tr[onclick*='reloadVideoSerie(']"):
        onclick = tr.get("onclick", "reloadVideoSerie(2837, 'f576078a6d201711ba4834c58f138b20')")
        id_video = onclick.split(",")[0].split("(")[1].strip()

        ths = tr.find_all("th")
        pos = ths[0].text.strip() if len(ths) > 0 else ""
        titulo = ths[-1].text.strip() if len(ths) > 1 else ""

        epsodios_result.append({"title": titulo, "pos": pos, "id_video": id_video})
    return epsodios_result