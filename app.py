from flask import Flask, session,render_template, request, redirect, url_for, flash
from models import db, Diario, RegistroHumor, Usuario
from datetime import datetime, date, timedelta
import random
import locale

app = Flask(__name__)
app.secret_key = 'chave_secreta' 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ==============================================================================
# RESPONSÁVEL: Kelly 
# ==============================================================================

# TELA: Login (Página Inicial obrigatória)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_digitado = request.form.get('email')
        senha_digitada = request.form.get('senha')
        
       
        usuario = Usuario.query.filter_by(email=email_digitado).first()
        
        # Verifica se o usuário existe e se a senha bate
        if usuario and usuario.senha == senha_digitada:

            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome

            print("SESSÃO CRIADA:", dict(session))

            return redirect(url_for('tela_inicial'))
        else:
            # Se errar
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
       
        confirme_senha = request.form.get('confirme_senha') 
        
        # Validação
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
        
        
        flash('Cadastro realizado com sucesso! Faça seu login.', 'sucesso')
        return redirect(url_for('index'))

    return render_template('cadastro.html')


# TELA: Recuperação de Senha
@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        nova_senha = request.form.get('nova_senha')
        confirme_senha = request.form.get('confirme_senha')

        # 1. Verifica se as senhas digitadas são iguais
        if nova_senha != confirme_senha:
            flash('As senhas não coincidem!', 'erro')
            return redirect(url_for('recuperar_senha'))

        # 2. Busca o usuário no banco
        usuario = Usuario.query.filter_by(email=email).first()

        # 3. Se o usuário existir, atualiza a senha e salva
        if usuario:
            usuario.senha = nova_senha
            db.session.commit()
            flash('Senha redefinida com sucesso! Faça login com a nova senha.', 'sucesso')
            return redirect(url_for('index'))
        else:
            flash('E-mail não encontrado em nosso sistema.', 'erro')
            return redirect(url_for('recuperar_senha'))

    return render_template('recuperar_senha.html')

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
    # sem login não dá pra saber de quem é a tela, então mando pro login
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    # pego só os registros de humor DESTE usuário e tiro a média.
    # enquanto o Quiz ainda não salva nada vem vazio e aparece "Sem registros"
    # no card, achei melhor do que deixar um humor de mentira aparecendo.
    registros = RegistroHumor.query.filter_by(usuario_id=session['usuario_id']).all()
    notas_humor = [nota_do_registro(r) for r in registros]

    humor = calcular_humor_medio(notas_humor)

    # nome de quem está logado, pra mostrar no "Olá, ..." (vem do login da Kelly)
    nome = session.get('usuario_nome')
    return render_template('tela_inicial.html', humor=humor, nome=nome)

# RESPONSÁVEL: Luiz
# sair da conta: limpa a sessão e volta pro login.
# é o ícone de porta na barra de baixo da tela inicial.
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# RESPONSÁVEL: Deivid
# TELA: Contatos
@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

#-------------------------------------------------------------------------------
 #RESPONSÁVEL: Amanda
# TELA: diário
# Configurações do Banco de Dados (Movidas para o topo)
# tenta deixar as datas em português; se o servidor não tiver esse idioma
# instalado, segue sem travar (a data só fica em inglês como reserva).
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    pass
@app.route("/diario")
def diario():

    print("SESSION NO DIARIO:", dict(session))

    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    registros = Diario.query.filter_by(
        usuario_id=session['usuario_id']
    ).all()

    hoje = datetime.now().strftime("%d de %B")

    return render_template(
        "diario.html",
        registros=registros,
        hoje=hoje
    )
# ROTA: Deletar
@app.route("/deletar/<int:id>")
def deletar(id):

    registro = Diario.query.filter_by(
    id=id,
    usuario_id=session['usuario_id']
    ).first()

    if registro: 
        db.session.delete(registro)
        db.session.commit()

    return redirect("/diario")

# ROTA: Editar: AMANDA 
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):

    registro = Diario.query.filter_by(
        id=id,
        usuario_id=session['usuario_id']
    ).first()

    if registro is None:
        return redirect("/diario")

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

    texto = request.form["texto"].strip()

    if texto == "":
        return render_template(
            "diario.html",
            registros=Diario.query.filter_by(
            usuario_id=session['usuario_id']).all(),
            hoje=datetime.now().strftime("%d de %B"),
            erro="Insira uma mensagem antes de salvar."
        )

    novo = Diario(
        texto=texto,
        usuario_id=session['usuario_id']
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
    # precisa estar logado pra saber de quem é o humor que vai salvar
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        humor = request.form['humor']
        # marco o humor com o id de quem está logado
        registro = RegistroHumor(humor=humor, usuario_id=session['usuario_id'])
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
    # Luiz: precisa de login pra mostrar só o humor deste usuário
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    humores = {
        "Feliz": 0,
        "Calmo": 0,
        "Neutro": 0,
        "Triste": 0
    }

    rotulo_por_nota = {1: "Triste", 2: "Triste", 3: "Neutro", 4: "Calmo", 5: "Feliz"}

    # só os registros deste usuário nos últimos 7 dias
    limite = date.today() - timedelta(days=7)
    registros = RegistroHumor.query.filter(
        RegistroHumor.usuario_id == session['usuario_id'],
        RegistroHumor.data >= limite
    ).all()
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
    # Luiz: precisa de login pra mostrar só o humor deste usuário
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    humores = {
        "Muito Feliz": 0,
        "Bem": 0,
        "Neutro": 0,
        "Triste": 0,
        "Muito Triste": 0
    }

    rotulo_por_nota = {1: "Muito Triste", 2: "Triste", 3: "Neutro", 4: "Bem", 5: "Muito Feliz"}

    # só os registros deste usuário nos últimos 30 dias
    limite = date.today() - timedelta(days=30)
    registros = RegistroHumor.query.filter(
        RegistroHumor.usuario_id == session['usuario_id'],
        RegistroHumor.data >= limite
    ).all()
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


# ==============================================================================
# RESPONSÁVEL: Eduardo
# TELA: Exercícios de Respiração
# ==============================================================================
import threading
import time
from flask import jsonify

# Variáveis globais para controlar o estado da respiração
atividade_rodando = False
estado_atual = {
    "fase": "Clique abaixo para começar",
    "tempo": "0s",
    "porcentagem": 0
}

def ciclo_respiracao():
    global atividade_rodando, estado_atual
    
    fases = [
        {"nome": "Inspire pelo nariz...", "tempo": 4},
        {"nome": "Segure o ar nos pulmões...", "tempo": 7},
        {"nome": "Expire lentamente pela boca...", "tempo": 8}
    ]
    
    ciclos_totais = 4
    tempo_total_tecnica = (4 + 7 + 8) * ciclos_totais
    tempo_decorrido_geral = 0

    for ciclo in range(ciclos_totais):
        if not atividade_rodando:
            break
            
        for fase in fases:
            if not atividade_rodando:
                return
                
            nome_fase = fase["nome"]
            tempo_fase = fase["tempo"]
            
            for segundo in range(tempo_fase, -1, -1):
                if not atividade_rodando:
                    return
                
                porcentagem = (tempo_decorrido_geral / tempo_total_tecnica) * 100
                
                estado_atual["fase"] = nome_fase
                estado_atual["tempo"] = f"{segundo}s"
                estado_atual["porcentagem"] = porcentagem
                
                if segundo > 0:
                    time.sleep(1)
                    tempo_decorrido_geral += 1

    if atividade_rodando:
        estado_atual["fase"] = "Parabéns!<br>Atividade Concluída 🎉"
        estado_atual["tempo"] = "Fim"
        estado_atual["porcentagem"] = 100
        atividade_rodando = False


@app.route('/respiracao')
def respiracao():
    return render_template('respiracao.html')


@app.route('/alternar', methods=['POST'])
def alternar_atividade():
    global atividade_rodando, estado_atual
    
    if atividade_rodando:
        atividade_rodando = False
        estado_atual = {
            "fase": "Clique abaixo para começar",
            "tempo": "0s",
            "porcentagem": 0
        }
        return jsonify({"botao": "Iniciar/Parar"})
    else:
        atividade_rodando = True
        thread_atual = threading.Thread(target=ciclo_respiracao)
        thread_atual.daemon = True
        thread_atual.start()
        return jsonify({"botao": "Parar"})


@app.route('/status', methods=['GET'])
def obter_status():
    global estado_atual
    return jsonify(estado_atual)

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
    # debug fica desligado pra rodar em servidor público (hospedagem).
    # se quiser desenvolver localmente com recarregamento automático,
    # troque pra debug=True só na sua máquina.
    app.run(debug=False)
