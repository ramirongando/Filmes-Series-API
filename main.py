
import os
import uvicorn
from fastapi import FastAPI
from src.routers import home, series


app = FastAPI(
    version="1.0", 
    title="Filmes online API", 
    description="API REST de Catálogo de Filmes/Séries (com autenticação)",
)

# Iniciar as Rotas
app.include_router(home.router, prefix="/api", tags=["FILMES"]),
app.include_router(series.router, prefix="/api", tags=["SERIES"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do ComandoPlay!"}

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
