# -*- coding: utf-8 -*-
# Título: Rotas de Exercícios Flask
# Descrição: Primeiras rotas simples e tratamento de status HTTP dinâmicos.
# Data: 28/04/2026
# __author__ = "Davidson Willis de Oliveira Silva"
# __email__ = "davidson.silva2@aluno.cps.sp.gov.br"
# __turma__ = "DSM - 2º Semestre / Noturno"
# __version__ = "1.0.0"

from flask import Blueprint, request, jsonify

rotas = Blueprint('rotas', __name__)    

@rotas.route('/message', methods=['GET'])
def message():
    return "Cadastro Salvo com Sucesso!",200

@rotas.route('/message/<int:status>', methods=['GET'])
def message_status(status):
    tabela_status ={
        200: "200 OK - Sucesso geral.",
        201: "201 Created - Sucesso na criação.",
        400: "400 Bad Request - Erro do Cliente (sintaxe).",
        401: "401 Unauthorized - Falta de autenticação.",
        404: "404 Not Found - Recurso não encontrado.",
        500: "500 Internal Server Error - Erro do Servidor."
    }

    mensagem = tabela_status.get(status, "Status não encontrado na tabela.")
    return mensagem, status if status in tabela_status else 400

@rotas.route('/auth/login', methods=['POST'])
def auth():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    if usuario == 'genivaldo' and senha == 'jerusa':
        return "200 Ok", 200
    
    return "401 Unauthorized", 401

def verificar_cpf_valido(cpf: str)-> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * (i + 1 - j) for j in range(i))
        digito = (soma * 10 % 11) % 10

        if digito != int(cpf[i]):
            return False
        
    return True

@rotas.route('/cliente/validate', methods=['POST'])
def cliente_validate():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')

    if verificar_cpf_valido(cpf):
        resposta = {
            'status': 200,
            'mensagem':'200 OK - Sucesso geral.'
        }
        return jsonify(resposta), 200
    else:
        resposta = {
            'status': 400,
            'mensagem':'400 Bad Request - Erro do Cliente (sintaxe).'
        }
        return jsonify(resposta), 400
    
@rotas.route('/convert/celsius/<float(signed=True):temp>', methods=['GET'])
def convert_celsius(temp):
    fahrenheit = (temp * 1.8) + 32
    resposta = {
        'Celsius': temp,
        'Fahrenheit': fahrenheit
    }
    return jsonify(resposta), 200


@rotas.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    
    if q and q.strip():
        return f"Você pesquisou por: {q}", 200
    
    return "Parâmetro de busca obrigatório", 400


@rotas.route('/api/register', methods=['POST'])
def api_register():
    nome = request.form.get('nome')
    idade_texto = request.form.get('idade')
    
    try:
        idade = int(idade_texto)
    except (TypeError, ValueError):
        return jsonify({"erro": "Idade inválida. Digite um número inteiro."}), 400

    if idade < 18:
        resposta_erro = {"erro": "Cadastro permitido apenas para maiores de idade"}
        return jsonify(resposta_erro), 403
    
    return f"Usuário {nome} cadastrado", 201


@rotas.route('/products', methods=['GET'])
def list_products():
    
    produtos = [
        {"id": 1, "nome": "Teclado Mecanico", "preco": 250.00},
        {"id": 2, "nome": "Mouse Gamer", "preco": 120.50},
        {"id": 3, "nome": "Monitor 144Hz", "preco": 899.90}
    ]
    
    #produtos = []
    
    if not produtos:
        return '', 204
        
    return jsonify(produtos), 200


@rotas.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    api_key = request.headers.get('X-Api-Key')
    
    if api_key == 'secret123':
        return "Acesso ao painel administrativo liberado", 200
        
    return "Unauthorized", 401