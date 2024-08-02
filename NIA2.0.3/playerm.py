#Importando Tkinter
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkreadonly import ReadOnlyText
from tkinter import filedialog as fd

from PIL import Image, ImageTk

#Pygame
import pygame
from pygame import mixer

import os
from tkinter import filedialog as fd


################# CORES ###################
co0 = "#2e2d2c"  # Preta
co1 = "#feffff"  # branca
co2 = "#4fa882"  # verde
co3 = "#38576b"  # valor
co4 = "#403d3d"  # letra
co5 = "#e06636"  # - profit
co6 = "#038cfc"  # azul
co7 = "#ef5350"  # vermelha
co8 = "#263238"  # + verde
co9 = "#e9edf5"  # sky blue
co10 = '#A020F0' # Purple


def player():
    player_wd = Tk()
    player_wd.title("NIA Play")
    player_wd.geometry('350x345')
    player_wd.iconbitmap("audio.ico")
    player_wd.configure(background=co0)
    player_wd.resizable(width=FALSE, height=FALSE)

    #Criando funções Play
    def play_musica():
        rodando = e_player.get(ACTIVE)
        l_status['text'] = 'Tocando agora: ' + rodando
        mixer.music.load(rodando)
        mixer.music.play()

    def pause_musica():
        mixer.music.pause()

    def continue_musica():
        mixer.music.unpause()

    def stop_musica():
        mixer.music.stop()
        
    
    def reduzir_v():
        volume_musica()
    
    '''def next_musica():
        tocando = l_status['text']
        play = os.listdir(pasta)
        index = play.index(tocando)

        novo_index = index + 1

        tocando = play[novo_index]

        mixer.music.load(tocando)
        mixer.music.play()

        e_player.delete(0, END)

        mostrar()

        e_player.select_set(novo_index)
        e_player.config(selectmode=SINGLE)
        l_status['text'] = tocando'''


    def mostrar():
        caminho = fd.askdirectory()
        lista = os.chdir(caminho)
        play = os.listdir(lista)
        for item in play:
            e_player.insert(END, item)


    def volume_musica(_=None):    
        mixer.music.set_volume(s1.get()/100.0)
    
    ###########################################################################
    #Configurando frame_direita

    frame_direita = Frame(player_wd, width=352, height=140, bg=co0)
    frame_direita.grid(row=0, column=0, pady=1, padx=0, sticky=NSEW)

    e_player = Listbox(frame_direita, selectmode=SINGLE, font=('ivy 9 bold'), width=47, height=10, bg=co1, fg=co0)    
    e_player.grid(row=0, column=0)

    s = Scrollbar(frame_direita)
    s.grid(row=0, column=2, sticky=NSEW)

    e_player.config(yscrollcommand=s.set)
    s.config(command=e_player.yview)

    ###########################################################################
    #Configurando frame_baixo

    frame_baixo = Frame(player_wd, width=404, height=180, bg=co1)
    frame_baixo.grid(row =1, column=0, columnspan=3, pady=1, padx=0, sticky=NSEW)

    img_status = Image.open('nia.png')
    img_status = img_status.resize((20,20))
    img_status = ImageTk.PhotoImage(img_status)

    l_imgs = Label(frame_baixo, image=img_status, bg=co1)
    l_imgs.place(x=5, y=6)

    l_status = Label(frame_baixo, text="Selecione uma música", width=50, anchor='nw', font=('ivy 8 bold'), bg=co1, fg=co0)
    l_status.place(x = 30, y=8)
      

    img_3 = Image.open('icon_play.png')
    img_3 = img_3.resize((30,30))
    img_3 = ImageTk.PhotoImage(img_3)
    l_play = Button(frame_baixo, command=play_musica, image=img_3, width=40, height=40, font=('ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co1)
    l_play.place(x = 60, y=50)


    img_5 = Image.open('icon_pause.png')
    img_5 = img_5.resize((30,30))
    img_5 = ImageTk.PhotoImage(img_5)
    l_stop = Button(frame_baixo, command=pause_musica, image=img_5, width=40, height=40, font=('ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co1)
    l_stop.place(x = 107, y=50)
   
    img_6 = Image.open('icon_playpause.png')
    img_6 = img_6.resize((30,30))
    img_6 = ImageTk.PhotoImage(img_6)
    l_stop = Button(frame_baixo, command=continue_musica, image=img_6, width=40, height=40, font=('ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co1)
    l_stop.place(x = 154, y=50)

    img_7 = Image.open('icon_stop.png')
    img_7 = img_7.resize((30,30))
    img_7 = ImageTk.PhotoImage(img_7)
    l_pp = Button(frame_baixo, command=stop_musica, image=img_7, width=40, height=40, font=('ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co1)
    l_pp.place(x = 201, y=50)   

    img_8 = Image.open('music_folder.png')
    img_8 = img_8.resize((30,30))
    img_8 = ImageTk.PhotoImage(img_8)
    l_load = Button(frame_baixo, command= mostrar, image=img_8, width=40, height=40, font=('ivy 10 bold'), relief=RAISED, overrelief=RIDGE, bg=co1)
    l_load.place(x = 248, y=50)

    l_v = Label(frame_baixo, text="Volume", width=50, anchor='nw', font=('ivy 8 bold'), bg=co1, fg=co0)
    l_v.place(x = 10, y=115)
    s1 = Scale(frame_baixo, command=volume_musica, from_=0, to=100, orient=HORIZONTAL, resolution=.1)
    s1.place(x=1, y=135, height=40, width=350)

    #Inicializar mixer
    mixer.init()
    volume_musica()

    player_wd.mainloop()  
