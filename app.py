from flask import Flask, render_template, request, redirect, url_for, flash # importa funções do flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'socjksjdsjkjkkdsfds2356fds6g456sg45f6dg4f5d6'  # Necessário para usar mensagens flash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

# Cria todas as tabelas
with app.app_context():
    db.create_all()

@app.route('/') 
def index():
    usuarios = Usuario.query.all()
    return render_template('login2.html', usuarios=usuarios)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    email = request.form['email']
    senha = request.form['senha']

    # Verifica se o email já está registrado
    if Usuario.query.filter_by(email=email).first():
        flash('Email já registrado!', 'danger')
        return redirect(url_for('index'))

    # Adiciona novo usuário
    novo_usuario = Usuario(email=email)
    novo_usuario.set_senha(senha)
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Usuário registrado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Busca o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e a senha está correta
        if usuario and usuario.verificar_senha(senha):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))  # Redireciona para uma página protegida (dashboard)
        else:
            flash('Email ou senha inválidos!', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return '<h1>Bem-vindo ao Dashboard!</h1>'
