import asyncio
import ast
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _parse(content_item):
    """Extrai JSON do conteúdo retornado pelo MCP tool, tolerando variações do SDK."""
    text = content_item.text
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return ast.literal_eval(text)


def _parse_list(content):
    """Reconstrói lista do resultado MCP, independente de como o SDK a serializou.

    FastMCP pode devolver uma lista como um único TextContent com JSON array,
    ou como múltiplos TextContent — um por elemento.
    """
    if not content:
        return []
    if len(content) == 1:
        result = _parse(content[0])
        return result if isinstance(result, list) else [result]
    return [_parse(item) for item in content]


async def main() -> dict:
    params = StdioServerParameters(command="python", args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            return {
                "tools": nomes,
                "criar_resultado": _parse(criar.content[0]),
                "listar_resultado": _parse_list(listar.content),
            }


if __name__ == "__main__":
    try:
        print(json.dumps(asyncio.run(main())))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
