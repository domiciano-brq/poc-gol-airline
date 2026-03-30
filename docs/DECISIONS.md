# Architecture Decisions

## ADR-001 — App unica `voos` para todos os models do dominio
**Data:** 2026-03-30
**Cards:** KAN-2, KAN-3
**Decisao:** Criar um unico app Django chamado `voos` para conter os models Voo, Passageiro e Reserva, os serializers e as views da API.
**Motivo:** O sistema esta em fase inicial. Separar em tres apps (voos, passageiros, reservas) seria over-engineering neste momento. Um app unico e mais simples de manter e pode ser refatorado quando o dominio crescer.

## ADR-002 — ReadOnlyModelViewSet para a API de voos
**Data:** 2026-03-30
**Cards:** KAN-3
**Decisao:** Usar `ReadOnlyModelViewSet` do DRF em vez de `ModelViewSet` completo.
**Motivo:** KAN-3 define apenas endpoints de leitura (GET). Expor escrita (POST/PUT/DELETE) sem historias correspondentes violaria o principio de minimo necessario. CRUD completo sera adicionado em cards futuros se necessario.

## ADR-003 — Filtros manuais via get_queryset em vez de django-filter
**Data:** 2026-03-30
**Cards:** KAN-3
**Decisao:** Implementar filtros por origem, destino e data dentro do metodo `get_queryset` do ViewSet, sem adicionar a dependencia `django-filter`.
**Motivo:** Tres filtros simples nao justificam uma dependencia adicional. Mantem o requirements.txt enxuto e segue a convencao de simplicidade do projeto.

## ADR-004 — dj-database-url para parsing de DATABASE_URL
**Data:** 2026-03-30
**Cards:** KAN-4
**Decisao:** Adicionar `dj-database-url` ao requirements.txt e usar `dj_database_url.parse(DATABASE_URL)` no settings.py.
**Motivo:** Permite trocar entre SQLite (dev local) e PostgreSQL (Docker/producao) apenas alterando a variavel de ambiente DATABASE_URL, sem modificar settings.py. Padrao amplamente adotado no ecossistema Django.

## ADR-005 — postgres:15-alpine no docker-compose
**Data:** 2026-03-30
**Cards:** KAN-4
**Decisao:** Usar a imagem `postgres:15-alpine` para o servico `db` no docker-compose.
**Motivo:** PostgreSQL 15 e a versao LTS estavel. A variante alpine reduz o tamanho da imagem. Compativel com psycopg2-binary ja presente no requirements.txt.

## ADR-006 — Python 3.11-slim como base do Dockerfile
**Data:** 2026-03-30
**Cards:** KAN-4
**Decisao:** Usar `python:3.11-slim` como imagem base no Dockerfile.
**Motivo:** Django 4.2 e totalmente suportado em Python 3.11. A variante slim elimina ferramentas desnecessarias, reduzindo o tamanho da imagem de ~900MB para ~130MB.
