"""
MCP Server using FastMCP
Exposes: one tool, one resource, one prompt
Run with: python mcp_server.py
"""

import json
from fastmcp import FastMCP # type: ignore
from sqlmodel import Session

from core_functions import (
    engine,
    core_get_equipa, core_create_equipa, core_update_equipa, core_delete_equipa, core_get_equipas,
    core_get_jogador, core_create_jogador, core_update_jogador, core_delete_jogador, core_get_jogadores,
)

mcp = FastMCP(name="SimpleAssistantServer")


# ─── TOOL ────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_equipa(equipa_id: int) -> str:
    """Obtém os detalhes de uma equipa de futebol pelo seu ID, diretamente da base de dados."""
    with Session(engine) as session:
        try:
            e = core_get_equipa(session, equipa_id)
            return json.dumps({
                "id": e.id,
                "name": e.name,
                "estadio": e.estadio,
                "ano_fundacao": e.ano_fundacao,
                "orcamento_transferencias": e.orcamento_transferencias,
                "orcamento_salarios": e.orcamento_salarios,
            }, ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)})
@mcp.tool()
def get_jogadores(
    equipa_id: int | None = None,
    posicao: str | None = None,
    salario_min: float | None = None,
    salario_max: float | None = None,
    mercado_min: float | None = None,
    mercado_max: float | None = None,
) -> str:
    """Obtém a lista de todos os jogadores com filtro, diretamente da base de dados."""
    with Session(engine) as session:
        try:
            jogadores = core_get_jogadores(
                session,
                equipa_id=equipa_id,
                posicao=posicao,
                salario_min=salario_min,
                salario_max=salario_max,
                mercado_min=mercado_min,
                mercado_max=mercado_max,
            )
            return json.dumps([{
                "id": j.id,
                "name": j.name,
                "posicao": j.posicao,
                "numero_camisola": j.numero_camisola,
                "mercado": j.mercado,
                "salario": j.salario,
                "equipa_id": j.equipa_id,
            } for j in jogadores], ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)})
@mcp.tool()
def create_jogador(
    name: str,
    posicao: str,
    numero_camisola: int,
    mercado: float,
    salario: float,
    equipa_id: int,
) -> str:
    """Cria um novo jogador na base de dados."""
    with Session(engine) as session:
        try:
            jogador = core_create_jogador(session, name, posicao, numero_camisola, mercado, salario, equipa_id)
            return json.dumps({
                "id": jogador.id,
                "name": jogador.name,
                "posicao": jogador.posicao,
                "numero_camisola": jogador.numero_camisola,
                "mercado": jogador.mercado,
                "salario": jogador.salario,
                "equipa_id": jogador.equipa_id,
            }, ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)})
@mcp.tool()
def delete_jogador(jogador_id: int) -> str:
    """Elimina um jogador da base de dados pelo seu ID."""
    with Session(engine) as session:
        try:
            core_delete_jogador(session, jogador_id)
            return json.dumps({"message": f"Jogador com ID {jogador_id} eliminado com sucesso."})
        except ValueError as e:
            return json.dumps({"erro": str(e)})
@mcp.tool()
def update_jogador(
    jogador_id: int,
    name: str | None = None,
    posicao: str | None = None,
    numero_camisola: int | None = None,
    mercado: float | None = None,
    salario: float | None = None,
    equipa_id: int | None = None,
) -> str:
    """Atualiza os detalhes de um jogador de futebol pelo seu ID, diretamente da base de dados."""
    with Session(engine) as session:
        try:
            jogador = core_update_jogador(
                session,
                jogador_id,
                name=name,
                posicao=posicao,
                numero_camisola=numero_camisola,
                mercado=mercado,
                salario=salario,
                equipa_id=equipa_id
            )
            return json.dumps({
                "id": jogador.id,
                "name": jogador.name,
                "posicao": jogador.posicao,
                "numero_camisola": jogador.numero_camisola,
                "mercado": jogador.mercado,
                "salario": jogador.salario,
                "equipa_id": jogador.equipa_id,
            }, ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)})
@mcp.tool()
def get_jogador(jogador_id: int) -> str:
    """Obtém os detalhes de um jogador de futebol pelo seu ID, diretamente da base de dados."""
    with Session(engine) as session:
        try:
            j = core_get_jogador(session, jogador_id)
            return json.dumps({
                "id": j.id,
                "name": j.name,
                "posicao": j.posicao,
                "numero_camisola": j.numero_camisola,
                "mercado": j.mercado,
                "salario": j.salario,
                "equipa_id": j.equipa_id,
            }, ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)}
            )
@mcp.tool()
def get_jogadores_equipa(equipa_id: int) -> str:
    """Obtém a lista de jogadores de uma equipa, diretamente da base de dados."""
    with Session(engine) as session:
        try:
            jogadores = core_get_jogadores(session, equipa_id=equipa_id)
            return json.dumps([{
                "id": j.id,
                "name": j.name,
                "posicao": j.posicao,
                "numero_camisola": j.numero_camisola,
                "mercado": j.mercado,
                "salario": j.salario,
                "equipa_id": j.equipa_id,
            } for j in jogadores], ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)})
@mcp.tool()
def get_jogador_posicao(posicao: str) -> str:
    """Obtém a lista de jogadores por posição, diretamente da base de dados."""
    with Session(engine) as session:
        try:
            jogadores = core_get_jogadores(session, posicao=posicao)
            return json.dumps([{
                "id": j.id,
                "name": j.name,
                "posicao": j.posicao,
                "numero_camisola": j.numero_camisola,
                "mercado": j.mercado,
                "salario": j.salario,
                "equipa_id": j.equipa_id,
            } for j in jogadores], ensure_ascii=False, indent=2)
        except ValueError as e:
            return json.dumps({"erro": str(e)})


# ─── RESOURCE ────────────────────────────────────────────────────────────────
@mcp.resource("info://app")
def get_app_info() -> str:
    """Returns general information about this MCP server / app."""
    return (
        "SimpleAssistantServer v1.0\n"
        "Purpose: Demo MCP server with a tool, resource, and prompt.\n"
        "Available tools: get_equipa, get_equipas, get_jogador, get_jogadores, create_jogador, update_jogador, delete_jogador\n"
        "Built with: FastMCP + Python\n"
    )


@mcp.resource("db://schema")
def get_db_schema() -> str:
    """Returns the database schema with table definitions and relationships."""
    return (
        "Football Database Schema\n"
        "========================\n\n"
        "TABLE: Equipa\n"
        "  - id (int, PRIMARY KEY)\n"
        "  - name (str, UNIQUE, INDEXED)\n"
        "  - estadio (str, INDEXED)\n"
        "  - ano_fundacao (int, INDEXED)\n"
        "  - orcamento_transferencias (float, INDEXED)\n"
        "  - orcamento_salarios (float, INDEXED)\n\n"
        "TABLE: Jogador\n"
        "  - id (int, PRIMARY KEY)\n"
        "  - name (str, INDEXED)\n"
        "  - posicao (str, INDEXED) — GR, DC, LD, LE, MCD, MC, MAO, EXT, AV\n"
        "  - numero_camisola (int, INDEXED)\n"
        "  - mercado (float, INDEXED)\n"
        "  - salario (float, INDEXED)\n"
        "  - equipa_id (int, FOREIGN KEY → Equipa.id)\n\n"
        "RELATIONSHIPS:\n"
        "  - Jogador.equipa_id → Equipa.id (One-to-Many)\n"
        "  - Cannot delete Equipa if it has Jogadores\n"
    )


@mcp.resource("file://regras_mercado")
def get_regras_mercado() -> str:
    """Returns the file content with transfer market rules."""
    try:
        with open("regras_mercado.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Ficheiro regras_mercado.txt não encontrado."


# ─── PROMPT ──────────────────────────────────────────────────────────────────
@mcp.prompt()
def health_advisor_prompt(user_name: str = "User") -> str:
    """A system prompt that turns the LLM into a friendly health advisor."""
    return (
        f"You are a friendly and knowledgeable health advisor. "
        f"You are currently helping {user_name}. "
        "You can calculate BMI using the `calculate_bmi` tool. "
        "Always remind users that your advice is informational only and not a substitute "
        "for professional medical guidance. Keep your tone warm and encouraging."
    )


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="sse", host="127.0.0.1", port=8002)
