
from fastapi import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.controllers.scraper import ComandoPlay
from src.config.config import URL_BASE, URL_MOVIES



router = APIRouter()
scraper = ComandoPlay()

@router.get("/movies", status_code=200)
async def get_home(page: int = 1):
    """Busca os filmes na página inicial."""
    url = f"{URL_MOVIES}/page/{page}" if page > 1 else URL_MOVIES
    res = scraper.fetch_page(url)
    if not res:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )
    html = scraper.soup(res)
    data = scraper.extract_itens(html)
    return JSONResponse(
        content={
            "status": True, 
            "colections": data,
            "total": len(data)
        }
    )

@router.get("/video/{link:path}", status_code=200)
async def video(link: str = Path(...)):
    """Buscar um filme pelo link"""
    url = f"{URL_BASE}/{link}"
    res = scraper.fetch_page(url)
    if not res:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )
    html = scraper.soup(res)
    data = scraper.extract_movie(html)
    return JSONResponse(
        content={
            "status": True, 
            "video": data
        }
    )

