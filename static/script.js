// static/script.js - VERSÃO DE DIAGNÓSTICO

document.addEventListener('DOMContentLoaded', () => {
    console.log("O script.js foi carregado e está sendo executado.");

    // Seletores dos elementos do DOM
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatWindow = document.getElementById('chat-window');
    const suggestionButtons = document.querySelectorAll('.suggestion');

    // =========== PONTO DE VERIFICAÇÃO 1 ===========
    // Vamos verificar se os elementos estão sendo encontrados corretamente.
    console.log("Formulário do chat encontrado:", chatForm);
    console.log("Campo de input encontrado:", messageInput);
    console.log("Botões de sugestão encontrados:", suggestionButtons);
    // ===============================================

    // Deixaremos as outras funções aqui por enquanto.
    const addMessage = (message, senderClass) => {
        const initialView = document.querySelector('.initial-view');
        if (initialView) {
            initialView.remove();
        }
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', senderClass);
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return messageElement;
    };

    const handleBackendCommunication = async (messageText) => {
        if (!messageText) return;
        addMessage(messageText, 'user-message');
        messageInput.value = '';
        const thinkingMessageElement = addMessage('Pensando...', 'ai-thinking');
        try {
            const response = await fetch('/ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: messageText }), });
            if (!response.ok) throw new Error('Falha na resposta do servidor.');
            const data = await response.json();
            thinkingMessageElement.remove();
            addMessage(data.answer, 'ai-message');
        } catch (error) {
            console.error('Erro ao chamar a API:', error);
            thinkingMessageElement.textContent = 'Desculpe, ocorreu um erro.';
            thinkingMessageElement.classList.remove('ai-thinking');
            thinkingMessageElement.classList.add('ai-error');
        }
    };

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const userMessage = messageInput.value.trim();
        handleBackendCommunication(userMessage);
    });

    // =========== PONTO DE VERIFICAÇÃO 2 ===========
    // Este código é ultra simplificado. Ele vai APENAS tentar colocar
    // o texto no campo, sem enviar o formulário.
    console.log("Adicionando listeners de clique aos botões...");

    suggestionButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            // Impede qualquer comportamento padrão do formulário ou do botão.
            event.preventDefault(); 
            
            const suggestionText = button.textContent;

            console.log("--- BOTÃO CLICADO! ---");
            console.log("Texto da sugestão:", suggestionText);

            // A linha mais importante para o nosso teste:
            messageInput.value = suggestionText;
            
            console.log("Valor do input foi DEFINIDO para:", messageInput.value);
        });
    });
});