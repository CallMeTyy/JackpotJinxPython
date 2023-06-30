import math

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
    """Retrieve AudioSegment for certain country."""
    if(input == 0):
        return AudioSegment.from_wav("Audio/Countries/Britain.wav") + constants.AUDIO_BOOST
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Countries/Nevada.wav") + constants.AUDIO_BOOST
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Countries/Macau.wav") + constants.AUDIO_BOOST
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Countries/Australia.wav") + constants.AUDIO_BOOST
    return

def _getGameWav(input):
    """Retrieve AudioSegment for certain game."""
    if(input == 1):
        return AudioSegment.from_wav("Audio/Games/Casinos.wav") + constants.AUDIO_BOOST
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Games/Bingo.wav") + constants.AUDIO_BOOST
    elif(input == 0):
        return AudioSegment.from_wav("Audio/Games/Lotteries.wav") + constants.AUDIO_BOOST
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Games/Sportsbetting.wav") + constants.AUDIO_BOOST
    return

def _getYearWav(input):
    """Retrieve AudioSegment for certain year."""
    if(input == 5):
        return AudioSegment.from_wav("Audio/Years/2015.wav") + constants.AUDIO_BOOST
    elif(input == 4):
        return AudioSegment.from_wav("Audio/Years/2016.wav") + constants.AUDIO_BOOST
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Years/2017.wav") + constants.AUDIO_BOOST
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Years/2018.wav") + constants.AUDIO_BOOST
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Years/2019.wav") + constants.AUDIO_BOOST
    elif(input == 0):
        return AudioSegment.from_wav("Audio/Years/2020.wav") + constants.AUDIO_BOOST
    elif(input == 6):
        return AudioSegment.from_wav("Audio/Years/2021.wav") + constants.AUDIO_BOOST
    return

def __get_sfx_audio(index: int):
    """Retrieve AudioSegment for certain SFX."""
    match index:
        case 0:
            return AudioSegment.from_wav("Audio/SFX/CasinoMusic.wav") + constants.AUDIO_BOOST
        case 1:
            return AudioSegment.from_wav("Audio/SFX/FirstWheelSpinning.wav") + constants.AUDIO_BOOST
        case 2:
            return AudioSegment.from_wav("Audio/SFX/SecondWheelSpinning.wav") + constants.AUDIO_BOOST
        case 3:
            return AudioSegment.from_wav("Audio/SFX/ThirdWheelSpinning.wav") + constants.AUDIO_BOOST
        case 4:
            return AudioSegment.from_wav("Audio/SFX/ConfirmFirstWheel.wav") + constants.AUDIO_BOOST
        case 5:
            return AudioSegment.from_wav("Audio/SFX/ConfirmSecondWheel.wav") + constants.AUDIO_BOOST
        case 6:
            return AudioSegment.from_wav("Audio/SFX/ConfirmThirdWheel.wav") + constants.AUDIO_BOOST
        case 7:
            return AudioSegment.from_wav("Audio/SFX/Shredding.wav") + constants.AUDIO_BOOST
        case 8:
            return AudioSegment.from_wav("Audio/SFX/ConfirmThirdWheel.wav") + constants.AUDIO_BOOST
        case 9:
            return AudioSegment.from_wav("Audio/SFX/PlatformRising.wav") + constants.AUDIO_BOOST
        case 10:
            return AudioSegment.from_wav("Audio/SFX/Win.wav") + constants.AUDIO_BOOST

def _getDataWav(input : tuple):
    """Retrieve AudioSegment for certain datapoint."""
    gameNum = 3-input[1]
    path = "Audio/Data/" + str(input[0]) + str(gameNum) + str(input[2]) + ".wav"
    if(Path(path).is_file()):
        return AudioSegment.from_wav(path) + constants.AUDIO_BOOST
    else:
       return "Not Found"

def playVoice(input : tuple):
    """Play the correct voiceline based on the datapoint."""
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
    """Play certain VFX sound based on index."""
    playFile = play_one_shot(__get_sfx_audio(index))
    if (index == constants.AUDIO_VICTORY):
        __wait_for_sounds[1] = playFile

def play_one_shot_path(path:str):
    """Play sound once based on path to the wav file."""
    if(Path(path).is_file):
        if constants.AUDIO_DEBUG:
            print("Playing sound: " + path)
        sound = AudioSegment.from_wav(path)
        play(sound)
    else:
        print("Sound: " + path + " Not found")

def play_one_shot(audio: AudioSegment):
    """Play given audioSegment once."""
    if audio:
        return play(audio)
    else:
        print("Invalid AudioSegment tried to play")

def play_sfx_loop(index: int):
    """Play certain VFX sound based on index and keep looping."""
    if __get_sfx_audio(index) not in playingLoops:
        playingLoops[__get_sfx_audio(index)] = play(__get_sfx_audio(index)*25)

def wait_for_voice_done():
    """Checks if a voiceline or the victory music is playing. returns 0 if voiceline has finished, 1 if victory music has finished and -1 if it is still playing either or not playing at all."""
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
    """Stop looping sound based on index."""
    if __get_sfx_audio(index) in playingLoops:
        playingLoops[__get_sfx_audio(index)].stop()
        playingLoops.pop(__get_sfx_audio(index))

def handle_loops():
    """Check for each item that should loop if it is still playing, if not start playing again. This function should be called every frame for loops to work correctly."""
    for wave,p in playingLoops.items():
        if not p.is_playing():            
            playingLoops[wave] = play(wave)

def play_shredder(value):
    """Plays the shredder sound for a duration tied to the value."""
    if constants.LOG_HGT and value != 0:
        value = math.log10(value)
    mmin = constants.MIN_MONEY if not constants.LOG_HGT else math.log(constants.MIN_MONEY)
    mmax = constants.MAX_MONEY if not constants.LOG_HGT else math.log(constants.MAX_MONEY)
    shredder = AudioSegment.from_wav("Audio/SFX/Shredding.wav")[:remap(value, mmin, mmax,
                                                            constants.SHRED_TIME_MIN, constants.SHRED_TIME_MAX) * 1000] + constants.AUDIO_BOOST + 3
    return play(shredder.fade_out(500))

def remap(old_val, old_min, old_max, new_min, new_max):
    """Remaps value to a new range."""
    return (new_max - new_min)*(old_val - old_min) / (old_max - old_min) + new_min


    