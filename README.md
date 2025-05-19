# ComandoPlay API 🎬

API REST para catálogo de filmes e séries, construída com **FastAPI**, que realiza scraping no site ComandoPlay para disponibilizar dados organizados via endpoints JSON.

## 📌 Funcionalidades

- 🔎 Listagem de filmes da página inicial (`/api/movies`)
- 🎞️ Busca de detalhes de filmes individuais (`/api/video/{link}`)
- 🚀 Rota raiz com mensagem de boas-vindas (`/`)
- 🔧 Projeto modular com separação por routers e controllers

---

## ⚙️ Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)
- Python 3.8+

---

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/ramirongando/Filmes-Series-API.git
cd Filmes-Series-API
pip install requirements.txt
python main.py
