class ConversionError(Exception):
    def __init__(self,message="Conversion error occured"):
        self.message = message
        
        super().__init__(self.message)

conversionTable = {
    "Y":1e24,
    "Z":1e21,
    "E":1e18,
    "P":1e15,
    "T":1e12,
    "G":1e9,
    "M":1e6,
    "K":1e3,
    "m":1e-3,
    "μ":1e-6,
    "n"1e-9,
    "p":1e-12,
    "f",1e-15,
    "a":1e-18,
    "z":1e-21,
    "y":1e-24
}

def convertSI(toConvert):
    unit = ""
    sNumber = ""
    
    for c in toConvert:
        if c.isnumeric():
            sNumber += c
        else:
            unit += c
    
    if unit == "" or sNumber == "":
        raise ConversionError
    
    number = int(sNumber)
    
    
    
    print(sNumber)
    print(unit)
    
convertSI("100kg")