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


# Tabela com o Feedback
class Resposta(Base):
    __tablename__ = 'respostas'
    id = Column(Integer, primary_key=True)
    resp1 = Column(String(20))
    resp2 = Column(String(20))
    resp3 = Column(String(20))
    resp4 = Column(String(20))
    resp5 = Column(String(20))
    resp6 = Column(String(20))
    resp7 = Column(String(20))
    resp8 = Column(String(20))
    resp9 = Column(String(100))
    resp10 = Column(String(100))
    resp11 = Column(String(100))

    def __repr__(self):
        return f'({self.resp1}, {self.resp2}, {self.resp3}, {self.resp4}, {self.resp5},' \
               f' {self.resp6}, {self.resp7}, {self.resp8}, {self.resp9}, {self.resp10}, {self.resp11})'


# Tabela de usuarios
class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    password = Column(String)

    def __repr__(self):
        return f'({self.username}, {self.password})'


# Carrega página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        endereco = session.query(Descarte).filter(Descarte.produto_id == request.form['item']).all()
        return render_template('destinos.html', endereco=endereco)
    return render_template("index.html")


# Carrega página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        if bool(session.query(User).filter_by(username=usuario, password=senha).first()):
            esperando = session.query(Cadastro).all()
            resp = session.query(Resposta).all()
            if bool(session.query(Resposta).filter_by(id="").first()) and \
                    bool(session.query(Cadastro).filter_by(id="").first()):
                vazio = "Não existem dados aguardando aprovação, nem formulários novos preenchidos!"
                return render_template("espera.html", vazio=vazio)
            else:
                return render_template("espera.html", esperando=esperando, resp=resp,)
        else:
            erro = "Login ou senha incorretos, por favor tente outra vez!"
            return render_template("login.html", erro=erro)
    return render_template("login.html")


# Carrega página que mostra os pontos de descarte na cidade
@app.route('/destinos')
def destinos():
    return render_template('destinos.html')


# Carrega a página com os feedbacks
@app.route('/opiniao', methods=['GET', 'POST'])
def opiniao():
    if request.method == 'POST':
        resposta = Resposta(resp1=request.form['resp1'], resp2=request.form['resp2'],
                            resp3=request.form['resp3'], resp4=request.form['resp4'],
                            resp5=request.form['resp5'], resp6=request.form['resp6'],
                            resp7=request.form['resp7'], resp8=request.form['resp8'],
                            resp9=request.form['resp9'], resp10=request.form['resp10'],
                            resp11=request.form['resp11'])

        session.add(resposta)
        session.commit()
        return render_template("index.html")
    return render_template("opiniao.html")


# Carrega a página para cadastrar itens e locais novos
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        cadastro = Cadastro(cad_item=request.form['cad_item'], cad_nome=request.form['cad_nome'],
                            cad_endereco=request.form['cad_endereco'], cad_telefone=request.form['cad_telefone'])

        session.add(cadastro)
        session.commit()
        return render_template("index.html")

    return render_template("cadastrar.html")


@app.route('/espera')
def espera():
    return render_template("espera.html")


if __name__ == '__main__':
    app.run(debug=True)
