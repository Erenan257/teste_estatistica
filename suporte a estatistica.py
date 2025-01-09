from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração da URL de conexão com o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/meu_estoque'
db = SQLAlchemy(app)

# Definição da classe Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('produtos', lazy=True))

    def __repr__(self):
        return f'<Produto {self.nome}>'

# Definição da classe Categoria
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Categoria {self.nome}>'

# Função para consultar o estoque de um produto
def consultar_estoque(nome_produto):
    start_time = time.time()
    produto = Produto.query.filter_by(nome=nome_produto).first()
    end_time = time.time()
    print(f"Tempo de consulta: {end_time - start_time:.5f}s")
    if produto:
        return produto.estoque
    else:
        return "Produto não encontrado"

if __name__ == "__main__":
    db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)