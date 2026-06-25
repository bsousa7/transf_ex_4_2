# Exercício 4.2 — MCP Server para API de Tarefas

MCP server que expõe duas *tools* sobre a API REST de TODO list construída no exercício 4.1.

## Arquitetura

```
Agente / LLM  ──MCP──▶  servidor_mcp.py  ──HTTP──▶  API 4.1 (localhost:8000)
```

## Tools disponíveis

| Tool | Assinatura | O que faz |
|------|-----------|-----------|
| `criar_tarefa` | `criar_tarefa(titulo: str) -> dict` | `POST /tarefas` — cria e devolve a tarefa |
| `listar_tarefas` | `listar_tarefas() -> list` | `GET /tarefas` — devolve todas as tarefas |

## Como rodar

**Terminal A** — suba a API do 4.1:
```bash
uvicorn app.main:app --port 8000
```

**Terminal B** — neste repo:
```bash
pip install -r requirements.txt
python cliente_teste.py
```

Saída esperada:
```json
{
  "tools": ["criar_tarefa", "listar_tarefas"],
  "criar_resultado": {"id": 1, "titulo": "tarefa via mcp", "concluida": false},
  "listar_resultado": [{"id": 1, "titulo": "tarefa via mcp", "concluida": false}]
}
```

## Reflexão

O MCP escondeu o protocolo HTTP: o agente só precisa saber que existe `criar_tarefa(titulo)` — o método, a URL, o formato do corpo e os códigos de status da API são completamente transparentes para quem chama.
