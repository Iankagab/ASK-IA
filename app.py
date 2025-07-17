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

# --- MODELO DO BANCO DE DADOS ---
class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keywords = db.Column(db.String(300), nullable=False)  # palavras separadas por vírgula
    response = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Knowledge {self.keywords}>'

# --- INTEGRAÇÃO FLASK-ADMIN ---
admin = Admin(app, name='Painel Admin', template_mode='bootstrap3')
admin.add_view(ModelView(KnowledgeBase, db.session))

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
    return jsonify({'answer': response_text})

def find_response_for_message(message):
    message_words = set(message.lower().split())
    all_knowledge = KnowledgeBase.query.all()

    for entry in all_knowledge:
        entry_keywords = set(k.strip() for k in entry.keywords.lower().split(','))
        if not message_words.isdisjoint(entry_keywords):
            return entry.response

    return "Desculpe, não entendi sua pergunta. Pode tentar reformulá-la com outras palavras?"

# Se quiser rodar com 'python app.py' (opcional)
if __name__ == '__main__':
    app.run(debug=True)
