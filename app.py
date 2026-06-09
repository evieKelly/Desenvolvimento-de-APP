from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Diario, RegistroHumor, Usuario
from datetime import datetime, date, timedelta
import random
import locale

app = Flask(__name__)
app.secret_key = 'chave_secreta' 



# ==============================================================================
# RESPONSÁVEL: Kelly 
# ==============================================================================

# TELA: Login (Página Inicial obrigatória)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_digitado = request.form.get('email')
        senha_digitada = request.form.get('senha')
        
        # Busca o usuário no banco de dados
        usuario = Usuario.query.filter_by(email=email_digitado).first()
        
        # Verifica se o usuário existe e se a senha bate
        if usuario and usuario.senha == senha_digitada:
            # Login efetuado com sucesso! Redireciona para a tela interna do Luiz
            return redirect(url_for('tela_inicial'))
        else:
            # Se errar, devolve uma mensagem de alerta na tela
            flash('E-mail ou senha incorretos!', 'erro')
            
    return render_template('index.html')


# TELA: Cadastro de Usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        idade = request.form.get('idade')
        senha = request.form.get('senha')
        # Captura o campo de confirmação do seu formulário
        confirme_senha = request.form.get('confirme_senha') 
        
        # Validação simples: as senhas precisam ser iguais
        if senha != confirme_senha:
            flash('As senhas não coincidem!', 'erro')
            return render_template('cadastro.html')
            
        # Verifica se o email já está cadastrado
        email_existente = Usuario.query.filter_by(email=email).first()
        if email_existente:
            flash('Este e-mail já está cadastrado!', 'erro')
            return render_template('cadastro.html')
            
        # Salva o novo usuário no banco.db
        novo_usuario = Usuario(nome=nome, email=email, idade=int(idade), senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Cadastro feito! Redireciona para o login para ele logar
        flash('Cadastro realizado com sucesso! Faça seu login.', 'sucesso')
        return redirect(url_for('index'))

    return render_template('cadastro.html')


# TELA: Recuperação de Senha
@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        
       
        usuario = Usuario.query.filter_by(email=email).first()
        
      
        return render_template('recuperar_senha.html', enviado=True)

    return render_template('recuperar_senha.html', enviado=False)

# RESPONSÁVEL: Luiz
# aqui eu calculo o humor médio com as notas de 1 a 5 e já devolvo pronto pra
# tela: o rótulo (tipo "Bom"), a carinha e o quanto preencher a barrinha.
# troquei os emoji por imagem, as carinhas estão em
# static/img/icones/humor_1.png (triste) até humor_5.png (feliz).
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
# Deivid, fiz isso aqui pra quando o teu Quiz começar a salvar o humor no banco.
# como a gente ainda não combinou se vai salvar número ou texto, deixei rodando
# dos dois jeitos: se vier número (1 a 5) eu uso direto, se vier texto eu traduzo
# pelo mapa de baixo. se cair alguma coisa que não tá no mapa eu boto neutro (3)
# pra não quebrar a tela. depois me fala qual formato vocês vão usar.
MAPA_HUMOR = {
    'muito triste': 1, 'triste': 2,
    'neutro': 3,
    'bem': 4, 'calmo': 4, 'feliz': 4,
    'muito feliz': 5,
}

def nota_do_registro(registro):
    valor = registro.humor
    try:
        nota = int(valor)               # se o Quiz salvar número
        if 1 <= nota <= 5:
            return nota
    except (TypeError, ValueError):
        pass
    return MAPA_HUMOR.get(str(valor).strip().lower(), 3)  # se salvar texto

# RESPONSÁVEL: Luiz
# TELA: Tela Inicial
@app.route('/tela-inicial')
def tela_inicial():
    # pego os registros de humor que o Quiz salva no banco e tiro a média.
    # enquanto o Quiz ainda não salva nada vem vazio e aparece "Sem registros"
    # no card, achei melhor do que deixar um humor de mentira aparecendo.
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

    if registro: 
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
# o quiz mostra as 5 carinhas de humor. quando o usuário clica em uma,
# o formulário manda o texto do humor por POST e eu salvo na tabela
# RegistroHumor. depois mando ele pra Tela Inicial, que já recalcula a média.
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        humor = request.form['humor']
        registro = RegistroHumor(humor=humor)
        db.session.add(registro)
        db.session.commit()
        return redirect(url_for('tela_inicial'))

    return render_template('quiz.html')



# RESPONSÁVEL: Augusto
# TELA: Relatório Semanal
# Luiz: liguei no banco. aqui são só 4 categorias, então junto as notas:
# 1 e 2 viram Triste, 3 Neutro, 4 Calmo e 5 Feliz. devolvo a % de cada uma.
@app.route('/relatorio-semanal')
def relatorio_semanal():
    humores = {
        "Feliz": 0,
        "Calmo": 0,
        "Neutro": 0,
        "Triste": 0
    }

    rotulo_por_nota = {1: "Triste", 2: "Triste", 3: "Neutro", 4: "Calmo", 5: "Feliz"}

    # só os registros dos últimos 7 dias
    limite = date.today() - timedelta(days=7)
    registros = RegistroHumor.query.filter(RegistroHumor.data >= limite).all()
    for r in registros:
        humores[rotulo_por_nota[nota_do_registro(r)]] += 1

    total = len(registros)
    if total > 0:
        for chave in humores:
            humores[chave] = round(humores[chave] / total * 100)

    return render_template(
        'relatorio_semanal.html',
        humores=humores
    )

# RESPONSÁVEL: Augusto
# TELA: Relatório Mensal
# Luiz: liguei no banco. conto os registros do Quiz em cada categoria usando a
# nota 1-5 (mesmo critério da Tela Inicial) e devolvo a % de cada humor.
@app.route('/relatorio-mensal')
def relatorio_mensal():
    humores = {
        "Muito Feliz": 0,
        "Bem": 0,
        "Neutro": 0,
        "Triste": 0,
        "Muito Triste": 0
    }

    rotulo_por_nota = {1: "Muito Triste", 2: "Triste", 3: "Neutro", 4: "Bem", 5: "Muito Feliz"}

    # só os registros dos últimos 30 dias
    limite = date.today() - timedelta(days=30)
    registros = RegistroHumor.query.filter(RegistroHumor.data >= limite).all()
    for r in registros:
        humores[rotulo_por_nota[nota_do_registro(r)]] += 1

    total = len(registros)
    if total > 0:
        for chave in humores:
            humores[chave] = round(humores[chave] / total * 100)

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
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # debug=True faz o Flask reiniciar sozinho sempre que vocês alterarem o código
    app.run(debug=True)