
from fastapi import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.controllers.scraper import AssistirBiz, debug
from src.config.config import U_SERIES, URL_SERIES


router = APIRouter()
scraper = AssistirBiz()
scraper.deal.headers.update({"upgrade-insecure-requests": "1"})

@router.get("/series", status_code=200)
def get_series():
    """Busca os Séries na página Series."""
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

@router.get("/serie/{link:path}", status_code=200)
def serie(link: str = Path(...)):
    """Buscar um série pelo link"""
    url = f"{U_SERIES}{link}"
    res = scraper.fetch_page(url)
    if not res:
        return JSONResponse(
            content={"error": "invalid request"}, status_code=443
        )
    debug(res)
    html = scraper.soup(res)
    data = scraper.extract_serie(html)
    return JSONResponse(
        content={
            "status": True, 
            "seriee": data
        }
    )