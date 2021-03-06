from flask import Flask, render_template, request
from models import *
from report import *
#iniciando app
app = Flask(__name__)

#Pagina inicial
@app.route("/")
def index():
    return render_template("index.html")

#Funcoes para o cadastro

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastroPage():
    estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
    'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    return render_template("cadastro.html", ufs = estados)

@app.route('/cadastro-success', methods=['GET', 'POST'])
def getFormCadastro():
    nome = request.form['cliente']
    cnpj = request.form['cnpj']
    email = request.form['email']
    endereco = request.form['endereco']
    estado = request.form['estado']
    cep = request.form['cep']

    checkCnpj = checar_cliente(cnpj)

    if not nome:
        return render_template('500.html'),500

    if checkCnpj:
        return '''<head><meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/"/></head>
        <script>alert("Operacao impossivel, CNPJ ja cadastrado!");</script>'''
    inserir_cliente(nome, cnpj, email, endereco, estado, cep)
    return '''<head><meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/"/></head>
        <script>alert("Dados enviados com sucesso.");</script>'''


#Funcoes para o laudo
@app.route("/laudo")
def laudoPage():
    cnpjs = selecionar_cnpjs()
    return render_template("laudo.html", cnpjs = cnpjs)

@app.route('/laudo-success', methods=['POST'])
def getFormLaudo():
    cnpj = request.form['cnpj']
    produto = request.form['produtos_cliente']
    qtProduto = request.form['qtd_produtos']
    nChamado = request.form['num_chamado']
    opcaoEmbalagem = request.form['opcao_embalagem']
    estadoEmbalagem = 'N/A'
    conservacaoEmbalagem = 'N/A'
    opcaoPragas = request.form['Havia_pragas']
    nivelIdentificacao = 'N/A'
    classePraga = 'N/A'
    ordemPraga = 'N/A'
    familiaPraga = 'N/A'
    generoPraga = 'N/A'
    especiePraga = 'N/A'
    nomePopular = 'N/A'
    conclusao = request.form['comentario']
    conteudoIdentificacao = ''
    checkChamado = checar_chamado(nChamado)

    if opcaoEmbalagem == 'Sim':
        estadoEmbalagem = request.form['estado_embalagem']
        conservacaoEmbalagem = request.form['estado_embalagem2']


    if opcaoPragas == 'Sim':
        nivelIdentificacao = request.form['identificação_pragas']

        if nivelIdentificacao == 'Nome popular':
            nomePopular = request.form['nome_praga']
            conteudoIdentificacao = nomePopular

        elif nivelIdentificacao == 'Especie':
            especiePraga = request.form['especie_praga']
            conteudoIdentificacao = especiePraga

        elif nivelIdentificacao == 'Genero':
            generoPraga = request.form['genero_praga']
            conteudoIdentificacao = generoPraga

        elif nivelIdentificacao == 'Familia':
            familiaPraga = request.form['familia_praga']
            conteudoIdentificacao = familiaPraga

        elif nivelIdentificacao == 'Ordem':
            ordemPraga = request.form['ordem_praga']
            conteudoIdentificacao = ordemPraga

        else:
            classePraga = request.form['classe_praga']
            conteudoIdentificacao = classePraga


    if (checkChamado):
        return '''<head><meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/"/></head>
    <script>alert("Operação impossível ! chamado ja cadastrado.");</script>'''

    inserir_laudo(cnpj, produto, qtProduto, nChamado, opcaoEmbalagem, estadoEmbalagem, conservacaoEmbalagem, opcaoPragas,
     nivelIdentificacao, classePraga, ordemPraga, familiaPraga, generoPraga, especiePraga, nomePopular, conclusao)

    criar_pasta('Relatorios')

    criar_relatorio(cnpj, produto, qtProduto, nChamado, opcaoEmbalagem, estadoEmbalagem, conservacaoEmbalagem, opcaoPragas,
     nivelIdentificacao, conteudoIdentificacao)

    return '''<head><meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/"/></head>
	<script>alert("Dados enviados com sucesso.");</script>'''

#Funcoes para a exclusao de clientes
@app.route("/deletar-cliente", methods = ['GET', 'POST'])
def deletarPage():
    return render_template("deletar.html")

@app.route("/deletar-success", methods = ['GET', 'POST'])
def deletarSucessPage():
    cnpj = request.form['cnpj']
    checkCnpj = checar_cliente(cnpj)
    if checkCnpj:
        deletar_cliente(cnpj)
        return '''<head><meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/"/></head>
	<script>alert("Cliente deletado com sucesso.");</script>'''

    return '''<head><meta http-equiv="refresh" content="0; url=http://127.0.0.1:5000/"/></head>
	<script>alert("Operação impossível! CNPJ não encontrado");</script>'''

if __name__ == '__main__':
    app.run(use_reloader=False, threaded=True)
