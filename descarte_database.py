from sqlalchemy import MetaData, create_engine, Table, Column, select, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

metadata = MetaData()
engine = create_engine('sqlite:///descarte_database', connect_args={'check_same_thread': False},
                       echo=True)  # echo=False
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


# Tabela produto
class Produto(Base):
    __tablename__ = 'produto'
    id_produto = Column(Integer, primary_key=True)
    nome_produto = Column(String)


# Tabela destino
class Destino(Base):
    __tablename__ = 'destino'
    id_destino = Column(Integer, primary_key=True)
    nome_destino = Column(String)
    endereco_destino = Column(String)
    telefone_destino = Column(String)
    mapa_destino = Column(String)


# Tabela descarte
class Descarte(Base):
    __tablename__ = 'descarte'
    id_descarte = Column(Integer, primary_key=True)
    id_produto = Column(ForeignKey('produto.id_produto'))
    id_destino = Column(ForeignKey('destino.id_destino'))
