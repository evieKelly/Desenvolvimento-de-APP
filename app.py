from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Diario
import random

app = Flask(__name__)
app.secret_key = 'chave_secreta' 

sugestoes = [
    '''Não guarde tudo para você. Use este espaço seguro
      para expressar sua alegria, sua frustração ou até 
      mesmo aquela sensação de que hoje foi um dia neutro.''',
    
    '''Você é muito mais forte do que a soma dos seus dias ruins. 
    Que tal escrever um pouco sobre como foi o seu dia e esvaziar a 
    mente para recarregar as energias?''',

    '''Não subestime o poder dos pequenos passos. Reservar um momento
    para colocar seus pensamentos em ordem hoje vai deixar o seu amanhã
     mais leve.''',
     
     '''Sua trajetória importa e seus sentimentos também. Não importa como 
     foi o dia de hoje, você venceu mais uma etapa. Como está o seu humor agora?''',

     '''Dias difíceis fazem parte da jornada, mas eles não definem quem você é. Use 
     este espaço para desabafar e deixar o peso de hoje para trás.''',

     
]


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

#-------------------------------------------------------------------------------
# RESPONSÁVEL: Amanda
# TELA: diário

@app.route("/diario")
def diario():

    registros = Diario.query.all()

    return render_template(
        "diario.html",
        registros=registros
    )

# deletar

@app.route("/deletar/<int:id>")
def deletar(id):

    registro = Diario.query.get(id)

    db.session.delete(registro)

    db.session.commit()

    return redirect("/diario")

# editar

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    registro = Diario.query.get(id)

    # salvar edição
    if request.method == "POST":

        registro.texto = request.form["texto"]

        db.session.commit()

        return redirect("/diario")

    # abrir página editar
    return render_template(
        "editar.html",
        registro=registro
    )

#iniciar servidor

if __name__ == "__main__":
    app.run(debug=True)
#--------------------------------------------------------------------------



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


#-----------------------------------------------------------------
# RESPONSÁVEL: Amanda
# TELA: Sugestões de Atividades 
@app.route('/sugestao')
def sugestao():

    sugestao_do_dia = random.choice(sugestoes)

    return render_template(
        'sugestao.html',
        sugestao=sugestao_do_dia
    )
#-------------------------------------------------------------------
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