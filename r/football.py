from fastapi import FastAPI
import uvicorn
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Equipa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    estadio: str = Field(index=True)
    ano_fundacao: int = Field(index=True)
    orcamento_transferencias: float = Field(index=True)
    orcamento_salarios: float = Field(index=True)




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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_data() 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
