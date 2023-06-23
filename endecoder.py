import constants

def encode_platform_height(money: float):
    """Creates the message for sending the platform height based on the amount of lost money"""
    outmin = constants.PLATFORM_MINHEIGHT
    outmax = constants.PLATFORM_MAXHEIGHT
    mmin = constants.MIN_MONEY
    mmax = constants.MAX_MONEY
    height = round(outmin + (((money - mmin) / (mmax - mmin)) * (outmax - outmin)))
    return f"PLAPOS{min(max(height,0),outmax)}"

def encode_platform_stop():
    """Creates the message for sending the platform stop command."""
    return "PLASTP"

def encode_light_pattern(decIndex: int):
    """Creates the message for sending the led decoration."""
    return f"LE2PAT{decIndex}"


def encode_light_height(money):
    """Creates the message for sending the led height to display the money lost."""
    outmin = constants.LED_MINHEIGHT
    outmax = constants.LED_MAXHEIGHT
    mmin = constants.MIN_MONEY
    mmax = constants.MAX_MONEY
    height = round(outmin + (((money - mmin) / (mmax - mmin)) * (outmax - outmin)))
    return f"LE1PAT{height}"

def encode_button_light_on(reel: int):
    """Creates the message for sending the command to send to the specified button to turn on their lights"""
    return f"BT{reel}ONN"

def encode_button_light_off(reel: int):
    """Creates the message for sending the command to send to the specified button to turn off their lights"""
    return f"BT{reel}OFF"

def encode_reel_stop(reel: int, val: int):
    """Creates the message for sending the command to stop the wheels on a specific angle based on the index value"""
    part = 1
    # Countries, games and years don't have the same amount of elements, so the angles encoded must be different. 
    match reel:
        case 1:
            part = (360/constants.COUNTRY_AMOUNT) 
        case 2:
            part = (360/constants.GAME_AMOUNT)
        case 3:
            part = (360/constants.YEAR_AMOUNT)
    angle = round(val * part + part * constants.IMAGE_POSITION_FRACTION)
    return f"RL{reel}STP{angle}"

def encode_reel_setv(reel: int,velocity: int):
    """Creates the message for sending the command to set the velocity of the specified reel"""
    return f"RL{reel}VEL{velocity}"

def encode_reel_requestangle(reel):
    """Creates the message for sending the command to request the angle of the specified reel"""
    return f"RL{reel}REQ"

def encode_fan_start():
    """Creates the message for sending the command to start the fans"""
    return "FANSTR"

def encode_fan_stop():
    """Creates the message for sending the command to stop the fans"""
    return "FANSTP"

def encode_sys_recalibrate():
    """Creates the message for sending the command to recalibrate the system"""
    return "SYSRECAL"

def encode_sys_stop():
    """Creates the message for sending the command to stop the system"""
    return "SYSSTP"

def encode_nodata():
    return "ND"




def decode(input: str, controller):
    """ checks what the header of the message is. After that, goes to specific decoder for the rest"""
    input = input.upper()
    header = input[:constants.HEADER_LENGTH] # Retrieves the header from the sent message 
    tail = input[constants.TAIL_LENGTH:] # Retrieves the tail
    
    match header[:-1]: # As the header can contain variable data, remove the last character and only check for the first two chars
        case "LE":
            p = __decode_lever(input, tail) # __decode_lever returns a boolean if the tail is P  
            if p: # only if the lever is pulled 
                controller.lever_pulled()         
        case "BT":
            b = __decode_button(input, tail) # __decode_button returns an int corresponding to a reel  
            controller.stop_button_pressed(int(b))
        case "RL":
            rl = __decode_reel(input, tail) # __decode_reel returns a tuple with [0] corresponding to a reel and [1] the value 
            controller.reel_stopped(rl[0]-1, rl[1])
        case "SY":
            __decode_sys(input, tail, controller)
        case "PL":
            __decode_platform(input, tail, controller)
        case "OK":
            controller.send_next_message()
        case "RS":
            # Resend last message
            controller.resend_message()
        case "RJ":
            controller.reset_installation()
        

def __decode_lever(input: str, tail: str):
    """Specific decoder for the lever"""
    if constants.COMM_DEBUG:
        print(f"LEV {tail}")
    return tail == "P"

def __decode_button(input: str, tail: str):
    """Specific decoder for the button"""
    headerdata = input[:constants.HEADER_LENGTH][2:]
    if constants.COMM_DEBUG:
        print(f"BT{headerdata} {tail}")
    return headerdata

def __decode_reel(input: str, tail: str):
    """Specific decoder for the reel"""
    headerdata = int(input[:constants.HEADER_LENGTH][2:])
    angle = float(tail[constants.HEADER_LENGTH:]) % 360
    part = 1
    match headerdata:
        case 1:
            part = (360 / constants.COUNTRY_AMOUNT)

        case 2:
            part = (360 / constants.GAME_AMOUNT)

        case 3:
            part = (360 / constants.YEAR_AMOUNT)
    angle = int(angle/part)
    if constants.COMM_DEBUG:
        print(f"RL{headerdata} {tail}")
    return (int(headerdata), int(angle))


def __decode_sys(input: str, tail: str, controller):
    """Specific decoder for the system"""
    if constants.COMM_DEBUG:
        print(f"Sys {tail}")
    match tail:
        case "READY":
            controller.calibration_finished()
        case "ERR":
            controller.external_error()


def __decode_platform(input: str, tail: str, controller):
    """specific decoder for platform"""
    if constants.COMM_DEBUG:
        print(f"Pla {tail}")
    match tail:
        case "DON":
            controller.platform_done()


