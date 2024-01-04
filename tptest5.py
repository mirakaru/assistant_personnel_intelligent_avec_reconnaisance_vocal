from speech_recognition import Recognizer, Microphone
from PicoTTS import TTS_engine
import datetime
from pyowm import OWM
from pyowm.utils.config import get_default_config
import re
import time 
from threading import Thread
import paho.mqtt.client as mqtt

config_dict = get_default_config()
config_dict['language'] = 'fr'

owm = OWM('eccb2a11886394588a935face7bc445a', config_dict)
mgr = owm.weather_manager()




def get_current_datetime():
    return datetime.datetime.now()

def voice_command():
    recognizer = Recognizer()
    tts = TTS_engine()
    
    host = "node02.myqtthub.com"
    port = 1883
    user_name = "haikel"
    password = "1234"
    client = mqtt.Client(client_id="voice_control", clean_session=True)
    client.username_pw_set(user_name, password)
    client.connect(host, port)
    client.loop_start()

    while True: 
        with Microphone() as source:
            print("Réglage du bruit ambiant... Patientez...")
            recognizer.adjust_for_ambient_noise(source)
            print("Vous pouvez parler...")
            recorded_audio = recognizer.listen(source)
            print("Enregistrement terminé !")

        try:
            print("Reconnaissance du texte...")
            text = recognizer.recognize_google(
                recorded_audio,
                language="fr-FR"
            )
            print("Vous avez dit : {}".format(text))
            
            keywords_lights = {
                "ouvrir la lumière de l'entrée": "La lumière de l'entrée est allumée.",
                "allumer la lumière de l'entrée": "La lumière de l'entrée est allumée.",
                "fermer la lumière de l'entrée": "La lumière de l'entrée est éteinte.",
                "éteindre la lumière de l'entrée": "La lumière de l'entrée est éteinte.",
                "ouvrir la lumière du salon": "La lumière du salon est allumée.",
                "allumer la lumière du salon": "La lumière du salon est allumée.",
                "fermer la lumière du salon": "La lumière du salon est éteinte.",
                "éteindre la lumière du salon": "La lumière du salon est éteinte.",
                "ouvrir la porte de l'entrée": "La porte de l'entrée est ouverte.",
                "fermer la porte de l'entrée": "La porte de l'entrée est fermée.",
                "ouvrir l'alarme": "L'alarme est activée.",
                "activer l'alarme": "L'alarme est activée.",
                "fermer l'alarme": "L'alarme est désactivée.",
                "déconnecter l'alarme": "L'alarme est désactivée."
            }

            found = False  

            for command, response in keywords_lights.items():
                if command in text:
                    client.publish("Gills/Commandes", command)  # Envoie la commande MQTT
                    tts.say(response)
                    found = True
                    break



            
            phrases = [
                u"quelle heure est-il?", u"il est quelle heure?",
                u"quel temps fait-il?", u"quelles sont les prévisions météo?",
                u"quelles sont les prévisions de la météo?",
                u"ouvrir la lumière de l'entrée",
                u"allumer la lumière de l'entrée",
                u"fermer la lumière de l'entrée",
                u"éteindre la lumière de l'entrée",
                u"ouvrir la lumière du salon",
                u"allumer la lumière du salon",
                u"fermer la lumière du salon",
                u"éteindre la lumière du salon",
                u"desactiver l'alarme",
            ]
            modeles = [
                "(.)*quelle\sheure(.)*", "(.)*quelle\sheure(.)*",
                "(.)*quel\stemps(.)*", u"(.)*quelle\ssont\s(.)*prévision(.)*",
                u"(.)*quelles\ssont\s(.)*prévisions(.)*",
                "(?i).*ouvrir\s+lumière\s+entrée.*",
                "(?i).*allumer\s+lumière\s+entrée.*",
                "(?i).*fermer\s+lumière\s+entrée.*",
                "(?i).*éteindre\s+lumière\s+entrée.*",
                "(?i).*ouvrir\s+lumière\s+salon.*",
                "(?i).*allumer\s+lumière\s+salon.*",
                "(?i).*fermer\s+lumière\s+salon.*",
                "(?i).*éteindre\s+lumière\s+salon.*",
                "(?i).*désactiver\s+alarme.*"
            ]
            
            for i in range(len(phrases)):
                if re.match(modeles[i], text) is not None:
                    tts_response = "J'ai trouvé!!! " + phrases[i]
                    tts.say(tts_response)
                    print(phrases[i]) # ma verificiation  
                    if phrases[i] in keywords_lights.keys():
                        print(keywords_lights[phrases[i]]) # verification de ma maniere
                        tts.say(keywords_lights[phrases[i]])
                    found = True

            if re.match(r".*quelle\s?heure.*", text):
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M")
                tts_response = "Il est {}.".format(current_time)
                tts.say(tts_response)
                        
            if re.match(r".*quel\s?temps.*", text):
                observation = mgr.weather_at_place('Montreal,CA')
                w = observation.weather
                temperature = w.temperature('celsius')['temp']
                tts_response = f"La température à Montréal est de {temperature} degrés Celsius."
                tts.say(tts_response)

            
            if not found:
                tts.say("Rien n'a été détecté.")




        except Exception as ex:
            print(ex)
    
        time.sleep(1) 

if __name__ == "__main__":
    voice_command()
