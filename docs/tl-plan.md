# Tech Lead Plan — KAN-2, KAN-3, KAN-4

Data: 2026-03-30
Projeto: kanban gol (Django 4.2)

---

## Visao Geral

Tres cards devem ser implementados em paralelo pelo agente Dev Fullstack. Todos operam sobre o mesmo repositorio Django ja configurado (KAN-1 concluido). O agente deve trabalhar nos tres em sequencia logica: modelos (KAN-2) -> API REST (KAN-3) -> Docker (KAN-4), pois KAN-3 depende dos models de KAN-2.

---

## KAN-2 — Criar models de Voo, Passageiro e Reserva

### App Django

Criar um novo app chamado `voos` dentro do projeto:

```
gol_airline/
voos/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

Comando para criar: `python manage.py startapp voos`

### Models a implementar em `voos/models.py`

**Voo**
- `numero` — CharField(max_length=10, unique=True)
- `origem` — CharField(max_length=3) — codigo IATA do aeroporto
- `destino` — CharField(max_length=3) — codigo IATA do aeroporto
- `data_partida` — DateTimeField
- `data_chegada` — DateTimeField
- `capacidade` — PositiveIntegerField
- `status` — CharField(max_length=20, choices) com opcoes: AGENDADO, CANCELADO, CONCLUIDO

**Passageiro**
- `nome` — CharField(max_length=200)
- `cpf` — CharField(max_length=14, unique=True)
- `email` — EmailField(unique=True)
- `telefone` — CharField(max_length=20, blank=True)
- `data_nascimento` — DateField

**Reserva**
- `voo` — ForeignKey(Voo, on_delete=CASCADE, related_name='reservas')
- `passageiro` — ForeignKey(Passageiro, on_delete=CASCADE, related_name='reservas')
- `assento` — CharField(max_length=5)
- `status` — CharField(max_length=20, choices) com opcoes: CONFIRMADA, CANCELADA, PENDENTE
- `data_reserva` — DateTimeField(auto_now_add=True)
- Constraint unique_together: (voo, assento)

### Admin em `voos/admin.py`

Registrar os tres models com `admin.site.register`. Usar `list_display` para melhorar a visualizacao:
- VooAdmin: list_display = ['numero', 'origem', 'destino', 'data_partida', 'status']
- PassageiroAdmin: list_display = ['nome', 'cpf', 'email']
- ReservaAdmin: list_display = ['voo', 'passageiro', 'assento', 'status', 'data_reserva']

### settings.py

Adicionar `'voos'` a INSTALLED_APPS.

### Migrations

Executar `python manage.py makemigrations voos` para gerar `voos/migrations/0001_initial.py`.

---

## KAN-3 — Criar API REST de consulta de voos disponiveis

### Dependencia

Requer KAN-2 concluido (models Voo existente).

### requirements.txt

Adicionar `djangorestframework==3.15.2` ao arquivo.

### settings.py

Adicionar `'rest_framework'` a INSTALLED_APPS.

### Arquivos a criar em `voos/`

**`voos/serializers.py`**
- `VooSerializer` — ModelSerializer com todos os campos de Voo
- `VooDetalheSerializer` — igual ao VooSerializer (pode herdar ou ser o mesmo; expandivel no futuro com nested reservas se necessario)

**`voos/views.py`** (substituir o gerado pelo startapp)
- `VooViewSet` — ReadOnlyModelViewSet (apenas GET) com:
  - `queryset = Voo.objects.all()`
  - `serializer_class = VooSerializer`
  - Metodo `get_queryset` com filtros opcionais via query params:
    - `?origem=GRU`
    - `?destino=CGH`
    - `?data=2026-03-30` — filtra por data_partida__date

**`voos/urls.py`** (novo arquivo)
- Criar DefaultRouter, registrar `VooViewSet` no prefixo `voos`
- Exportar `urlpatterns = router.urls`

### gol_airline/urls.py

Adicionar inclusao da rota do app voos:
```python
from django.urls import include
path('api/', include('voos.urls')),
```

### Endpoints resultantes

- `GET /api/voos/` — lista todos os voos (com filtros opcionais)
- `GET /api/voos/{id}/` — detalhe de um voo especifico

### docs/API.md

Documentar os endpoints com descricao, parametros de query, exemplos de resposta 200 e 404.

---

## KAN-4 — Configurar Docker e docker-compose

### Dockerfile (raiz do projeto)

```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "gol_airline.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml (raiz do projeto)

Servicos:
- `db`: postgres:15-alpine, variaveis POSTGRES_DB/USER/PASSWORD via env_file, volume nomeado `postgres_data`
- `web`: build a partir do Dockerfile local, depends_on db, env_file .env, porta 8000:8000, volume para hot-reload em desenvolvimento

### settings.py — DATABASE_URL

Substituir o bloco DATABASES atual para ler `DATABASE_URL` via decouple com dj-database-url:

```python
import dj_database_url
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
```

Adicionar `dj-database-url==2.1.0` ao requirements.txt.

### .env.example (atualizar)

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_URL=postgres://gol_user:gol_pass@db:5432/gol_db
POSTGRES_DB=gol_db
POSTGRES_USER=gol_user
POSTGRES_PASSWORD=gol_pass
```

### .gitignore

Verificar se `.env` ja esta no .gitignore (ja esta, conforme setup inicial).

---

## Ordem de implementacao recomendada

1. KAN-2: criar app `voos`, models, migrations, admin — sem dependencias externas
2. KAN-3: serializers, viewset, urls — depende dos models do KAN-2
3. KAN-4: Dockerfile, docker-compose, ajuste de settings, .env.example — independente do codigo da app, pode ser feito em paralelo com KAN-2/KAN-3, mas a atualizacao do settings.py deve ser coordenada

---

## Estrutura final de arquivos apos os 3 cards

```
/
├── Dockerfile                        # KAN-4 (novo)
├── docker-compose.yml                # KAN-4 (novo)
├── .env.example                      # KAN-4 (atualizar)
├── manage.py
├── requirements.txt                  # KAN-3 + KAN-4 (adicionar deps)
├── gol_airline/
│   ├── settings.py                   # KAN-2 + KAN-3 + KAN-4 (atualizar)
│   └── urls.py                       # KAN-3 (atualizar)
├── voos/                             # KAN-2 (app novo)
│   ├── __init__.py
│   ├── admin.py                      # KAN-2
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py           # KAN-2
│   ├── models.py                     # KAN-2
│   ├── serializers.py                # KAN-3 (novo)
│   ├── urls.py                       # KAN-3 (novo)
│   └── views.py                      # KAN-3
└── docs/
    └── API.md                        # KAN-3 (preencher)
```

---

## Decisoes tecnicas

- App unica `voos` agrupa todos os models relacionados a voos, passageiros e reservas — evita fragmentacao prematura
- ReadOnlyModelViewSet para a API de voos — KAN-3 define apenas leitura; escrita (CRUD completo) e escopo de cards futuros
- Filtros via `get_queryset` manual em vez de django-filter — mantem dependencias minimas conforme convencao de simplicidade
- dj-database-url para parsear DATABASE_URL — padrao da industria, compativel com Heroku e Railway alem do Docker
- postgres:15-alpine no docker-compose — imagem leve, versao LTS estavel
- gunicorn como servidor WSGI no container — ja esta no requirements.txt desde KAN-1
