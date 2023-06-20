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

def encode_platform_height(money):
    outmin = constants.PLATFORM_MINHEIGHT
    outmax = constants.PLATFORM_MAXHEIGHT
    mmin = constants.MIN_MONEY
    mmax = constants.MAX_MONEY
    height = round(outmin + (((money - mmin) / (mmax - mmin)) * (outmax - outmin)))
    return f"PLAPOS{min(max(height,0),outmax)}"

def encode_light_pattern(money):
    outmin = constants.LED_MINHEIGHT
    outmax = constants.LED_MAXHEIGHT
    mmin = constants.MIN_MONEY
    mmax = constants.MAX_MONEY
    height = round(outmin + (((money - mmin) / (mmax - mmin)) * (outmax - outmin)))
    return f"LE1PAT{height}"

def encode_light_height(decIndex):
    return f"LE2PAT{decIndex}"

def encode_reel_stop(reel):
    return f"RL{reel}STP"

def encode_reel_setv(reel,velocity):
    return f"RL{reel}VEL{velocity}"

def encode_reel_requestangle(reel):
    return f"RL{reel}REQ"

def encode_fan_start():
    return "FANSTR"

def encode_fan_stop():
    return "FANSTP"

def encode_sys_recalibrate():
    return "SYSRECAL"

def encode_sys_stop():
    return "SYSSTP"


def decode_header(input):
    """ checks what the header of the message is. After that, goes to specific decoder for the rest"""
    head = input[:constants.HEADER_LENGTH]   
    tail = input[constants.TAIL_LENGTH:]
    match head:
        case "LE":
            _decode_lever(input, tail)            
        case "BT":
            _decode_button(input, tail)
        case "RL":
            _decode_reel(input, tail)
        case "SY":
            _decode_sys(input, tail)      
        

def _decode_lever(input, tail):
    """Specific decoder for the lever"""
    print(f"LEV {tail}")

def _decode_button(input, tail):
    """Specific decoder for the button"""
    headerdata = input[:constants.HEADER_LENGTH+1][2:]
    print(f"BT{headerdata} {tail}")

def _decode_reel(input, tail):
    """Specific decoder for the reel"""
    headerdata = input[:constants.HEADER_LENGTH+1][2:]
    print(f"RL{headerdata} {tail}")

def _decode_sys(input, tail):
    """Specific decoder for the system"""
    print(f"Sys {tail}")

