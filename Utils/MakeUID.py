import string
import random

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase

def MakeUID(lenght=19):
    final_uid = ""
    for number in range(1,lenght+1):
        if number % 5 == 0:
            final_uid += "-"
        elif number % 2 == 0:
            final_uid += random.choice(lowercase)
        else:
            final_uid += random.choice(uppercase)
    
    return final_uid