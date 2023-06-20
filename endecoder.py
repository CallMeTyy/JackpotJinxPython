

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
    head = input[:3]
    tail = input[3:]

