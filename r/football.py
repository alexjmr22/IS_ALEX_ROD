"""
football.py — Servidor REST (FastAPI)
As regras de negócio vivem em core_functions.py.
Este ficheiro é apenas o "casaco" HTTP: recebe pedidos, chama a core function e devolve o resultado.
"""

from fastapi import FastAPI, HTTPException, Query, Body
import uvicorn
from sqlmodel import Session
from typing import Optional

from core_functions import (
    Equipa, EquipaUpdate, Jogador, PosicaoEnum, engine,
    create_db_and_tables, seed_data,
    core_get_equipas, core_get_equipa, core_create_equipa, core_update_equipa, core_delete_equipa,
    core_get_jogadores, core_get_jogador, core_sign_jogador, core_renew_jogador, core_delete_jogador,
    core_get_jogadores_por_equipa, core_get_jogadores_por_posicao,
)

app = FastAPI()


# ─── HELPER ──────────────────────────────────────────────────────────────────

def _http(e: ValueError):
    """Converte um ValueError das core functions numa HTTPException 400."""
    raise HTTPException(status_code=400, detail=str(e))


# ─── EQUIPAS ─────────────────────────────────────────────────────────────────

@app.get("/equipas")
def get_equipas(
    name: Optional[str] = Query(None),
    estadio: Optional[str] = Query(None),
    ano_min: Optional[int] = Query(None),
    ano_max: Optional[int] = Query(None),
    orcamento_transferencias_min: Optional[float] = Query(None),
    orcamento_salarios_min: Optional[float] = Query(None),
):
    with Session(engine) as session:
        return core_get_equipas(session, name, estadio, ano_min, ano_max,
                                 orcamento_transferencias_min, orcamento_salarios_min)


@app.get("/equipas/{equipa_id}")
def get_equipa(equipa_id: int):
    with Session(engine) as session:
        try:
            e = core_get_equipa(session, equipa_id)
            return {"id": e.id, "name": e.name, "estadio": e.estadio,
                    "ano_fundacao": e.ano_fundacao,
                    "orcamento_transferencias": e.orcamento_transferencias,
                    "orcamento_salarios": e.orcamento_salarios}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))


@app.post("/equipas")
def create_equipa(
    name: str = Body(...),
    estadio: str = Body(...),
    ano_fundacao: int = Body(...),
    orcamento_transferencias: float = Body(...),
    orcamento_salarios: float = Body(...),
):
    with Session(engine) as session:
        try:
            return core_create_equipa(session, name, estadio, ano_fundacao,
                                       orcamento_transferencias, orcamento_salarios)
        except ValueError as e:
            _http(e)


@app.put("/equipas/{equipa_id}")
def update_equipa(equipa_id: int, equipa_data: EquipaUpdate):
    with Session(engine) as session:
        try:
            return core_update_equipa(session, equipa_id, equipa_data.name, equipa_data.estadio,
                                       equipa_data.ano_fundacao, equipa_data.orcamento_transferencias,
                                       equipa_data.orcamento_salarios)
        except ValueError as e:
            _http(e)


@app.delete("/equipas/{equipa_id}")
def delete_equipa(equipa_id: int):
    with Session(engine) as session:
        try:
            return core_delete_equipa(session, equipa_id)
        except ValueError as e:
            _http(e)


# ─── JOGADORES ───────────────────────────────────────────────────────────────

@app.get("/jogadores")
def get_jogadores(
    equipa_id: Optional[int] = Query(None),
    posicao: Optional[str] = Query(None),
    salario_min: Optional[float] = Query(None),
    salario_max: Optional[float] = Query(None),
    mercado_min: Optional[float] = Query(None),
    mercado_max: Optional[float] = Query(None),
):
    with Session(engine) as session:
        return core_get_jogadores(session, equipa_id, posicao,
                                   salario_min, salario_max, mercado_min, mercado_max)


@app.get("/jogadores/{jogador_id}")
def get_jogador(jogador_id: int):
    with Session(engine) as session:
        try:
            return core_get_jogador(session, jogador_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))


@app.post("/jogadores")
def create_jogador(
    name: str = Body(...),
    posicao: PosicaoEnum = Body(...),
    numero_camisola: int = Body(...),
    mercado: float = Body(...),
    salario: float = Body(...),
    equipa_id: int = Body(...),
):
    with Session(engine) as session:
        try:
            return core_sign_jogador(session, name, posicao, numero_camisola,
                                        mercado, salario, equipa_id)
        except ValueError as e:
            _http(e)


@app.put("/jogadores/{jogador_id}")
def update_jogador(
    jogador_id: int,
    posicao: Optional[PosicaoEnum] = Body(None),
    numero_camisola: Optional[int] = Body(None),
    mercado: Optional[float] = Body(None),
    salario: Optional[float] = Body(None),
    equipa_id: Optional[int] = Body(None),
):
    with Session(engine) as session:
        try:
            return core_renew_jogador(session, jogador_id, posicao=posicao,
                                        numero_camisola=numero_camisola,
                                        mercado=mercado, salario=salario,
                                        equipa_id=equipa_id)
        except ValueError as e:
            _http(e)


@app.delete("/jogadores/{jogador_id}")
def delete_jogador(jogador_id: int):
    with Session(engine) as session:
        try:
            return core_delete_jogador(session, jogador_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))


# ─── AUXILIARES ──────────────────────────────────────────────────────────────

@app.get("/jogadores/equipa/{equipa_id}")
def get_jogadores_por_equipa(equipa_id: int):
    with Session(engine) as session:
        try:
            return core_get_jogadores_por_equipa(session, equipa_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))


@app.get("/jogadores/posicao/{posicao}")
def get_jogadores_por_posicao(posicao: str):
    with Session(engine) as session:
        return core_get_jogadores_por_posicao(session, posicao)


# ─── STARTUP ─────────────────────────────────────────────────────────────────

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_data()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
