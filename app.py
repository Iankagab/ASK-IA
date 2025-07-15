# app.py

from flask import Flask, render_template, request, jsonify

# Inicializa a aplicação Flask
app = Flask(__name__)

# Rota principal que renderiza a página do chat
@app.route('/')
def home():
    """
    Esta função é chamada quando alguém acessa a URL raiz ('/').
    Ela renderiza e retorna o arquivo 'index.html' da pasta 'templates'.
    """
    return render_template('index.html')

# Rota para receber as perguntas do usuário (nosso endpoint da API)
@app.route('/ask', methods=['POST'])
def ask():
    """
    Esta função é chamada via JavaScript (fetch).
    Ela espera um pedido POST na URL '/ask'.
    """
    # Pega os dados JSON enviados pelo frontend
    data = request.get_json()
    user_message = data.get('message')

    # Validação simples
    if not user_message:
        return jsonify({'error': 'Nenhuma mensagem recebida'}), 400

    # --- SIMULAÇÃO DA IA (FASE 2) ---
    # Aqui, vamos substituir pela chamada à OpenAI na próxima fase.
    # Por enquanto, apenas devolvemos uma resposta fixa do backend.
    ai_response = f"Resposta do backend para a sua pergunta: '{user_message}'"
    
    # Retorna a resposta em formato JSON
    return jsonify({'answer': ai_response})

# Inicia o servidor quando o script é executado diretamente
if __name__ == '__main__':
    app.run(debug=True)