from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Doador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    whatsapp = db.Column(db.String(15), nullable=False)
    pode_entregar = db.Column(db.Boolean, default=False)
    itens_doacao = db.Column(db.Text, nullable=False)
    prazo_disponibilidade = db.Column(db.Date, nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class Receptor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    whatsapp = db.Column(db.String(15), nullable=False)
    qtde_pessoas = db.Column(db.Integer, nullable=False)
    pode_retirar = db.Column(db.Boolean, default=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    descricao = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(200))
    situacao = db.Column(db.String(20), nullable=False)  # 'achado' ou 'perdido'
    local_encontro = db.Column(db.String(200))
    contato = db.Column(db.String(100), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)