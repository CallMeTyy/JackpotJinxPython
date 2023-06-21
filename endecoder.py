import constants
#from controller import Controller

def encode_platform_height(money):
    outmin = constants.PLATFORM_MINHEIGHT
    outmax = constants.PLATFORM_MAXHEIGHT
    mmin = constants.MIN_MONEY
    mmax = constants.MAX_MONEY
    height = round(outmin + (((money - mmin) / (mmax - mmin)) * (outmax - outmin)))
    return f"PLAPOS{min(max(height,0),outmax)}"

def encode_platform_stop():
    return "PLASTP"

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


def decode(input: str, controller):
    """ checks what the header of the message is. After that, goes to specific decoder for the rest"""
    input = input.upper()
    header = input[:constants.HEADER_LENGTH]   
    tail = input[constants.TAIL_LENGTH:]
    
    match header[:-1]:
        case "LE":
            p = __decode_lever(input, tail)   
            if p:
                controller.lever_pulled()         
        case "BT":
            b = __decode_button(input, tail)
            controller.stop_button_pressed(int(b))
        case "RL":
            rl = __decode_reel(input, tail)
            # if constants.DEBUG:
            #     print(f"{rl}  {rl[0]}")
            controller.reel_stopped(rl[0]-1, rl[1])
        case "SY":
            __decode_sys(input, tail, controller)
        

def __decode_lever(input: str, tail: str):
    """Specific decoder for the lever"""
    if constants.DEBUG:
        print(f"LEV {tail}")
    return tail == "P"

def __decode_button(input: str, tail: str):
    """Specific decoder for the button"""
    headerdata = input[:constants.HEADER_LENGTH][2:]
    if constants.DEBUG:
        print(f"BT{headerdata} {tail}")
    return headerdata

def __decode_reel(input: str, tail: str):
    """Specific decoder for the reel"""
    headerdata = int(input[:constants.HEADER_LENGTH][2:])
    angle = float(tail[constants.HEADER_LENGTH:])
    match headerdata:
        case 1:
            angle = round(angle/90)
        case 2:
            angle = round(angle/90)  
        case 3:
            angle = round(angle/(360/7))  
    if constants.DEBUG:
        print(f"RL{headerdata} {tail}")
    return (int(headerdata), int(angle))


def __decode_sys(input: str, tail: str, controller):
    """Specific decoder for the system"""
    if constants.DEBUG:
        print(f"Sys {tail}")
    match tail:
        case "READY":
            controller.calibration_finished()
        case "ERR":
            controller.external_error()


