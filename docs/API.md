# API de Voos — Documentacao

Base URL: `/api/`

---

## Endpoints

### GET /api/voos/

Lista todos os voos cadastrados. Suporta filtros opcionais via query params.

**Query Parameters**

| Parametro | Tipo   | Descricao                              | Exemplo        |
|-----------|--------|----------------------------------------|----------------|
| `origem`  | string | Codigo IATA do aeroporto de origem     | `?origem=GRU`  |
| `destino` | string | Codigo IATA do aeroporto de destino    | `?destino=CGH` |
| `data`    | date   | Data de partida no formato YYYY-MM-DD  | `?data=2026-03-30` |

**Exemplo de Requisicao**

```
GET /api/voos/?origem=GRU&destino=CGH
```

**Resposta 200 OK**

```json
[
    {
        "id": 1,
        "numero": "G31234",
        "origem": "GRU",
        "destino": "CGH",
        "data_partida": "2026-03-30T08:00:00-03:00",
        "data_chegada": "2026-03-30T08:35:00-03:00",
        "capacidade": 180,
        "status": "agendado"
    },
    {
        "id": 2,
        "numero": "G31235",
        "origem": "GRU",
        "destino": "CGH",
        "data_partida": "2026-03-30T14:00:00-03:00",
        "data_chegada": "2026-03-30T14:35:00-03:00",
        "capacidade": 180,
        "status": "agendado"
    }
]
```

---

### GET /api/voos/{id}/

Retorna o detalhe de um voo especifico pelo seu ID.

**Path Parameters**

| Parametro | Tipo    | Descricao       |
|-----------|---------|-----------------|
| `id`      | integer | ID do voo       |

**Exemplo de Requisicao**

```
GET /api/voos/1/
```

**Resposta 200 OK**

```json
{
    "id": 1,
    "numero": "G31234",
    "origem": "GRU",
    "destino": "CGH",
    "data_partida": "2026-03-30T08:00:00-03:00",
    "data_chegada": "2026-03-30T08:35:00-03:00",
    "capacidade": 180,
    "status": "agendado"
}
```

**Resposta 404 Not Found**

```json
{
    "detail": "Not found."
}
```

---

## Valores validos para `status`

| Valor       | Descricao  |
|-------------|------------|
| `agendado`  | Voo agendado e ativo |
| `cancelado` | Voo cancelado        |
| `concluido` | Voo ja realizado     |

---

## Exemplos de filtros combinados

```
GET /api/voos/?origem=GRU&destino=GIG&data=2026-04-01
GET /api/voos/?data=2026-03-30
GET /api/voos/?destino=BSB
```
