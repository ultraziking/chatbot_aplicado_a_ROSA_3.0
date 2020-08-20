#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mttkinter import mtTkinter as tk
from PIL import Image, ImageTk
import os
from subprocess import *
from time import sleep
import time
import random
import psutil
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition as sr
import pyttsx3
import threading
from multiprocessing import Process
import rosnode


input_voz = sr.Recognizer()  #inicializamos el reconocimiento de voz
salida = pyttsx3.init()  #inicializamos el conversor de texto en voz para la salida

voices = salida.getProperty('voices')
#indice para voz [1] - Español-HELENA ; [0] Ingles-ZIRA;[2] Ingles-SABINA
salida.setProperty('voice', voices[1].id)  #elegimos que la voz de salida sea castellano

chatterbot1 = ChatBot("chat1", 
    trainer = "chatterbot.trainers.ChatterBotCorpusTrainer",
    #preprocessors=[
    #    'chatterbot.preprocessors.convert_to_ascii'
    #],
    database_uri=None,
    #database_uri='sqlite:///database.sqlite3',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapter=[
        "chatterbot.logic.BestMatch"
        "chatterbot.logic.ClosestMeaningAdapter"
        "chatterbot.logic.ClosestMatchAdapter"
#        "chatterbot.logic.TimeLogicAdapter"
#        "chatterbot.logic.MathematicalEvaluation"
    ]
)

chatterbot2 = ChatBot("chat2", 
    trainer = "chatterbot.trainers.ChatterBotCorpusTrainer",
    #preprocessors=[
    #    'chatterbot.preprocessors.convert_to_ascii'
    #],
    database_uri=None,
    #database_uri='sqlite:///database.sqlite3',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapter=[
        "chatterbot.logic.BestMatch"
        "chatterbot.logic.ClosestMeaningAdapter"
        "chatterbot.logic.ClosestMatchAdapter"
#        "chatterbot.logic.TimeLogicAdapter"
#        "chatterbot.logic.MathematicalEvaluation"
    ]
)

chatterbot3 = ChatBot("chat3", 
    trainer = "chatterbot.trainers.ChatterBotCorpusTrainer",
    #preprocessors=[
    #    'chatterbot.preprocessors.convert_to_ascii'
    #],
    database_uri=None,
    #database_uri='sqlite:///database.sqlite3',   
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapter=[
        "chatterbot.logic.BestMatch"
        "chatterbot.logic.ClosestMeaningAdapter"
        "chatterbot.logic.ClosestMatchAdapter"
#        "chatterbot.logic.TimeLogicAdapter"
#        "chatterbot.logic.MathematicalEvaluation"
    ]
)

entrenador1 = ChatterBotCorpusTrainer(chatterbot1)
entrenador1.train("chatterbot.corpus.spanish.consulta_rosa")

entrenador2 = ChatterBotCorpusTrainer(chatterbot2)
entrenador2.train("chatterbot.corpus.spanish.comunicacion_rosa")

entrenador3 = ChatterBotCorpusTrainer(chatterbot3)
entrenador3.train("chatterbot.corpus.spanish.robot_rosa")


path = os.path.dirname(__file__)
root = Tk()
flag_fullscreen = False

# Node flags
flag_master = False
flag_laser = False
flag_us = False
flag_rviz= False
flag_kinect = False
flag_nav = False
flag_gamepad = False
flag_slam = False
flag_chatbot = False  #####################################################

# Node texts
text_master = StringVar()
text_us = StringVar()
text_laser = StringVar()
text_rviz = StringVar()
text_kinect = StringVar()
text_nav = StringVar()
text_slam = StringVar()
text_gamepad = StringVar()
text_chatbot = StringVar()    #########################################################################

# Process pid
pid_us = int()
pid_laser = int()
pid_rviz = int()
pid_model = int()
pid_kinect = int()
pid_nav = int()
pid_slam = int()
pid_gamepad = int()
pid_teleop = int()
	
def start_ros():
    global flag_master
    print("Starting ROS")
    try:
        Popen("roscore", stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
        sleep(1)
        print("ROS started")
	
    except ValueError:
        print("Error: could not start roscore")
        pass

def stop_ros():
    if tkMessageBox.askokcancel("Stop ROS", "Are you sure? This will close every node"):
        global flag_master
        print("Killing nodes...")
        os.system("rosnode kill -a")  # Kill nodes
        sleep(0.5)
        print("Nodes killed. Killing ROS master...")
        os.system("killall -9 roscore")  # Kill ROS master
        os.system("killall -9 rosmaster")
        print("ROS killed")
        sleep(0.5)
     

def close():
    if tkMessageBox.askokcancel ("Close RoSA","This will quit RoSA_interface\nAre you sure?"):
        stop_ros()
        root.destroy()


def shutdown():
    if tkMessageBox.askokcancel("Shut down RoSA", "Are you sure?"):
        if tkMessageBox.askokcancel( "Are you really sure? Remember to save everything before shut down"):
            root.destroy()
            os.system("poweroff")


def restart():
    if tkMessageBox.askokcancel("Restart RoSA", "Are you sure?"):
        if tkMessageBox.askokcancel( "Are you really sure? Remember to save everything before restart"):
            root.destroy()
            os.system("reboot")


def switch_fullscreen():
    global flag_fullscreen
    if flag_fullscreen:
        root.attributes("-fullscreen", False)
        flag_fullscreen = False
    else:
        root.attributes("-fullscreen", True)
        flag_fullscreen = True

def information():
    tkMessageBox.showinfo("About RoSA", "RoSA is a social assistant robot designed to be a guide in hospitals, events, etc.")

def help():
    tkMessageBox.showinfo("Help", "It is very simple to use RoSA\n1.Pulse the botton Start ROS\n2.Pulse Start RoSA\n3.Choose the type of Navigation\nFinaly if you want to visualize the robot model and the data sensors pulse Start Rviz")

def start_RoSA():

    global pid_model

    if tkMessageBox.askokcancel("Start RoSA", "Remember to Start ROS before Start RoSA"):	    
   	 pid_model=Popen(["roslaunch", "rosa_sensors", "sensors_main.launch"]).pid
  	 print ("Model started under process " + str(pid_model))



def stop_RoSA():
    global pid_model 
    p = psutil.Process(pid_model)
    p.terminate()


def chatbot(x):
    messagebox.showinfo("lista de funciones: ", "1. chatear: puede chatear con rosa\n2. consulta: puede consultar horarios y servicios de las instalaciones de etsidi, y otras sorpresas\n3. navegacion: lanza la navegacion autonoma y puede decir a donde quiere ir y rosa le guiara\n4. teclado: puede controlar rosa mediante teclado\n5. mapa: genera una mapa\n6. visualizador: abre el visualizador rviz") 
    global flag_chatbot
    while x==1:
        while True:
            try:                              
                print('dime en que modo quiere que funcione por favor')
                salida.say("dime en que modo quiere que funcione por favor")
                print("di adios para salir del modo chatbot")
                salida.say("di adios para salir del modo chatbot")
                salida.runAndWait()

                with sr.Microphone() as source:   
                    input_voz.adjust_for_ambient_noise(source, duration=0.2)
                    audio = input_voz.listen(source)
                    text = input_voz.recognize_google(audio, language = "es-ES")
                    user_input = format(text)
                    if user_input == "chatear":
                        print("este es el modo chatear")
                        salida.say("este es el modo chatear")
                        salida.runAndWait()
                        chat(1)
                    elif user_input == "navegacion" or user_input == "navegación":
                        salida.say("este es el modo de navegacion autonoma")
                        print("este es el modo de navegacion autonoma")
                        salida.runAndWait()
                        interaccion(1)
                    elif user_input == "control teclado" or user_input == "teclado":
                        salida.say("este es el modo de controlar rosa mediante teclado, di ya no quiero teclado para salir de este modo")
                        print("este es el modo de controlar rosa mediante teclado, di ya no quiero teclado para salir de este modo")
                        salida.runAndWait()
                        start_gamepad()
                    elif user_input == "ya no quiero teclado":
                        salida.say("se cierra el modo de controlar rosa mediante teclado")
                        print("se cierra el modo de controlar rosa mediante teclado")
                        salida.runAndWait()
                        stop_gamepad()
                    elif user_input == "mapa":
                        salida.say("este es el modo de generar una mapa del entorno de rosa, di ya no quiero mapa para salir de este modo")
                        print("este es el modo de generar una mapa del entorno de rosa, di ya no quiero mapa para salir de este modo")
                        salida.runAndWait()
                        start_slam()
                    elif user_input == "ya no quiero mapa" or user_input == "mapa fuera":
                        salida.say("se cierra el modo de generacion del mapa de entorno")
                        print("se cierra el modo de generacion del mapa de entorno")
                        salida.runAndWait()
                        stop_slam()
                    elif user_input == "visualizador":
                        salida.say("a continuacion se muestra el visualizador de rosa, di ya no quiero visualizador para salir de este modo")
                        print("a continuacion se muestra el visualizador de rosa, di ya no quiero visualizador para salir de este modo")
                        salida.runAndWait()
                        start_rviz()
                    elif user_input == "ya no quiero visualizador":
                        salida.say("se cierra el visualizador de rosa")
                        print("se cierra el visualizador de rosa")
                        salida.runAndWait()
                        stop_rviz()
                    elif user_input == "adios" or user_input == "adiós":
                        salida.say("adios")
                        print("adios~")
                        salida.runAndWait()
                        flag_chatbot = False
                        x == 2
                        return
                    elif user_input == "consulta":
                        salida.say("este es el modo de consultar horarios y servicios de las instalaciones de ETSIDI")
                        print("este es el modo de consultar horarios y servicios de las instalaciones de ETSIDI")
                        salida.runAndWait()
                        consulta(1)
                    else:
                        salida.say("por favor vuelve a introducir su comando")
                        print("por favor vuelve a introducir su comando")
                        salida.runAndWait()
                

            # Press ctrl-c or ctrl-d on the keyboard to exit
            except (sr.UnknownValueError):
                print("speech recognition no entiende este audio")
                salida.say("el reconocimiento de voz no entiende este audio")
                salida.runAndWait()
                break
    while x!=1:
        break


#######################################################################
def consulta(x):
    while x==1: 
        print("hola, estamos en modo consulta, puedo informarle sobre horarios de secretaria, biblioteca, cafeteria, publicaciones, servicios que ofrece las instalaciones y unos proyectos muy interesantes del laboratorio")
        salida.say("hola, estamos en modo consulta, puedo informarle sobre horarios de secretaria, biblioteca, cafeteria, publicaciones, servicios que ofrece las instalaciones y unos proyectos muy interesantes del laboratorio")
        salida.runAndWait()
        clave = "vamos"

        while True:
            try:
                with sr.Microphone() as source: 
                    input_voz.adjust_for_ambient_noise(source, duration=0.2)  
                    audio = input_voz.listen(source)
                    text = input_voz.recognize_google(audio, language = "es-ES")
                    inpu = format(text)

                    if inpu =="adios" or inpu =="adiós":
                        salida.say("adios")
                        print("adios~")
                        salida.runAndWait()
                        x == 2
                        return
                    elif clave in inpu:
                        salida.say("dirigimos al modo interacción para comenzar la navegación autonoma")
                        print("dirigimos al modo interacción para comenzar la navegación autonoma")
                        salida.runAndWait()
                        x == 2
                        interaccion(1)
                        return 
                    else:
                        bot_response = chatterbot1.get_response(inpu)
                        salida.say(bot_response)
                        salida.runAndWait()
                        print(bot_response)

            except(sr.UnknownValueError):
                print("speech recognition no entiende este audio, por favor repite")
                salida.say("el reconocimiento de voz no entiende este audio, por favor repite")
                salida.runAndWait()
                break

    while x!=1:
        break
#######################################################################

#######################################################################
def interaccion(x):

    coordenadas = {

    "secretaria" : "2.1.3",
    "cafeteria" : "-9.2.3",
    "crea" : "-1.5.3",
    "biblioteca" : "-4.0.12",
    "impresora 3D" : "0.3.-2",
    "robot pintor" : "1.2.-2",
    "conserjeria" : "2.0.0",
    "oficina de practicas" : "-2.1.3",
    "publicaciones" : "0.3.0",
    "fotocopiadora" : "0.5.0",
    "robot industrial" : "1.3.-2",
    "laboratorio de TFG" : "1.4.-2"
}
    
    activo = ["voy muy rapido? di frena un poco y voy mas lento", "la velocidad actual esta bien? di frena un poco o mas rapido para cambiar la velocidad", "me sigues? di frena un poco si voy rapido", "me puede seguir sin problema?, si voy rapido puedes decir frena un poco", "voy lento? di mas rapido y aumento la velocidad"]
    
    print("Hola, estamos en ETSIDI, a donde quiere ir?  Di adios si quiere salir de este modo, di recomendacion para recibir algunas explicaciones de ETSIDI")
    salida.say("Hola, estamos en ETSIDI, a donde quiere ir?  Di adios si quiere salir de este modo, di recomendacion para recibir algunas explicaciones de ETSIDI")
    salida.runAndWait()

    while x==1: 
        start_nav()        
        while True:
            try:
                with sr.Microphone() as source: 
                    input_voz.adjust_for_ambient_noise(source, duration=0.2)  
                    audio = input_voz.listen(source)
                    text = input_voz.recognize_google(audio, language = "es-ES")
                    inpu = format(text)

                    if inpu =="adios" or inpu =="adiós":
                        salida.say("adios")
                        print("adios~")
                        salida.runAndWait()
                        stop_nav()
                        x == 2
                        return
                    if inpu == "recomendacion" or inpu == "recomendación":
                        salida.say("pasamos al modo consulta para hacer recomendaciones")
                        print("pasamos al modo consulta para hacer recomendaciones")
                        salida.runAndWait()
                        x == 2
                        consulta(1)
                        return
                    else:
                        if "secretaria" in inpu:
                            print(coordenadas["secretaria"])
                        elif "cafeteria" in inpu:
                            print(coordenadas["cafeteria"])
                        elif "biblioteca" in inpu:
                            print(coordenadas["biblioteca"])
                        elif "crea" in inpu:
                            print(coordenadas["crea"])
                        elif "conserjeria" in inpu:
                            print(coordenadas["conserjeria"])
                        elif "oficina de practicas" in inpu:
                            print(coordenadas["oficina de practicas"])
                        elif "publicaciones" in inpu:
                            print(coordenadas["publicaciones"])
                        elif "fotocopiadora" in inpu:
                            print(coordenadas["fotocopiadora"])
                        elif "robot industrial" in inpu:
                            print(coordenadas["robot industrial"])
                        elif "impresora 3D" in inpu:
                            print(coordenadas["impresora 3D"])
                        elif "robot pintor" in inpu:
                            print(coordenadas["robot pintor"])
                        elif "laboratorio" in inpu:
                            print(coordenadas["laboratorio de TFG"])

                        bot_response = chatterbot2.get_response(inpu)
                        salida.say(bot_response)
                        salida.runAndWait()
                        print(bot_response)
                        texto = random.choice(activo)

                        if bot_response:
                            time.sleep(10)
                            salida.say(texto)
                            salida.runAndWait()

                            with sr.Microphone() as source: 
                                input_voz.adjust_for_ambient_noise(source, duration=0.2)  
                                audio = input_voz.listen(source)
                                text = input_voz.recognize_google(audio, language = "es-ES")
                                inp = format(text)

                                if inp == "más rápido":
                                    salida.say("a su orden, iŕe más rapido")
                                    salida.runAndWait()
                                    time.sleep(10)
                                    salida.say("ya hemos llegado!")
                                    salida.runAndWait()
                                elif inp == "frena un poco" or inp == "más lento":
                                    salida.say("a su orden, disminuyo mi velocidad")
                                    salida.runAndWait()
                                    time.sleep(10)
                                    salida.say("ya hemos llegado!")
                                    salida.runAndWait()
                                elif inp == "esta bien" or inp == "está bien":
                                    salida.say("perfecto")
                                    salida.runAndWait()
                                    time.sleep(10)
                                    salida.say("ya hemos llegado!")
                                    salida.runAndWait()
                                else:
                                    salida.say("a su orden")
                                    salida.runAndWait()
                                    time.sleep(10)
                                    salida.say("ya hemos llegado!")
                                    salida.runAndWait()


            except(sr.UnknownValueError):
                print("speech recognition no entiende este audio, por favor repite")
                salida.say("el reconocimiento de voz no entiende este audio, por favor repite")
                salida.runAndWait()
                break

    while x!=1:
        break
#######################################################################

#######################################################################
def chat(x):
    while x==1: 
        print("Hola, me llamo rosa, me puedes preguntar qué cosas puedo hacer o decir dime algo ")
        salida.say("Hola, me llamo rosa, me puedes preguntar qué cosas puedo hacer o decir dime algo")
        salida.runAndWait()
        clave = "vamos"

        while True:
            try:
                with sr.Microphone() as source:   
                    input_voz.adjust_for_ambient_noise(source, duration=0.2)
                    audio = input_voz.listen(source)
                    text = input_voz.recognize_google(audio, language = "es-ES")
                    inp = format(text)

                    if inp =="adios" or inp =="adiós":
                        salida.say("adios")
                        print("adios~")
                        salida.runAndWait()
                        x == 2
                        return
                    elif inp == "dime algo":
                        salida.say("sabes que es un robot antropomorfico?")
                        salida.runAndWait()
                    elif clave in inp:
                        salida.say("dirigimos al modo interacción para comenzar la navegación autonoma")
                        salida.runAndWait()
                        interaccion(1)
                        return
                    else:
                        bot_response = chatterbot3.get_response(inp)
                        salida.say(bot_response)
                        salida.runAndWait()
                        print(bot_response)

            except(sr.UnknownValueError):
                print("speech recognition no entiende este audio, por favor repite")
                salida.say("el reconocimiento de voz no entiende este audio, por favor repite")
                salida.runAndWait()
                break

    while x!=1:
        break
#######################################################################



def startchatbot():

    global flag_chatbot
    flag_chatbot = True
    chatbot(1)
    print("iniciando chatbot")

def stopchatbot():
    global flag_chatbot
    flag_chatbot = False
    chatbot(2)
    print("end chatbot")




def start_rviz():
    global pid_rviz
    global pid_nav
    global pid_slam
    global flag_nav
    global flag_slam
    global flag_kinect
	
    tkMessageBox.showinfo("About Rviz", "Rviz often fails to start. If so, close rviz and try again")
    if flag_slam:
        pid_rviz=Popen(["rosrun", "rviz","rviz","-d","/home/rosa/TFG_IGNACIO/TFG/catkin_ws/src/rosa_interface/rviz/slam.rviz"]).pid
        print ("Rviz started under process " + str(pid_rviz))
    elif flag_nav:
        pid_rviz=Popen(["rosrun", "rviz","rviz","-d","/home/rosa/TFG_IGNACIO/TFG/catkin_ws/src/rosa_interface/rviz/navigation.rviz"]).pid
        print ("Rviz started under process " + str(pid_rviz))
    else:
        pid_rviz=Popen(["rosrun", "rviz","rviz","-d","/home/rosa/TFG_IGNACIO/TFG/catkin_ws/src/rosa_interface/rviz/rosa_sensors.rviz"]).pid
        print ("Rviz started under process " + str(pid_rviz))


def stop_rviz():
    global pid_rviz
    p = psutil.Process(pid_rviz)
    p.terminate()


def start_nav():
    global pid_nav
    global pid_slam
    global pid_teleop
    global flag_slam
    global flag_gamepad
    if flag_slam:
       p = psutil.Process(pid_slam)
       p.terminate()
       p = psutil.Process(pid_teleop)
       p.terminate()
    if flag_gamepad:
       p = psutil.Process(pid_gamepad)
       p.terminate()
    pid_nav=Popen(["roslaunch", "rosa_navigation", "rosa_navigation.launch"]).pid
    print ("Navigation started under process " + str(pid_nav))

def stop_nav():
    global pid_nav
    p = psutil.Process(pid_nav)
    p.terminate()

def start_slam():
    global pid_slam
    global pid_teleop
    global pid_nav
    global flag_nav
    global flag_gamepad
    if flag_nav:
      p = psutil.Process(pid_nav)
      p.terminate()
    if flag_gamepad:
      p = psutil.Process(pid_gamepad)
      p.terminate()
    pid_slam=Popen(["rosrun", "gmapping", "slam_gmapping"]).pid
    print ("SLAM started under process " + str(pid_slam))
    pid_teleop=Popen(["rosrun", "teleop_twist_keyboard", "teleop_twist_keyboard.py"]).pid
    print ("Teleop started under process " + str(pid_teleop))

def stop_slam():
    global pid_slam
    global pid_teleop
    p = psutil.Process(pid_slam)
    p.terminate()
    p = psutil.Process(pid_teleop)
    p.terminate()


def start_gamepad():
    global pid_gamepad
    global pid_slam
    global pid_teleop
    global pid_nav
    global flag_nav
    global flag_slam
	
    if flag_slam:
       p = psutil.Process(pid_slam)
       p.terminate()
       p = psutil.Process(pid_teleop)
       p.terminate()
    if flag_nav:
      p = psutil.Process(pid_nav)
      p.terminate()  
	
    pid_gamepad=Popen(["roslaunch", "teleop_twist_keyboard", "teleop_twist_keyboard"]).pid #Se debería lanzar el nodo joy del gamepad pero no está configurado el gamepad por eso se utiliza el teclado
    print ("Teleop started under process " + str(pid_gamepad))
	
def stop_gamepad():
    global pid_gamepad
    p = psutil.Process(pid_gamepad)
    p.terminate()

def check_nodes():

    # Get nodes
    try:
        nodes = rosnode.get_node_names()
        global flag_master
        flag_master = True
    except rosnode.ROSNodeIOException:
        nodes = "roscore_not_found"
        flag_master = False

    # Reset flags
    global flag_laser
    global flas_us
    global flag_rviz
    global flag_kinect
    global flag_nav
    global flag_slam
    global flag_gamepad
    flag_laser = False
    flag_us = False
    flag_rviz = False
    flag_kinect = False
    flag_nav = False
    flag_slam = False
    flag_gamepad = False

    # Check nodes
    for node in nodes:
        # Laser
        if node == "/hokyuo_node":
            flag_laser = True
        # Rviz
        if node.startswith("/rviz_"):
            flag_rviz = True
        # Ultrasonidos
        if node == "/serial_node":
            flag_us = True
        # kinect
        if node.startswith("/camera/"):
            flag_kinect = True
        # Navigation
        if node.startswith("/move_base"):
            flag_nav = True
        # SLAM
        if node.startswith("/slam_gmapping"):
            flag_slam = True
        # Gamepad
        if node.startswith("/teleop"): #node == "/joy" para el gamepad. Se pone el teleop hasta que se termine de incorporar el gamepad:
            flag_gamepad = True


def update_text():

	# Global flags
	global flag_master
	global flag_us
	global flag_laser
	global flag_kinect
	global flag_nav
	global flag_slam
	global flag_gamepad
    global flag_chatbot    ##########################################################################


	if flag_master:
        	text_master.set("Running")

		if flag_us:
		    text_us.set("Node running")
		else:
		    text_us.set("Not running")
		if flag_laser:
		    text_laser.set("Node running")
		else:
		    text_laser.set("Not running")
		if flag_rviz:
		    text_rviz.set("Node running")
		else:
		    text_rviz.set("Not running")
		if flag_kinect:
		    text_kinect.set("Node running")
		else:
		    text_kinect.set("Not running")
		if flag_nav:
		    text_nav.set("Node running")
		else:
		    text_nav.set("Not running")
		if flag_slam:
		    text_slam.set("Node running")
		else:
		    text_slam.set("Not running")
		if flag_gamepad:
		    text_gamepad.set("Node running")
		else:
		    text_gamepad.set("Not running")
        if flag_chatbot:            ########################################################################## 
            text_chatbot.set("Node running")     ##########################################################################
        else:                     ##########################################################################
            text_chatbot.set("Not running")      ##########################################################################

  	else:
		text_master.set("Not running")
		text_us.set("Master not running")
		text_laser.set("Master not running")	
		text_rviz.set("Master not running")
		text_kinect.set("Master not running")	
		text_nav.set("Master not running")
		text_slam.set("Master not running")	
		text_gamepad.set("Master not running")
        text_chatbot.set("Master not running")       ##########################################################################



root.title("RoSA_interface")
root.minsize(950, 550)
root.columnconfigure(0, weigh=1)
root.rowconfigure(0, weigh=1)
# Main frame
mainframe = ttk.Frame(root, padding="15 15 15 15", borderwidth=4, relief=SUNKEN)
mainframe.grid(column=0, row=0, sticky=N+S+E+W)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=1)
mainframe.rowconfigure(3, weight=1)

# Frame 1: top bar
top_bar = Frame(mainframe, borderwidth=1, relief=SUNKEN)
top_bar.grid(column=1, row=1, rowspan=1, columnspan=3, sticky=N+S+E+W)
for x in range(5):
    top_bar.columnconfigure(x, weight=1)

# Frame 1.1: title
title = Frame(top_bar)
title.grid(column=2, row=1, rowspan=1, columnspan=2, sticky=N+S+E)

# Label 1.1.1(1,1): title label: Rosa_interface
text1 = Label(title, text='RoSA Interface',fg="DodgerBlue4", justify=LEFT)
text1.configure(font=("Arial", 40,"bold"))
text1.grid(column=1, row=1, sticky=N+S+E, padx=10, pady=4)

# Label 1.1.2(1,2): subtitle label: developed at
subtext1 = Label(title, text='Developed at ETSIDI UPM - 2019', justify=LEFT)
subtext1.configure(font=("Arial", 12))
subtext1.grid(column=1, row=2, sticky=N+S+E, padx=10)

# Label 1.1.3(1,3): subtitle label: by me
subtext2 = Label(title, text='by Ignacio Lanseros Villén', justify=LEFT)
subtext2.configure(font=("Arial", 12))
subtext2.grid(column=1, row=3, sticky=N+S+E, padx=10)

#Label 1.2 ROS PHOTO1
image = Image.open("/home/ultraziking/文档/rosa-3.0-master/catkin_ws/src/rosa_interface/src/ROS.png")
[imageSizeWidth, imageSizeHeight] = image.size
scale = 0.3
image = image.resize((int(imageSizeWidth*scale), int(imageSizeHeight*scale)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
labelROS = Label(top_bar, image=photo)
labelROS.image = photo
labelROS.grid(column=1, row=1, sticky=N+S+W, padx=5)


# LabelFrame 2: info area
info_frame = Frame(mainframe, borderwidth=1, relief=SUNKEN)
info_frame.grid(column=1, row=2, rowspan=1, sticky=N+S+E+W)
info_frame.columnconfigure(1, weight=1)
info_frame.rowconfigure(1, weight=1)

info = LabelFrame(info_frame, text='System information')
info.grid(column=1, row=1, rowspan=1, padx=10, pady=5, sticky=N+S+E+W)

# Info ROS
info_ROS = Label(info, text="ROS:")
info_ROS.grid(column=1, row=1, sticky=N+W, padx=10, pady=5, rowspan=1)
info_ROS.configure(font=("Arial", 10, "bold"))
info_ROS1 = Label(info, textvariable=text_master)
info_ROS1.grid(column=1, row=2, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info Navigation
info_nav = Label(info, text="Navigation:")
info_nav.grid(column=1, row=3, sticky=N+W, padx=10, pady=5, rowspan=1)
info_nav.configure(font=("Arial", 10, "bold"))
info_nav1 = Label(info, textvariable=text_nav)
info_nav1.grid(column=1, row=4, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info ultrasonidos
info_us = Label(info, text="Ultrasonidos:")
info_us.grid(column=1, row=5, sticky=N+W, padx=10, pady=5, rowspan=1)
info_us.configure(font=("Arial", 10, "bold"))
info_us1 = Label(info, textvariable=text_us)
info_us1.grid(column=1, row=6, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info laser
info_laser = Label(info, text="Laser:")
info_laser.grid(column=1, row=7, sticky=N+W, padx=10, pady=5, rowspan=1)
info_laser.configure(font=("Arial", 10, "bold"))
info_laser1 = Label(info, textvariable=text_us)
info_laser1.grid(column=1, row=8, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info Kinect
info_kinect = Label(info, text="Kinect:")
info_kinect.grid(column=1, row=9, sticky=N+W, padx=10, pady=5, rowspan=1)
info_kinect.configure(font=("Arial", 10, "bold"))
info_kinect1 = Label(info, textvariable=text_kinect)
info_kinect1.grid(column=1, row=10, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info rviz
info_rviz = Label(info, text="Rviz:")
info_rviz.grid(column=1, row=11, sticky=N+W, padx=10, pady=5, rowspan=1)
info_rviz.configure(font=("Arial", 10, "bold"))
info_rviz1 = Label(info, textvariable=text_rviz)
info_rviz1.grid(column=1, row=12, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info SLAM
info_slam = Label(info, text="SLAM:")
info_slam.grid(column=1, row=13, sticky=N+W, padx=10, pady=5, rowspan=1)
info_slam.configure(font=("Arial", 10, "bold"))
info_slam1 = Label(info, textvariable=text_slam)
info_slam1.grid(column=1, row=14, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info Gamepad
info_gamepad = Label(info, text="Gamepad:")
info_gamepad.grid(column=1, row=15, sticky=N+W, padx=10, pady=5, rowspan=1)
info_gamepad.configure(font=("Arial", 10, "bold"))
info_gamepad1 = Label(info, textvariable=text_gamepad)
info_gamepad1.grid(column=1, row=16, sticky=N+W, padx=20, pady=5, rowspan=1)

# Info Chatbot
info_chatbot = Label(info, text="Chatbot:")     ##########################################################################
info_chatbot.grid(column=1, row=17, sticky=N+W, padx=10, pady=5, rowspan=1)  ##########################################################################
info_chatbot.configure(font=("Arial", 10, "bold"))  ##########################################################################
info_chatbot1 = Label(info, textvariable=text_chatbot)    ##########################################################################
info_chatbot1.grid(column=1, row=18, sticky=N+W, padx=20, pady=5, rowspan=1)    ##########################################################################


# Frame 3: central button area
center_buttons = Frame(mainframe, borderwidth=1, relief=SUNKEN)
center_buttons.grid(column=2, row=2, rowspan=1, columnspan=1, sticky=N+S+E+W)
center_buttons.columnconfigure(1, weight=1)
for x in range(4):
    center_buttons.rowconfigure(x, weight=1)

# Button: ROS
button_ROS = Button(center_buttons, text='Start ROS', bg='lime green',fg="white",font=("Arial", 12, "bold"), activebackground='chartreuse', width=12, height=3)
button_ROS.grid(column=1, row=1, padx=10, pady=10, sticky=N)

# Button: RoSA
button_rosa = Button(center_buttons, text='Start RoSA', bg='DodgerBlue4', activebackground='royal blue', width=12, height=3,fg="white",font=("Arial", 12, "bold"))
button_rosa.grid(column=1, row=2, padx=10, pady=10, sticky=N)

# Button: Rviz
button_rviz = Button(center_buttons, text='Start rviz', bg='gold', activebackground='royal blue', width=12, height=3,fg="white",font=("Arial", 12, "bold"))
button_rviz.grid(column=1, row=4, padx=10, pady=10, sticky=N)

# Button: Navigation
button_nav = Button(center_buttons, text='Start Navigation', bg='lime green',fg="white",font=("Arial", 12, "bold"), activebackground='chartreuse', width=12, height=5)
button_nav.grid(column=2, row=1, padx=10, pady=10, sticky=N)

# Button: SLAM
button_slam = Button(center_buttons, text='Start SLAM', bg='lime green',fg="white",font=("Arial", 12, "bold"), activebackground='chartreuse', width=12, height=5)
button_slam.grid(column=2, row=2, padx=10, pady=10, sticky=N)

# Button: Gamepad
button_gamepad = Button(center_buttons, text='Start Gamepad', bg='lime green',fg="white",font=("Arial", 12, "bold"), activebackground='chartreuse', width=12, height=5)
button_gamepad.grid(column=2, row=3, padx=10, pady=10, sticky=N)

# Button: Chatbot
button_chatbot = Button(center_buttons, text='Start Chatbot', bg='gold',fg="black",font=("Arial", 12, "bold"), activebackground='chartreuse', width=12, height=3)
button_chatbot.grid(column=1, row=3, padx=10, pady=10, sticky=N)

#Frame 4: Right bar 1
right_bar = Frame(mainframe, borderwidth=1, relief=SUNKEN)
right_bar.grid(column=3, row=2, rowspan=1, columnspan=1, sticky=N+S+W+E)
right_bar.rowconfigure(3, weight=1)

# Button: fullscreen
fullscreen = Button(right_bar, text='Toggle\nfullscreen', width=6, height=3, fg="blue", command=switch_fullscreen)
fullscreen.grid(column=1, row=1, padx=10, pady=10, sticky=N)

# Button: Info
info_space = Button(right_bar, text='Info', width=6, height=3, fg="blue", command=information)
info_space.grid(column=1, row=2, padx=10, pady=10, sticky=N)

# Button: Help
restart = Button(right_bar, text='Help', width=6, height=3, fg="blue", command=help)
restart.grid(column=1, row=3, padx=10, pady=10, sticky=N)

#Frame 5: Right bar 2
right_bar2 = Frame(mainframe, borderwidth=1, relief=SUNKEN)
right_bar2.grid(column=3, row=2, rowspan=1, columnspan=1, sticky=N+S+E)
right_bar2.rowconfigure(3, weight=1)

# Button: shut down
shut_down = Button(right_bar2, text='Shut down\nRoSA', width=6, height=3, fg="red", command=shutdown)
shut_down.grid(column=1, row=1, padx=10, pady=10, sticky=N)

# Button: restart
restart = Button(right_bar2, text='Restart\nRoSA', width=6, height=3, fg="red", command=restart)
restart.grid(column=1, row=2, padx=10, pady=10, sticky=N)

# Button: exit
exit_button = Button(right_bar2, text='Exit', width=6, height=3, command=close)
exit_button.grid(column=1, row=3, padx=10, pady=10, sticky=N)

#Frame 6: Botton bar
bottom_bar = Frame(mainframe, borderwidth=1, relief=SUNKEN)
bottom_bar.grid(column=1, row=3, rowspan=1, columnspan=3, sticky=N+S+E+W)

#ETSIDI
image = Image.open("/home/ultraziking/文档/rosa-3.0-master/catkin_ws/src/rosa_interface/src/ETSIDI.bmp")
[imageSizeWidth, imageSizeHeight] = image.size
scale = 0.3
image = image.resize((int(imageSizeWidth*scale), int(imageSizeHeight*scale)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
labelROS = Label(bottom_bar, image=photo)
labelROS.image = photo
labelROS.grid(column=1, row=1, sticky=N+S+W+E, padx=10)

#UPM
image = Image.open("/home/ultraziking/文档/rosa-3.0-master/catkin_ws/src/rosa_interface/src/UPM.jpeg")
[imageSizeWidth, imageSizeHeight] = image.size
scale = 0.5
image = image.resize((int(imageSizeWidth*scale), int(imageSizeHeight*scale)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
labelROS = Label(bottom_bar, image=photo)
labelROS.image = photo
labelROS.grid(column=2, row=1, sticky=N+S+W+E, padx=10)

#Aura
image = Image.open("/home/ultraziking/文档/rosa-3.0-master/catkin_ws/src/rosa_interface/src/3009aura.jpg")
[imageSizeWidth, imageSizeHeight] = image.size
scale = 0.7
image = image.resize((int(imageSizeWidth*scale), int(imageSizeHeight*scale)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
labelROS = Label(bottom_bar, image=photo)
labelROS.image = photo
labelROS.grid(column=3, row=1, sticky=N+S+W+E, padx=10)

#Arduino
image = Image.open("/home/ultraziking/文档/rosa-3.0-master/catkin_ws/src/rosa_interface/src/arduino-logosvg.png")
[imageSizeWidth, imageSizeHeight] = image.size
scale = 0.1
image = image.resize((int(imageSizeWidth*scale), int(imageSizeHeight*scale)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)
labelROS = Label(bottom_bar, image=photo)
labelROS.image = photo
labelROS.grid(column=4, row=1, sticky=N+S+W+E, padx=10)


def update_buttons():
    # Global flags
    global flag_master
    global flag_us
    global flag_laser
    global flag_rviz
    global flag_kinect
    global flag_slam
    global flag_nav
    global flag_follower
    global flag_chatbot    ###########################################################################
    


# ROS master button
    if flag_master:
        button_ROS.configure(text='Stop ROS', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                             height=3, command=stop_ros)
    else:
        button_ROS.configure(text='Start ROS', bg='red4', activebackground='red3', width=12,
                             height=3, command=start_ros)
# RoSA button
    if flag_us or flag_laser or flag_kinect or flag_rosa:
        button_rosa.configure(text='Stop RoSA', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                                 height=3, command=stop_RoSA)
    else:
        button_rosa.configure(text='Start RoSA', bg='DodgerBlue4', activebackground='DodgerBlue3',
                                 width=12, height=3, command=start_RoSA)
# Rviz button
    if flag_rviz:
        button_rviz.configure(text='Stop Rviz', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                                 height=3, command=stop_rviz)
    else:
        button_rviz.configure(text='Start Rviz', bg='SpringGreen4', activebackground='SpringGreen3',
                                 width=12, height=3, command=start_rviz)
# Navigation button
    if flag_nav:
        button_nav.configure(text='Stop Navigation', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                                 height=5, command=stop_nav)
    else:
        button_nav.configure(text='Start Navigation', bg='yellow3', activebackground='yellow2',
                                 width=12, height=5, command=start_nav)
# SLAM button
    if flag_slam:
        button_slam.configure(text='Stop SLAM', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                                 height=5, command=stop_slam)
    else:
        button_slam.configure(text='Start SLAM', bg='yellow3', activebackground='yellow2',
                                 width=12, height=5, command=start_slam)
# Gamepad button
    if flag_gamepad:
        button_gamepad.configure(text='Stop Gamepad', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                                 height=5, command=stop_gamepad)
    else:
        button_gamepad.configure(text='Start Gamepad', bg='yellow3', activebackground='yellow2',
                                 width=12, height=5, command=start_gamepad)
# Chatbot button
    if flag_master:
        if flag_chatbot:
            button_chatbot.configure(text='Stop Chatbot', bg='DarkOrange2', activebackground='DarkOrange1', width=12,
                                 height=3, command=stopchatbot)
        else:
            button_chatbot.configure(text='Start Chatbot', bg='yellow3', activebackground='yellow2',
                                 width=12, height=3, command=startchatbot)

while True:
    check_nodes()
    update_text()
    update_buttons()
    root.update()
