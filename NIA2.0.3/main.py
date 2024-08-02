from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot import filters
from chatterbot.conversation import Statement
from difflib import SequenceMatcher

import streamlit as st

# Create a new chat bot named Charlie
bot = ChatBot('Nia', 
            filters=[filters.get_recent_repeated_responses],
            storage_adapter = 'chatterbot.storage.SQLStorageAdapter',
            logic_adapters = [
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
           

def chat():
    # Get a response to the input text 'I would like to book a flight.'
    st.title('NIA')

    prompt = st.chat_input(placeholder='Digite sua mensagem')

    messages = st.container(height=360, border=True)

    chatlist = []
    
    if prompt != '':
       
        messages.chat_message('Roger', avatar='roger.ico').write(str(prompt) + '\n')
        response = bot.get_response(str(prompt))
       
        messages.chat_message('Nia',  avatar='nia.ico').write(str(response) + '\n')
    
    else:
        messages.chat_message('Nia',  avatar='nia.ico').write('Desculpe, ainda não entendi.')

    


chat()



