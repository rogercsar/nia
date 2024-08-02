import holidays.countries
import serial.tools
import serial.tools.list_ports
import streamlit as st
from streamlit_modal import Modal
from st_chat_message import message
from streamlit_monaco import st_monaco
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot import filters
from datetime import datetime
import os
from os import system
import wikipedia
import time
from tkinter import filedialog as fd
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
#Import News Data 
from newsdataapi import NewsDataApiClient
#Import Request
import json, requests
import re
import threading
#Import Socket
from socket import *
import socket
import platform
import smtplib
import streamlit as st
import pandas as pd
import numpy as np
from conv import *
from alarms import *
from io import StringIO
import random
from deep_translator import GoogleTranslator
import brazilcep
import asyncio
from brasilapi import BrasilAPI
from GoogleNews import GoogleNews
import wave
from playsound import playsound
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import calendar
import openrouteservice
from openrouteservice import convert
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy import distance
from plyer import notification
from plyer import audio
#Pygame
import pygame
from pygame import mixer
import pyautogui
import ctypes
import hashlib
from marvel import Marvel
import serial
from pyfirmata import Arduino, util
import psutil as ps
from pytube import YouTube
import webbrowser
import holidays
import sidrapy
import locale
from streamlit_elements import elements, mui, html
from streamlit_elements import media
from youtubesearchpython import VideosSearch
from urllib.parse import quote
from bs4 import BeautifulSoup

alpha_api = 'KS1U4RZ56M42S6A9'

marvel_particular = '7a4f512e5653276139d1e9f485103c41ce688d11'
marvel_public = 'ceddf751ddeef3fb50d69b5c98d4765f'

marvel = Marvel(PUBLIC_KEY='ceddf751ddeef3fb50d69b5c98d4765f', 
                PRIVATE_KEY='7a4f512e5653276139d1e9f485103c41ce688d11')

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

engine = pyttsx3.init()

# Inicializa o cliente da OpenRouteService com a chave da API
client = openrouteservice.Client(key='5b3ce3597851110001cf62486ec377a429e2473987ea5bd98da0d101')

API_KEY = '7ec1ae1461da5ec0324095bd682667d7'

api = NewsDataApiClient(apikey="5465a83eb76f4178a6b7235cb061ad66")

FIPE_API_BASE_URL = "https://parallelum.com.br/fipe/api/v1"

geolocator = Nominatim(user_agent="myGeocoder")

# Define o ícone da aplicação
st.set_page_config(page_title="NIA", page_icon="nia.ico", layout="centered", initial_sidebar_state="expanded")

def mic():
    # Função responsável por ouvir e reconhecer a fala
    # Habilita o microfone para ouvir o usuário
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        # Chama a função de redução de ruído disponível na speech_recognition
        microfone.adjust_for_ambient_noise(source)                                                      
        # Avisa ao usuário que está pronto para ouvir
        print("Diga alguma coisa: ")
        # Armazena a informação de áudio na variável
        audio = microfone.listen(source)
        try:
            # Passa o áudio para o reconhecedor de padrões do speech_recognition
            frase = microfone.recognize_google(audio, language='pt-BR')
            # Após alguns segundos, retorna a frase falada
            print("Você disse: " + frase)
            # Envia a frase reconhecida para o chat do Streamlit (se aplicável)
            st.session_state['messages'].append({'message': frase, 'is_user': True})
            bot_response = bot.get_response(str(frase))
            st.session_state['messages'].append({'message': str(bot_response), 'is_user': False})
        # Caso não tenha reconhecido o padrão de fala, exibe esta mensagem
        except sr.UnknownValueError:
            st.session_state['messages'].append({'message': "Não entendi", 'is_user': False})
        # Captura erros de requisição ao serviço de reconhecimento de fala
        except sr.RequestError as e:
            st.session_state['messages'].append({'message': f"Erro ao requisitar os resultados do serviço Google Speech Recognition; {e}", 'is_user': False})
        

def consultar_fipe(veiculo_tipo, marca, modelo, ano):
    """
    Função para consultar a tabela FIPE usando a API.

    Args:
    veiculo_tipo (str): Tipo de veículo ('carros', 'motos', 'caminhoes').
    marca (str): Marca do veículo.
    modelo (str): Modelo do veículo.
    ano (str): Ano do veículo.

    Returns:
    dict: Dados do veículo obtidos na consulta.
    """
    try:
        # Endpoint para obter as marcas
        marcas_url = f"{FIPE_API_BASE_URL}/{veiculo_tipo}/marcas"
        marcas_response = requests.get(marcas_url).json()

        # Encontrar a marca selecionada pelo usuário
        marca_id = next((item['codigo'] for item in marcas_response if item['nome'].casefold() == marca.casefold()), None)
        if not marca_id:
            return "Marca não encontrada."

        # Endpoint para obter os modelos
        modelos_url = f"{FIPE_API_BASE_URL}/{veiculo_tipo}/marcas/{marca_id}/modelos"
        modelos_response = requests.get(modelos_url).json()

        # Encontrar o modelo selecionado pelo usuário
        modelo_id = next((item['codigo'] for item in modelos_response['modelos'] if item['nome'].casefold() == modelo.casefold()), None)
        if not modelo_id:
            return "Modelo não encontrado."

        # Endpoint para obter os anos do modelo
        anos_url = f"{FIPE_API_BASE_URL}/{veiculo_tipo}/marcas/{marca_id}/modelos/{modelo_id}/anos"
        anos_response = requests.get(anos_url).json()

        # Encontrar o ano selecionado pelo usuário
        ano_codigo = next((item['codigo'] for item in anos_response if ano in item['nome']), None)
        if not ano_codigo:
            return "Ano não encontrado."

        # Endpoint para obter os dados do veículo
        veiculo_url = f"{FIPE_API_BASE_URL}/{veiculo_tipo}/marcas/{marca_id}/modelos/{modelo_id}/anos/{ano_codigo}"
        veiculo_response = requests.get(veiculo_url).json()

        return veiculo_response
    except Exception as e:
        return f"Erro ao consultar a tabela FIPE: {str(e)}"
    

def buscar_primeiro_video(termo):
    videos_search = VideosSearch(termo, limit=1)
    results = videos_search.result()
    
    if results['result']:
        first_video = results['result'][0]
        video_url = f"https://www.youtube.com/watch?v={first_video['id']}"
        return video_url
    return None

def search_drug(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        return None
    
def traduzir(texto, source_lang, target_lang):
    tradutor = GoogleTranslator(source=source_lang, target=target_lang)
    return tradutor.translate(texto)

def search_disease_government(disease_name):
    try:
        url = f"http://dados.gov.br/api/3/action/package_search?q={disease_name}"
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
        if response.content:
            data = response.json()
            return data['result']['results']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição: {e}")
        return None

def obter_coordenadas(endereco):
    geolocator = Nominatim(user_agent="myGeocoder")
    try:
        location = geolocator.geocode(endereco)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return None

def get_code_example():
        # Retorna um exemplo de código Python
        code = """\
        def saudacao(nome):
            return f'Olá, {nome}!'

        nome_usuario = 'Roger'
        print(saudacao(nome_usuario))"""
        return code

# Configurando a língua da Wikipedia
wikipedia.set_lang("pt")

def get_wikipedia_summary(query):
    try:
        page = wikipedia.page(query)
        return page.summary
    except wikipedia.DisambiguationError as e:
        st.session_state['messages'].append({'message': f"A consulta '{query}' retornou múltiplos resultados: {e.options}", 'is_user': False})
    except wikipedia.PageError:
        st.session_state['messages'].append({'message': f"Não foi possível encontrar uma página para '{query}'.", 'is_user': False})
    except Exception as e:
        st.session_state['messages'].append({'message': f"Ocorreu um erro ao buscar na Wikipedia: {e}", 'is_user': False})

def generate_calendar(year, month=None):
    cal = calendar.TextCalendar(calendar.SUNDAY)
    if month:
        try:
            # Gera o calendário para um mês específico
            month_calendar = cal.formatmonth(year, month)
            return f"```\n{month_calendar}\n```"
        except calendar.IllegalMonthError:
            st.session_state['messages'].append({'message': "Por favor, forneça um mês válido (1-12).", 'is_user': False})
    else:
        # Gera o calendário para o ano inteiro
        year_calendar = cal.formatyear(year, 2, 1, 1, 3)
        return f"```\n{year_calendar}\n```"


# Função para converter nomes em siglas
def get_country_code(country_name):
    return country_mapping.get(country_name.lower(), country_name.upper())

def get_state_code(state_name):
    return state_mapping.get(state_name.lower(), state_name.upper())

def process_user_input(user_input):
    user_input = user_input.casefold()
    if 'wiki' in user_input or 'me fale sobre' in user_input or 'o que você sabe sobre' in user_input:
        # Extrai a consulta, aqui assumindo que a estrutura é "wiki: [consulta]"
        query = user_input.replace('wiki', '').replace('me fale sobre', '').replace('o que você sabe sobre', '').strip()
        if query:
            response = get_wikipedia_summary(query)
        else:
            response = "Por favor, forneça um termo para pesquisar na Wikipedia."
        st.session_state['messages'].append({'message': response, 'is_user': False})
    
    elif 'calendário do ano' in user_input.casefold():
        try:
            parts = user_input.split('calendário do ano')[-1].strip().split()
            year = int(parts[0])
            if len(parts) > 1:
                month = int(parts[1])
                response = generate_calendar(year, month)
            else:
                response = generate_calendar(year)
        except (ValueError, IndexError):
                response = "Por favor, forneça um ano válido e, opcionalmente, um mês (1-12)."
        st.session_state['messages'].append({'message': response, 'is_user': False})

    elif any(word in list_code for word in user_input.casefold().strip().split(" ")):
        code_example = get_code_example()
        response = f"Aqui está um exemplo de código Python:\n\n```python\n{code_example}\n```"
        st.session_state['messages'].append({'message': response, 'is_user': False})

    elif 'trajeto de' in user_input.casefold():
       
        # Criar um geolocalizador com Nominatim
        geolocator = Nominatim(user_agent="myGeocoder")

        # Extração dos endereços do input do usuário
        endereco_origem = user_input.split('de')[-1].split('para')[0].strip()
        endereco_destino = user_input.split('para')[-1].strip()

        print(f"Endereço de origem: {endereco_origem}")
        print(f"Endereço de destino: {endereco_destino}")

        # Obtém as coordenadas dos endereços de origem e destino
        origem_coords = obter_coordenadas(endereco_origem)
        destino_coords = obter_coordenadas(endereco_destino)

        if not origem_coords or not destino_coords:
            st.session_state['messages'].append({'message': "Não foi possível obter as coordenadas para um dos endereços fornecidos.", 'is_user': False})
            return None

        # Inicializa o cliente da OpenRouteService com a chave da API
        client = openrouteservice.Client(key='5b3ce3597851110001cf62486ec377a429e2473987ea5bd98da0d101')

        # Calcula as direções entre os pontos de origem e destino
        directions_result = client.directions((origem_coords[0], origem_coords[1]),
                                            (destino_coords[0], destino_coords[1]),
                                            profile='driving-car')

        # Obtém a distância da rota em metros e converte para quilômetros
        distancia = directions_result['routes'][0]['summary']['distance'] / 1000

        if distancia is not None:
            st.session_state['messages'].append({'message': f"A distância entre os dois pontos é de aproximadamente {distancia:.2f} km.", 'is_user':False})


    elif 'criar alarme' in user_input.casefold() or 'definir alarme' in user_input.casefold():
        try:
            # Extrair o horário e a data do alarme da entrada do usuário
            alarm_msg = user_input.split('para')[-1].strip()
            alarm_data = user_input.split('do dia')[-1].split('para')[0].strip()
            alarm_time = user_input.split('alarme para as')[-1].split('do dia')[0].strip()
            
            # Converter a data para o formato datetime
            alarm_datetime = datetime.strptime(alarm_data + " " + alarm_time, '%d/%m/%Y %H:%M')
            
            def check_alarm(alarm_datetime):
                """
                Verifica se é hora de acionar o alarme com base na hora e data fornecidas.
                """
                while True:
                    now = datetime.now()
                    if now >= alarm_datetime:
                        notification.notify(
                            title="Alarme",
                            message= f"{alarm_msg}",
                            app_name="Nia",
                            app_icon="nia.ico",
                            timeout=10
                        )
                        if alarm_time == f"12:00":
                            mixer.init()
                            mixer.music.load('nahoradopapa.mp3')
                            mixer.music.play()
                        elif alarm_time == f"13:50":
                            mixer.init()
                            mixer.music.load('notify_alarm.mp3')
                            mixer.music.play()
                        break
                    time.sleep(30)  # Espera 30 segundos antes de verificar novamente

            # Iniciar a verificação do alarme em um novo thread para não bloquear o bot
            alarm_thread = threading.Thread(target=check_alarm, args=(alarm_datetime,))
            alarm_thread.start()

            st.session_state['messages'].append({'message': f"Alarme definido para {alarm_datetime.strftime('%d/%m/%Y' +' às ' + '%H:%M')}.", 'is_user':False})
            with open('alarms.py'):
                alarm = f"Alarme: {alarm_datetime.strftime('%d/%m/%Y' +' às ' + '%H:%M')}."
                list_alarms.append(alarm)
        except Exception as e:
            st.session_state['messages'].append({'message': f"Erro ao definir o alarme: {str(e)}", 'is_user':False})

    elif 'consultar fipe' in user_input.casefold():
        # Exemplo de input: "consultar fipe carros Honda Civic 2020"
        partes = user_input.split()
        if len(partes) >= 5:
            veiculo_tipo = partes[2]
            marca = partes[3]
            modelo = partes[4]
            ano = partes[5]
            result = consultar_fipe(veiculo_tipo, marca, modelo, ano)          
           
            st.session_state['messages'].append({'message': f"{result}", 'is_user':False}) 
        else:
            st.session_state['messages'].append({'message': "Por favor, forneça o tipo de veículo, marca, modelo e ano para a consulta.", 'is_user':False}) 

    else:
        # Aqui você pode adicionar outros processamentos do input do usuário
        pass    

if st.button('Falar'):
    mic()

def chat():

    # Interface do usuário para entrada de texto
    user_input = st.chat_input("Mensagem para NIA") 

    # Inicializa a lista de mensagens apenas uma vez, quando a aplicação é iniciada
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    if 'show_player' not in st.session_state:
        st.session_state['show_player'] = False

    if 'show_mail' not in st.session_state:
        st.session_state['show_mail'] = False
    
    if 'show_data' not in st.session_state:
        st.session_state['show_data'] = False

    if 'show_code' not in st.session_state:
        st.session_state['show_code'] = False

    if user_input:
        st.session_state['messages'].append({'message': user_input, 'is_user': True})
        bot_response = bot.get_response(str(user_input))
        if any(word in list_words_sads for word in user_input.casefold().strip().split(" ")):
            sad_word = user_input.casefold().strip().split(" ")
            good_word = np.array(frases_motivacionais)
            motivacional = np.random.choice(good_word)
            # Verifica se qualquer palavra na entrada do usuário está na lista de palavras tristes
            if any(word in sad_word for word in list_words_sads):
                st.session_state['messages'].append({'message': motivacional, 'is_user': False})
            else:
                list_words_sads.append(sad_word)
        
        elif any(word in list_words_bad for word in user_input.casefold().strip().split(" ")):
            bad_word = user_input.casefold().strip().split(" ")
            at_word = np.array(frases_atencao)
            att_word = np.random.choice(at_word)
            if any(word in bad_word for word in list_words_bad):
                st.session_state['messages'].append({'message': att_word, 'is_user': False})
            else:
                list_words_bad.append(bad_word)

        elif any(word in list_words_happy for word in user_input.casefold().strip().split(" ")):
            happy_word = user_input.casefold().strip().split(" ")
            lh_word = np.array(frases_alegres)
            flh_word = np.random.choice(lh_word)
            if any(word in happy_word for word in list_words_happy):
                st.session_state['messages'].append({'message': flh_word, 'is_user': False})
            else:
                list_words_happy.append(happy_word)
        
        elif any(word in list_words_restless for word in user_input.casefold().strip().split(" ")):
            rest_word = user_input.casefold().strip().split(" ")
            lr_word = np.array(frases_calmas)
            flr_word = np.random.choice(lr_word)
            if any(word in rest_word for word in list_words_restless):
                st.session_state['messages'].append({'message': flr_word, 'is_user': False})
            else:
                list_words_restless.append(rest_word)
        
        elif 'que horas são' in user_input.casefold():
            # Responde com a hora atual
            current_time = datetime.now().strftime("%H:%M:%S")
            st.session_state['messages'].append({'message': f"São {current_time}.", 'is_user': False})

        elif 'que dia é hoje' in user_input.casefold():
            # Responde com o dia atual
            current_date = datetime.now().strftime("%d/%m/%Y")
            st.session_state['messages'].append({'message': f"Hoje é {current_date}.", 'is_user': False})
        
        elif 'lista de prompts' in user_input.casefold():
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            lista = format_list_as_string(conversa)
            st.session_state['messages'].append({'message': f"\n\nMinha lista atualizada:\n{lista}", 'is_user': False})
        
        elif 'nota' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Notepad', 'is_user': False})
            os.startfile('notepad.exe')

        elif 'abrir arduino' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo IDE Arduino', 'is_user': False})
            os.startfile('C:\\Program Files\\Arduino IDE\\Arduino IDE.exe')

        elif 'abrir vscode' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo IDE Arduino', 'is_user': False})
            os.startfile('C:\\Users\\roger\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
        
        elif 'abrir desktop' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo a pasta Desktop', 'is_user': False})
            os.startfile('D:\\Área de Trabalho')
        
        elif 'abrir documentos' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo a pasta Documentos', 'is_user': False})
            os.startfile('D:\\Documentos')

        elif 'abrir downloads' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo a pasta Documentos', 'is_user': False})
            os.startfile('D:\\Downloads')
        
        elif 'abrir imagens' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo a pasta Imagens', 'is_user': False})
            os.startfile('D:\\Imagens')

        elif 'abrir musicas' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo a pasta Músicas', 'is_user': False})
            os.startfile('D:\\Músicas')

        elif 'abrir vídeos' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo a pasta Vídeos', 'is_user': False})
            os.startfile('D:\\Vídeos')
            
        elif 'navegador' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Google', 'is_user': False})
            os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        
        elif 'youtube' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo YouTube', 'is_user': False})
            os.startfile('https://www.youtube.com/')
        
        elif 'acesso remoto' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Anydesk', 'is_user': False})
            os.startfile('C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe')
            
        elif 'documento' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Word', 'is_user': False})
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word 2016')
        
        elif 'planilha' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Excel', 'is_user': False})
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel 2016')
        
        elif 'powerpoint' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo PowerPoint', 'is_user': False})
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint 2016')
        
        elif 'access' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Access', 'is_user': False})
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Access 2016')
        
        elif 'outlook' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Outlook', 'is_user': False})
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Outlook 2016')
        
        elif 'obs' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo OBS', 'is_user': False})
            os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OBS Studio\\OBS Studio (64bit)')
        
        elif 'zimbra' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo Zimbra', 'is_user': False})
            os.startfile('https://mail.grupocanopus.com.br/')
            
        elif 'cec' in user_input.casefold():
            st.session_state['messages'].append({'message': 'Abrindo CEC', 'is_user': False})
            os.startfile('http://10.2.6.22/CecWeb/')
        
        elif 'wiki' in user_input.casefold() or 'me fale sobre' in user_input.casefold() or 'o que você sabe sobre' in user_input.casefold():
            process_user_input(user_input.casefold())                
        
        elif 'player' in user_input.casefold():
            st.session_state['show_player'] = True
            st.session_state['show_mail'] = False
            st.session_state['messages'].append({'message': 'Abrindo Player', 'is_user': False})

        elif 'tempo hoje em' in user_input.casefold() or 'clima hoje em' in user_input.casefold(): 
            list_cidade = None      
            try:     
                for cidade in cidades:
                    if cidade.casefold() in user_input.casefold():
                        list_cidade = cidade
                        break
                if list_cidade:
                    city = user_input.split(list_cidade, 1)
                    city_name = list_cidade
                elif not city:
                    st.session_state['messages'].append({'message': "Por favor, forneça o nome da cidade.", 'is_user': False})
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
                    st.session_state['messages'].append({'message': f"{prev}", 'is_user': False})
                else:
                    st.session_state['messages'].append({'message': "Não consegui encontrar a previsão para essa cidade. Verifique o nome e tente novamente.", 'is_user': False})
            except Exception as e:
                st.session_state['messages'].append({'message': f"Ocorreu um erro ao buscar a previsão do tempo: {str(e)}", 'is_user': False})
            

        elif 'info do sistema' in user_input.casefold() or 'informações do pc' in user_input.casefold():
            so = platform.system() 
            host = platform.node()
            proc = platform.machine()
            extras = platform.platform()
            ip = socket.gethostbyname(socket.gethostname())
            info = [so, host, proc, extras, ip ]
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            sys = format_list_as_string(info)
            st.session_state['messages'].append({'message': f"\n\nInfos do PC:\n{sys}", 'is_user': False})

        elif 'telegram' in user_input.casefold():
           os.startfile('C:\\Users\\roger\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe')
           st.session_state['messages'].append({'message': 'Abrindo Telegram', 'is_user': False})

        elif 'enviar email' in user_input.casefold():
            st.session_state['show_mail'] = True
            st.session_state['show_player'] = False
            st.session_state['messages'].append({'message': 'Abrindo email', 'is_user': False})

        elif 'abrir dados' in user_input.casefold() or 'abrir tabela' in user_input.casefold():
            st.session_state['show_data'] = True
            st.session_state['messages'].append({'message':  'Abrindo visualização de dados', 'is_user': False})
            
        elif 'fechar dados' in user_input.casefold() or 'fechar tabela' in user_input.casefold():
            st.session_state['show_data'] = False
            st.session_state['messages'].append({'message':  'Fechando visualização de dados', 'is_user': False})

        elif 'mercado financeiro' in user_input.casefold():
            # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=ITUB4.SAO&apikey={alpha_api}&datatype=csv'
            r = requests.get(url)

            tabela = pd.read_csv(StringIO(r.text))
            st.session_state['messages'].append({'message':  'Dados mercado financeiro', 'is_user': False})
            st.write(tabela)

        elif 'valor do' in user_input.casefold() or 'preço da ação' in user_input.casefold():
            list_symbols = None      
            try:     
                for symbol in acoes_symbols:
                    if symbol.casefold() in user_input.casefold():
                        list_symbols = symbol
                        break
                if list_symbols:
                    acao = user_input.split(list_symbols, 1)
                    acao_name = list_symbols
                elif not acao:
                    st.session_state['messages'].append({'message': "Por favor, forneça o nome da ação.", 'is_user': False})
                    return
                base_url = 'https://www.alphavantage.co/query'
                params = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': acao_name,
                    'interval': '1min',
                    'apikey': alpha_api
                }
                response = requests.get(base_url, params=params)
                data = response.json()
                
                if 'Time Series (1min)' in data:
                    latest_timestamp = list(data['Time Series (1min)'].keys())[0]
                    latest_data = data['Time Series (1min)'][latest_timestamp]
                    price = latest_data['1. open']
                    st.session_state['messages'].append({'message': f"O preço atual da ação {acao_name} é ${price}", 'is_user': False})
                else:
                    st.session_state['messages'].append({'message': "Não foi possível obter os dados. Verifique o símbolo da ação e tente novamente.", 'is_user': False})

            except Exception as e:
                st.session_state['messages'].append({'message': f"Ocorreu um erro ao buscar a ação: {str(e)}", 'is_user': False})

        elif 'traduza' in user_input.casefold():
            tradutor = GoogleTranslator(source= "en", target= "pt")
            list_en = None      
            try:     
                for en in list_words_en:
                    if en.casefold() in user_input.casefold():
                        list_en = en
                        break
                if list_en:
                    word = user_input.split(list_en, 1)
                    word_en = list_en
                else:
                    st.session_state['messages'].append({'message': "Por favor, forneça o um idioma válido.", 'is_user': False})
                    return
                traducao = tradutor.translate(word_en)
                st.session_state['messages'].append({'message': f"A tradução para {word_en} é {traducao}", 'is_user': False})       

            except Exception as e:
                st.session_state['messages'].append({'message': f"Ocorreu um erro ao buscar a ação: {str(e)}", 'is_user':False})


        elif 'consulta cep' in user_input.casefold():           
            lcep = None 
            for num in list_cep:
                if num.casefold() in user_input.casefold():
                    lcep = num
                    break 
                                
            if lcep:
                wcep = user_input.split(lcep, 1)
                cep = lcep
               
                async def run():
                    async with BrasilAPI() as client:
                        result = await client.ceps.get(cep)
                        endereco=repr(result)

                        st.session_state['messages'].append({'message': f"{endereco}", 'is_user': False})
                asyncio.run(run())             

            else:
                st.session_state['messages'].append({'message': "Por favor, forneça o um cep válido.", 'is_user': False})
                return


        elif 'notícias' in user_input.casefold():
            list_nt = None      
            try:     
                for i in list_noticias:
                    if i.casefold() in user_input.casefold():
                        list_nt = i
                        break
                if list_nt:
                    word = user_input.split(list_nt, 1)
                    word_nt = list_nt               
                    googleNews = GoogleNews(period='d')
                    googleNews.set_lang('pt')
                    googleNews.search(word_nt)
                    result = googleNews.result()

                    # Formatar os resultados como uma lista de strings
                    news_list = [f"Title: {item['title']}\n Conteúdo: {item.get('desc', 'N/A')}\n Data: {item.get('date', 'N/A')}\n Link: {item['link']}" for item in result]
                    formatted_news = "\n\n".join(news_list)
                
                    st.session_state['messages'].append({'message': f"{formatted_news}", 'is_user':False})

                else:
                    st.session_state['messages'].append({'message': "Por favor, forneça o termo válido para pesquisa.", 'is_user': False})
                    return

            except Exception as e:
                st.session_state['messages'].append({'message': f"Ocorreu um erro ao buscar a notícia: {str(e)}", 'is_user':False})


        elif 'imagem do espaço' in user_input.casefold():
            api_url = 'https://api.nasa.gov/planetary/apod?api_key=IBDqMUQcVfOoQ3TmvqkEdGBPGaNC2ixUjUtrCKUp'
            req = requests.get(api_url)

            if req.status_code == 200:
                dados = req.json()
                img = [f"Título: {dados['title']}\n Dados: {dados['copyright']}\n Data: {dados['date']}\n Explicação: {dados['explanation']}\n Url: {dados['url']}"]
                st.session_state['messages'].append({'message': f"{img}", 'is_user':False})
        
        elif 'converter de' in user_input.casefold():
            list_md = None
            try:
                for i in list_moedas:
                    if i.casefold() in user_input.casefold():
                        list_md = i
                        break

                if list_md:
                    # Constrói a URL da API para o par de moedas encontrado
                    url_api = f'https://economia.awesomeapi.com.br/last/{list_md}'
                    # Realiza a solicitação à API
                    req = requests.get(url_api)
                    # Processa a resposta da API
                    conversao = req.json()

                    # Extração dos dados relevantes da resposta
                    moeda_base, moeda_cotacao = list_md.split('-')
                    key = f"{moeda_base}{moeda_cotacao}"
                    if key in conversao:
                        info_moeda = conversao[key]
                        valor = info_moeda['bid']
                        resposta = f"1 {moeda_base} é igual a {valor} {moeda_cotacao}."

                        # Adiciona a resposta na sessão do Streamlit
                        st.session_state['messages'].append({'message': resposta, 'is_user': False})
                    else:
                        st.session_state['messages'].append({'message': "Não foi possível obter a conversão solicitada.", 'is_user': False})
                else:
                    st.session_state['messages'].append({'message': "Moeda não encontrada na lista de moedas suportadas.", 'is_user': False})
            
            except Exception as e:
                st.session_state['messages'].append({'message': f"Ocorreu um erro ao converter as moedas: {str(e)}", 'is_user': False})   

        elif 'o que você faz' in user_input.casefold() or 'quais suas funções' in user_input.casefold():
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            lista = format_list_as_string(list_do)
            st.session_state['messages'].append({'message': f"\n\nAlgumas coisas que eu faço:\n{lista}", 'is_user': False})  

        elif 'calendário' in user_input.casefold():
            process_user_input(user_input)
            
        elif 'código' in user_input.casefold():
            process_user_input(user_input)   

        elif 'trajeto de' in user_input.casefold():
            process_user_input(user_input)       

        elif 'endereço' in user_input.casefold() or 'localização' in user_input.casefold():
            endereco = user_input.split('endereço do')[-1].strip().split()
            location = geolocator.geocode(endereco)
            st.session_state['messages'].append({'message': location, 'is_user': False})

        elif 'criar alarme' in user_input.casefold() or 'definir alarme' in user_input.casefold():
            process_user_input(user_input)

        elif 'quero um conselho' in user_input.casefold():
            url = 'https://api.adviceslip.com/advice'
            tradutor = GoogleTranslator(source= "en", target= "pt")
            def randomadvice():
                Data = requests.get(url)
                json_data = Data.json()
                random_advice = json_data['slip']
                traducao = tradutor.translate(random_advice['advice'])
                st.session_state['messages'].append({'message': traducao, 'is_user': False})
            randomadvice()

        elif 'consultar fipe' in user_input.casefold():
            process_user_input(user_input)

        elif 'ameaças em tempo real' in user_input.casefold():
            iframe_html = (
                '<iframe width="602" height="433" src="https://cybermap.kaspersky.com/pt/widget/dynamic/dark" '
                'frameborder="0"></iframe>'
            )
            st.session_state['messages'].append({'message': iframe_html, 'is_user': False})

        elif 'mostrar alarmes' in user_input.casefold():
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            lista = format_list_as_string(list_alarms)
            if lista == None:
                st.session_state['messages'].append({'message': lista, 'is_user': False})
            else:
                st.session_state['messages'].append({'message': "Nennhum alarme definido ainda.", 'is_user': False})

        elif 'redes wifi' in user_input.casefold():
            resultado = os.system('netsh wlan show profile')
            if resultado == 0:
                st.session_state['messages'].append({'message': "Nenhuma rede wifi conectada.", 'is_user': False})
            else:
                st.session_state['messages'].append({'message': resultado, 'is_user': False})

        elif 'bloquear tela' in user_input.casefold():
            time.sleep(3) 
            ctypes.windll.user32.LockWorkStation()
            
        elif 'desenhe alguma coisa' in user_input.casefold():             
            pyautogui.hotkey('win', 'm')
            time.sleep(2) 
            pyautogui.moveTo(40, 740)
            pyautogui.click()
            time.sleep(3)
            pyautogui.moveTo(540, 400)
            pyautogui.click()
            distance = 200
            time.sleep(10)
            while distance > 0:
                pyautogui.drag(distance, 0, duration=0.5)   # move right
                distance -= 5
                pyautogui.drag(0, distance, duration=0.5)   # move down
                pyautogui.drag(-distance, 0, duration=0.5)  # move left
                distance -= 5
                pyautogui.drag(0, -distance, duration=0.5)  # move up         
        
        elif 'escreva alguma coisa' in user_input.casefold():
            time.sleep(2)
            pyautogui.hotkey('win', 'm')
            time.sleep(3)
            os.startfile('notepad.exe')
            time.sleep(3)
            pyautogui.typewrite('Oie, eu sou Nia. \n', interval=0.25)
            pyautogui.typewrite('E voce esta vendo um exemplo de texto. \n', interval=0.25)
            pyautogui.typewrite('Xau xau.', interval=0.25)
            st.session_state['messages'].append({'message': "Escrevi um texto de exemplo.", 'is_user': False})

        elif 'tirar print' in user_input.casefold():
            imgprint = pyautogui.screenshot()
            imgprint.save('meuscreenshoot.png')
            st.session_state['messages'].append({'message': "Captura de tela tirada e salva.", 'is_user': False})                    

        elif 'editor de registros' in user_input.casefold():
            os.startfile('C:\\Windows\\regedit.exe')     
            st.session_state['messages'].append({'message': "Abrindo regedit", 'is_user': False})      

        elif 'resolução do monitor' in user_input.casefold():
            size = pyautogui.size()
            st.session_state['messages'].append({'message': size, 'is_user': False})

        elif 'comunicar arduino' in user_input.casefold():
            ports = serial.tools.list_ports.comports()
            port = ports[0].device
            arduino = serial.Serial(port, 9600, timeout=1)
            try:
               req = arduino.read_until()
               st.session_state['messages'].append({'message': f"Conectado na porta {port}. Resultado da resposta serial: {req}", 'is_user': False}) 
            except serial.SerialException as e:
               st.session_state['messages'].append({f"Falha ao conectar: {e}."})

        elif 'abrir pasta da ti' in user_input.casefold():
            time.sleep(1)
            pyautogui.hotkey('winleft', 'r')
            time.sleep(1) 
            pyautogui.typewrite(r'\\172.16.10.53', interval=0.25)
            pyautogui.press('enter')
            st.session_state['messages'].append({'message': "Abrindo Pasta da TI", 'is_user': False})

        elif 'abrir pasta da rede' in user_input.casefold():
            time.sleep(1)
            pyautogui.hotkey('winleft', 'r')
            time.sleep(1) 
            pyautogui.typewrite(r'\\10.2.6.16', interval=0.25)
            pyautogui.press('enter')
            st.session_state['messages'].append({'message': "Abrindo Pasta do Servidor", 'is_user': False})
        
        elif 'ping no servidor' in user_input.casefold():
            time.sleep(1)
            pyautogui.hotkey('winleft', 'r')
            time.sleep(1) 
            pyautogui.typewrite('cmd', interval=0.25)
            pyautogui.press('enter')
            time.sleep(2)
            pyautogui.typewrite('ping 10.2.6.16', interval=0.25)
            pyautogui.press('enter')

        elif 'gerenciador de tarefas' in user_input.casefold():
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'shift', 'esc')
            st.session_state['messages'].append({'message': "Abrindo Gerenciador de Tarefas", 'is_user': False})

        elif 'processos do sistema' in user_input.casefold():      
            # Executar o comando 'tasklist' e capturar a saída
            tasklist_output = os.popen('tasklist').read()
            # Dividir a saída em linhas e armazená-las em uma lista
            process_list = tasklist_output.split('\n')
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            lista = format_list_as_string(process_list)   
            st.session_state['messages'].append({'message': f"Processos em execução:\n\n{lista}", 'is_user': False})  

        elif 'abrir configurações' in user_input.casefold():
            time.sleep(2)
            pyautogui.hotkey('winleft', 'i')  
            st.session_state['messages'].append({'message': "Abrindo Configurações", 'is_user': False})

        elif 'alterar plano de fundo' in user_input.casefold():
            time.sleep(1)
            pyautogui.hotkey('win', 'm')
            time.sleep(1)
            pyautogui.moveTo(550, 250)
            time.sleep(1)
            pyautogui.click(button='right')  
            time.sleep(1)
            pyautogui.move(100,155)
            pyautogui.click()
            st.session_state['messages'].append({'message': "Alterando o Fundo", 'is_user': False})

        elif 'pesquisar vídeo' in user_input.casefold():
            try:
                termo = user_input.split('de')[-1].strip()
                
                if termo:  # Verifica se o termo não está vazio
                    video_url = buscar_primeiro_video(termo)
                    if video_url:
                        st.session_state['messages'].append({
                            'message': f"Abrindo o vídeo de {termo}: {video_url}",
                            'is_user': False,
                            'video_link': video_url
                        })
                    else:
                        st.session_state['messages'].append({
                            'message': f"Nenhum vídeo encontrado para o termo: {termo}.",
                            'is_user': False
                        })
                else:
                    st.session_state['messages'].append({
                        'message': "Nenhum termo de pesquisa fornecido.",
                        'is_user': False
                    })
            except Exception as e:
                st.session_state['messages'].append({
                    'message': f"Erro ao tentar abrir o vídeo: {str(e)}",
                    'is_user': False
                })

        elif 'feriados' in user_input.casefold():
            data_input = user_input.split('do ano')[-1].split('em')[0].strip()
            country_name = user_input.split('em')[-1].split('no estado de')[0].strip()
            state_name = user_input.split('no estado de')[-1].strip() if 'no estado de' in user_input else None            
            country_code = get_country_code(country_name)
            state_code = get_state_code(state_name) if state_name else None            
            try:
                year = int(data_input)
                if state_code:
                    holidays_obj = holidays.country_holidays(country_code, subdiv=state_code, years=year)
                else:
                    holidays_obj = holidays.country_holidays(country_code, years=year)                
                list_fer = [f"{date}: {name}" for date, name in holidays_obj.items()]                
                if list_fer:
                    def format_list_as_string(items):
                        return "\n".join([f"- {item}" for item in items])
                    lista = format_list_as_string(list_fer)
                    st.session_state['messages'].append({'message': f"Os feriados para {year} em {country_name}{f' no estado de {state_name}' if state_name else ''}:\n\n{lista}", 'is_user': False})
                else:
                    st.session_state['messages'].append({'message': f"Não foram encontrados feriados para o ano {year}.", 'is_user': False})
            except ValueError:
                st.session_state['messages'].append({'message': "Por favor, insira um ano válido.", 'is_user': False}) 

        elif 'ibge' in user_input.casefold():
            link = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"

            requisicao = requests.get(link)
            infos = requisicao.json()
            def format_list_as_string(items):
                return "\n".join([f"- {item}" for item in items])
            lista = format_list_as_string(infos)
            st.session_state['messages'].append({'message': lista, 'is_user': False})

        elif 'população estimada' in user_input.casefold():
            municipio = user_input.split('população estimada de')[-1].strip().casefold()
            max_retries = 5  # Número máximo de tentativas
            for attempt in range(max_retries):
                try:
                    # Obter dados de população estimada da SIDRA
                    data = sidrapy.get_table(table_code='4709', territorial_level="6", ibge_territorial_code="all", variable='93')
                    
                    # Exibir as colunas disponíveis para verificação
                    #st.session_state['messages'].append({'message': f"Colunas disponíveis no dataframe: {data.columns.tolist()}", 'is_user': False})
                    
                    # Substitui as colunas pela primeira observação
                    data.columns = data.iloc[0]
                    # Remove a primeira linha (agora cabeçalho)
                    data = data.iloc[1:]
                    
                    # Seleciona apenas as colunas necessárias
                    data = data[['Município', 'Valor', 'Ano']]  
                    # Renomeia as colunas
                    data.columns = ['municipio', 'populacao', 'ano']
                    # Separa município e UF
                    data[['municipio', 'UF']] = data['municipio'].str.split(' - ', expand=True)

                    # Filtra pelo município
                    municipio_data = data[data['municipio'].str.contains(municipio, case=False, na=False)]

                    if not municipio_data.empty:
                        municipio_data = municipio_data.sort_values(by='ano', ascending=False).iloc[0]  # Pega o ano mais recente

                        # Formata o valor da população
                        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                        populacao_formatada = locale.format_string('%d', int(municipio_data['populacao']), grouping=True)

                        st.session_state['messages'].append({
                            'message': f"A população estimada de {municipio_data['municipio']} ({municipio_data['UF']}) em {municipio_data['ano']} é de {populacao_formatada} habitantes.",
                            'is_user': False
                        })
                    else:
                        st.session_state['messages'].append({
                            'message': f"Não foram encontrados dados de população para o município de {municipio}.",
                            'is_user': False
                        })
                    break  # Saia do loop se a tentativa for bem-sucedida
                except Exception as e:
                    if attempt < max_retries - 1:  # Não tentar novamente na última tentativa
                        wait_time = (2 ** attempt) + random.uniform(0, 1)  # Espera exponencial com jitter
                        time.sleep(wait_time)  # Aguarde um pouco antes de tentar novamente
                        continue
                    st.session_state['messages'].append({'message': f"Erro ao buscar dados de população: {str(e)}", 'is_user': False})

        elif 'videos' in user_input.casefold():
            with elements("media_player"):

                # Play video from many third-party sources: YouTube, Facebook, Twitch,
                # SoundCloud, Streamable, Vimeo, Wistia, Mixcloud, DailyMotion and Kaltura.
                #
                # This element is powered by ReactPlayer (GitHub link below).

                from streamlit_elements import media

                media.Player(url="https://www.youtube.com/watch?v=iik25wqIuFo", controls=True)

        elif 'verificar monitoramento' in user_input.casefold():
            pyautogui.hotkey('win', 'm')
            os.startfile('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge')
            time.sleep(4)
            pyautogui.typewrite('http://192.168.13.115/', interval=0.25)
            pyautogui.press('enter')
            time.sleep(4)
            pyautogui.press('backspace')
            pyautogui.press('backspace')
            pyautogui.press('backspace')
            pyautogui.press('backspace')
            time.sleep(4)
            pyautogui.typewrite('user', interval=0.25)
            time.sleep(1)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.typewrite('monitor@123', interval=0.25)
            time.sleep(1)
            pyautogui.press('enter')
            st.session_state['messages'].append({'message': 'Abrindo página de monitoramento.', 'is_user': False})

        elif 'teste' in user_input.casefold():
           
            button7location = pyautogui.locateOnScreen('word.png')         
            button7point = pyautogui.center(button7location)          
            button7x, button7y = button7point
            pyautogui.click(button7x, button7y)
            pyautogui.click()


        elif 'remédio' in user_input.casefold():
            try:
                drug_name = user_input.split('remédio')[-1].strip()
                # Traduzir o nome do remédio para inglês
                traducao_nome = traduzir(drug_name, "pt", "en")
                # Buscar informações sobre o remédio em inglês
                drug_info = search_drug(traducao_nome)

                if drug_info:
                    for info in drug_info:
                        # Traduzir cada campo individualmente de volta para português
                        brand_name = traduzir(info['openfda']['brand_name'][0], 'en', 'pt')
                        manufacturer_name = traduzir(info['openfda']['manufacturer_name'][0], 'en', 'pt')
                        purpose = traduzir(info['purpose'][0], 'en', 'pt')
                        indications_and_usage = traduzir(info['indications_and_usage'][0], 'en', 'pt')
                        
                        # Consolidar todas as informações em uma única mensagem
                        mensagem = {
                            f"Nome da Marca: {brand_name}\n",
                            f"Nome do Fabricante: {manufacturer_name}\n",
                            f"Uso: {purpose}\n",
                            f"Indicações e Uso: {indications_and_usage}\n"
                        }

                        def format_list_as_string(items):
                            return "\n".join([f"- {item}" for item in items])
                        lista = format_list_as_string(mensagem)
                        
                        # Adicionar a mensagem consolidada ao estado da sessão do Streamlit
                        st.session_state['messages'].append({'message': lista, 'is_user': False})
                else:
                    st.session_state['messages'].append({'message': "Não foi possível encontrar informações sobre o remédio.", 'is_user': False})
            except Exception as e:
                st.session_state['messages'].append({'message': f"Não foi possível encontrar o remédio informado: {e}", 'is_user': False}) 

        elif 'doença' in user_input.casefold():
            try:
                disease_name = user_input.split('doença')[-1].strip()
                disease_info = search_disease_government(disease_name)

                if disease_info:
                    for info in disease_info:
                        mensagem = (
                            f"Nome da Doença: {info['title']}\n"
                            f"Descrição: {info['notes']}\n"
                        )
                        st.session_state['messages'].append({'message': mensagem, 'is_user': False})
                else:
                    st.session_state['messages'].append({'message': "Não foi possível encontrar informações sobre a doença.", 'is_user': False})
            except Exception as e:
                st.session_state['messages'].append({'message': f"Não foi possível encontrar a doença informada: {e}", 'is_user': False})


        elif user_input in conversa:
            # Adiciona a mensagem do usuário à lista de mensagens
            st.session_state['messages'].append({'message': str(bot_response), 'is_user': False})         

        else:
            # Gera a resposta do bot e adiciona à lista de mensagens
            with open('conv.py'):
                conversa.append(str(user_input))
                bot_response = bot.get_response(str(user_input))
                st.session_state['messages'].append({'message': str(bot_response), 'is_user': False})


    # Cria o contêiner de rolagem para as mensagens
    background_color = '#ADD8E6' 
    border_color = '#0000FF' 
    border_radius = '10px'
    st.markdown(
        """
        <div style='background-color: {background_color}; border: 2px solid {border_color}; border-radius: {border_radius}; max-height: 400px; overflow-y: auto; padding: 10px;'>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    for msg in st.session_state['messages']:
        if msg['is_user']:
            st.chat_message("Roger", avatar='roger.ico').write(f"{msg['message']}")
        else:
            st.chat_message("Nia", avatar='nia.ico').write(f"{msg['message']}", unsafe_allow_html=True)
            if 'video_link' in msg:
                st.video(msg['video_link'])
    
    st.markdown('</div>', unsafe_allow_html=True)


    # Mostra a janela lateral se show_sidebar estiver True
    if st.session_state['show_player']:
        with st.sidebar:
            st.session_state['show_code'] = False
            st.session_state['show_data'] = False
            st.session_state['show_mail'] = False 
            st.header("Nia Player")
            def file_selector(folder_path='./'):
                filenames = os.listdir(folder_path)
                selected_filename = st.selectbox('Selecione uma música', filenames)
                return os.path.join(folder_path, selected_filename)

            filename = file_selector()
            st.write('Você selecionou `%s`' % filename)
        
            audio = open(filename, 'rb')
            audiob = audio.read()
            st.audio(audiob, format='audio/ogg')


    if st.session_state['show_mail']:
        with st.sidebar:
            st.session_state['show_player'] = False
            st.session_state['show_data'] = False
            st.session_state['show_code'] = False
            st.header("Nia Mail")
            
            # Função para enviar e-mail
            def send_email(y_mail, d_mail, p_mail, m_mail, a_mail):
                try:
                    msg_from = y_mail
                    smtp_obj = smtplib.SMTP('smtp.outlook.com', 587)
                    smtp_obj.ehlo()
                    smtp_obj.starttls()
                    msg_to = d_mail
                    to_pass = p_mail
                    smtp_obj.login(msg_from, to_pass)
                    msg = m_mail
                    assunto = a_mail
                    email_message = f'Subject: {assunto}\n\n{msg}'
                    smtp_obj.sendmail(msg_from, msg_to, email_message)
                    smtp_obj.quit()
                    return "Email enviado com sucesso!"
                except Exception as e:
                    return f"Falha ao enviar e-mail: {e}"

            # Interface do Streamlit           
            y_mail = st.text_input("Seu E-mail")
            d_mail = st.text_input("E-mail de Destino")
            p_mail = st.text_input("Senha", type="password")
            a_mail = st.text_input("Assunto")
            m_mail = st.text_area("Mensagem")

            if st.button('Enviar'):
                response = send_email(y_mail, d_mail, p_mail, m_mail, a_mail)
                if "sucesso" in response.lower():
                    st.success(response)
                else:
                    st.error(response)


    if st.session_state['show_data']:
        with st.sidebar:
            st.session_state['show_player'] = False
            st.session_state['show_code'] = False
            st.session_state['show_mail'] = False
            def file_selector(folder_path='./'):
                uploaded_file = st.file_uploader("Selecione um arquivo")
                if uploaded_file is not None:

                    df = pd.read_csv(uploaded_file)
                    st.write(df)

            file_selector()
    
    if st.session_state['show_code']:
        with st.sidebar:
            content = st_monaco(value="", height="200px", language="markdown")
            st.write('Seu código: ')
            st.code(content)
           

chat()



