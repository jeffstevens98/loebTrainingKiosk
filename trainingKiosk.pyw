"""
Loeb Electric Training Kiosk script
@author Jeff Stevens
This script launches a chrome browser in kiosk mode and detects user activity. If a lack of user activity is detected,
then a session timeout occurs, where the chrome browser is restarted.
"""

import os #used for killing chrome tasks
import time #used for sleeping
#import requests #used to check for error landing page
from win32 import win32api #used for getting user input
from selenium import webdriver #used for controlling browser
from selenium.webdriver.chrome.options import Options #used for adding kiosk mode to browser
from selenium.webdriver.common.by import By
from plyer import notification


TIMEOUT = 15 #The amount of time in seconds of inactivity that a session timeout will occur 
TIMEOUT_WARNING = 10 #The amount of time in seconds of inactivity that the user will be sent a message warning them of a session timeout
DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n' #The message the webdriver logs when the user closes the browser window
HOME = "https://go.bluevolt.com/loeblearningcenter/s/login" #Where to redirect after session timeout(replace as necessary for your project)

chrome_options = Options()
chrome_options.add_argument("--kiosk") #Start in kiosk mode
#chrome_options.add_argument("--start-fullscreen") #start in fullscreen
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #removes the message "Chrome is being controlled by automated test software"

########################## EDIT THESE TWO LINES BELOW BASED ON YOUR USER DATA FOLDER LOCATION AND THE PROFILE YOU WANT TO LAUNCH CHROME WITH ##################
chrome_options.add_argument(r"--user-data-dir=C:\Users\Training\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
chrome_options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
###############################################################################################################################################################



os.system("taskkill /im chrome.exe /f") #Kill all chrome windows that aren't attached to the kiosk
driver = webdriver.Chrome(options=chrome_options) #start the webdriver with the given options
driver.get(HOME)#Go to the loeb training homepage
inactiveTime = 0 #The amount of time the user has been inactive
active = False #False if we have not received in input in the last 30 minutes. True if we have!

while(True):
    #Inactive state
    lastInput = win32api.GetLastInputInfo(); #Changes only when a keyboard or mouse event occurs
    time.sleep(1)
    ### If we detect keyboard or mouse input, then we say the user is active ###
    if(lastInput != win32api.GetLastInputInfo()):
        #Triggers an active state
        active = True
    while(active):
        #Active state
        lastInput = win32api.GetLastInputInfo(); #Changes only when a keyboard or mouse event occurs
        time.sleep(1)
        if(lastInput == win32api.GetLastInputInfo()): #If we don't detect any keyboard or mouse input, then we increase the inactive time, if we do, we reset it
            inactiveTime += 1
        else:
            inactiveTime = 0
        ### Restart browser when inactive time has reached the timeout time ###
        if (inactiveTime >= TIMEOUT):
            #Close the webdriver
            driver.close()
            #Reinitialize the webdriver
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://go.bluevolt.com/loeblearningcenter/s/login")
            inactiveTime = 0
            active = False
            break
        elif (inactiveTime == TIMEOUT_WARNING):
            notification.notify(title = "Session timeout", message = F"The computer has detected inactivity and will reset the browser in {TIMEOUT - TIMEOUT_WARNING} seconds unless the keyboard or mouse receives input." , timeout=7)
        
