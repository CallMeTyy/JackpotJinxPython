import simpleaudio
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from pathlib import Path
import re
import Dataset
import constants

playingLoops = {}
__wait_for_sounds = {}

Congratulations = AudioSegment.from_wav("Audio/Standard/Congratulations.wav")

music = simpleaudio.WaveObject.from_wave_file("Audio/Standard/Congratulations.wav")

win = AudioSegment.from_wav("Audio/SFX/Win.wav")

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
        case 8:
            return AudioSegment.from_wav("Audio/SFX/ConfirmThirdWheel.wav") # TODO actually input the win sound
        case 9:
            return AudioSegment.from_wav("Audio/SFX/PlatformRising.wav")
        case 10:
            return AudioSegment.from_wav("Audio/SFX/Win.wav")

def _getDataWav(input):
    path = "Audio/Data/" + str(input[0]) + str(input[1]) + str(input[2]) + ".wav"
    if(Path(path).is_file()):
        return AudioSegment.from_wav(path)
    else:
       return "Not Found"

def playVoice(input : tuple):
    if(re.fullmatch("\([0-9], [0-9], [0-9]\)", str(input))):
        money = Dataset.fetch_data(input)
        if constants.AUDIO_DEBUG:
            print("The value for country " + str(input[0]) +  ", column " + str(input[1]) +", row " + str(input[2]) + ", is: " + str(money))
        if money == 0.0:
            clip = _getDataWav(input)
            playing = play(clip)
            __wait_for_sounds[0] = playing
        else:
            clip = win + Congratulations + _getDataWav(input) + _getCountryWav(input[0]) + _getGameWav(input[1]) + _getYearWav(input[2])
            playing = play(clip)
            __wait_for_sounds[0] = playing
    else:
        print("Input not accepted, it should be in the form of int,int,int")

def play_vfx_once(index: int):
    playFile = play_one_shot(__get_sfx_audio(index))
    if (index == constants.AUDIO_VICTORY):
        __wait_for_sounds[1] = playFile

def play_one_shot_path(path:str):
    if(Path(path).is_file):
        if constants.AUDIO_DEBUG:
            print("Playing sound: " + path)
        sound = AudioSegment.from_wav(path)
        play(sound)
    else:
        print("Sound: " + path + " Not found")

def play_one_shot(audio: AudioSegment):
    if audio:
        return play(audio)
    else:
        print("Invalid AudioSegment tried to play")

def play_sfx_loop(index: int):
    if __get_sfx_audio(index) not in playingLoops:
        playingLoops[__get_sfx_audio(index)] = play(__get_sfx_audio(index))

def wait_for_voice_done():
    if 0 in __wait_for_sounds:
        if not __wait_for_sounds[0].is_playing():
            __wait_for_sounds.pop(0)
            return 0
    elif 1 in __wait_for_sounds:
        if not __wait_for_sounds[1].is_playing():
            __wait_for_sounds.pop(1)
            return 1
    return -1
def stop_sfx_loop(index: int):
    if __get_sfx_audio(index) in playingLoops:
        playingLoops[__get_sfx_audio(index)].stop()
        playingLoops.pop(__get_sfx_audio(index))

def handle_loops():
    for wave,p in playingLoops.items():
        if not p.is_playing():            
            playingLoops[wave] = play(wave)

def play_shredder(value):
    shredder = AudioSegment.from_wav("Audio/SFX/Shredding.wav")[:remap(value, 0.02, 1500, 3, 10) * 1000]
    return play(shredder.fade_out(500))

def remap(old_val, old_min, old_max, new_min, new_max):
    return (new_max - new_min)*(old_val - old_min) / (old_max - old_min) + new_min


    