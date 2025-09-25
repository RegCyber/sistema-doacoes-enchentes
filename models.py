from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class Doador(db.Model):
    __tablename__ = 'doadores'
    
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
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'endereco': self.endereco,
            'numero': self.numero,
            'cep': self.cep,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'telefone': self.telefone,
            'whatsapp': self.whatsapp,
            'pode_entregar': self.pode_entregar,
            'itens_doacao': self.itens_doacao,
            'prazo_disponibilidade': self.prazo_disponibilidade.strftime('%Y-%m-%d'),
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M')
        }

class Receptor(db.Model):
    __tablename__ = 'receptores'
    
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
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome,
            'endereco': self.endereco,
            'numero': self.numero,
            'cep': self.cep,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            'telefone': self.telefone,
            'whatsapp': self.whatsapp,
            'qtde_pessoas': self.qtde_pessoas,
            'pode_retirar': self.pode_retirar,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M')
        }

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    descricao = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(500))
    situacao = db.Column(db.String(20), nullable=False)  # 'achado' ou 'perdido'
    local_encontro = db.Column(db.String(200))
    contato = db.Column(db.String(100), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'especie': self.especie,
            'raca': self.raca,
            'descricao': self.descricao,
            'foto': self.foto,
            'situacao': self.situacao,
            'local_encontro': self.local_encontro,
            'contato': self.contato,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M')
        }

def init_db(app):
    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso!")