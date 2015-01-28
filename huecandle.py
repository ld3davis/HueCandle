import json
import requests
import time
import random
import os
import platform

# Change this to the ID of the light you would like to control.
# For now only one light can be controlled. 
selectedLight = 3

# config.txt is expected to have the URL of your Hue base including your application key:
# example: http://YOURHUEBASEIP/api/YOURAPPLICATIONKEY
# This will be expanded in the future to allow for more variables and settings.
def getUrl():
   f = open('config.txt', 'r')
   url = f.read().rstrip()
   return "{}/lights/{}/state".format(url,selectedLight)

def hueCandle(randomizeBrightness):
   url = getUrl()

   colorList = (12750,0)
   while True:
      try:
         bright = 255
         if (randomizeBrightness):
            bright = random.randint(1, 255)
         colorListIndex = random.randint(0, len(colorList) - 1)
         hue = colorList[colorListIndex]
         sleep = random.randint(1, 5) * 0.1
         data = json.dumps({"on":True, "bri":bright, "sat":255, "hue":hue})
         f = requests.put(url, data=data)
         print(f.content)
         time.sleep(sleep)
      except KeyboardInterrupt:
         break;

   data = json.dumps({"on":False})
   f = requests.put(url, data=data)
   print(f.content)

# Cycle light(s) with random colors every n seconds where n is a random number between 1 and 5
# If randomizeBrightness parameter is True, also randomize the brightness of the light(s) from 1 to 255
def randomColors(randomizeBrightness):
   url = getUrl()

   while True:
      try:
         bright = 255
         if (randomizeBrightness):
            bright = random.randint(1, 255)
         hue = random.randint(0, 65280)
         sleep = random.randint(1, 5)
         data = json.dumps({"on":True, "bri":bright, "sat":255, "hue":hue})
         f = requests.put(url, data=data)
         print(f.content)
         time.sleep(sleep)
      except KeyboardInterrupt:
         break

   data = json.dumps({"on":False})
   f = requests.put(url, data=data)
   print(f.content)

# Clears the terminal
def clearTerminal():
   if 'win' in platform.platform().lower():
      os.system("cls")
   else:
      os.system("clear")

# Prints the main menu
def printMenu():
   print("==============================================")
   print("=Hue Candle                                  =")
   print("=                                            =")
   print("=Select an action:                           =")
   print("=1) Candle Simulation                        =")
   print("=2) Candle Simluation (random brightness)    =")
   print("=3) Random Colors                            =")
   print("=4) Random Colors (random brightness)        =")
   print("=9) Exit                                     =")
   print("==============================================")

def main():
   userInput = 0

   while (userInput == 0):
      clearTerminal()
      printMenu()
      try:
         userInput = int(input("Selection: "))
      except NameError:
         print("\nBad Input!")
         userInput = 0
      except KeyboardInterrupt:
         print("\nCTRL+C detected!")
         userInput = 0
      if (userInput == 1):
         hueCandle(False)
         userInput = 0
      elif (userInput == 2):
         hueCandle(True)
         userInput = 0
      elif (userInput == 3):
         randomColors(False)
         userInput = 0
      elif (userInput == 4):
         randomColors(True)
         userInput = 0
      else: 
         if (userInput == 9):
            break
         else: 
            userInput = 0

main()
