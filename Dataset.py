from pandas import DataFrame
from pathlib import Path
import re

import constants

# Dataset for Britain. If data is missing a value of 0 is used.
dataBritain = DataFrame([[202.70,75.68,177.16,37.01],[193.69,89.94,187.45,38.74],[168.34,77.00,156.74,32.61],[177.64,73.87,160.07,33.08],[190.99,68.96,114.99,27.44],[240.57,21.64,59.76,14.21],[288.47,67.45,147.93,27.02]], columns=(0,1,2,3))
# Dataset for Nevada. If data is missing a value of 0 is used.
dataNevada = DataFrame([[0.00,296.72,7.54,0.93],[0.00,349.62,8.25,1.05],[0.00,350.68,8.89,1.23],[0.00,317.16,9.17,1.16],[0.00,303.62,9.30,1.17],[0.00,468.07,24.18,1.64],[0.00,448.20,22.53,2.04]], columns=(0,1,2,3))
# Dataset for Macau. If data is missing a value of 0 is used.
dataMacau = DataFrame([[0.02,765.75,3.20,0.00],[0.03,817.81,3.34,0.00],[0.04,958.74,3.08,0.00],[0.04,863.39,2.91,0.00],[0.04,792.42,2.28,0.00],[0.23,1088.05,10.69,0.00],[0.27,1484.64,11.55,0.00]], columns=(0,1,2,3))
# Dataset for Australia. If data is missing a value of 0 is used.
dataAustralia = DataFrame([[77.74,627.86,146.14,13.73],[71.02,600.11,155.18,13.87],[74.62,627.52,176.16,13.87],[85.67,582.79,166.78,12.94],[81.10,423.80,141.15,10.38],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]], columns=(0,1,2,3))
# Create tuple holding all of the datasets.
data = (dataBritain,dataNevada,dataAustralia,dataMacau)

# Function to retrieve data from the dataset. Checks if input is in range, if it is return the datapoint.
def fetch_data(input : tuple):
    """Function to retrieve the data from the dataset. Returns float. or nothing if input is out of range."""
    if constants.AUDIO_DEBUG:
        print("final reel values = " + str(input))
    if(re.fullmatch("\([0-9], [0-9], [0-9]\)", str(input))):
        if(input[0] >= len(data)):
            print("Country not in dataset...")
        elif(input[1] >= data[input[0]].shape[1]):
            print("Game not found in dataset...")
        elif(input[2] >= data[input[0]].shape[0]):
            print("Year not found in dataset...")
        else:
            country = data[input[0]]
            game = country[input[1]]
            money_lost = game[input[2]]
            return money_lost
    else:
        print("Input not accepted, it should be in the form of int,int,int")




