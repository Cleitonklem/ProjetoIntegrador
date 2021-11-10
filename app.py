from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///descartes.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
Bootstrap()
app = Flask(__name__)


# Tabela Descartes
class Descarte(Base):
    __tablename__ = 'descartes'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    destino_id = Column(Integer, ForeignKey('destinos.id'))
    produto = relationship('Produto')
    destino = relationship('Destino')

    def __repr__(self):
        return f'Descarte(item={self.produto.item}, nome={self.destino.nome}, endereco={self.destino.endereco}, ' \
               f' telefone={self.destino.telefone}, mapa={self.destino.mapa})'


# Tabela Destinos
class Destino(Base):
    __tablename__ = 'destinos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    endereco = Column(String(100))
    telefone = Column(String(15))
    mapa = Column(String)
    desc_dest = relationship(Descarte, backref='destinos')

    def __repr__(self):
        return f'Destino({self.nome}, {self.endereco}, {self.telefone}, {self.mapa})'


# Tabala Produtos
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    item = Column(String(100))
    desc_pro = relationship(Descarte, backref='produtos')

    def __repr__(self):
        return f'Produto({self.item})'


# Tabela para Cadastro
class Cadastro(Base):
    __tablename__ = 'cadastros'
    id = Column(Integer, primary_key=True)
    cad_item = Column(String(100))
    cad_nome = Column(String(100))
    cad_endereco = Column(String(100))
    cad_telefone = Column(String(15))

    def __repr__(self):
        return f'Cadastro({self.cad_item},{self.cad_nome}, {self.cad_endereco}, {self.cad_telefone})'


global endereco


# Carrega página principal
@app.route('/', methods=['GET', 'POST'],)
def index():
    global endereco
    if request.method == 'POST':
        if not request.form['item']:
            return render_template("index.html")
        else:
            endereco = session.query(Descarte).filter(Descarte.produto_id == request.form['item']).all()
            print(endereco)
            return render_template('destinos.html', endereco=endereco)
    return render_template("index.html")


# Carrega página que mostra os pontos de descarte na cidade
@app.route('/destinos')
def destinos():
    return render_template('destinos.html')


# Carrega a página com os feedbacks
@app.route('/opiniao')
def opiniao():
    return render_template("opiniao.html")


# Carrega a página para cadastrar itens e locais novos
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        cad_item = request.form['cad_item']
        cad_nome = request.form['cad_nome']
        cad_endereco = request.form['cad_endereco']
        cad_telefone = request.form['cad_telefone']

        cad_dados = Cadastro(cad_item, cad_nome, cad_endereco, cad_telefone)
       # session.add(cad_dados)
        #session.commit()

       # return render_template("index.html")

    return render_template("cadastrar.html")


@app.route('/espera')
def espera():
    esperando = Cadastro.query.all()
    return render_template("espera.html", esperando=esperando)


if __name__ == '__main__':
    app.run(debug=True)
