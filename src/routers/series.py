
from fastapi import Path
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.security.auth import autorisation
from src.controllers.scraper import SeriesScraper
from src.config.config import URL_S, URL_SERIES


router = APIRouter()
scraper = SeriesScraper()

@router.get("/series", dependencies=[Depends(autorisation)], status_code=200)
def fetch_all_series():
    """Retorna uma lista todas as séries disponíveis."""
    url = f"{URL_SERIES}"
    res = scraper.fetch_page(url)
    if not res:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )
    html = scraper.soup(res)
    data = scraper.extract_series(html)
    return JSONResponse(
        content={
            "status": True, 
            "series": data,
            "total": len(data)
        }
    )

@router.get("/temporadas/{serie:path}", dependencies=[Depends(autorisation)], status_code=200)
def fetch_a_serie(serie: str = Path(...)):
    """Busca os detalhes de uma série e as temporadas."""
    url = f"{URL_S}{serie}"
    res = scraper.fetch_page(url)
    if not res:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )

    html = scraper.soup(res)
    episodios = scraper.extract_temporadas(html)
    return JSONResponse(
        content={
            "status": True, 
            "serie-data": episodios,
        }
    )

@router.get("/episodios/{temporada:path}", dependencies=[Depends(autorisation)], status_code=200)
def catch_episodes(temporada: str = Path(...)):
    """Lista os episódios de uma temporada"""
    url = f"{URL_S}{temporada}"
    res = scraper.fetch_page(url)
    if not res:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )
    
    html = scraper.soup(res)
    episodios = scraper.extract_episodes(html)
    return JSONResponse(
        content={
            "status": True, 
            "episodios": episodios,
            "total":len(episodios)
        }
    )

@router.post("/video/{id_video:path}", dependencies=[Depends(autorisation)], status_code=200)
def video(id_video: str = Path(...)):
    """Retorna o link do vídeo de um episódio por ID"""
    res = scraper.get_ep_link_video(id_video)
    if "error" in res[0]:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )
    return JSONResponse(content={"video": res})
