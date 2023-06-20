import simpleaudio as Audio
from pandas import DataFrame
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
from pathlib import Path
import re

dataBritain = DataFrame([[75.68,37.01,202.70,177.16],[89.94,38.74,193.69,187.45],[77.00,32.61,168.34,156.74],[73.87,33.08,177.64,160.07],[68.96,27.44,190.99,114.99],[21.64,14.21,240.57,59.76],[67.45,27.02,288.47,147.93]], columns=(0,1,2,3))
print(dataBritain)
dataNevada = DataFrame([[296.72,0.93, "N/A",7.54],[349.62,1.05,"N/A",8.25],[350.68,1.23,"N/A",8.89],[317.16,1.16,"N/A",9.17],[303.62,1.17,"N/A",9.30],[468.07,1.64,"N/A",24.18],[448.20,2.04,"N/A",22.53]], columns=(0,1,2,3))
print(dataNevada)
dataMacau = DataFrame([[765.75, "N/A",0.02,3.20],[817.81,"N/A",0.03,3.34],[958.74,"N/A",0.04,3.08],[863.39,"N/A",0.04,2.91],[792.42,"N/A",0.04,2.28],[1088.05,"N/A",0.23,10.69],[1484.64,"N/A",0.27,11.55]], columns=(0,1,2,3))
print(dataMacau)
dataAustralia = DataFrame([[627.86,13.73,77.74,146.14],[600.11,13.87,71.02,155.18],[627.52,13.87,74.62,176.16],[582.79,12.94,85.67,166.78],[423.80,10.38,81.10,141.15],["N/A", "N/A", "N/A", "N/A"],["N/A", "N/A", "N/A", "N/A"]], columns=(0,1,2,3))
print(dataAustralia)
data = (dataBritain,dataNevada,dataMacau,dataAustralia)

def FetchData(input):
    country = data[input[0]]
    game = country[input[1]]
    year = game[input[2]]
    return year

hasPlayed = False;
Congratulations = AudioSegment.from_wav("Audio/Standard/Congratulations.wav")



def GetCountryWav(input):
    if(input == 0):
        return AudioSegment.from_wav("Audio/Countries/Britain.wav")
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Countries/Nevada.wav")
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Countries/Macau.wav")
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Countries/Australia.wav")
    return

def GetGameWav(input):
    if(input == 0):
        return AudioSegment.from_wav("Audio/Games/Casinos.wav")
    elif(input == 1):
        return AudioSegment.from_wav("Audio/Games/Bingo.wav")
    elif(input == 2):
        return AudioSegment.from_wav("Audio/Games/Lotteries.wav")
    elif(input == 3):
        return AudioSegment.from_wav("Audio/Games/Sportsbetting.wav")
    return

def GetYearWav(input):
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

def GetDataWav(input):
    path = "Audio/Data/" + str(a[0]) + str(a[1]) + str(a[2]) + ".wav"
    if(Path(path).is_file()):
        return AudioSegment.from_wav(path)
    else:
       return "Not Found"

while(True):
    a=input ('What Country, Game and year to retrieve? : ') 
    
    if(re.fullmatch("[0-9],[0-9],[0-9]", a) != None):
        a = tuple(int(x)for x in a.split(","))
        if(a[0] >= len(data)):
            print("Country not in dataset...")
        elif(a[1] >= len(data)):
            print("Game not found in dataset...")
        else:
            money = str(FetchData(a))
            print("The value for country " + str(a[0]) +  ", column " + str(a[1]) +", row " + str(a[2]) + ", is: " + money)
            if (money is "N/A"):
                clip = GetDataWav(a)
                playing = play(clip)
            else:
                clip = Congratulations + GetDataWav(a) + GetCountryWav(a[0]) + GetGameWav(a[1]) + GetYearWav(a[2])
                playing = play(clip)
    else:
        print("Input not accepted, it should be in the form of int,int,int")