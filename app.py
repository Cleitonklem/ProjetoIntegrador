from flask import Flask, render_template, request, flash, redirect, url_for
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
    endereco = Column(String(50))
    telefone = Column(String(200))
    mapa = Column(String(10))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    desc_dest = relationship(Descarte, backref='destinos')

    def __repr__(self):
        return f'Destino({self.nome}, {self.endereco}, {self.telefone}, {self.mapa})'


# Tabala Produtos
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    item = Column(String(100))
    desc_pro = relationship(Descarte, backref='produtos')
    dest_pro = relationship(Destino, backref='produtos')

    def __repr__(self):
        return f'Produto({self.item})'


global endereco


# Carrega página principal
@app.route('/', methods=['GET', 'POST'],)
def index():
    global endereco
    if request.method == 'POST':
        if not request.form['item']:
            return render_template("index.html")
            #flash('Por Favor selecione um dos items', 'error')
        else:
            endereco = session.query(Destino).filter(Destino.produto_id == request.form['item']).all()
            print(endereco)
            return render_template('destinos.html', endereco=endereco)
            #return redirect(url_for('destinos'))
    return render_template("index.html")


# Carrega página que mostra os pontos de descarte na cidade
@app.route('/destinos')
def destinos():
    return render_template('destinos.html', endereco=endereco)


# Carrega a página com os feedbacks
@app.route('/opiniao')
def opiniao():
    return render_template("opiniao.html")


if __name__ == '__main__':
    app.run(debug=True)
