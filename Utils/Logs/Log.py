import os
from ..GetTime import GetTime

def Log(message):
    if os.path.exists("Logs.txt"):
        with open("Logs.txt","a") as file:
            file.write(f"\n{GetTime()} - {message}")