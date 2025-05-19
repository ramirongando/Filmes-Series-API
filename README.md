# 📽️ Catálogo de Filmes e Séries - API 🎬

API REST para catálogo de filmes e séries, construída com **FastAPI**, que realiza scraping em fontes públicas online. O objetivo é fornecer uma interface estruturada para consumo de dados de entretenimento organizados via endpoints JSON.

## 📌 Funcionalidades

- 📄 Listar filmes da página inicial (com paginação)
- 🔍 Buscar detalhes de um filme por link
- 📺 Listar séries (em breve)
- 🚀 Rota raiz com mensagem de boas-vindas (`/`)
- 🔧 Projeto modular com separação por routers e controllers

---

## ⚙️ Tecnologias utilizadas

- Python 3.12+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)

---

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/ramirongando/Filmes-Series-API.git
cd Filmes-Series-API 
```

### 2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode o servidor
```bash
python main.py
```

---

## 📫 Endpoints

| Método | Rota                    | Descrição                             |
|--------|-------------------------|---------------------------------------|
| GET    | `/`                     | Mensagem de boas-vindas               |
| GET    | `/api/movies?page=1`    | Lista filmes da página inicial        |
| GET    | `/api/video/{link}`     | Busca detalhes de um filme pelo link  |

---

## 🧑‍💻 Autor

- **Ramiro Ngando** — [@ramirongando](https://github.com/ramirongando)

---