# PO Briefing — Sprint Ativa (Projeto: kanban gol)

Data: 2026-03-30
Cloud ID: 6ada5b32-f313-475d-a367-57bb73a51580

---

## Cards Ativos (status: A fazer)

### KAN-2 — Criar models de Voo, Passageiro e Reserva
- **Prioridade:** Medium
- **Tipo:** Tarefa
- **Descrição:**
  Criar os models Django para as entidades principais do sistema:
  - **Voo**: numero, origem, destino, data_partida, data_chegada, capacidade, status
  - **Passageiro**: nome, cpf, email, telefone, data_nascimento
  - **Reserva**: voo, passageiro, assento, status, data_reserva
  - Criar migrations e registrar no Django Admin.
- **Critério de aceitação:** Models criados com migrations, registrados no Admin, sem erros.

---

### KAN-3 — Criar API REST de consulta de voos disponíveis
- **Prioridade:** Medium
- **Tipo:** Tarefa
- **Descrição:**
  Implementar endpoint REST para consulta de voos usando Django REST Framework:
  - `GET /api/voos/` — listar voos com filtros por origem, destino e data
  - `GET /api/voos/{id}/` — detalhe de um voo específico
  - Serializers, ViewSets e roteamento via router
  - Adicionar `djangorestframework` ao requirements.txt
  - Documentar os endpoints no `docs/API.md`.
- **Critério de aceitação:** Endpoints funcionando, DRF configurado, API documentada.

---

### KAN-4 — Configurar Docker e docker-compose para ambiente de desenvolvimento
- **Prioridade:** Medium
- **Tipo:** Tarefa
- **Descrição:**
  Containerizar o projeto para padronizar o ambiente de desenvolvimento:
  - `Dockerfile` para a aplicação Django (Python 3.11 slim)
  - `docker-compose.yml` com serviços: `web` (Django) e `db` (PostgreSQL 15)
  - Atualizar `settings.py` para ler `DATABASE_URL` via decouple
  - Atualizar `.env.example` com as variáveis do Postgres
  - O comando `docker-compose up` deve subir o ambiente completo pronto para desenvolvimento.
- **Critério de aceitação:** `docker-compose up` sobe o ambiente completo sem erros.

---

## Contexto
- Projeto: **kanban gol** (KAN) — sistema de reservas aéreas em Django
- KAN-1 (setup inicial Django) já está **Concluído**
- Os 3 cards acima devem ser resolvidos e movidos para "Em análise"
