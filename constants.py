# ===== Debug Settings =====
COMM_DEBUG = False
AUDIO_DEBUG = False

SIMULATED_SERIAL = False

# ===== Arduino Settings =====
ARDUINO_PORT_MAC = '/dev/cu.usbmodem142101'
ARDUINO_PORT_WINDOWS = 'COM5'
ARDUINO_PORT_WINDOWS2 = 'COM6'
ARDUINO_PORT_RASPI = '/dev/ttyACM0'
BAUD_RATE = 115200
LOCAL_SEND_DELAY = .01     # in seconds

# ===== Incoming Messages Settings =====
HEADER_LENGTH = 3
TAIL_LENGTH = 3
INSTR_LENGTH = 3
MAX_DATA_SIZE = 1023

# ===== Electronic Mapping Settings Settings =====
PLATFORM_MINHEIGHT = 0
PLATFORM_MAXHEIGHT = 200

LED_MINHEIGHT = 0
LED_MAXHEIGHT = 100

MIN_MONEY = 0
MAX_MONEY = 1500

REEL_SPEED = 1

LED_IDLE_PATTERN = 0
LED_SPIN_PATTERN = 1

LED_WIN_PATTERN = 2

IMAGE_POSITION_FRACTION = 0.5   # this is where the image is in the angular range of the value on the reel

# ===== Database Settings =====
COUNTRY_AMOUNT = 4
GAME_AMOUNT = 4
YEAR_AMOUNT = 7

# ===== Audio Constants =====
AUDIO_MUSIC = 0
AUDIO_RLOOP1 = 1
AUDIO_RLOOP2 = 2
AUDIO_RLOOP3 = 3
AUDIO_RSTP1 = 4
AUDIO_RSTP2 = 5
AUDIO_RSTP3 = 6
AUDIO_SHRED = 7
AUDIO_VICTORY = 8
