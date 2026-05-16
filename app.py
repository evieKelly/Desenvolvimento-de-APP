from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'chave_secreta' 

# RESPONSÁVEL: Kelly 
# TELA: Login (Página Inicial obrigatória)
@app.route('/')
def index():
    return render_template('index.html')



# RESPONSÁVEL: Kelly
# TELA: Cadastro de Usuário
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# RESPONSÁVEL: Kelly
# TELA: Recuperação de Senha
@app.route('/recuperar-senha')
def recuperar_senha():
    return render_template('recuperar_senha.html')

# RESPONSÁVEL: Luiz
# TELA: Tela Inicial 
@app.route('/tela-inicial')
def tela_inicial():
    return render_template('tela_inicial.html')

# RESPONSÁVEL: Deivid
# TELA: Contatos 
@app.route('/contatos')
def contatos():
    return render_template('contatos.html')


# RESPONSÁVEL: AManda
# TELA: Diário
@app.route('/diario')
def diario():
    return render_template('diario.html')

# RESPONSÁVEL: Eduardo
# TELA:  Forms Uniceplac
@app.route('/forms')
def forms():
    return render_template('forms.html')

# RESPONSÁVEL: Deivid
# TELA: Quiz 
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')



# RESPONSÁVEL: Augusto
# TELA: Relatório Semanal
@app.route('/relatorio-semanal')
def relatorio_semanal():
    return render_template('relatorio_semanal.html')

# RESPONSÁVEL: Augusto
# TELA: Relatório Mensal
@app.route('/relatorio-mensal')
def relatorio_mensal():
    return render_template('relatorio_mensal.html')


# RESPONSÁVEL: Eduardo
# TELA: Exercícios de Respiração
@app.route('/respiracao')
def respiracao():
    return render_template('respiracao.html') 

# RESPONSÁVEL: Amanda
# TELA: Sugestões de Atividades 
@app.route('/sugestao')
def sugestao():
    return render_template('sugestao.html')

# RESPONSÁVEL: Luiz
# TELA: Centros de Atendimento 
@app.route('/centros-atendimento')
def centros_atendimento():
    return render_template('centros_atendimento.html')


# ==============================================================================
# INICIALIZAÇÃO DO SERVIDOR
# ==============================================================================
if __name__ == '__main__':
    # debug=True faz o Flask reiniciar sozinho sempre que vocês alterarem o código
    app.run(debug=True)