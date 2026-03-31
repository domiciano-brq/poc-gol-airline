# Architecture

Projeto **kanban gol** — sistema de reservas aereas em Django 4.2.

## Stack

- **Backend:** Django 4.2, Python 3.11
- **API REST:** Django REST Framework 3.15
- **Banco de dados:** PostgreSQL 15 (producao/Docker) / SQLite (desenvolvimento local sem Docker)
- **Servidor WSGI:** Gunicorn
- **Containerizacao:** Docker + docker-compose
- **Configuracao:** python-decouple + dj-database-url

## Estrutura

```
/
├── Dockerfile                  # Imagem Django (Python 3.11 slim)
├── docker-compose.yml          # Servicos: web (Django) + db (PostgreSQL 15)
├── .env.example                # Variaveis de ambiente de referencia
├── manage.py
├── requirements.txt
├── gol_airline/                # Pacote de configuracao do projeto Django
│   ├── settings.py
│   ├── urls.py                 # Roteamento raiz: /admin/ e /api/
│   ├── wsgi.py
│   └── asgi.py
├── voos/                       # App Django: dominio de voos e reservas
│   ├── models.py               # Voo, Passageiro, Reserva
│   ├── serializers.py          # VooSerializer
│   ├── views.py                # VooViewSet (ReadOnly)
│   ├── urls.py                 # Router DRF: /api/voos/
│   ├── admin.py                # Registro no Django Admin
│   └── migrations/
└── docs/                       # Documentacao do projeto
    ├── API.md                  # Documentacao dos endpoints REST
    ├── ARCHITECTURE.md         # Este arquivo
    ├── CONVENTIONS.md
    └── DECISIONS.md
```

## Key Components

- **gol_airline/** — configuracao central do Django (settings, urls, wsgi)
- **voos/** — app responsavel por Voos, Passageiros e Reservas; expoe API REST em `/api/voos/`
- **Django Admin** — interface administrativa disponivel em `/admin/` para gerenciar os tres models
- **docs/** — documentacao centralizada, incluindo contrato de API

## Data Flow

```
Cliente HTTP
    |
    v
GET /api/voos/?origem=GRU
    |
    v
gol_airline/urls.py  -->  voos/urls.py (DRF Router)
    |
    v
VooViewSet.list()  -->  get_queryset() aplica filtros
    |
    v
VooSerializer  -->  JSON response
    |
    v
PostgreSQL / SQLite
```

## Ambientes

| Ambiente         | Banco de dados          | Como subir                         |
|-----------------|-------------------------|------------------------------------|
| Local (sem Docker) | SQLite (db.sqlite3)   | `python manage.py runserver`       |
| Docker (dev)     | PostgreSQL 15           | `docker-compose up`                |
