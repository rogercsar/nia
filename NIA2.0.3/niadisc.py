import discord
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import filters

from conv import *

#Import Socket
from socket import *
import socket
import platform

#Import News Data 
from newsdataapi import NewsDataApiClient

#Import Request
import json, requests

import os

from datetime import datetime

import wikipedia

from io import StringIO
import numpy as np

from deep_translator import GoogleTranslator

import brazilcep
import asyncio
from brasilapi import BrasilAPI

from GoogleNews import GoogleNews

alpha_api = 'KS1U4RZ56M42S6A9'

# Defina o caminho do banco de dados
db_directory = 'C:\\Users\\roger\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\chatterbot\\storage'
db_file = 'new_database.db'
db_path = os.path.join(db_directory, db_file)

# Certifique-se de que o diretório existe
if not os.path.exists(db_directory):
    os.makedirs(db_directory)
    
# Configurar o chatbot
bot = ChatBot(
    'Nia',
    filters=[filters.get_recent_repeated_responses],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=f'sqlite:///{db_path}',
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


trainer.train(conversa)

API_KEY = '7ec1ae1461da5ec0324095bd682667d7'

api = NewsDataApiClient(apikey="5465a83eb76f4178a6b7235cb061ad66")

# Configurar o bot do Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    user_message = message.content
    bot_response = bot.get_response(user_message)

    if user_message:
        if any(word in list_words_sads for word in user_message.strip().split(" ")):
            sad_word = user_message.casefold().strip().split(" ")
            good_word = np.array(frases_motivacionais)
            motivacional = np.random.choice(good_word)
            # Verifica se qualquer palavra na entrada do usuário está na lista de palavras tristes
            if any(word in sad_word for word in list_words_sads):
                await message.channel.send(motivacional)
            else:
                list_words_sads.append(sad_word)

        elif any(word in list_words_bad for word in user_message.casefold().strip().split(" ")):
            bad_word = user_message.casefold().strip().split(" ")
            at_word = np.array(frases_atencao)
            att_word = np.random.choice(at_word)
            if any(word in bad_word for word in list_words_bad):
                await message.channel.send(att_word)
            else:
                list_words_bad.append(bad_word)

        elif any(word in list_words_happy for word in user_message.casefold().strip().split(" ")):
            happy_word = user_message.casefold().strip().split(" ")
            lh_word = np.array(frases_alegres)
            flh_word = np.random.choice(lh_word)
            if any(word in happy_word for word in list_words_happy):
                await message.channel.send(flh_word)
            else:
                list_words_happy.append(happy_word)

        elif any(word in list_words_restless for word in user_message.casefold().strip().split(" ")):
            rest_word = user_message.casefold().strip().split(" ")
            lr_word = np.array(frases_calmas)
            flr_word = np.random.choice(lr_word)
            if any(word in rest_word for word in list_words_restless):
                await message.channel.send(flr_word)
            else:
                list_words_restless.append(rest_word)     

        elif 'tempo em' in user_message.casefold():
            list_cidade = None      
            try:     
                for cidade in cidades:
                    if cidade.casefold() in user_message.casefold():
                        list_cidade = cidade
                        break
                if list_cidade:
                    city = user_message.split(list_cidade, 1)
                    city_name = list_cidade
                elif not city:
                    await message.channel.send("Por favor, forneça o nome da cidade.")
                    return
                link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang=pt_br"
                req = requests.get(link)
                req_dic = req.json()
                if req.status_code == 200:
                    desc = req_dic['weather'][0]['description']
                    temp = req_dic['main']['temp'] - 273.15  # Convertendo de Kelvin para Celsius
                    clima = [f"Cidade: {city_name}", f"Descrição: {desc}", f"Temperatura: {temp:.2f}°C"]
                    
                    def format_list_as_string(items):
                        return "\n".join([f"- {item}" for item in items])
                    
                    prev = format_list_as_string(clima)
                    await message.channel.send(prev)
                else:
                    await  message.channel.send("Não consegui encontrar a previsão para essa cidade. Verifique o nome e tente novamente.")
            except Exception as e:
                await  message.channel.send(f"Ocorreu um erro ao buscar a previsão do tempo: {str(e)}")
        
        elif 'que horas são' in user_message.casefold():
            # Responde com a hora atual
            current_time = datetime.now().strftime("%H:%M:%S")
            await  message.channel.send(f"São {(current_time)}.")

        elif 'dia é hoje' in user_message.casefold():
            # Responde com o dia atual
            current_date = datetime.now().strftime("%d/%m/%Y")
            await  message.channel.send(f"Hoje é {(current_date)}.")

        elif 'lista de prompts' in user_message.casefold():
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            lista = format_list_as_string(conversa)
            await  message.channel.send(f" {(lista)}")

        elif 'wiki' in str(user_message):
            wikipedia.set_lang("pt")
            # Pesquisa na Wikipedia e exibe o resumo do artigo
            query = user_message[len('pesquisar na wikipedia:'):]
            resp = wikipedia.page(query)
            await  message.channel.send(f" {(resp.content)}")

        elif 'sistema' in user_message.casefold():
            so = platform.system() 
            host = platform.node()
            proc = platform.machine()
            extras = platform.platform()
            ip = socket.gethostbyname(socket.gethostname())
            info = [so, host, proc, extras, ip]

            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            sys = format_list_as_string(info)

            await message.channel.send(sys)

        elif 'valor do' in str(user_message.casefold()):
            list_symbols = None      
            try:     
                for symbol in acoes_symbols:
                    if symbol.casefold() in user_message.casefold():
                        list_symbols = symbol
                        break
                if list_symbols:
                    acao = user_message.split(list_symbols, 1)
                    acao_name = list_symbols
                elif not acao:
                    await message.channel.send("Por favor, forneça o nome da ação.")
                    return
                base_url = 'https://www.alphavantage.co/query'
                params = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': acao,
                    'interval': '1min',
                    'apikey': alpha_api
                }
                response = requests.get(base_url, params=params)
                data = response.json()
                
                if 'Time Series (1min)' in data:
                    latest_timestamp = list(data['Time Series (1min)'].keys())[0]
                    latest_data = data['Time Series (1min)'][latest_timestamp]
                    price = latest_data['1. open']
                    await message.channel.send(f"O preço atual da ação {acao} é ${price}")
                else:
                    await message.channel.send("Não foi possível obter os dados. Verifique o símbolo da ação e tente novamente.")

            except Exception as e:
                    await message.channel.send(f"Ocorreu um erro ao buscar a ação: {str(e)}")

        elif 'traduza' in user_message.casefold():
            tradutor = GoogleTranslator(source= "en", target= "pt")
            list_en = None      
            try:     
                for en in list_words_en:
                    if en.casefold() in user_message.casefold():
                        list_en = en
                        break
                if list_en:
                    word = user_message.split(list_en, 1)
                    word_en = list_en
                elif not word:
                    await message.channel.send("Por favor, forneça o um idioma válido.")
                    return
                traducao = tradutor.translate(word_en)
                await message.channel.send(f"A tradução para {word_en} é {traducao}.")       

            except Exception as e:
                await message.channel.send(f"Ocorreu um erro ao buscar a tradução: {str(e)}.")

        elif 'consulta' in user_message.casefold():
            lcep = None 
            for num in list_cep:
                if num.casefold() in user_message.casefold():
                    lcep = num
                    break
            if lcep:
                wcep = user_message.split(lcep, 1)
                cep = lcep
               
                async def run():
                    async with BrasilAPI() as client:
                        result = await client.ceps.get(cep)
                        endereco=repr(result)

                        await  message.channel.send(f"{endereco}")
                asyncio.run(run())

            else:
                await message.channel.send("Por favor, forneça o um cep válido.")
                return


        elif 'notícias' in user_message.casefold():
            list_nt = None      
            try:     
                for i in list_noticias:
                    if i.casefold() in user_message.casefold():
                        list_nt = i
                        break
                if list_nt:
                    word = user_message.split(list_nt, 1)
                    word_nt = list_nt               
                    googleNews = GoogleNews(period='d')
                    googleNews.set_lang('pt')
                    googleNews.search(word_nt)
                    result = googleNews.result()

                    # Formatar os resultados como uma lista de strings
                    news_list = [f"Título: {item['title']}\nConteúdo: {item.get('desc', 'N/A')}\nData: {item.get('date', 'N/A')}\n Link: {item['link']}" for item in result]
                    formatted_news = "\n\n".join(news_list)
                
                    await message.channel.send(f"{formatted_news}")

                else:
                    await message.channel.send("Por favor, forneça o termo válido para pesquisa.")
                    return

            except Exception as e:
                await message.channel.send(f"Ocorreu um erro ao buscar a notícia: {str(e)}")

        
        elif user_message in conversa:
            # Adiciona a mensagem do usuário à lista de mensagens
            await message.channel.send(str(bot_response))

        else:
            conversa.append(str(user_message))
            # Gera a resposta do bot e adiciona à lista de mensagens
            bot_response = bot.get_response(str(user_message))
            await message.channel.send(str(bot_response))  

# Token do bot (substitua pelo seu próprio token)
TOKEN = 'MTI0MzkwMzI0NjA5NjEzODMyMA.GDg8Sn.Rp-Gw7u_by5uO4o4rqy6_yLEaXHV-P6Var2XLI'

client.run(TOKEN)
