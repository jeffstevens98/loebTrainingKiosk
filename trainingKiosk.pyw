"""
Loeb Electric Training Kiosk script
@author Jeff Stevens
This script launches a chrome browser in kiosk mode and detects user activity. If a lack of user activity is detected,
then a session timeout occurs, where the chrome browser is restarted.
"""

import os #used for killing chrome tasks
#import psutil #used for checking to see if chrome is running
import time #used for sleeping
#import requests #used to check for error landing page
from win32 import win32api #used for getting user input
from selenium import webdriver #used for controlling browser
from selenium.webdriver.chrome.options import Options #used for adding kiosk mode to browser
from selenium.webdriver.common.by import By
from plyer import notification

TIMEOUT = 60 #The amount of time in seconds of inactivity that a session timeout will occur 
TIMEOUT_WARNING = 45 #The amount of time in seconds of inactivity that the user will be sent a message warning them of a session timeout
HOME = "https://go.bluevolt.com/loeblearningcenter/s/login" #Where to redirect after session timeout(replace as necessary for your project)




'''
CURRENTLY COMMENTED OUT: Requires Visual C++14 build tools and I'm not sure I want to bloat the
installation of this training kiosk tool anymore

Checks to see if a process is running by its executable name. We use 'chrome.exe' by default.
Taken from: https://stackoverflow.com/questions/63105717/how-do-i-run-a-test-to-check-if-google-chrome-is-running-python
def process_is_running_by_exename(exename):
    for proc in psutil.process_iter(['pid', 'name']):
        # This will check if there exists any process running with executable name
        if proc.info['name'] == exename:
            return True
    return False
'''


'''
Given what page the webdriver is currently on, search it for the error message
that has been bugging our training computers. If we find an error, return true.
If we don't find an error, return false.

@driver The webdriver object from selenium

@return a boolean value; true if error, false if no error
'''
def reachedErrorPage(driver):
    if (driver.title != "Loeb Learning Center"):
        return True
    else:
        return False


'''
Uses the selenium webdriver to get the homepage of the kiosk.
If we reach an error page, we refresh the page until we don't get an error

@driver The webdriver object from selenium
'''
def getHOME_ReloadOnError(driver):
    attempts = 0
    while(True):
        driver.get(HOME)
        if(reachedErrorPage(driver)):
            attempts += 1
            if (attempts > 10):
                print("There's an error and we can't get the kiosk homepage!")
                break
            continue
        else:
            break


'''
Detects if the browser has been closed

@returns true if the browser has been closed and false otherwise
'''
def browserClosed(driver):
    log = driver.get_log("driver")
    if(len(log) > 0):
        if(log[0]["message"].find('disconnected')):
            return True
        else:
            return False
    


'''
This is where everything happens!
'''
def main():
    bannerTextFile = open("banner.txt",'r')
    print(bannerTextFile.read())

    chrome_options = Options()
    chrome_options.add_argument("--kiosk") #Start in kiosk mode
    #chrome_options.add_argument("--start-fullscreen") #start in fullscreen
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #removes the message "Chrome is being controlled by automated test software"

    ########################## EDIT THESE TWO LINES BELOW BASED ON YOUR USER DATA FOLDER LOCATION AND THE PROFILE YOU WANT TO LAUNCH CHROME WITH ##################
    chrome_options.add_argument(r"--user-data-dir=C:\Users\Training\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    chrome_options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
    ###############################################################################################################################################################

    #Kill all chrome windows that aren't attached to the kiosk on startup of this script
    os.system("taskkill /im chrome.exe /f")
    
    driver = webdriver.Chrome(options=chrome_options) #start the webdriver with the given options
    getHOME_ReloadOnError(driver)#Go to the loeb training homepage
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
            #If we don't detect any keyboard or mouse input, then we increase the inactive time, if we do, we reset it
            if(lastInput == win32api.GetLastInputInfo()):
                inactiveTime += 1
            else:
                inactiveTime = 0
            #If we close the browser while a user is active, reopen it
            if(browserClosed(driver)):
                print("A user closed the browser: Initiating automatic restart")
                driver.quit()
                driver = webdriver.Chrome(options=chrome_options)
                getHOME_ReloadOnError(driver)
                print("Restart successful")
            ### Restart browser when inactive time has reached the timeout time ###
            if (inactiveTime >= TIMEOUT):
                #Close the webdriver
                driver.quit()
                #Reinitialize the webdriver
                driver = webdriver.Chrome(options=chrome_options)
                getHOME_ReloadOnError(driver)
                inactiveTime = 0
                active = False
                break
            elif (inactiveTime == TIMEOUT_WARNING):
                notification.notify(title = "Session timeout", message = F"The computer has detected inactivity and will reset the browser in {TIMEOUT - TIMEOUT_WARNING} seconds unless the keyboard or mouse receives input." , timeout=7)
            

main()
