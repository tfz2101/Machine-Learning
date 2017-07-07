import pandas as pd
import numpy as np
import datetime as dt

INPUT = "1.1.1.0:80:192.9.1.1:90"

def getColonBlock(input, character=":"):
    index = input.find(character)
    sub = input[0:index]
    remainder = input[index+1:len(input)]
    return sub, remainder


sub, remainder = getColonBlock(INPUT)



print(sub)
print(remainder)
