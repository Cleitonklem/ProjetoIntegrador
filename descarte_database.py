from sqlalchemy import MetaData, create_engine, Table, Column, select, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

metadata = MetaData()
engine = create_engine('sqlite:///descarte_database', connect_args={'check_same_thread': False},
                       echo=False)  # echo=False
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


# Tabela produto
class Produto(Base):
    __tablename__ = 'produto'
    id_produto = Column(Integer, primary_key=True)
    nome_produto = Column(String)

    produto_aceito_data = relationship("Aceito", backref="produto")


# Tabela destino
class Destino(Base):
    __tablename__ = 'destino'
    id_destino = Column(Integer, primary_key=True)
    nome_destino = Column(String)
    endereco_destino = Column(String)
    telefone_destino = Column(String)
    mapa_destino = Column(String)

    destino_aceito_data = relationship("Aceito", backref="destino")


# Tabela produto_aceito
class Aceito(Base):
    __tablename__ = 'produto_aceito'
    id_aceito = Column(Integer, primary_key=True)
    id_produto = Column(ForeignKey('produto.id_produto'))
    id_destino = Column(ForeignKey('destino.id_destino'))


def get_aceitos():
    return db_session.query(Aceito)


def get_produtos(aceito):
    return [produto.id_produto for produto in produto.produto_aceito_data]


def get_destinos(aceito):
    return [destino.id_destino for destino in destino.destino_aceito_data]


data = get_aceitos()
