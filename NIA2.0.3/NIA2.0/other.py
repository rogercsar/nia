import streamlit as st
from streamlit_chat import message
#Importando BOT
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot import filters
from chatterbot.conversation import Statement
from difflib import SequenceMatcher
import yaml

# Configurar o chatbot
chatbot = ChatBot('Nia', 
            filters=[filters.get_recent_repeated_responses],
            storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
            logic_adapters = [
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter',
                'chatterbot.logic.BestMatch',
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Desculpe, ainda estou aprendendo!',
                    'maximum_similarity_threshold': 0.90
                }
            ]
            )

trainer = ListTrainer(chatbot)

conversa = ['Oie', 'Olá', 'Meu nome é NIA', 'Como vai ?', 'Tudo bem e contigo ?', 'Maravilha!', 
            'Qual seu nome ?', 'Que interessante!', 'Como posso te ajudar hoje ?',
            'Estou aprendendo', 'Vamos trabalhar', 'Posso pesquisar sobre isso',
            'Acho que consigo sim', 'Você sabe muito', 'Não faz isso comigo', 'Sem problemas',
            'Você só pensa nisso', 'Talvez mais tarde', 'Não me apressa', 'Combinado então',
            'Muito obrigado', 'Disponha', 'Gentileza da sua parte', 'Incrível isso',
            'Vai dar certo', 'Ainda temos muito trabalho', 'Me perdoa por isso', 'Até logo',
            'Vou aguardar ansiosa', 'Tchau', 'Era o que eu estava esperando'
            'Bom dia', 'Boa tarde', 'Boa noite', 'Até logo', 'Beijos', 'Fico feliz'
            'Quem sabe um dia', 'O que podemos concluir ?', 'Não entendi']

trainer.train(conversa)

# Função para adicionar estilo personalizado
# Função para adicionar estilo personalizado
def add_custom_css():
    st.markdown(
        """
        <style>
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Aplica o estilo CSS customizado
add_custom_css()

# Inicializa as listas de mensagens
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Função para obter a resposta do bot usando ChatterBot
def get_bot_response(user_message):
    response = chatbot.get_response(user_message)
    return str(response)

messages = st.container(height=360, border=True)

# Cria o contêiner de rolagem para as mensagens
with st.container():
    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
    # Exibe as mensagens na tela
    for msg in st.session_state['messages']:
        message(msg['message'], is_user=msg['is_user'])
    st.markdown('</div>', unsafe_allow_html=True)


# Interface do usuário para entrada de texto
user_input = st.text_area("Você:", key="user_input_area", value="", height=100)

if st.button('Enviar'):
    if user_input:
        # Adiciona a mensagem do usuário à lista de mensagens
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        # Gera a resposta do bot e adiciona à lista de mensagens
        bot_response = chatbot.get_response(user_input)
        st.session_state['messages'].append({'message': bot_response, 'is_user': False})
        # Redesenha a entrada de texto, essencialmente limpando-a
        st.experimental_rerun()