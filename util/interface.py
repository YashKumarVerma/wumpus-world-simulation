
def genericInput(message):
    ctx = "number"
    data = input(f"[{ctx:^8}]  : " + message)
    return data

def getInt(message):
    return int(genericInput(message))
    