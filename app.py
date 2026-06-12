# -*- coding: utf-8 -*-
# Título: Arquivo Principal do App
# Descrição: Inicializa o Flask, registra as blueprints de rotas e manipula páginas.
# Data: 28/04/2026
# __author__ = "Davidson Willis de Oliveira Silva"
# __email__ = "davidson.silva2@aluno.cps.sp.gov.br"
# __turma__ = "DSM - 2º Semestre / Noturno"
# __version__ = "1.0.0"

from flask import Flask, Blueprint, render_template
from rotas import rotas

app = Flask(__name__)
app.register_blueprint(rotas)

paginas = Blueprint('paginas', __name__, template_folder='templates')   

@paginas.route('/')
def index():
    return render_template('paginas/layout.html', title="Página Inicial do Trabalho Flask")

app.register_blueprint(paginas)

if __name__ == '__main__':
    app.run(debug=True)

