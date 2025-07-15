# app.py

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
# Define o caminho absoluto para o projeto
basedir = os.path.abspath(os.path.dirname(__file__))
# Configura a URI do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy(app)

# --- MODELO DO BANCO DE DADOS ---
class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # keywords armazena palavras-chave separadas por vírgula, ex: "eleitor,titulo"
    keywords = db.Column(db.String(300), nullable=False)
    response = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Knowledge {self.keywords}>'

# --- ROTAS DA APLICAÇÃO ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.get_json().get('message')

    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem recebida'}), 400

    # Lógica de busca por palavra-chave
    response_text = find_response_for_message(user_message)
    
    return jsonify({'answer': response_text})

def find_response_for_message(message):
    """
    Busca no banco de dados uma resposta baseada nas palavras da mensagem do usuário.
    """
    # Converte a mensagem para minúsculas para busca case-insensitive
    message_words = set(message.lower().split())

    # Busca todos os registros do banco de dados
    all_knowledge = KnowledgeBase.query.all()

    for entry in all_knowledge:
        # Pega as palavras-chave do registro e as separa
        entry_keywords = set(entry.keywords.lower().split(','))
        
        # Se qualquer palavra da mensagem do usuário estiver nas palavras-chave do registro...
        if not message_words.isdisjoint(entry_keywords):
            return entry.response # ...retorna a resposta correspondente

    # Se nenhum laço encontrar uma correspondência, retorna uma resposta padrão
    return "Desculpe, não entendi sua pergunta. Pode tentar reformulá-la com outras palavras?"

# O if __name__ == '__main__' foi removido para seguir a convenção do 'flask run',
# mas pode ser adicionado de volta se você preferir rodar com 'python app.py'