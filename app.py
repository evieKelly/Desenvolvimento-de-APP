from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Diario
from datetime import datetime
import locale
import random

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
# Calcula o "Humor Médio" a partir de uma lista de notas de humor (1 a 5),
# que virão do Registro Diário de Humor (Quiz). Devolve um dicionário pronto
# para a tela: rótulo, carinha (emoji) e o quanto preencher a barra (0 a 100%).
def calcular_humor_medio(notas):
    if not notas:
        return {'rotulo': 'Sem registros', 'emoji': '🙂', 'porcentagem': 0}

    media = sum(notas) / len(notas)

    if media < 1.5:
        rotulo, emoji = 'Muito ruim', '😣'
    elif media < 2.5:
        rotulo, emoji = 'Ruim', '🙁'
    elif media < 3.5:
        rotulo, emoji = 'Neutro', '😐'
    elif media < 4.5:
        rotulo, emoji = 'Bom', '🙂'
    else:
        rotulo, emoji = 'Muito bom', '😄'

    return {
        'rotulo': rotulo,
        'emoji': emoji,
        'porcentagem': round((media / 5) * 100),
    }

# RESPONSÁVEL: Luiz
# TELA: Tela Inicial
@app.route('/tela-inicial')
def tela_inicial():
    # TODO: quando o Quiz (Registro Diário de Humor) começar a salvar as notas,
    #       trocar a lista abaixo pela consulta real ao banco.
    #       Ex.: notas = [r.nota for r in RegistroHumor.query.all()]
    notas_humor = [2, 1, 2, 1, 2]  # dados de exemplo (placeholder) -> média "Ruim"

    humor = calcular_humor_medio(notas_humor)
    return render_template('tela_inicial.html', humor=humor)

# RESPONSÁVEL: Deivid
# TELA: Contatos 
@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

#-------------------------------------------------------------------------------
# RESPONSÁVEL: Amanda
# TELA: diário
# Configurações do Banco de Dados (Movidas para o topo)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diario.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
@app.route("/diario")
def diario():

    registros = Diario.query.all()

    hoje = datetime.now().strftime("%d de %B")

    return render_template(
        "diario.html",
        registros=registros,
        hoje=hoje
    )
# ROTA: Deletar
@app.route("/deletar/<int:id>")
def deletar(id):

    registro = Diario.query.get(id)

    db.session.delete(registro)

    db.session.commit()

    return redirect("/diario")

# ROTA: Editar: AMANDA 
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    registro = Diario.query.get(id)

    if request.method == "POST":

        registro.texto = request.form["texto"]

        db.session.commit()

        return redirect("/diario")
    
    return render_template(
        "editar.html",
        registro=registro
    )
#ROTA: registrar

@app.route("/registrar", methods=["POST"])
def registrar():
    texto = request.form["texto"]

    novo = Diario(
        texto=texto,
        data=str(datetime.now())
    )

    db.session.add(novo)
    db.session.commit()

    return redirect("/diario")

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


db.init_app(app)


with app.app_context():
    db.create_all()


# Lista de Sugestões
sugestoes = [
    '''Não guarde tudo para você. Use este espaço seguro para expressar sua alegria, sua frustração ou até mesmo aquela sensação de que hoje foi um dia neutro.''',
   
    '''Você é muito mais forte do que a soma dos seus dias ruins. Que tal escrever um pouco sobre como foi o seu dia e esvaziar a mente para recarregar as energias?''',


    '''Não subestime o poder dos pequenos passos. Reservar um momento para colocar seus pensamentos em ordem hoje vai deixar o seu amanhã mais leve.''',
     
    '''Sua trajetória importa e seus sentimentos também. Não importa como foi o dia de hoje, você venceu mais uma etapa. Como está o seu humor agora?''',


    '''Dias difíceis fazem parte da jornada, mas eles não definem quem você é. Use este espaço para desabafar e deixar o peso de hoje para trás.''',
]


# ROTA: Sugestões
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