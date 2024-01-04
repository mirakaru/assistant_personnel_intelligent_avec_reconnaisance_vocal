from tkinter import *
import paho.mqtt.client as mqtt
import pymongo
import datetime as dt
from tptest5 import get_current_datetime

from threading import Thread

from tptest5 import *

import requests
from PIL import Image, ImageTk
from io import BytesIO
from pyowm import OWM
from pyowm.utils.config import get_default_config



mongo_client = pymongo.MongoClient("localhost")
db = mongo_client["mon_historique"]
historique_collection = db["historique"]


def enregistrer_historique(commande, etat):
    now = get_current_datetime()
    date_heure = now.strftime("%Y-%m-%d %H:%M:%S")
    historique_data = {"commande": commande, "etat": etat, "date_heure": date_heure}
    historique_collection.insert_one(historique_data)
  


def fermer():
    print("Quitter proprement")
    client.loop_stop()
    client.disconnect()
    fen1.destroy()

def cmd_on_porte_entree(): 
    enregistrer_historique("on_porte_entree", "Ouverte")
    client.publish("Gills/Commandes", "on_porte_entree")
    lblEtatPorteEntree.configure(text="Ouverte")  # Mettre à jour l'état de la porte d'entrée

def cmd_off_porte_entree():
    enregistrer_historique("off_porte_entree", "Fermée")
    client.publish("Gills/Commandes", "off_porte_entree")
    lblEtatPorteEntree.configure(text="Fermée") 
def cmd_on_alarme():
    enregistrer_historique("on_alarme", "Armé")
    client.publish("Gills/Commandes", "on_alarme")
    lblEtatAlarme.configure(text="Armé")  # Mettre à jour l'état de l'alarme

def cmd_off_alarme():
    enregistrer_historique("off_alarme", "Désarmé")
    client.publish("Gills/Commandes", "off_alarme")
    lblEtatAlarme.configure(text="Désarmé")  # Mettre à jour l'état de l'alarme
    

def cmd_on_lumiere_entree():
    enregistrer_historique("on_lumiere_entree", "Allumée")
    client.publish("Gills/Commandes", "on_lumiere_entree")
    lblEtatLumiereEntree.configure(text="Allumée")  # Mettre à jour l'état de la lumière d'entrée

def cmd_off_lumiere_entree():
    enregistrer_historique("off_lumiere_entree", "Éteinte")
    client.publish("Gills/Commandes", "off_lumiere_entree")
    lblEtatLumiereEntree.configure(text="Éteinte")  # Mettre à jour l'état de la lumière d'entrée

def cmd_on_lumiere_salon():
    enregistrer_historique("on_lumiere_salon", "Allumée")
    client.publish("Gills/Commandes", "on_lumiere_salon")
    lblEtatLumiereSalon.configure(text="Allumée")  # Mettre à jour l'état de la lumière du salon

def cmd_off_lumiere_salon():
    enregistrer_historique("off_lumiere_salon", "Éteinte")
    client.publish("Gills/Commandes", "off_lumiere_salon")
    lblEtatLumiereSalon.configure(text="Éteinte")

def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))
    commande = str(message.payload.decode("utf-8"))
    if commande == "on_alarme" or commande =="activer l'alarme" : 
        lblEtatAlarme.configure(text="Armé")  # Mettre à jour l'état de l'alarme
    elif commande == "off_alarme" :
        lblEtatAlarme.configure(text="Désarmé")  # Mettre à jour l'état de l'alarme
    elif commande == "on_lumiere_entree" :
        lblEtatLumiereEntree.configure(text="Allumée")  # Mettre à jour l'état de la lumière d'entrée
    elif commande == "off_lumiere_entree" :
        lblEtatLumiereEntree.configure(text="Éteinte")  # Mettre à jour l'état de la lumière d'entrée
    elif commande == "on_lumiere_salon" :
        lblEtatLumiereSalon.configure(text="Allumée")  # Mettre à jour l'état de la lumière du salon
    elif commande == "off_lumiere_salon" :
        lblEtatLumiereSalon.configure(text="Éteinte")  # Mettre à jour l'état de la lumière du salon
    elif commande == "on_porte_entree" :
        lblEtatPorteEntree.configure(text="Ouverte")
    elif commande == "off_porte_entree":
        lblEtatPorteEntree .configure(text="Fermée")
		
def afficher_commande_vocale():
    Thread(target=voice_command).start()


def afficher_historique():
    historique_window = Toplevel(fen1)
    historique_window.title("Historique")
    
    lbl_historique = Label(historique_window, text="Historique des commandes:")
    lbl_historique.pack()

    scrollbar = Scrollbar(historique_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    historique_listbox = Listbox(historique_window, yscrollcommand=scrollbar.set)
    historique_listbox.pack(fill=BOTH, expand=YES)
    
    for entry in historique_collection.find().sort("date_heure"):
        historique_listbox.insert(END, f"{entry['date_heure']} - Commande: {entry['commande']} - État: {entry['etat']}")

    scrollbar.config(command=historique_listbox.yview)

def set_custom_style():
    fen1.configure(background='#f2f2f2')
    frameAlarme.configure(bg='#f2f2f2', bd=2, relief=SOLID)  # Cadre pour l'alarme
    frameLumiereEntree.configure(bg='#f2f2f2', bd=2, relief=SOLID)  # Cadre pour la lumière d'entrée
    frameLumiereSalon.configure(bg='#f2f2f2', bd=2, relief=SOLID)  # Cadre pour la lumière du salon
    lblAlarme.configure(bg='#f2f2f2', fg='#333333')
    lblLumiereEntree.configure(bg='#f2f2f2', fg='#333333')
    lblLumiereSalon.configure(bg='#f2f2f2', fg='#333333')
    lblEtatAlarme.configure(bg='#f2f2f2', fg='#333333')
    lblEtatLumiereEntree.configure(bg='#f2f2f2', fg='#333333')
    lblEtatLumiereSalon.configure(bg='#f2f2f2', fg='#333333')
    btnOnAlarme.configure(bg='#4287f5', fg='#ffffff')
    btnOffAlarme.configure(bg='#ff4c4c', fg='#ffffff')
    btnOnLumiereEntree.configure(bg='#4287f5', fg='#ffffff')
    btnOffLumiereEntree.configure(bg='#ff4c4c', fg='#ffffff')
    btnOnLumiereSalon.configure(bg='#4287f5', fg='#ffffff')
    btnOffLumiereSalon.configure(bg='#ff4c4c', fg='#ffffff')
    
def update_current_time_label():
    now = get_current_datetime()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    lbl_current_time.configure(text=f"Heure actuelle: {current_time}")
    fen1.after(1000, update_current_time_label)


def display_weather_on_door():
    config_dict = get_default_config()
    config_dict['language'] = 'fr'

    owm = OWM("eccb2a11886394588a935face7bc445a", config=config_dict)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Montreal,CA')
    w = observation.weather

    icon_url = f"http://openweathermap.org/img/w/{w.weather_icon_name}.png"
    response = requests.get(icon_url)
    img = Image.open(BytesIO(response.content))
    img_tk = ImageTk.PhotoImage(img)
    
    frameWeather = Frame(fen1, bd=2, relief=SOLID)
    frameWeather.grid(row=1, column=3, padx=10, pady=10)
    img_label = Label(frameWeather, image=img_tk)
    img_label.image = img_tk
    img_label.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
    
    frameW = Frame(fen1, bd=2, relief=SOLID)
    frameW.grid(row=2, column=3, padx=10, pady=10)
	
    temperature = w.temperature('celsius')['temp']
    lblTemperature = Label(frameW, text=f"Montréal: {temperature:.1f}°C", font="Helvetica 12 bold", bg='#ffffff')
    lblTemperature.grid(row=1, column=1, columnspan=2, padx=5, pady=5)



    
    



    

""" MQTT """
host = "node02.myqtthub.com"
port = 1883
clean_session = True
client_id = "thermo"
user_name = "haikel"
password = "1234"

client = mqtt.Client(client_id=client_id, clean_session=clean_session)
client.username_pw_set(user_name, password)
client.connect(host, port)
client.loop_start()

client.subscribe("Gills/Etats")
client.on_message = on_message

""" Interface Tk """
fen1 = Tk()
fen1.protocol("WM_DELETE_WINDOW", fermer)

frameAlarme = Frame(fen1, bd=2, relief=SOLID)  # Cadre pour l'alarme
frameAlarme.grid(row=0, column=0, padx=10, pady=10)

lblAlarme = Label(frameAlarme, text="Alarme", font="Helvetica 20 bold")
lblAlarme.grid(row=0, column=0, columnspan=2, pady=10)

lblEtatAlarme = Label(frameAlarme, text="État", font="Helvetica 20 bold")
lblEtatAlarme.grid(row=1, column=0, columnspan=2, pady=10)

btnOnAlarme = Button(frameAlarme, text='ON', font="Helvetica 20 bold", command=cmd_on_alarme)
btnOnAlarme.grid(row=2, column=0, padx=10, pady=5)  # Bouton ON pour l'alarme déplacé vers le haut

btnOffAlarme = Button(frameAlarme, text='OFF', font="Helvetica 20 bold", command=cmd_off_alarme)
btnOffAlarme.grid(row=2, column=1, padx=10, pady=5)  # Bouton OFF pour l'alarme déplacé vers le haut

frameLumiereEntree = Frame(fen1, bd=2, relief=SOLID)  # Cadre pour la lumière d'entrée
frameLumiereEntree.grid(row=1, column=0, padx=10, pady=10)

lblLumiereEntree = Label(frameLumiereEntree, text="Lumière Entrée", font="Helvetica 20 bold")
lblLumiereEntree.grid(row=0, column=0, columnspan=2, pady=10)

lblEtatLumiereEntree = Label(frameLumiereEntree, text="État", font="Helvetica 20 bold") 
lblEtatLumiereEntree.grid(row=1, column=0, columnspan=2, pady=10)

btnOnLumiereEntree = Button(frameLumiereEntree, text='ON', font="Helvetica 20 bold", command=cmd_on_lumiere_entree)
btnOnLumiereEntree.grid(row=2, column=0, padx=10, pady=5)  # Bouton ON pour la lumière d'entrée déplacé vers le haut

btnOffLumiereEntree = Button(frameLumiereEntree, text='OFF', font="Helvetica 20 bold", command=cmd_off_lumiere_entree)
btnOffLumiereEntree.grid(row=2, column=1, padx=10, pady=5)  # Bouton OFF pour la lumière d'entrée déplacé vers le haut

frameLumiereSalon = Frame(fen1, bd=2, relief=SOLID)  # Cadre pour la lumière du salon
frameLumiereSalon.grid(row=2, column=0, padx=10, pady=10)

lblLumiereSalon = Label(frameLumiereSalon, text="Lumière Salon", font="Helvetica 20 bold")
lblLumiereSalon.grid(row=0, column=0, columnspan=2, pady=10)

lblEtatLumiereSalon = Label(frameLumiereSalon, text="État", font="Helvetica 20 bold") 
lblEtatLumiereSalon.grid(row=1, column=0, columnspan=2, pady=10)

btnOnLumiereSalon = Button(frameLumiereSalon, text='ON', font="Helvetica 20 bold", command=cmd_on_lumiere_salon)
btnOnLumiereSalon.grid(row=2, column=0, padx=10, pady=5)  # Bouton ON pour la lumière du salon déplacé vers le haut

btnOffLumiereSalon = Button(frameLumiereSalon, text='OFF', font="Helvetica 20 bold", command=cmd_off_lumiere_salon)
btnOffLumiereSalon.grid(row=2, column=1, padx=10, pady=5)  # Bouton OFF pour la lumière du salon déplacé vers le haut

btnHistorique = Button(fen1, text='Historique', font="Helvetica 15 bold", command=afficher_historique)
btnHistorique.grid(row=1, column=4, padx=10, pady=10)



framePorteEntree = Frame(fen1, bd=2, relief=SOLID)  # Cadre pour la porte d'entrée
framePorteEntree.grid(row=0, column=1, padx=10, pady=10)
framePorteEntree.configure(bg='#ffffff')

lblPorteEntree = Label(framePorteEntree, text="Porte Entrée", font="Helvetica 20 bold", bg='#ffffff')  # Set background color to white
lblPorteEntree.grid(row=0, column=0, columnspan=2, pady=10)

lblEtatPorteEntree = Label(framePorteEntree, text="État", font="Helvetica 20 bold", bg='#ffffff')  # Set background color to white
lblEtatPorteEntree.grid(row=1, column=0, columnspan=2, pady=10)

btnOnPorteEntree = Button(framePorteEntree, text='ON', font="Helvetica 20 bold", command=cmd_on_porte_entree, bg='#4287f5', fg='#ffffff')
btnOnPorteEntree.grid(row=2, column=0, padx=10, pady=5)

btnOffPorteEntree = Button(framePorteEntree, text='OFF', font="Helvetica 20 bold", command=cmd_off_porte_entree, bg='#ff4c4c', fg='#ffffff')
btnOffPorteEntree.grid(row=2, column=1, padx=10, pady=5)





btnCommandeVocale = Button(fen1, text='Commande Vocale', font="Helvetica 15 bold", command=afficher_commande_vocale)
btnCommandeVocale.grid(row=2, column=4, padx=10, pady=10)

top_frame = Frame(fen1, bd=2, relief=SOLID)  
top_frame.grid(row=0, column=2, columnspan=10, padx=10, pady=10)
lbl_current_time = Label(top_frame, text="", font="Helvetica 14 bold")
lbl_current_time.pack()
update_current_time_label()

#framePorteEntree = Frame(fen1, bd=2, relief=SOLID)  # Cadre pour la porte d'entrée
#framePorteEntree.grid(row=0, column=1, padx=10, pady=10)






set_custom_style()
display_weather_on_door()

fen1.mainloop()


