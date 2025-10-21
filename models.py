from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re
from sqlalchemy import text

db = SQLAlchemy()

# Função para corrigir URL do PostgreSQL
def get_database_url():
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///doacoes.db')
    
    # Se for PostgreSQL no Heroku/Render, ajusta a URL
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

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
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M'),
            'ativo': self.ativo
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
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M'),
            'ativo': self.ativo
        }

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    descricao = db.Column(db.Text, nullable=False)
    foto = db.Column(db.String(500))  # Aumentado para URLs longas
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
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M'),
            'ativo': self.ativo
        }

def init_db(app):
    """Função para inicializar o banco de dados"""
    with app.app_context():
        try:
            db.create_all()
            print("✅ Tabelas criadas/verificadas com sucesso!")
            
            # ← CORREÇÃO: Nova forma de listar tabelas no SQLAlchemy 2.0
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Tabelas no banco: {tables}")
            
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            # Em produção, não levantamos exceção, apenas registramos
            if os.environ.get('FLASK_ENV') == 'development':
                raise e

def test_db_connection():
    """Testa a conexão com o banco de dados"""
    try:
        # ← CORREÇÃO: Usar text() para queries SQL
        db.session.execute(text('SELECT 1'))
        print("✅ Conexão com o banco de dados estabelecida com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com o banco: {e}")
        return False