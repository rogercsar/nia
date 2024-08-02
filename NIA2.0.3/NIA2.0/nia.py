from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import filters
import streamlit as st

from datetime import datetime

#Import Play
from playerm import *

import sys
import os

import wikipedia
from googlesearch import search

# Configurar o chatbot
bot = ChatBot(
    'Nia',
    filters=[filters.get_recent_repeated_responses],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Desculpe, ainda estou aprendendo!',
            'maximum_similarity_threshold': 0.90
        }
    ]
)

trainer = ListTrainer(bot)

conversa = [
    'Oie', 'Olá', 'Meu nome é NIA', 'Como vai?', 'Tudo bem e contigo?', 'Maravilha!',
    'Qual seu nome?', 'Que interessante!', 'Como posso te ajudar hoje?',
    'Estou aprendendo', 'Vamos trabalhar', 'Posso pesquisar sobre isso',
    'Acho que consigo sim', 'Você sabe muito', 'Não faz isso comigo', 'Sem problemas',
    'Você só pensa nisso', 'Talvez mais tarde', 'Não me apressa', 'Combinado então',
    'Muito obrigado', 'Disponha', 'Gentileza da sua parte', 'Incrível isso',
    'Vai dar certo', 'Ainda temos muito trabalho', 'Me perdoa por isso', 'Até logo',
    'Vou aguardar ansiosa', 'Tchau', 'Era o que eu estava esperando',
    'Bom dia', 'Boa tarde', 'Boa noite', 'Até logo', 'Beijos', 'Fico feliz',
    'Quem sabe um dia', 'O que podemos concluir?', 'Não entendi'
]

trainer.train(conversa)

# Define o ícone da aplicação
st.set_page_config(page_title="NIA", page_icon="nia.ico")


st.markdown("<h1 style='text-align: center; font-size: 16px; color: #ffffff; background-color: #800080; margin-bottom: 80px; border: 1px solid #800080; border-radius: 10px'>NIA</h1>", unsafe_allow_html=True)  

def search_wikipedia(query):
    # Realiza a pesquisa na Wikipedia e retorna o texto do resumo do artigo encontrado
    try:
        summary = wikipedia.summary(query)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # Se houver ambiguidade, retorna uma mensagem informando ao usuário
        return "A busca retornou múltiplos resultados. Por favor, seja mais específico."

def chat():       
    # Inicializa a lista de mensagens apenas uma vez, quando a aplicação é iniciada
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
                  
    # Interface do usuário para entrada de texto
    user_input = st.chat_input("Mensagem para NIA") 
    bot_response = bot.get_response(str(user_input))
    if user_input in conversa:
        # Adiciona a mensagem do usuário à lista de mensagens
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': str(bot_response), 'is_user': False})
        conversa.append(str(user_input))
    elif 'que horas são' in str(user_input):
            # Responde com a hora atual
            current_time = datetime.now().strftime("%H:%M:%S")
            st.session_state['messages'].append({'message': user_input, 'is_user': True})
            st.session_state['messages'].append({'message': f"São {current_time}.", 'is_user': False})
    elif 'que dia é hoje' in str(user_input):
        # Responde com o dia atual
        current_date = datetime.now().strftime("%d/%m/%Y")
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': f"Hoje é {current_date}.", 'is_user': False})
    
    elif 'lista de prompts' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': ''.join(conversa), 'is_user': False})
    
    elif 'nota' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Notepad', 'is_user': False})
        os.startfile('notepad.exe')
        
    elif 'navegador' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Google', 'is_user': False})
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
    
    elif 'youtube' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo YouTube', 'is_user': False})
        os.startfile('https://www.youtube.com/')
    
    elif 'acesso remoto' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Anydesk', 'is_user': False})
        os.startfile('C:\Program Files (x86)\AnyDesk\AnyDesk.exe')
        
    elif 'documento' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Word', 'is_user': False})
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word 2016')
    
    elif 'planilha' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Excel', 'is_user': False})
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel 2016')
    
    elif 'powerpoint' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo PowerPoint', 'is_user': False})
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint 2016')
    
    elif 'access' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Access', 'is_user': False})
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Access 2016')
    
    elif 'outlook' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Outlook', 'is_user': False})
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Outlook 2016')
    
    elif 'obs' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo OBS', 'is_user': False})
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OBS Studio\OBS Studio (64bit)')
    
    elif 'zimbra' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo Zimbra', 'is_user': False})
        os.startfile('https://mail.grupocanopus.com.br/')
        
    elif 'cec' in str(user_input):
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': 'Abrindo CEC', 'is_user': False})
        os.startfile('http://10.2.6.22/CecWeb/')
    
    elif 'wiki' in str(user_input):
        # Pesquisa na Wikipedia e exibe o resumo do artigo
        query = user_input[len('pesquisar na wikipedia:'):]
        summary = search_wikipedia(query)
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': summary, 'is_user': False})
    
    else:
        # Gera a resposta do bot e adiciona à lista de mensagens
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        st.session_state['messages'].append({'message': str(bot_response), 'is_user': False})
        conversa.append(str(user_input))

    # Cria o contêiner de rolagem para as mensagens
    with st.container():
        for msg in st.session_state['messages']:
            if msg['is_user']:
                st.chat_message("Roger", avatar='roger.ico').write(f" {msg['message']}")
            else:
                st.chat_message("Nia", avatar='nia.ico').write(f" {msg['message']}")

    user_input = ''


chat()
