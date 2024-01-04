# -*- coding: utf-8 -*-
'''
Created on 10 avr. 2019


Installation de la librairie libpico (Svox Pico)
Installation de aplay

'''
import subprocess

class TTS_engine():
    def __init__(self):
        self.wavfile = "say.wav"
        self.voice = "fr-FR"
        
    def say(self, msg):
        cmd = ["pico2wave", "-l", self.voice, "-w", self.wavfile, msg]
        subprocess.call(cmd)
        cmd = ["aplay", "-q", self.wavfile]
        subprocess.call(cmd)
        
if __name__ == "__main__":
    tts = TTS_engine();
    tts.say(u"Bonjour stephane, il est 9 heures")
    print("fin")
