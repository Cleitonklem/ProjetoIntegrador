from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///descartes.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
Bootstrap()


# Tabala Produtos
class Produtos(db.Model):
    id = db.Column('produto_id', db.Integer, primary_key=True)
    item = db.Column(db.String(100))


# Tabela Destinos
class Destinos(db.Model):
    id = db.Column('destino_id', db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(50))
    telefone = db.Column(db.String(200))
    mapa = db.Column(db.String(10))


# Tabela Descartes
class Descartes(db.Model):
    id = db.Column('descarte_id', db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, ForeignKey(Produtos.id))
    destino_id = db.Column(db.Integer, ForeignKey(Destinos.id))


def __init__(self, item, nome, endereco, telefone, mapa, produto_id, destino_id):
    self.item = item
    self.nome = nome
    self.endereco = endereco
    self.telefone = telefone
    self.mapa = mapa
    self.produto_id = produto_id
    self.destino_id = destino_id


# Carrega página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    global busca
    if request.method == 'POST':
        if not request.form['item']:
            flash('Por Favor selecione um dos items', 'error')
        else:
            busca = request.form['item']
           # dados = Destinos.query.filter(Descartes.produto_id == busca).all()

            #for linha in dados:
              #  print(f'Nome: {linha.produto_id} ')

            flash('Record was successfully added')
            return redirect(url_for('destinos'))
    return render_template("index.html")


# Carrega página que mostra os pontos de descarte na cidade
@app.route('/destinos')
def destinos():
    return render_template('destinos.html', local=Destinos.query.filter(Destinos.id == busca).all())


# Carrega a página com os feedbacks
@app.route('/opiniao')
def opiniao():
    return render_template("opiniao.html")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
