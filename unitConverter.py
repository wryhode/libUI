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
    "":1,
    "m":1e-3,
    "μ":1e-6,
    "n":1e-9,
    "p":1e-12,
    "f":1e-15,
    "a":1e-18,
    "z":1e-21,
    "y":1e-24
}

unitTable = {
    "g":"K",
    "m":1,
    "s":1
}

def getConversion(unit):
    if isinstance(unit,int):
        return 1
    else:
        return conversionTable[unit]

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

    if len(unit) > 1:
        unitSize = unit[0]
        unitType = unit[1]
    else:
        unitSize = ""
        unitType = unit[0]

    result = (number * conversionTable[unitSize]) / getConversion(unitTable[unitType])
    
    unitTableResult = unitTable[unitType]
    if isinstance(unitTable[unitType],int):
        unitTableResult = ""

    print(str(result) + str(unitTableResult) + unitType)
    
convertSI("1000ms")