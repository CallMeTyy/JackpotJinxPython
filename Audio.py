import simpleaudio
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from pathlib import Path
import re
import Dataset
import constants



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

def __get_sfx_audio(index: int):
    match index:
        case 0:
            return AudioSegment.from_wav("Audio/SFX/CasinoMusic.wav")
        case 1:
            return AudioSegment.from_wav("Audio/SFX/FirstWheelSpinning.wav")
        case 2:
            return AudioSegment.from_wav("Audio/SFX/SecondWheelSpinning.wav")
        case 3:
            return AudioSegment.from_wav("Audio/SFX/ThirdWheelSpinning.wav")
        case 4:
            return AudioSegment.from_wav("Audio/SFX/ConfirmFirstWheel.wav")
        case 5:
            return AudioSegment.from_wav("Audio/SFX/ConfirmSecondWheel.wav")
        case 6:
            return AudioSegment.from_wav("Audio/SFX/ConfirmThirdWheel.wav")
        case 7:
            return AudioSegment.from_wav("Audio/SFX/Shredding.wav")

def _getDataWav(input):
    path = "Audio/Data/" + str(input[0]) + str(input[1]) + str(input[2]) + ".wav"
    if(Path(path).is_file()):
        return AudioSegment.from_wav(path)
    else:
       return "Not Found"

def playVoice(input : tuple):
    if(re.fullmatch("\([0-9], [0-9], [0-9]\)", str(input))):
        money = str(Dataset.fetchData(input))
        print("The value for country " + str(input[0]) +  ", column " + str(input[1]) +", row " + str(input[2]) + ", is: " + money)
        if (money is "N/A"):
            clip = _getDataWav(input)
            playing = play(clip)
        else:
            clip = Congratulations + _getDataWav(input) + _getCountryWav(input[0]) + _getGameWav(input[1]) + _getYearWav(input[2])
            playing = play(clip)
    else:
        print("Input not accepted, it should be in the form of int,int,int")

def play_vfx_once(index: int):
    play_one_shot(__get_sfx_audio(index))

def play_one_shot_path(path:str):
    if(Path(path).is_file):
        print("Playing sound: " + path)
        sound = AudioSegment.from_wav(path)
        play(sound)
    else:
        print("Sound: " + path + " Not found")

def play_one_shot(audio: AudioSegment):
    if audio:
        play(audio)
    else:
        print("Invalid AudioSegment tried to play")

def playLoop(index):
        if(index == 0):
            if(0 not in playingLoops):
                playingLoops[index] = music.play()
                if constants.COMM_DEBUG:
                    print("Playing loop " + str(index))

def play_sfx_loop(index: int):
    if __get_sfx_audio(index) not in playingLoops:
        playingLoops[__get_sfx_audio(index)] = play(__get_sfx_audio(index))

def stopLoop(index):
    if(index in playingLoops):
        playingLoops.pop(index)
        if constants.COMM_DEBUG:
            print("Stopping loop " + str(index))

def stop_sfx_loop(index: int):
    if __get_sfx_audio(index) in playingLoops:
        playingLoops[__get_sfx_audio(index)].stop()
        playingLoops.pop(__get_sfx_audio(index))

def handleLoops():
    for wave,p in playingLoops.items():
        if not p.is_playing():            
            playingLoops[wave] = play(wave)


    