# filepath: /home/renan/Documentos/teste_estatistica/teste_estatistica/app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

# Cria todas as tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('registro.html', usuarios=usuarios)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    email = request.form['email']
    senha = request.form['senha']

    # Verifica se o email já está registrado
    if Usuario.query.filter_by(email=email).first():
        return "Email já registrado!"