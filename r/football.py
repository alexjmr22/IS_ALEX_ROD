from fastapi import FastAPI, HTTPException, Query, Body
import uvicorn
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, Literal

PosicaoEnum = Literal["GR", "DC", "LD", "LE", "MCD", "MC", "MAO", "EXT", "AV"]

class Equipa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    estadio: str = Field(index=True)
    ano_fundacao: int = Field(index=True)
    orcamento_transferencias: float = Field(index=True)
    orcamento_salarios: float = Field(index=True)


class EquipaUpdate(SQLModel):
    name: str
    estadio: str
    ano_fundacao: int
    orcamento_transferencias: float
    orcamento_salarios: float


class Jogador(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    posicao: str = Field(index=True)
    numero_camisola: int = Field(index=True)
    mercado: float = Field(index=True)
    salario: float = Field(index=True)
    equipa_id: int = Field(default=None, foreign_key="equipa.id")

sqlite_file_name = "football.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def seed_data():
    with Session(engine) as session:
        if session.exec(select(Equipa)).first():
            return
 
        equipas = [
            Equipa(name="Sport Lisboa e Benfica", estadio="Estádio da Luz",             ano_fundacao=1904, orcamento_transferencias=116.0, orcamento_salarios=120.0),
            Equipa(name="Sporting CP",            estadio="Estádio José Alvalade",       ano_fundacao=1906, orcamento_transferencias=71.0,  orcamento_salarios=115.0),
            Equipa(name="FC Porto",               estadio="Estádio do Dragão",           ano_fundacao=1893, orcamento_transferencias=90.0,  orcamento_salarios=110.0),
            Equipa(name="Vitória SC",             estadio="Estádio D. Afonso Henriques", ano_fundacao=1922, orcamento_transferencias=4.0,   orcamento_salarios=12.0),
        ]
        for e in equipas:
            session.add(e)
        session.commit()
        for e in equipas:
            session.refresh(e)
 
        jogadores = [
            # ── Benfica ──────────────────────────────
            Jogador(name="Anatoliy Trubin",      posicao="GR",  numero_camisola=1,  mercado=25.0, salario=3.5, equipa_id=equipas[0].id),
            Jogador(name="Nicolás Otamendi",     posicao="DC",  numero_camisola=30, mercado=5.0,  salario=3.8, equipa_id=equipas[0].id),
            Jogador(name="Tomás Araújo",         posicao="DC",  numero_camisola=44, mercado=30.0, salario=2.5, equipa_id=equipas[0].id),
            Jogador(name="António Silva",        posicao="DC",  numero_camisola=4,  mercado=55.0, salario=3.2, equipa_id=equipas[0].id),
            Jogador(name="Amar Dedić",           posicao="LD",  numero_camisola=17, mercado=18.0, salario=2.0, equipa_id=equipas[0].id),
            Jogador(name="Leandro Barreiro",     posicao="MC",  numero_camisola=18, mercado=22.0, salario=2.8, equipa_id=equipas[0].id),
            Jogador(name="Richard Ríos",         posicao="MC",  numero_camisola=20, mercado=28.0, salario=3.0, equipa_id=equipas[0].id),
            Jogador(name="Heorhiy Sudakov",      posicao="MAO", numero_camisola=10, mercado=35.0, salario=4.0, equipa_id=equipas[0].id),
            Jogador(name="Andreas Schjelderup",  posicao="EXT", numero_camisola=21, mercado=25.0, salario=2.5, equipa_id=equipas[0].id),
            Jogador(name="Vangelis Pavlidis",    posicao="AV",  numero_camisola=14, mercado=30.0, salario=3.5, equipa_id=equipas[0].id),
 
            # ── Sporting CP ─────────────────────────────
            Jogador(name="Rui Silva",            posicao="GR",  numero_camisola=1,  mercado=10.0, salario=2.0, equipa_id=equipas[1].id),
            Jogador(name="Gonçalo Inácio",       posicao="DC",  numero_camisola=25, mercado=45.0, salario=3.5, equipa_id=equipas[1].id),
            Jogador(name="Ousmane Diomande",     posicao="DC",  numero_camisola=26, mercado=40.0, salario=3.0, equipa_id=equipas[1].id),
            Jogador(name="Morten Hjulmand",      posicao="MCD", numero_camisola=42, mercado=30.0, salario=3.2, equipa_id=equipas[1].id),
            Jogador(name="Pedro Gonçalves",      posicao="MAO", numero_camisola=8,  mercado=40.0, salario=4.0, equipa_id=equipas[1].id),
            Jogador(name="Geovany Quenda",       posicao="EXT", numero_camisola=7,  mercado=35.0, salario=2.2, equipa_id=equipas[1].id),
            Jogador(name="Francisco Trincão",    posicao="EXT", numero_camisola=17, mercado=20.0, salario=3.0, equipa_id=equipas[1].id),
            Jogador(name="Luis Suárez",          posicao="AV",  numero_camisola=97, mercado=22.0, salario=2.8, equipa_id=equipas[1].id),
            Jogador(name="Fotis Ioannidis",      posicao="AV",  numero_camisola=89, mercado=22.0, salario=2.5, equipa_id=equipas[1].id),
            Jogador(name="Zeno Debast",          posicao="DC",  numero_camisola=6,  mercado=28.0, salario=2.8, equipa_id=equipas[1].id),
 
            # ── FC Porto ─────────────────────────
            Jogador(name="Diogo Costa",          posicao="GR",  numero_camisola=99, mercado=40.0, salario=4.0, equipa_id=equipas[2].id),
            Jogador(name="Thiago Silva",         posicao="DC",  numero_camisola=3,  mercado=2.0,  salario=2.5, equipa_id=equipas[2].id),
            Jogador(name="Nehuén Pérez",         posicao="DC",  numero_camisola=18, mercado=18.0, salario=2.2, equipa_id=equipas[2].id),
            Jogador(name="Alan Varela",          posicao="MCD", numero_camisola=22, mercado=22.0, salario=2.8, equipa_id=equipas[2].id),
            Jogador(name="Gabri Veiga",          posicao="MAO", numero_camisola=10, mercado=30.0, salario=3.5, equipa_id=equipas[2].id),
            Jogador(name="Seko Fofana",          posicao="MC",  numero_camisola=42, mercado=18.0, salario=3.0, equipa_id=equipas[2].id),
            Jogador(name="Pepê",                 posicao="EXT", numero_camisola=11, mercado=22.0, salario=2.5, equipa_id=equipas[2].id),
            Jogador(name="Samu Aghehowa",        posicao="AV",  numero_camisola=9,  mercado=50.0, salario=3.8, equipa_id=equipas[2].id),
            Jogador(name="Borja Sainz",          posicao="EXT", numero_camisola=17, mercado=23.0, salario=2.5, equipa_id=equipas[2].id),
            Jogador(name="Oskar Pietuszewski",   posicao="AV",  numero_camisola=77, mercado=12.0, salario=1.8, equipa_id=equipas[2].id),
 
            # ── Vitória SC ───────────────────────            
            Jogador(name="Charles",              posicao="GR",  numero_camisola=1,  mercado=1.5,  salario=0.4, equipa_id=equipas[3].id),
            Jogador(name="Miguel Maga",          posicao="LD",  numero_camisola=2,  mercado=3.0,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Oscar Rivas",          posicao="DC",  numero_camisola=5,  mercado=2.5,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Rodrigo Abascal",      posicao="DC",  numero_camisola=3,  mercado=1.5,  salario=0.4, equipa_id=equipas[3].id),
            Jogador(name="Beni Mukendi",         posicao="MCD", numero_camisola=6,  mercado=4.0,  salario=0.7, equipa_id=equipas[3].id),
            Jogador(name="Diogo Sousa",         posicao="MC",  numero_camisola=8,  mercado=3.5,  salario=0.6, equipa_id=equipas[3].id),
            Jogador(name="Gustavo Silva",          posicao="MC",  numero_camisola=20, mercado=2.0,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Telmo Arcanjo",        posicao="EXT", numero_camisola=11, mercado=4.0,  salario=0.7, equipa_id=equipas[3].id),
            Jogador(name="Oumar Camará",         posicao="EXT", numero_camisola=7,  mercado=3.0,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Nélson Oliveira",      posicao="AV",  numero_camisola=9,  mercado=1.5,  salario=0.8, equipa_id=equipas[3].id),
        ]
        for j in jogadores:
            session.add(j)
        session.commit()

app = FastAPI()

# ===== ENDPOINTS DAS EQUIPAS =====

@app.get("/equipas")
def get_equipas(
    name: Optional[str] = Query(None, description="Filtrar por nome"),
    estadio: Optional[str] = Query(None, description="Filtrar por estádio"),
    ano_min: Optional[int] = Query(None, description="Ano de fundação mínimo"),
    ano_max: Optional[int] = Query(None, description="Ano de fundação máximo"),
    orcamento_transferencias_min: Optional[float] = Query(None, description="Orçamento de transferências mínimo"),
    orcamento_salarios_min: Optional[float] = Query(None, description="Orçamento de salários mínimo"),
):
    """Listar todas as equipas com filtros opcionais"""
    with Session(engine) as session:
        query = select(Equipa)

        if name:
            query = query.where(col(Equipa.name).contains(name))
        if estadio:
            query = query.where(col(Equipa.estadio).contains(estadio))
        if ano_min:
            query = query.where(Equipa.ano_fundacao >= ano_min)
        if ano_max:
            query = query.where(Equipa.ano_fundacao <= ano_max)
        if orcamento_transferencias_min:
            query = query.where(Equipa.orcamento_transferencias >= orcamento_transferencias_min)
        if orcamento_salarios_min:
            query = query.where(Equipa.orcamento_salarios >= orcamento_salarios_min)

        equipas = session.exec(query).all()
        return equipas


@app.get("/equipas/{equipa_id}")
def get_equipa(equipa_id: int):
    """Obter uma equipa específica por ID"""
    with Session(engine) as session:
        equipa = session.get(Equipa, equipa_id)
        if not equipa:
            raise HTTPException(status_code=404, detail="Equipa não encontrada")
        return equipa


@app.post("/equipas")
def create_equipa(
    name: str = Body(...),
    estadio: str = Body(...),
    ano_fundacao: int = Body(...),
    orcamento_transferencias: float = Body(...),
    orcamento_salarios: float = Body(...),
):
    """Criar uma nova equipa"""
    # Validações
    if not name.strip():
        raise HTTPException(status_code=400, detail="O nome da equipa não pode estar vazio")
    if ano_fundacao < 1800 or ano_fundacao > 2025:
        raise HTTPException(status_code=400, detail="Ano de fundação inválido")
    if orcamento_transferencias < 0:
        raise HTTPException(status_code=400, detail="Orçamento de transferências não pode ser negativo")
    if orcamento_salarios < 0:
        raise HTTPException(status_code=400, detail="Orçamento de salários não pode ser negativo")

    with Session(engine) as session:
        # Verificar se já existe uma equipa com o mesmo nome
        existing = session.exec(select(Equipa).where(Equipa.name == name)).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Já existe uma equipa com o nome '{name}'")

        equipa = Equipa(
            name=name,
            estadio=estadio,
            ano_fundacao=ano_fundacao,
            orcamento_transferencias=orcamento_transferencias,
            orcamento_salarios=orcamento_salarios,
        )
        session.add(equipa)
        session.commit()
        session.refresh(equipa)
        return equipa


@app.put("/equipas/{equipa_id}")
def update_equipa(equipa_id: int, equipa_data: EquipaUpdate):
    """Atualizar uma equipa existente"""
    with Session(engine) as session:
        equipa = session.get(Equipa, equipa_id)
        if not equipa:
            raise HTTPException(status_code=404, detail="Equipa não encontrada")

        # Verificar duplicado de nome (excluindo a própria equipa)
        if equipa_data.name != equipa.name:
            existing = session.exec(
                select(Equipa).where(Equipa.name == equipa_data.name)
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail=f"Já existe uma equipa com o nome '{equipa_data.name}'")

        if orcamento_transferencias := equipa_data.orcamento_transferencias:
            if orcamento_transferencias < 0:
                raise HTTPException(status_code=400, detail="Orçamento de transferências não pode ser negativo")
        if orcamento_salarios := equipa_data.orcamento_salarios:
            if orcamento_salarios < 0:
                raise HTTPException(status_code=400, detail="Orçamento de salários não pode ser negativo")

        equipa.name = equipa_data.name
        equipa.estadio = equipa_data.estadio
        equipa.ano_fundacao = equipa_data.ano_fundacao
        equipa.orcamento_transferencias = equipa_data.orcamento_transferencias
        equipa.orcamento_salarios = equipa_data.orcamento_salarios

        session.add(equipa)
        session.commit()
        session.refresh(equipa)
        return equipa


@app.delete("/equipas/{equipa_id}")
def delete_equipa(equipa_id: int):
    """Eliminar uma equipa"""
    with Session(engine) as session:
        equipa = session.get(Equipa, equipa_id)
        if not equipa:
            raise HTTPException(status_code=404, detail="Equipa não encontrada")

        # Verificar se ainda existem jogadores nesta equipa
        jogadores = session.exec(
            select(Jogador).where(Jogador.equipa_id == equipa_id)
        ).all()
        if jogadores:
            raise HTTPException(
                status_code=400,
                detail=f"Não é possível eliminar a equipa '{equipa.name}' porque ainda tem {len(jogadores)} jogador(es) associado(s)"
            )

        session.delete(equipa)
        session.commit()
        return {"message": f"Equipa '{equipa.name}' eliminada com sucesso"}


# ===== ENDPOINTS DOS JOGADORES =====

@app.get("/jogadores")
def get_jogadores(
    equipa_id: Optional[int] = Query(None, description="Filtrar por ID da equipa"),
    posicao: Optional[str] = Query(None, description="Filtrar por posição"),
    salario_min: Optional[float] = Query(None, description="Salário mínimo"),
    salario_max: Optional[float] = Query(None, description="Salário máximo"),
    mercado_min: Optional[float] = Query(None, description="Valor de mercado mínimo"),
    mercado_max: Optional[float] = Query(None, description="Valor de mercado máximo")
):
    """Listar todos os jogadores com filtros opcionais"""
    with Session(engine) as session:
        query = select(Jogador)

        if equipa_id:
            query = query.where(Jogador.equipa_id == equipa_id)
        if posicao:
            query = query.where(Jogador.posicao == posicao)
        if salario_min:
            query = query.where(Jogador.salario >= salario_min)
        if salario_max:
            query = query.where(Jogador.salario <= salario_max)
        if mercado_min:
            query = query.where(Jogador.mercado >= mercado_min)
        if mercado_max:
            query = query.where(Jogador.mercado <= mercado_max)

        jogadores = session.exec(query).all()
        return jogadores


@app.get("/jogadores/{jogador_id}")
def get_jogador(jogador_id: int):
    """Obter um jogador específico por ID"""
    with Session(engine) as session:
        jogador = session.get(Jogador, jogador_id)
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        return jogador


@app.post("/jogadores")
def create_jogador(
    name: str = Body(...),
    posicao: PosicaoEnum = Body(...),
    numero_camisola: int = Body(...),
    mercado: float = Body(...),
    salario: float = Body(...),
    equipa_id: int = Body(...)
):
    """Criar um novo jogador"""
    jogador = Jogador(
        name=name,
        posicao=posicao,
        numero_camisola=numero_camisola,
        mercado=mercado,
        salario=salario,
        equipa_id=equipa_id
    )
    with Session(engine) as session:
        # Verificar se a equipa existe
        if jogador.equipa_id:
            equipa = session.get(Equipa, jogador.equipa_id)
            if not equipa:
                raise HTTPException(status_code=400, detail="Equipa não encontrada")

            # Verificar orçamentos da equipa
            jogadores_equipa = session.exec(
                select(Jogador).where(Jogador.equipa_id == jogador.equipa_id)
            ).all()
            
            salario_total_atual = sum(j.salario for j in jogadores_equipa)
            if salario_total_atual + jogador.salario > equipa.orcamento_salarios:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Orçamento de salários insuficiente. A equipa tem disponível: {equipa.orcamento_salarios - salario_total_atual:.2f} (necessário: {jogador.salario})"
                )
            
            if jogador.mercado > equipa.orcamento_transferencias:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Orçamento de transferências insuficiente. A equipa tem disponível: {equipa.orcamento_transferencias:.2f} (necessário: {jogador.mercado})"
                )
            
            # Deduz o valor da transferência ao orçamento da equipa
            equipa.orcamento_transferencias -= jogador.mercado
            session.add(equipa)

        # Verificar se o número da camisola já está ocupado na equipa
        existing_player = session.exec(
            select(Jogador).where(
                Jogador.numero_camisola == jogador.numero_camisola,
                Jogador.equipa_id == jogador.equipa_id
            )
        ).first()

        if existing_player:
            raise HTTPException(
                status_code=400,
                detail=f"Número de camisola {jogador.numero_camisola} já está ocupado nesta equipa"
            )

        session.add(jogador)
        session.commit()
        session.refresh(jogador)
        return jogador


@app.put("/jogadores/{jogador_id}")
def update_jogador(
    jogador_id: int,
    posicao: Optional[PosicaoEnum] = Body(None),
    numero_camisola: Optional[int] = Body(None),
    mercado: Optional[float] = Body(None),
    salario: Optional[float] = Body(None),
    equipa_id: Optional[int] = Body(None)
):
    """Atualizar um jogador existente"""
    with Session(engine) as session:
        jogador = session.get(Jogador, jogador_id)
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")

        # Se os campos não forem fornecidos (None), mantém os dados atuais
        posicao = posicao if posicao is not None else jogador.posicao
        numero_camisola = numero_camisola if numero_camisola is not None else jogador.numero_camisola
        mercado = mercado if mercado is not None else jogador.mercado
        salario = salario if salario is not None else jogador.salario
        equipa_id = equipa_id if equipa_id is not None else jogador.equipa_id

        # Verificar se a nova equipa existe (se fornecida)
        if equipa_id:
            equipa = session.get(Equipa, equipa_id)
            if not equipa:
                raise HTTPException(status_code=400, detail="Equipa não encontrada")

            # Verificar orçamento se houver mudança de equipa ou de salário
            if (equipa_id != jogador.equipa_id) or (salario != jogador.salario):
                jogadores_equipa = session.exec(
                    select(Jogador).where(
                        Jogador.equipa_id == equipa_id,
                        Jogador.id != jogador_id
                    )
                ).all()
                salario_total_atual = sum(j.salario for j in jogadores_equipa)
                
                if salario_total_atual + salario > equipa.orcamento_salarios:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Orçamento de salários insuficiente. A equipa tem disponível: {equipa.orcamento_salarios - salario_total_atual:.2f} (necessário: {salario})"
                    )
            
            # Se for uma transferência entre equipas, validar e deduzir o orçamento de transferências
            if equipa_id != jogador.equipa_id:
                if mercado > equipa.orcamento_transferencias:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Orçamento de transferências insuficiente na nova equipa. Disponível: {equipa.orcamento_transferencias:.2f} (necessário: {mercado})"
                    )
                
                equipa.orcamento_transferencias -= mercado
                session.add(equipa)

        # Verificar conflito de número de camisola (se alterado)
        if (numero_camisola != jogador.numero_camisola or
            equipa_id != jogador.equipa_id):
            existing_player = session.exec(
                select(Jogador).where(
                    Jogador.numero_camisola == numero_camisola,
                    Jogador.equipa_id == equipa_id,
                    Jogador.id != jogador_id
                )
            ).first()

            if existing_player:
                raise HTTPException(
                    status_code=400,
                    detail=f"Número de camisola {numero_camisola} já está ocupado nesta equipa"
                )

        # Atualizar dados
        jogador.posicao = posicao
        jogador.numero_camisola = numero_camisola
        jogador.mercado = mercado
        jogador.salario = salario
        jogador.equipa_id = equipa_id

        session.add(jogador)
        session.commit()
        session.refresh(jogador)
        return jogador


@app.delete("/jogadores/{jogador_id}")
def delete_jogador(jogador_id: int):
    """Eliminar um jogador"""
    with Session(engine) as session:
        jogador = session.get(Jogador, jogador_id)
        if not jogador:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")

        session.delete(jogador)
        session.commit()
        return {"message": f"Jogador {jogador.name} eliminado com sucesso"}


# ===== ENDPOINTS AUXILIARES =====

@app.get("/jogadores/equipa/{equipa_id}")
def get_jogadores_por_equipa(equipa_id: int):
    """Obter todos os jogadores de uma equipa específica"""
    with Session(engine) as session:
        # Verificar se a equipa existe
        equipa = session.get(Equipa, equipa_id)
        if not equipa:
            raise HTTPException(status_code=404, detail="Equipa não encontrada")

        jogadores = session.exec(
            select(Jogador).where(Jogador.equipa_id == equipa_id)
        ).all()
        return {
            "equipa": equipa.name,
            "jogadores": jogadores
        }


@app.get("/jogadores/posicao/{posicao}")
def get_jogadores_por_posicao(posicao: str):
    """Obter todos os jogadores de uma posição específica"""
    with Session(engine) as session:
        jogadores = session.exec(
            select(Jogador).where(Jogador.posicao == posicao)
        ).all()
        return {
            "posicao": posicao,
            "jogadores": jogadores
        }


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_data() 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
