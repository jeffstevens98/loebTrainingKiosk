import time #used for sleeping
from win32 import win32api #used for getting user input
from selenium import webdriver #used for controlling browser
from selenium.webdriver.chrome.options import Options #used for adding kiosk mode to browser


chrome_options = Options()
#chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--start-fullscreen") #start in fullscreen
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) #removes the message "Chrome is being controlled by automated test software"
chrome_options.add_argument(r"--user-data-dir=C:\Users\jsteve\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\jsteve\AppData\Local\Google\Chrome\User Data
chrome_options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
driver = webdriver.Chrome(options=chrome_options) #start the webdriver with the given options
driver.get("http://intranet")
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
        if (inactiveTime >= 900): #should be 900 seconds for triggering a timeout on 15 minutes of inactivity
            #Close the webdriver
            driver.close()
            #Reinitialize the webdriver
            chrome_options = Options()
            #chrome_options.add_argument("--kiosk")
            chrome_options.add_argument("--start-fullscreen")
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            driver = webdriver.Chrome(options=chrome_options)
            ###########################
            driver.get("http://intranet")
            inactiveTime = 0
            active = False
            break
        
        
