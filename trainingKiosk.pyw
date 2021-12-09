import time #used for sleeping
from win32 import win32api #used for getting user input
from selenium import webdriver #used for controlling browser
from selenium.webdriver.chrome.options import Options #used for adding kiosk mode to browser
from plyer import notification

TIMEOUT = 30
TIMEOUT_WARNING = 20

chrome_options = Options()
#chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--start-fullscreen") #start in fullscreen
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #removes the message "Chrome is being controlled by automated test software"

###############################################################################################################################################################
########################## EDIT THESE TWO LINES BELOW BASED ON YOUR USER DATA FOLDER LOCATION AND THE PROFILE YOU WANT TO LAUNCH CHROME WITH ##################
###############################################################################################################################################################
chrome_options.add_argument(r"--user-data-dir=C:\Users\Training\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
chrome_options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
###############################################################################################################################################################
###############################################################################################################################################################

driver = webdriver.Chrome(options=chrome_options) #start the webdriver with the given options
driver.get("https://go.bluevolt.com/loeblearningcenter/s/login")
inactiveTime = 0 #The amount of time the user has been inactive
active = False #False if we have not received in input in the last 30 minutes. True if we have!

while(True):
    lastInput = win32api.GetLastInputInfo(); #Changes only when a keyboard or mouse event occurs
    #print(lastInput)
    time.sleep(1)
    if(lastInput != win32api.GetLastInputInfo()): #If we detect keyboard or mouse input, then we say the user is active
        #print("now active!")
        active = True
    while(active):
        lastInput = win32api.GetLastInputInfo(); #Changes only when a keyboard or mouse event occurs
        time.sleep(1)
        inactiveTime += 1
        if (inactiveTime >= TIMEOUT): #should be 900 seconds for triggering a timeout on 15 minutes of inactivity
            #Close the webdriver
            driver.close()
            #Reinitialize the webdriver
            chrome_options = Options()
            #chrome_options.add_argument("--kiosk")
            chrome_options.add_argument("--start-fullscreen")
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            driver = webdriver.Chrome(options=chrome_options)
            ###########################
            driver.get("https://go.bluevolt.com/loeblearningcenter/s/login")
            inactiveTime = 0
            active = False
            break
        elif (inactiveTime == TIMEOUT_WARNING):
            notification.notify(title = "Session timeout", message = F"The computer has detected inactivity and will reset the browser in {TIMEOUT - TIMEOUT_WARNING} seconds unless the keyboard or mouse receives input." , timeout=7)
        
