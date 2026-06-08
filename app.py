from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Diario, RegistroHumor
import random

app = Flask(__name__)
app.secret_key = 'chave_secreta' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
# Calcula o "Humor Médio" a partir de uma lista de notas de humor (1 a 5),
# que virão do Registro Diário de Humor (Quiz). Devolve um dicionário pronto
# para a tela: rótulo, carinha (imagem 2D) e o quanto preencher a barra (0 a 100%).
# As carinhas ficam em static/img/icones/humor_1.png (triste) a humor_5.png (feliz).
def calcular_humor_medio(notas):
    if not notas:
        return {'rotulo': 'Sem registros', 'imagem': 'humor_3.png', 'porcentagem': 0}

    media = sum(notas) / len(notas)

    if media < 1.5:
        rotulo, imagem = 'Muito ruim', 'humor_1.png'
    elif media < 2.5:
        rotulo, imagem = 'Ruim', 'humor_2.png'
    elif media < 3.5:
        rotulo, imagem = 'Neutro', 'humor_3.png'
    elif media < 4.5:
        rotulo, imagem = 'Bom', 'humor_4.png'
    else:
        rotulo, imagem = 'Muito bom', 'humor_5.png'

    return {
        'rotulo': rotulo,
        'imagem': imagem,
        'porcentagem': round((media / 5) * 100),
    }

# RESPONSÁVEL: Luiz
# Transforma um registro de humor (salvo pelo Quiz no banco) numa nota de 1 a 5,
# que é o formato que o calcular_humor_medio entende.
# O Quiz (Deivid) ainda vai definir COMO salva o humor, então cobrimos os 2 casos:
#   - se salvar número (ex: 4), usamos direto;
#   - se salvar texto (ex: "Feliz"), traduzimos pelo mapa abaixo.
# IMPORTANTE: combinar com o grupo o formato exato pra esse mapa bater certinho.
# Humor desconhecido cai em neutro (3) só pra nunca quebrar a tela.
MAPA_HUMOR = {
    'muito triste': 1, 'triste': 2,
    'neutro': 3,
    'bem': 4, 'calmo': 4, 'feliz': 4,
    'muito feliz': 5,
}

def nota_do_registro(registro):
    valor = registro.humor
    try:
        nota = int(valor)               # caso o Quiz salve um número
        if 1 <= nota <= 5:
            return nota
    except (TypeError, ValueError):
        pass
    return MAPA_HUMOR.get(str(valor).strip().lower(), 3)  # caso salve texto

# RESPONSÁVEL: Luiz
# TELA: Tela Inicial
@app.route('/tela-inicial')
def tela_inicial():
    # Lê os registros de humor salvos pelo Quiz (Registro Diário de Humor).
    # Enquanto o Quiz do Deivid não salvar nada, a lista vem vazia e o card
    # mostra "Sem registros" — estado honesto, sem dado falso.
    registros = RegistroHumor.query.all()
    notas_humor = [nota_do_registro(r) for r in registros]

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
    humores = {
        "Feliz": 0,
        "Calmo": 0,
        "Neutro": 0,
        "Triste": 0
    }

    return render_template(
        'relatorio_semanal.html',
        humores=humores
    )

# RESPONSÁVEL: Augusto
# TELA: Relatório Mensal
@app.route('/relatorio-mensal')
def relatorio_mensal():
    humores = {
        "Muito Feliz": 0,
        "Bem": 0,
        "Neutro": 0,
        "Triste": 0,
        "Muito Triste": 0
    }

    return render_template(
        'relatorio_mensal.html',
        humores=humores
    )


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
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # debug=True faz o Flask reiniciar sozinho sempre que vocês alterarem o código
    app.run(debug=True)