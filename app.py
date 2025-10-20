from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Doador, Receptor, Pet, init_db
from datetime import datetime
import os
import re

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados para produção
def get_database_url():
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///doacoes.db')
    
    # Se for PostgreSQL no Heroku/Render, ajusta a URL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações de segurança para produção
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-aqui-trocar-em-producao')

db.init_app(app)
init_db(app)

# Rotas para Doadores
@app.route('/api/doadores', methods=['GET'])
def listar_doadores():
    doadores = Doador.query.all()
    return jsonify([{
        'id': d.id,
        'nome': d.nome,
        'cidade': d.cidade,
        'itens_doacao': d.itens_doacao,
        'prazo_disponibilidade': d.prazo_disponibilidade.strftime('%d/%m/%Y'),
        'pode_entregar': d.pode_entregar,
        'telefone': d.telefone
    } for d in doadores])

@app.route('/api/doadores', methods=['POST'])
def cadastrar_doador():
    try:
        data = request.json
        novo_doador = Doador(
            cpf=data['cpf'],
            nome=data['nome'],
            endereco=data['endereco'],
            numero=data['numero'],
            cep=data['cep'],
            bairro=data['bairro'],
            cidade=data['cidade'],
            estado=data['estado'],
            telefone=data['telefone'],
            whatsapp=data['whatsapp'],
            pode_entregar=data['pode_entregar'],
            itens_doacao=data['itens_doacao'],
            prazo_disponibilidade=datetime.strptime(data['prazo_disponibilidade'], '%Y-%m-%d')
        )
        db.session.add(novo_doador)
        db.session.commit()
        return jsonify({'message': 'Doador cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rotas para Receptores
@app.route('/api/receptores', methods=['GET'])
def listar_receptores():
    receptores = Receptor.query.all()
    return jsonify([{
        'id': r.id,
        'nome': r.nome,
        'cidade': r.cidade,
        'qtde_pessoas': r.qtde_pessoas,
        'pode_retirar': r.pode_retirar,
        'telefone': r.telefone
    } for r in receptores])

@app.route('/api/receptores', methods=['POST'])
def cadastrar_receptor():
    try:
        data = request.json
        novo_receptor = Receptor(
            cpf=data['cpf'],
            nome=data['nome'],
            endereco=data['endereco'],
            numero=data['numero'],
            cep=data['cep'],
            bairro=data['bairro'],
            cidade=data['cidade'],
            estado=data['estado'],
            telefone=data['telefone'],
            whatsapp=data['whatsapp'],
            qtde_pessoas=data['qtde_pessoas'],
            pode_retirar=data['pode_retirar']
        )
        db.session.add(novo_receptor)
        db.session.commit()
        return jsonify({'message': 'Receptor cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rotas para Pets
@app.route('/api/pets', methods=['GET'])
def listar_pets():
    pets = Pet.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'especie': p.especie,
        'raca': p.raca,
        'descricao': p.descricao,
        'situacao': p.situacao,
        'local_encontro': p.local_encontro,
        'contato': p.contato,
        'foto': p.foto
    } for p in pets])

@app.route('/api/pets', methods=['POST'])
def cadastrar_pet():
    try:
        data = request.json
        novo_pet = Pet(
            nome=data.get('nome', ''),
            especie=data['especie'],
            raca=data.get('raca', ''),
            descricao=data['descricao'],
            situacao=data['situacao'],
            local_encontro=data.get('local_encontro', ''),
            contato=data['contato'],
            foto=data.get('foto', '')
        )
        db.session.add(novo_pet)
        db.session.commit()
        return jsonify({'message': 'Pet cadastrado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_doador')
def cadastro_doador():
    return render_template('cadastro_doador.html')

@app.route('/cadastro_receptor')
def cadastro_receptor():
    return render_template('cadastro_receptor.html')

@app.route('/achados_perdidos')
def achados_perdidos():
    return render_template('achados_perdidos.html')

# Health check para monitoramento
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Manipulador de erro 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

# Manipulador de erro 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)