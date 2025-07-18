from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'minha-chave-secreta'  # necessário para Flask-Admin

# Inicializa o banco
db = SQLAlchemy(app)

# --- MODELOS DO BANCO DE DADOS ---
class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.String(300), nullable=False)  # palavras separadas por vírgula
    response = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Knowledge {self.keywords}>'

class UserResponse(db.Model):
    __tablename__ = 'userresponse'  # força o nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    response_given = db.Column(db.Text, nullable=False)

class Orgao(db.Model):
    __tablename__ = 'orgao'  # nome da tabela
    id = db.Column(db.Integer, primary_key=True)
    orgao = db.Column(db.String(100), nullable=False)
    cidade_estado = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)

# --- INTEGRAÇÃO FLASK-ADMIN ---
admin = Admin(app, name='Painel Admin', template_mode='bootstrap3')
admin.add_view(ModelView(KnowledgeBase, db.session))
admin.add_view(ModelView(UserResponse, db.session))
admin.add_view(ModelView(Orgao, db.session))

# --- ROTAS DA APLICAÇÃO ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.get_json().get('message')

    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem recebida'}), 400

    response_text = find_response_for_message(user_message)

    # Salva resposta do usuário + resposta do chatbot no banco (tabela userresponse)
    user_response = UserResponse(user_message=user_message, response_given=response_text)
    db.session.add(user_response)
    db.session.commit()

    return jsonify({'answer': response_text})

def find_response_for_message(message):
    message_words = set(message.lower().split())
    all_knowledge = KnowledgeBase.query.all()

    for entry in all_knowledge:
        entry_keywords = set(k.strip() for k in entry.keywords.lower().split(','))
        if not message_words.isdisjoint(entry_keywords):
            return entry.response

    return "Desculpe, não entendi sua pergunta. Pode tentar reformulá-la com outras palavras?"

def buscar_orgaos_com_base_em_respostas():
    # Busca todas as respostas armazenadas
    respostas = UserResponse.query.all()

    atributos = set()
    for r in respostas:
        palavras = r.response_given.lower().split()
        atributos.update(palavras)

    orgaos = Orgao.query.filter(Orgao.attribute.in_(atributos)).all()
    return orgaos

@app.route('/orgaos')
def orgaos():
    orgaos_encontrados = Orgao.query.all()  # ou use a sua lógica de busca
    lista = []
    for o in orgaos_encontrados:
        lista.append({
            'orgao': o.orgao,
            'cidade_estado': o.cidade_estado,
            'endereco': o.endereco
        })
    return jsonify({'orgaos': lista})


# Rodar a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

