import constants
import re



def Decode(inputData):
    """Docodes the data into a tuple. {string inputData}"""
    decodedData = tuple()
    # Decode the data into a tuple to be used to call several functions and retrieve data from the input table
    return decodedData

def Encode(processedData):
    """Encodes the data required back into a string. {int dataType}"""
    encodedData = ""
    # Encode the processed data into a simple protocol to send back to the arduino
    return encodedData



def decode_header(input):
    """ checks what the header of the message is. After that, goes to specific decoder for the rest"""
    head = input[:constants.HEADER_LENGTH]   
    tail = input[constants.TAIL_LENGTH:]
    match head:
        case "LE":
            decode_lever(input, tail)            
        case "BT":
            decode_button(input, tail)
        case "RL":
            decode_reel(input, tail)
        case "SY":
            decode_sys(input, tail)      
        

def decode_lever(input, tail):
    """Specific decoder for the lever"""
    print(f"LEV {tail}")

def decode_button(input, tail):
    """Specific decoder for the button"""
    headerdata = input[:constants.HEADER_LENGTH+1][2:]
    print(f"BT{headerdata} {tail}")

def decode_reel(input, tail):
    """Specific decoder for the reel"""
    headerdata = input[:constants.HEADER_LENGTH+1][2:]
    print(f"RL{headerdata} {tail}")

def decode_sys(input, tail):
    """Specific decoder for the system"""
    print(f"Sys {tail}")
    

