import simpleaudio
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from pathlib import Path
import re
import Dataset

playingLoops = {}

Congratulations = AudioSegment.from_wav("Audio/Standard/Congratulations.wav")

music = simpleaudio.WaveObject.from_wave_file("Audio/Standard/Congratulations.wav")

def _getCountryWav(input):
    if(input == 0):
        return AudioSegment.from_wav("Audio/Countries/Britain.wav")
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Countries/Nevada.wav")
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Countries/Macau.wav")
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Countries/Australia.wav")
    return

def _getGameWav(input):
    if(input == 0):
        return AudioSegment.from_wav("Audio/Games/Casinos.wav")
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Games/Bingo.wav")
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Games/Lotteries.wav")
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Games/Sportsbetting.wav")
    return

def _getYearWav(input):
    if(input == 0):
        return AudioSegment.from_wav("Audio/Years/2015.wav")
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Years/2016.wav")
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Years/2017.wav")
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Years/2018.wav")
    elif(input == 4):
        return AudioSegment.from_wav("Audio/Years/2019.wav")
    elif(input == 5):
        return AudioSegment.from_wav("Audio/Years/2020.wav")
    elif(input == 6):
        return AudioSegment.from_wav("Audio/Years/2021.wav")
    return

def _getDataWav(input):
    path = "Audio/Data/" + str(input[0]) + str(input[1]) + str(input[2]) + ".wav"
    if(Path(path).is_file()):
        return AudioSegment.from_wav(path)
    else:
       return "Not Found"

def playVoice(inputs):
    if(re.fullmatch("[0-9],[0-9],[0-9]", str(inputs))):
        input = tuple(int(x)for x in inputs.split(","))
        if(input[0] >= len(data)):
            print("Country not in dataset...")
        elif(input[1] >= len(data)):
            print("Game not found in dataset...")
        else:
            money = str(Dataset.fetchData(inputs))
            print("The value for country " + str(input[0]) +  ", column " + str(input[1]) +", row " + str(input[2]) + ", is: " + money)
            if (money is "N/A"):
                clip = _getDataWav(input)
                playing = play(clip)
            else:
                clip = Congratulations + _getDataWav(input) + _getCountryWav(input[0]) + _getGameWav(input[1]) + _getYearWav(input[2])
                playing = play(clip)
    else:
        print("Input not accepted, it should be in the form of int,int,int")

def playOneShot(path):
    if(Path(path).is_file):
        print("Playing sound: " + path)
        sound = AudioSegment.from_wav(path)
        play(sound)
    else:
        print("Sound: " + path + " Not found")

def playLoop(index):
        if(index == 0):
            if(0 not in playingLoops):
                playingLoops[index] = music.play()
                print("Playing loop " + str(index))


def stopLoop(index):
    if(index in playingLoops):
        playingLoops.pop(index)
        print("Stopping loop " + str(index))

def handleLoops():
    for entries in playingLoops:
        if(entries == 0):
            if not playingLoops[entries].is_playing():
                playingLoops[entries] = music.play()


    