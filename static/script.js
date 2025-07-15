document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatWindow = document.getElementById('chat-window');
    const initialView = document.querySelector('.initial-view');
    const suggestionButtons = document.querySelectorAll('.suggestion');

    let isChatStarted = false;

    // Função para adicionar uma mensagem à janela do chat
    const addMessage = (message, sender) => {
        // Remove a tela inicial se for a primeira mensagem
        if (initialView && !isChatStarted) {
            chatWindow.innerHTML = ''; // Limpa a janela de chat
            isChatStarted = true;
        }

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'ai-message');
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);

        // Rola para a mensagem mais recente
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    // Evento de envio do formulário
    // Substitua o listener de evento 'submit' antigo por este:

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = messageInput.value.trim();

    if (userMessage) {
        addMessage(userMessage, 'user');
        messageInput.value = '';
        
        // Exibe um indicador de que a IA está "pensando"
        addMessage('Pensando...', 'ai-thinking');

        try {
            // Chama o nosso backend Python
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error('A resposta da rede não foi boa.');
            }

            const data = await response.json();
            
            // Remove a mensagem "Pensando..."
            const thinkingMessage = document.querySelector('.ai-thinking');
            if (thinkingMessage) {
                thinkingMessage.remove();
            }

            // Adiciona a resposta real do backend
            addMessage(data.answer, 'ai');

        } catch (error) {
            console.error('Erro ao chamar a API:', error);
            const thinkingMessage = document.querySelector('.ai-thinking');
            if (thinkingMessage) {
                // Remove a mensagem "Pensando..." e exibe uma de erro
                thinkingMessage.textContent = 'Desculpe, ocorreu um erro ao conectar com o servidor.';
                thinkingMessage.classList.remove('ai-thinking');
                thinkingMessage.classList.add('ai-error');
            }
        }
    }
});

    // Evento de clique nos botões de sugestão
    suggestionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const suggestionText = button.textContent;
            messageInput.value = suggestionText;
            chatForm.requestSubmit(); // Envia o formulário com o texto da sugestão
        });
    });
});