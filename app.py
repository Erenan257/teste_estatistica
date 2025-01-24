from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secreta'  # Necessário para usar mensagens flash
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/renan/Documentos/teste_estatistica/teste_estatistica/instance/meu_banco.db'
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
        flash('Email já registrado!', 'danger')
        return redirect(url_for('index'))

    # Adiciona novo usuário
    novo_usuario = Usuario(email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Usuário registrado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
