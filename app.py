from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

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

    novo_usuario = Usuario(email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
