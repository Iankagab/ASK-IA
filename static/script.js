document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chat-form');
  const messageInput = document.getElementById('message-input');
  const chatWindow = document.getElementById('chat-window');
  const sendButton = document.getElementById('send-button');

  let firstInteractionDone = false;
  let hasClickedOption = false;

  const addBubble = (html, cls) => {
    const initialView = document.querySelector('.initial-view');
    if (initialView) initialView.remove();
    const el = document.createElement('div');
    el.classList.add('message', cls);
    el.innerHTML = html;
    chatWindow.appendChild(el);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return el;
  };

  const clearButtonsList = () => {
    chatWindow.querySelectorAll('.buttons-list').forEach(el => el.remove());
    chatWindow.querySelectorAll('.actions-row').forEach(el => el.remove()); // remove linha de ações
  };

  const renderOptions = (labels) => {
    clearButtonsList();
    const wrapper = document.createElement('div');
    wrapper.classList.add('buttons-list');
    labels.forEach(label => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.classList.add('option-btn');
      btn.textContent = label;
      btn.addEventListener('click', () => handleOption(label));
      wrapper.appendChild(btn);
    });
    chatWindow.appendChild(wrapper);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  };

  const fetchOpcoes = async () => {
    const res = await fetch('/opcoes');
    if (!res.ok) throw new Error('Falha ao carregar opções');
    const data = await res.json();
    return data.opcoes || [];
  };

  const renderActionsRow = () => {
    if (!hasClickedOption) return;

    const existing = chatWindow.querySelector('.actions-row');
    if (existing) existing.remove();

    const row = document.createElement('div');
    row.classList.add('actions-row');

    const backBtn = document.createElement('button');
    backBtn.type = 'button';
    backBtn.classList.add('back-btn');
    backBtn.textContent = 'Retornar as opções';
    backBtn.addEventListener('click', async () => {
      clearButtonsList();
      try {
        const opts = await fetchOpcoes();
        renderOptions(opts.length ? opts : ['civil', 'criminal', 'eleitoral', 'federal', 'trabalhista']);
      } catch {
        renderOptions(['civil', 'criminal', 'eleitoral', 'federal', 'trabalhista']);
      }
      renderActionsRow();
    });

    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.classList.add('clear-btn');
    clearBtn.textContent = 'Apagar conversa';
    clearBtn.addEventListener('click', resetConversation);

    row.appendChild(backBtn);
    row.appendChild(clearBtn);

    chatWindow.appendChild(row);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  };

  const renderInitialView = () => {
    chatWindow.innerHTML = '';
    const initial = document.createElement('div');
    initial.classList.add('initial-view');
    initial.innerHTML = `<h2>Olá cidadão,<br>como posso te ajudar?</h2>`;
    chatWindow.appendChild(initial);

    const inputBar = document.querySelector('.chat-input-area');
    if (inputBar) inputBar.classList.remove('hidden');

    chatWindow.scrollTop = chatWindow.scrollHeight;
  };

  const resetConversation = () => {
    firstInteractionDone = false;
    hasClickedOption   = false;
    renderInitialView();
  };

  const handleOption = async (opcao) => {
    const thinking = addBubble('Buscando endereço...', 'ai-thinking');
    try {
      const res = await fetch(`/endereco?opcao=${encodeURIComponent(opcao)}`);
      if (!res.ok) throw new Error('Falha na resposta do servidor');
      const data = await res.json();
      thinking.remove();

      if (data.count && Array.isArray(data.resultados) && data.resultados.length > 0) {
        const rows = data.resultados.map(r => {
          const tel = r.telefone && String(r.telefone).trim() ? r.telefone : "-";
          return `
            <tr>
              <td class="td-orgao"><strong>${r.nome}</strong></td>
              <td class="td-end">${r.endereco_completo}</td>
              <td class="td-tel">${tel}</td>
            </tr>
          `;
        }).join("");

        addBubble(`
          <div class="addr-table">
            <table class="result-table" aria-label="Órgãos e endereços encontrados">
              <thead>
                <tr>
                  <th>Órgão</th>
                  <th>Endereço</th>
                  <th>Telefone</th>
                </tr>
              </thead>
              <tbody>${rows}</tbody>
            </table>
          </div>
        `, 'ai-endereco');
      } else {
        addBubble(data.message || `Não encontrei endereços para <strong>${opcao}</strong>.`, 'ai-error');
      }

      hasClickedOption = true;
      renderActionsRow(); 
    } catch (err) {
      console.error(err);
      thinking.textContent = 'Erro ao buscar endereço.';
      thinking.classList.remove('ai-thinking');
      thinking.classList.add('ai-error');
      hasClickedOption = true;
      renderActionsRow();
    }
  };

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (firstInteractionDone) return;

    const text = messageInput.value.trim();
    if (!text) return;

    addBubble(text, 'user-message');
    messageInput.value = '';
    sendButton.disabled = true;

    addBubble(`
      <strong>Olá Cidadão!</strong><br/>
      Sou o <strong>ASK-IA</strong> e estou aqui para te auxiliar a encontrar o órgão competente mais próximo de você de acordo com a sua necessidade.<br/><br/>
      Abaixo uma lista dos serviços jurídicos que podem te ajudar:
    `, 'ai-greeting');

    try {
      const opcoes = await fetchOpcoes();
      renderOptions(opcoes.length ? opcoes : ['civil', 'criminal', 'eleitoral', 'federal', 'trabalhista']);
    } catch {
      renderOptions(['civil', 'criminal', 'eleitoral', 'federal', 'trabalhista']);
    } finally {
      firstInteractionDone = true;
      const inputBar = document.querySelector('.chat-input-area');
      if (inputBar) inputBar.classList.add('hidden');
      sendButton.disabled = false;
    }
  });

  if (!chatWindow.querySelector('.initial-view') && chatWindow.children.length === 0) {
    renderInitialView();
  }
});

