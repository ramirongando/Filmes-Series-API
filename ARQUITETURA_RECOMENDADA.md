# 🏗️ Arquitetura Recomendada para API de Filmes

## 📋 Visão Geral

Com base na análise do seu projeto atual e nas melhores práticas da indústria, recomendo uma **Arquitetura em Camadas (Layered Architecture)** combinada com **Clean Architecture** para sua API de filmes. Esta abordagem oferece escalabilidade, manutenibilidade e testabilidade.

## 🎯 Arquitetura Atual vs. Recomendada

### ✅ Pontos Fortes da Arquitetura Atual
- Separação clara entre routers e controllers
- Uso do FastAPI (excelente escolha)
- Estrutura modular básica
- Sistema de autenticação implementado

### 🚀 Melhorias Recomendadas

## 📐 Estrutura de Diretórios Recomendada

```
projeto/
├── src/
│   ├── api/                    # Camada de Apresentação
│   │   ├── routers/           # Rotas da API
│   │   ├── middleware/        # Middlewares personalizados
│   │   ├── dependencies/      # Dependências injetáveis
│   │   └── schemas/           # Modelos Pydantic (DTOs)
│   ├── core/                   # Camada de Domínio
│   │   ├── entities/          # Entidades de negócio
│   │   ├── use_cases/         # Casos de uso
│   │   ├── interfaces/        # Contratos/Abstrações
│   │   └── exceptions/        # Exceções customizadas
│   ├── infrastructure/         # Camada de Infraestrutura
│   │   ├── database/          # Configuração do banco
│   │   ├── external_apis/     # APIs externas (TMDB, OMDB)
│   │   ├── cache/             # Sistema de cache
│   │   ├── scraping/          # Web scraping
│   │   └── storage/           # Armazenamento de arquivos
│   ├── services/              # Camada de Aplicação
│   │   ├── movie_service.py
│   │   ├── user_service.py
│   │   └── auth_service.py
│   └── config/                # Configurações
├── tests/                     # Testes automatizados
├── migrations/                # Migrações do banco
├── docs/                      # Documentação
└── docker/                    # Arquivos Docker
```

## 🏛️ Padrões Arquiteturais Recomendados

### 1. **Clean Architecture + Hexagonal Architecture**

```python
# Exemplo de estrutura de caso de uso
class GetMovieDetailsUseCase:
    def __init__(
        self, 
        movie_repository: MovieRepositoryInterface,
        external_api: ExternalMovieAPIInterface,
        cache_service: CacheServiceInterface
    ):
        self.movie_repository = movie_repository
        self.external_api = external_api
        self.cache_service = cache_service
    
    async def execute(self, movie_id: str) -> MovieEntity:
        # Lógica de negócio pura
        pass
```

### 2. **Repository Pattern**
- Abstração da camada de dados
- Facilita testes e mudanças de banco de dados

### 3. **Dependency Injection**
- Inversão de controle
- Facilita testes unitários

## 🗄️ Estratégia de Dados Recomendada

### Banco de Dados Principal: **PostgreSQL**
```sql
-- Exemplo de estrutura de tabelas
CREATE TABLE movies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    original_title VARCHAR(255),
    release_date DATE,
    duration INTEGER,
    rating DECIMAL(3,1),
    synopsis TEXT,
    poster_url VARCHAR(500),
    trailer_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE genres (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE movie_genres (
    movie_id UUID REFERENCES movies(id),
    genre_id UUID REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);
```

### Cache: **Redis**
```python
# Exemplo de implementação de cache
class MovieCacheService:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1 hora
    
    async def get_movie(self, movie_id: str) -> Optional[dict]:
        cached = await self.redis.get(f"movie:{movie_id}")
        return json.loads(cached) if cached else None
    
    async def set_movie(self, movie_id: str, movie_data: dict):
        await self.redis.setex(
            f"movie:{movie_id}", 
            self.ttl, 
            json.dumps(movie_data)
        )
```

## 🔧 Stack Tecnológica Recomendada

### Backend Core
- **FastAPI** (mantém atual)
- **SQLAlchemy 2.0** (ORM)
- **Alembic** (migrações)
- **Pydantic V2** (validação)

### Banco de Dados
- **PostgreSQL** (principal)
- **Redis** (cache/sessions)

### APIs Externas
- **TMDB API** (The Movie Database)
- **OMDB API** (backup/complemento)

### Monitoramento & Logs
- **Prometheus** + **Grafana**
- **Sentry** (error tracking)
- **Structlog** (logging estruturado)

### Infraestrutura
- **Docker** + **Docker Compose**
- **Nginx** (reverse proxy)
- **Gunicorn** (WSGI server)

## 🔐 Autenticação & Autorização

### JWT + OAuth2
```python
# Exemplo de implementação
class AuthService:
    def __init__(self, jwt_service: JWTService, user_repository: UserRepository):
        self.jwt_service = jwt_service
        self.user_repository = user_repository
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repository.get_by_email(email)
        if user and self.verify_password(password, user.password_hash):
            return user
        return None
    
    async def create_access_token(self, user: User) -> str:
        payload = {"sub": str(user.id), "email": user.email}
        return self.jwt_service.encode(payload)
```

## 📊 Sistema de Cache Multicamadas

```python
# Cache L1: Memória (para dados frequentes)
# Cache L2: Redis (para dados compartilhados)
# Cache L3: CDN (para assets estáticos)

class MultiLevelCacheService:
    def __init__(self):
        self.memory_cache = {}  # L1
        self.redis_cache = redis_client  # L2
        self.cdn_cache = cdn_client  # L3
    
    async def get(self, key: str):
        # Tenta L1 primeiro
        if key in self.memory_cache:
            return self.memory_cache[key]
        
        # Depois L2
        value = await self.redis_cache.get(key)
        if value:
            self.memory_cache[key] = value
            return value
        
        return None
```

## 🚀 Performance & Escalabilidade

### 1. **Paginação Eficiente**
```python
class PaginationParams:
    def __init__(self, page: int = 1, size: int = 20):
        self.page = max(1, page)
        self.size = min(100, max(1, size))
        self.offset = (self.page - 1) * self.size
```

### 2. **Rate Limiting**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/movies")
@limiter.limit("100/minute")
async def get_movies(request: Request):
    pass
```

### 3. **Background Tasks**
```python
# Para tarefas pesadas como scraping
from celery import Celery

celery_app = Celery('movie_api')

@celery_app.task
def scrape_movie_data(movie_id: str):
    # Scraping em background
    pass
```

## 🧪 Estratégia de Testes

```python
# Testes unitários
class TestMovieService:
    def test_get_movie_details(self):
        # Mock das dependências
        mock_repo = Mock(spec=MovieRepository)
        service = MovieService(mock_repo)
        # Testes...

# Testes de integração
class TestMovieAPI:
    async def test_get_movie_endpoint(self, client):
        response = await client.get("/api/movies/123")
        assert response.status_code == 200
```

## 🐳 Containerização

```dockerfile
# Dockerfile otimizado
FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY . .

# Usuário não-root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
```

## 📈 Monitoramento & Observabilidade

```python
# Métricas customizadas
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('api_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

## 🔄 CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy API

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deploy steps
```

## 📚 Próximos Passos Recomendados

1. **Implementar banco de dados PostgreSQL**
2. **Adicionar sistema de cache Redis**
3. **Integrar APIs externas (TMDB)**
4. **Implementar autenticação JWT**
5. **Adicionar testes automatizados**
6. **Configurar monitoramento**
7. **Dockerizar aplicação**
8. **Implementar CI/CD**

## 💡 Considerações Finais

Esta arquitetura oferece:
- ✅ **Escalabilidade horizontal e vertical**
- ✅ **Manutenibilidade e testabilidade**
- ✅ **Performance otimizada**
- ✅ **Segurança robusta**
- ✅ **Monitoramento completo**
- ✅ **Deploy automatizado**

A implementação pode ser feita de forma incremental, mantendo o sistema atual funcionando enquanto migra gradualmente para a nova arquitetura.