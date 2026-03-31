# Implementation Report — KAN-2, KAN-3, KAN-4

Data: 2026-03-30

---

## KAN-2 — Criar models de Voo, Passageiro e Reserva

### Arquivos Criados

| Arquivo | Descricao |
|---------|-----------|
| `voos/__init__.py` | Inicializador do app Django |
| `voos/apps.py` | Configuracao do app VoosConfig |
| `voos/models.py` | Models Voo, Passageiro e Reserva |
| `voos/admin.py` | Registro dos 3 models no Django Admin com list_display |
| `voos/tests.py` | Arquivo de testes (scaffolding) |
| `voos/migrations/__init__.py` | Inicializador do modulo migrations |
| `voos/migrations/0001_initial.py` | Migration inicial criando as 3 tabelas |

### Arquivos Modificados

| Arquivo | Modificacao |
|---------|-------------|
| `gol_airline/settings.py` | Adicionado `'voos'` a INSTALLED_APPS |

### Models implementados

**Voo**
- `numero`: CharField(max_length=10, unique=True)
- `origem`: CharField(max_length=3) — codigo IATA
- `destino`: CharField(max_length=3) — codigo IATA
- `data_partida`: DateTimeField
- `data_chegada`: DateTimeField
- `capacidade`: PositiveIntegerField
- `status`: CharField com choices agendado/cancelado/concluido

**Passageiro**
- `nome`: CharField(max_length=200)
- `cpf`: CharField(max_length=14, unique=True)
- `email`: EmailField(unique=True)
- `telefone`: CharField(max_length=20, blank=True)
- `data_nascimento`: DateField

**Reserva**
- `voo`: ForeignKey(Voo, CASCADE, related_name='reservas')
- `passageiro`: ForeignKey(Passageiro, CASCADE, related_name='reservas')
- `assento`: CharField(max_length=5)
- `status`: CharField com choices confirmada/cancelada/pendente
- `data_reserva`: DateTimeField(auto_now_add=True)
- unique_together: (voo, assento)

---

## KAN-3 — Criar API REST de consulta de voos disponiveis

### Arquivos Criados

| Arquivo | Descricao |
|---------|-----------|
| `voos/serializers.py` | VooSerializer e VooDetalheSerializer (ModelSerializer) |
| `voos/views.py` | VooViewSet (ReadOnlyModelViewSet) com filtros em get_queryset |
| `voos/urls.py` | DefaultRouter registrando VooViewSet no prefixo `voos` |
| `docs/API.md` | Documentacao completa dos endpoints |

### Arquivos Modificados

| Arquivo | Modificacao |
|---------|-------------|
| `gol_airline/settings.py` | Adicionado `'rest_framework'` a INSTALLED_APPS |
| `gol_airline/urls.py` | Adicionada rota `path('api/', include('voos.urls'))` |
| `requirements.txt` | Adicionado `djangorestframework==3.15.2` |

### Endpoints resultantes

| Metodo | URL | Descricao |
|--------|-----|-----------|
| GET | `/api/voos/` | Lista todos os voos (filtros: origem, destino, data) |
| GET | `/api/voos/{id}/` | Detalhe de um voo especifico |
| GET | `/api/` | API root (DRF browsable API) |

### Filtros disponiveis em GET /api/voos/

- `?origem=GRU` — filtra por codigo IATA de origem (case-insensitive)
- `?destino=CGH` — filtra por codigo IATA de destino (case-insensitive)
- `?data=2026-03-30` — filtra por data de partida (formato YYYY-MM-DD)

---

## KAN-4 — Configurar Docker e docker-compose

### Arquivos Criados

| Arquivo | Descricao |
|---------|-----------|
| `Dockerfile` | Imagem python:3.11-slim, instala deps, copia projeto, roda gunicorn na porta 8000 |
| `docker-compose.yml` | Servicos `web` (Django) e `db` (postgres:15-alpine) com volume `postgres_data` |

### Arquivos Modificados

| Arquivo | Modificacao |
|---------|-------------|
| `gol_airline/settings.py` | DATABASES agora usa `dj_database_url.parse(DATABASE_URL)` via python-decouple |
| `requirements.txt` | Adicionado `dj-database-url==2.1.0` |
| `.env.example` | Atualizado com DATABASE_URL postgres, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD |

### Variaveis de ambiente (.env.example)

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgres://gol_user:gol_pass@db:5432/gol_db
POSTGRES_DB=gol_db
POSTGRES_USER=gol_user
POSTGRES_PASSWORD=gol_pass
```

---

## Estrutura final do projeto

```
/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── manage.py
├── requirements.txt
├── gol_airline/
│   ├── __init__.py
│   ├── settings.py          (atualizado: rest_framework, voos, DATABASE_URL, dj_database_url)
│   ├── urls.py              (atualizado: include voos.urls em /api/)
│   ├── asgi.py
│   └── wsgi.py
├── voos/
│   ├── __init__.py
│   ├── apps.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── docs/
│   └── API.md               (documentacao dos endpoints)
└── reports/
    └── implementation-report.md
```
