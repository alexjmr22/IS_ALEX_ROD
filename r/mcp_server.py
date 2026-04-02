"""
MCP Server using FastMCP
Exposes: one tool, one resource, one prompt
Run with: python mcp_server.py
"""

import json
from fastmcp import FastMCP
from sqlmodel import Session

from core_functions import (
    engine,
    core_get_equipa, core_create_equipa, core_update_equipa, core_delete_equipa, core_get_equipas,
    core_get_jogador, core_create_jogador, core_update_jogador, core_delete_jogador, core_get_jogadores,
)

mcp = FastMCP(name="SimpleAssistantServer")


# ─── TOOL ────────────────────────────────────────────────────────────────────
@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> str:
    """Calculate the Body Mass Index (BMI) given weight in kg and height in meters."""
    if height_m <= 0:
        return "Error: height must be greater than 0."
    bmi = weight_kg / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return f"BMI: {bmi:.2f} — Category: {category}"


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


# ─── RESOURCE ────────────────────────────────────────────────────────────────
@mcp.resource("info://app")
def get_app_info() -> str:
    """Returns general information about this MCP server / app."""
    return (
        "SimpleAssistantServer v1.0\n"
        "Purpose: Demo MCP server with a tool, resource, and prompt.\n"
        "Available tools: calculate_bmi, get_equipa\n"
        "Built with: FastMCP + Python\n"
    )


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
