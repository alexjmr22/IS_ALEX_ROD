"""
core_functions.py
Lógica de negócio central partilhada entre REST (football.py) e MCP (mcp_server.py).
Raises ValueError em caso de violação de regras — cada interface trata o erro à sua maneira.
"""

from typing import Literal, Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select, col

# ─── ENUMS & MODELS ──────────────────────────────────────────────────────────

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


# ─── DATABASE SETUP ───────────────────────────────────────────────────────────

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

            # ── Sporting CP ──────────────────────────────
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

            # ── FC Porto ─────────────────────────────────
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

            # ── Vitória SC ───────────────────────────────
            Jogador(name="Charles",              posicao="GR",  numero_camisola=1,  mercado=1.5,  salario=0.4, equipa_id=equipas[3].id),
            Jogador(name="Miguel Maga",          posicao="LD",  numero_camisola=2,  mercado=3.0,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Oscar Rivas",          posicao="DC",  numero_camisola=5,  mercado=2.5,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Rodrigo Abascal",      posicao="DC",  numero_camisola=3,  mercado=1.5,  salario=0.4, equipa_id=equipas[3].id),
            Jogador(name="Beni Mukendi",         posicao="MCD", numero_camisola=6,  mercado=4.0,  salario=0.7, equipa_id=equipas[3].id),
            Jogador(name="Diogo Sousa",          posicao="MC",  numero_camisola=8,  mercado=3.5,  salario=0.6, equipa_id=equipas[3].id),
            Jogador(name="Gustavo Silva",        posicao="MC",  numero_camisola=20, mercado=2.0,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Telmo Arcanjo",        posicao="EXT", numero_camisola=11, mercado=4.0,  salario=0.7, equipa_id=equipas[3].id),
            Jogador(name="Oumar Camará",         posicao="EXT", numero_camisola=7,  mercado=3.0,  salario=0.5, equipa_id=equipas[3].id),
            Jogador(name="Nélson Oliveira",      posicao="AV",  numero_camisola=9,  mercado=1.5,  salario=0.8, equipa_id=equipas[3].id),
        ]
        for j in jogadores:
            session.add(j)
        session.commit()


# ─── CORE FUNCTIONS — EQUIPAS ────────────────────────────────────────────────

def core_get_equipas(session: Session, name: Optional[str] = None, estadio: Optional[str] = None,
                     ano_min: Optional[int] = None, ano_max: Optional[int] = None,
                     orcamento_transferencias_min: Optional[float] = None,
                     orcamento_salarios_min: Optional[float] = None):
    """Listar equipas com filtros opcionais."""
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
    return session.exec(query).all()


def core_get_equipa(session: Session, equipa_id: int) -> Equipa:
    """Obter uma equipa por ID. Raises ValueError se não encontrada."""
    equipa = session.get(Equipa, equipa_id)
    if not equipa:
        raise ValueError(f"Equipa com ID {equipa_id} não encontrada.")
    return equipa


def core_create_equipa(session: Session, name: str, estadio: str, ano_fundacao: int,
                        orcamento_transferencias: float, orcamento_salarios: float) -> Equipa:
    """Criar uma nova equipa com validações. Raises ValueError se regras falharem."""
    if not name.strip():
        raise ValueError("O nome da equipa não pode estar vazio.")
    if ano_fundacao < 1800 or ano_fundacao > 2025:
        raise ValueError("Ano de fundação inválido (deve estar entre 1800 e 2025).")
    if orcamento_transferencias < 0:
        raise ValueError("Orçamento de transferências não pode ser negativo.")
    if orcamento_salarios < 0:
        raise ValueError("Orçamento de salários não pode ser negativo.")

    existing = session.exec(select(Equipa).where(Equipa.name == name)).first()
    if existing:
        raise ValueError(f"Já existe uma equipa com o nome '{name}'.")

    equipa = Equipa(name=name, estadio=estadio, ano_fundacao=ano_fundacao,
                    orcamento_transferencias=orcamento_transferencias,
                    orcamento_salarios=orcamento_salarios)
    session.add(equipa)
    session.commit()
    session.refresh(equipa)
    return equipa


def core_update_equipa(session: Session, equipa_id: int, name: str, estadio: str,
                        ano_fundacao: int, orcamento_transferencias: float,
                        orcamento_salarios: float) -> Equipa:
    """Atualizar uma equipa existente. Raises ValueError se regras falharem."""
    equipa = session.get(Equipa, equipa_id)
    if not equipa:
        raise ValueError(f"Equipa com ID {equipa_id} não encontrada.")

    if name != equipa.name:
        existing = session.exec(select(Equipa).where(Equipa.name == name)).first()
        if existing:
            raise ValueError(f"Já existe uma equipa com o nome '{name}'.")

    if orcamento_transferencias < 0:
        raise ValueError("Orçamento de transferências não pode ser negativo.")
    if orcamento_salarios < 0:
        raise ValueError("Orçamento de salários não pode ser negativo.")

    equipa.name = name
    equipa.estadio = estadio
    equipa.ano_fundacao = ano_fundacao
    equipa.orcamento_transferencias = orcamento_transferencias
    equipa.orcamento_salarios = orcamento_salarios

    session.add(equipa)
    session.commit()
    session.refresh(equipa)
    return equipa


def core_delete_equipa(session: Session, equipa_id: int) -> dict:
    """Eliminar uma equipa. Raises ValueError se tiver jogadores associados."""
    equipa = session.get(Equipa, equipa_id)
    if not equipa:
        raise ValueError(f"Equipa com ID {equipa_id} não encontrada.")

    jogadores = session.exec(select(Jogador).where(Jogador.equipa_id == equipa_id)).all()
    if jogadores:
        raise ValueError(
            f"Não é possível eliminar '{equipa.name}' porque ainda tem {len(jogadores)} jogador(es) associado(s)."
        )

    nome = equipa.name
    session.delete(equipa)
    session.commit()
    return {"message": f"Equipa '{nome}' eliminada com sucesso."}


# ─── CORE FUNCTIONS — JOGADORES ──────────────────────────────────────────────

def core_get_jogadores(session: Session, equipa_id: Optional[int] = None,
                        name: Optional[str] = None, posicao: Optional[str] = None,
                        salario_min: Optional[float] = None,
                        salario_max: Optional[float] = None, mercado_min: Optional[float] = None,
                        mercado_max: Optional[float] = None):
    """Listar jogadores com filtros opcionais."""
    query = select(Jogador)
    if equipa_id:
        query = query.where(Jogador.equipa_id == equipa_id)
    if name:
        query = query.where(col(Jogador.name).contains(name))
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
    return session.exec(query).all()


def core_get_jogador(session: Session, jogador_id: int) -> Jogador:
    """Obter um jogador por ID. Raises ValueError se não encontrado."""
    jogador = session.get(Jogador, jogador_id)
    if not jogador:
        raise ValueError(f"Jogador com ID {jogador_id} não encontrado.")
    return jogador


def core_sign_jogador(session: Session, name: str, posicao: str, numero_camisola: int,
                         mercado: float, salario: float, equipa_id: int) -> Jogador:
    """Criar um jogador com validações de orçamento e camisola. Raises ValueError se regras falharem."""
    equipa = session.get(Equipa, equipa_id)
    if not equipa:
        raise ValueError("Equipa não encontrada.")

    jogadores_equipa = session.exec(select(Jogador).where(Jogador.equipa_id == equipa_id)).all()
    salario_total = sum(j.salario for j in jogadores_equipa)
    if salario_total + salario > equipa.orcamento_salarios:
        raise ValueError(
            f"Orçamento de salários insuficiente. Disponível: {equipa.orcamento_salarios - salario_total:.2f}M€ (necessário: {salario}M€)."
        )
    if mercado > equipa.orcamento_transferencias:
        raise ValueError(
            f"Orçamento de transferências insuficiente. Disponível: {equipa.orcamento_transferencias:.2f}M€ (necessário: {mercado}M€)."
        )

    existing = session.exec(
        select(Jogador).where(Jogador.numero_camisola == numero_camisola, Jogador.equipa_id == equipa_id)
    ).first()
    if existing:
        raise ValueError(f"Número de camisola {numero_camisola} já está ocupado nesta equipa.")

    equipa.orcamento_transferencias -= mercado
    session.add(equipa)

    jogador = Jogador(name=name, posicao=posicao, numero_camisola=numero_camisola,
                       mercado=mercado, salario=salario, equipa_id=equipa_id)
    session.add(jogador)
    session.commit()
    session.refresh(jogador)
    return jogador


def core_renew_jogador(session: Session, jogador_id: int, posicao: Optional[str] = None,
                         numero_camisola: Optional[int] = None, mercado: Optional[float] = None,
                         salario: Optional[float] = None, equipa_id: Optional[int] = None) -> Jogador:
    """Atualizar um jogador. Raises ValueError se regras falharem."""
    jogador = session.get(Jogador, jogador_id)
    if not jogador:
        raise ValueError(f"Jogador com ID {jogador_id} não encontrado.")

    posicao        = posicao        if posicao        is not None else jogador.posicao
    numero_camisola = numero_camisola if numero_camisola is not None else jogador.numero_camisola
    mercado        = mercado        if mercado        is not None else jogador.mercado
    salario        = salario        if salario        is not None else jogador.salario
    equipa_id      = equipa_id      if equipa_id      is not None else jogador.equipa_id

    if equipa_id:
        equipa = session.get(Equipa, equipa_id)
        if not equipa:
            raise ValueError("Equipa não encontrada.")

        if equipa_id != jogador.equipa_id or salario != jogador.salario:
            outros = session.exec(
                select(Jogador).where(Jogador.equipa_id == equipa_id, Jogador.id != jogador_id)
            ).all()
            salario_total = sum(j.salario for j in outros)
            if salario_total + salario > equipa.orcamento_salarios:
                raise ValueError(
                    f"Orçamento de salários insuficiente. Disponível: {equipa.orcamento_salarios - salario_total:.2f}M€ (necessário: {salario}M€)."
                )

        if equipa_id != jogador.equipa_id:
            if mercado > equipa.orcamento_transferencias:
                raise ValueError(
                    f"Orçamento de transferências insuficiente. Disponível: {equipa.orcamento_transferencias:.2f}M€ (necessário: {mercado}M€)."
                )
            equipa.orcamento_transferencias -= mercado
            session.add(equipa)

    if numero_camisola != jogador.numero_camisola or equipa_id != jogador.equipa_id:
        existing = session.exec(
            select(Jogador).where(
                Jogador.numero_camisola == numero_camisola,
                Jogador.equipa_id == equipa_id,
                Jogador.id != jogador_id
            )
        ).first()
        if existing:
            raise ValueError(f"Número de camisola {numero_camisola} já está ocupado nesta equipa.")

    jogador.posicao = posicao
    jogador.numero_camisola = numero_camisola
    jogador.mercado = mercado
    jogador.salario = salario
    jogador.equipa_id = equipa_id

    session.add(jogador)
    session.commit()
    session.refresh(jogador)
    return jogador


def core_delete_jogador(session: Session, jogador_id: int) -> dict:
    """Eliminar um jogador. Raises ValueError se não encontrado."""
    jogador = session.get(Jogador, jogador_id)
    if not jogador:
        raise ValueError(f"Jogador com ID {jogador_id} não encontrado.")
    nome = jogador.name
    session.delete(jogador)
    session.commit()
    return {"message": f"Jogador '{nome}' eliminado com sucesso."}


def core_get_jogadores_por_equipa(session: Session, equipa_id: int) -> dict:
    """Obter todos os jogadores de uma equipa. Raises ValueError se equipa não existir."""
    equipa = session.get(Equipa, equipa_id)
    if not equipa:
        raise ValueError(f"Equipa com ID {equipa_id} não encontrada.")
    jogadores = session.exec(select(Jogador).where(Jogador.equipa_id == equipa_id)).all()
    return {"equipa": equipa.name, "jogadores": jogadores}


def core_get_jogadores_por_posicao(session: Session, posicao: str) -> dict:
    """Obter todos os jogadores de uma posição específica."""
    jogadores = session.exec(select(Jogador).where(Jogador.posicao == posicao)).all()
    return {"posicao": posicao, "jogadores": jogadores}
