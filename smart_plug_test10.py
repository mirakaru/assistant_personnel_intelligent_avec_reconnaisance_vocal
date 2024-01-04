'''
Created on 21 juin 2021

@author: gills
'''
from RPiSim import GPIO
import paho.mqtt.client as mqtt
import time
import sys
import signal




def terminer(signum, frame):
    print("Terminer")
    GPIO.output(18, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(14, GPIO.LOW)
    
    
    GPIO.cleanup()
    sys.exit(0)

def event_17(channel):
    print("event_17: Bouton poussoir")
    if GPIO.input(18):
        GPIO.output(18, GPIO.LOW)
        print("alarme OFF")
        client.publish("Gills/Etats", "off_alarme")
    else:
        GPIO.output(18, GPIO.HIGH)
        print("alarme On")
        client.publish("Gills/Etats", "on_alarme")
def event_27(channel):
    print("event_27: Bouton poussoir")
    if GPIO.input(23):
        GPIO.output(23, GPIO.LOW)
        print("lumiere entrée OFF")
        client.publish("Gills/Etats", "off_lumiere_entree")
    else:
        GPIO.output(23, GPIO.HIGH)
        print("lumiere entrée On")
        client.publish("Gills/Etats", "on_lumiere_entree")

def event_22(channel):
    print("event_22: Bouton poussoir")
    if GPIO.input(24):
        GPIO.output(24, GPIO.LOW)
        print("lumiere salon OFF")
        client.publish("Gills/Etats", "off_lumiere_salon")
    else:
        GPIO.output(24, GPIO.HIGH)
        print("lumiere salon On")
        client.publish("Gills/Etats", "on_lumiere_salon")
def event_4(channel):
    print("event4: Bouton poussoir")
    if GPIO.input(14):
        GPIO.output(14, GPIO.LOW)
        print("Porte entree fermee")
        client.publish("Gills/Etats", "off_porte_entree")
    else:
        GPIO.output(14, GPIO.HIGH)
        print("Porte entree ouverte")
        client.publish("Gills/Etats", "on_porte_entree")


def on_message(client, userdata, message):

    print("received message1: " , str(message.payload.decode("utf-8")))
    commande = str(message.payload.decode("utf-8"))
    if commande == "on_alarme" or commande =="ouvrir l'alarme" or commande =="activer l'alarme":
        GPIO.output(18, GPIO.HIGH)
        
        print("alarme On")
        client.publish("Gills/Etats", "activer l'alarme")
    elif commande == "off_alarme"  or commande =="fermer l'alarme" or commande =="déconnecter l'alarme":
        GPIO.output(18, GPIO.LOW)
        print("alarme Off")
        client.publish("Gills/Etats", "off_alarme")
    elif commande == "on_lumiere_entree" or commande =="ouvrir la lumière de l'entrée" or commande =="allumer la lumière de l'entrée":
        GPIO.output(23, GPIO.HIGH)
        print("lumiere entrée On")
        client.publish("Gills/Etats", "on_lumiere_entree")
    elif commande == "off_lumiere_entree" or commande =="fermer la lumière de l'entrée" or commande =="éteindre la lumière de l'entrée":
        GPIO.output(23, GPIO.LOW)
        print("lumiere entré Off")
        client.publish("Gills/Etats", "off_lumiere_entree")
    elif commande == "on_lumiere_salon" or commande =="ouvrir la lumière du salon" or commande =="allumer la lumière du salon":
        GPIO.output(24, GPIO.HIGH)
        print("lumiere salon On")
        client.publish("Gills/Etats", "on_lumiere_salon")
    elif commande == "off_lumiere_salon"or commande =="fermer la lumière du salon" or commande =="éteindre la lumière du salon":
        GPIO.output(24, GPIO.LOW)
        print("lumiere salon Off")
        client.publish("Gills/Etats", "off_lumiere_salon")
    elif commande == "on_porte_entree"or commande =="ouvrir la porte de l'entrée" :
        GPIO.output(14, GPIO.HIGH)
        print("Porte entrée ouverte")
        client.publish("Gills/Etats", "on_porte_entree")
    elif commande == "off_porte_entree"or commande =="fermer la porte de l'entrée" :
        GPIO.output(14, GPIO.LOW)
        print("Porte entrée fermé")
        client.publish("Gills/Etats", "off_porte_entree")
    elif commande == "activer l'alarme" or commande =="ouvrir l'alarme" :
        GPIO.output(18, GPIO.HIGH)
        print("alarme On")
        client.publish("Gills/Etats", "on")
    elif commande == "fermer l'alarme" or commande == "déconnecter l'alarme":
            GPIO.output(18, GPIO.LOW)
            print("alarme Off")
            client.publish("Gills/Etats", "off")
        
        
        
     

        


""" Les GPIO  """
signal.signal(signal.SIGINT, terminer)
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    """ Bouton poussoir on/off """
    GPIO.setup(17,GPIO.MODE_IN,pull_up_down = GPIO.PUD_UP) 
    GPIO.add_event_detect(17, GPIO.FALLING, callback=event_17)
    GPIO.setup(27,GPIO.MODE_IN,pull_up_down = GPIO.PUD_UP) 
    GPIO.add_event_detect(27, GPIO.FALLING, callback=event_27)
    GPIO.setup(22,GPIO.MODE_IN,pull_up_down = GPIO.PUD_UP) 
    GPIO.add_event_detect(22, GPIO.FALLING, callback=event_22)
    GPIO.setup(4,GPIO.MODE_IN,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(4, GPIO.FALLING, callback=event_4)
    
    
    """ Lumière """
    GPIO.setup(18,GPIO.MODE_OUT, initial=GPIO.LOW)
    GPIO.setup(23,GPIO.MODE_OUT, initial=GPIO.LOW)
    GPIO.setup(24,GPIO.MODE_OUT, initial=GPIO.LOW)
    GPIO.setup(14,GPIO.MODE_OUT, initial=GPIO.LOW)
    
except Exception:
    print("Problème avec les GPIO")

host = "node02.myqtthub.com"
port = 1883
clean_session = True
client_id = "thermo"
user_name = "haikel"
password = "1234"

client = mqtt.Client(client_id=client_id, clean_session=clean_session)
client.username_pw_set(user_name, password)
client.connect(host, port)

client2 = mqtt.Client(client_id="lumiere_entree", clean_session=clean_session)
client2.username_pw_set("haikel", "1234")  # Remplacez par les valeurs appropriées pour la lumière de l'entrée
client2.connect(host, port)

client.loop_start()
client.subscribe("Gills/Commandes")
client.on_message = on_message

client2.loop_start()
client2.subscribe("Gills/Commandes_Lumiere_Entree")
client2.on_message = on_message

client3 = mqtt.Client(client_id="voice_control", clean_session=clean_session)
client3.username_pw_set("haikel", "1234")  # Remplacez par les valeurs appropriées pour la lumière de l'entrée
client3.connect(host, port)

client3.loop_start()
client3.subscribe("Gills/Commandes_voice_control")
client3.on_message = on_message

client4 = mqtt.Client(client_id="voice_control", clean_session=clean_session)
client4.username_pw_set("haikel", "1234")  # Remplacez par les valeurs appropriées pour la lumière de l'entrée
client4.connect(host, port)

client4.loop_start()
client4.subscribe("Gills/Commandes_voice_control")
client4.on_message = on_message
    
while True:
    time.sleep(0.5)
    
