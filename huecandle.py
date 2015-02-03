import json
import requests
import time
import random
import os
import platform
import pickle

# Change this to the ID of the light you would like to control.
# For now only one light can be controlled. 
selectedLights = 0

# prints responses from Hue bridge if set to True
verbose = True

# config.txt is expected to have the URL of your Hue bridge including your application key:
# example: http://YOURHUEBRIDGEIP/api/YOURAPPLICATIONKEY
# This will be expanded in the future to allow for more variables and settings.
def getUrl():
   f = open('config.txt', 'r')
   url = f.read().rstrip()
   return "{}/lights/{}/state".format(url,selectedLights[0])

def hueCandle(randomizeBrightness):
   url = getUrl()
   colorList = (12750,0)
   on = False

   while True:
      try:
         bright = 255
         if (randomizeBrightness):
            bright = random.randint(1, 255)
         colorListIndex = random.randint(0, len(colorList) - 1)
         hue = colorList[colorListIndex]
         sleep = random.randint(1, 5) * 0.1
         if (not on):
            data = json.dumps({"on":True, "bri":bright, "sat":255, "hue":hue})
            on = True
         else:
            data = json.dumps({"bri":bright, "hue":hue})
         f = requests.put(url, data=data)
         if (verbose):
            print(f.content)
         time.sleep(sleep)
      except KeyboardInterrupt:
         break;

   data = json.dumps({"on":False})
   f = requests.put(url, data=data)
   if (verbose):
      print(f.content)

# Cycle light(s) with random colors every n seconds where n is a random number between 1 and 5
# If randomizeBrightness parameter is True, also randomize the brightness of the light(s) from 1 to 255
def randomColors(randomizeBrightness):
   url = getUrl()
   on = False

   while True:
      try:
         bright = 255
         if (randomizeBrightness):
            bright = random.randint(1, 255)
         hue = random.randint(0, 65280)
         sleep = random.randint(1, 5)
         if (not on):
            data = json.dumps({"on":True, "bri":bright, "sat":255, "hue":hue})
            on = True
         else:
            data = json.dumps({"bri":bright, "hue":hue})
         f = requests.put(url, data=data)
         if (verbose):
            print(f.content)
         time.sleep(sleep)
      except KeyboardInterrupt:
         break

   data = json.dumps({"on":False})
   f = requests.put(url, data=data)
   if (verbose):
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
   print("=Hue Candle                                   ")
   print("=                                             ")
   print("=Select an action:                            ")
   print("=1) Candle Simulation                         ")
   print("=2) Candle Simluation (random brightness)     ")
   print("=3) Random Colors                             ")
   print("=4) Random Colors (random brightness)         ")
   print("=5) Toggle Verbose mode (current: {})         ").format(verbose)
   print("=9) Exit                                      ")
   print("==============================================")

# Checks for the existence of a preferences file
# If no file exists, initializePreferences is called to create a base preferences file
# Finally, preferences file is loaded into global variables
def checkPreferences():
   if os.path.isfile(".hueCandlePrefs"):
      print("Preferences file found!")
   else:
      print("No preference file found! Initializing...")
      initializePreferences()
   loadPreferences()

def loadPreferences():
   global selectedLights
   with open(".hueCandlePrefs", "rb") as fileHandle:
      preferencesDictionary = pickle.load(fileHandle)
      selectedLights = preferencesDictionary["selectedBulbs"]

# Creates and saves a preferences dictionary to the file .hueCandlePrefs
# For now, only a list of selected bulbs is stored.  The list is initialized as a list with one element (bulb #1)      
def initializePreferences():
   preferencesDictionary = {"selectedBulbs" : [1]}
   pickle.dump(preferencesDictionary, open(".hueCandlePrefs", "wb")) 

def main():
   checkPreferences()

   userInput = 0
   global verbose

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
      elif (userInput == 5):
         verbose = not verbose
         userInput = 0
      else: 
         if (userInput == 9):
            break
         else: 
            userInput = 0

main()
