from BinanceAPI import getCandles
from os import system
from time import sleep, time
import json

dataset = []
start = round(time() - (60 * 500)) * 1000
nbIter = 250

for i in range(0, nbIter):
    try:
        dataset = getCandles("BNBUSDT", "1m", start) + dataset
        start = round(((start/1000) - (60 * 500)) * 1000)
        system("clear")
        print("download... {}%".format(round((i/nbIter) * 100)))
        sleep(0.2)
    except:
        print("Connexion Lost")
        sleep(0.5)
        continue

f = open("dataset1M.json", "w")
f.write(json.dumps(dataset))
f.close()