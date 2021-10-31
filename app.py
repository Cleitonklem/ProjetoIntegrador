from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

db = SQLAlchemy()
Bootstrap()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cadastrar')
def cadastrar():
    return render_template("cadastrar.html")


@app.route('/opiniao')
def opiniao():
    return render_template("opiniao.html")


if __name__ == '__main__':
    app.run()
