Hello! This is a guide to setting up this training kiosk software on your machine (with specific use in google chrome).

This is a python script and small batch file that work together to open google chrome in fullscreen (or kiosk mode, whichever suits your requirements)
and keeps track of user input. Whenever no input is received for a given period of time, the session times out, and the browser is restarted to its 
home URL. This little project is being used to manage machines that employees use to watch training videos.

------------   Contents   ------------
1. Installing python
2. Installing and configuring the selenium package
3. Configuring chromedriver
4. Configuring the script for your data directories
--------------------------------------



------------ 1. Installing Python ------------

This script runs in python, so you will need to install python on your machine in order for it to work.
The repository comes with an installer for python 3.10, as of 12/8/21. Launch this python installer and follow
the instructions in the wizard to get python installed.

Remember where you installed python! We will need that information in the next step.



------------ 2. Installing and configuring the selenium package ------------

This script uses a dependency called selenium to control a web browser. To install selenium, open
the command prompt (found by typing cmd in the windows start menu) and enter the following command

pip install selenium

This will use the pip package installer to set up selenium in your python libs folder. 

Now's the time to remember where you installed python. In the folder where you installed python, we
need to navigate to where we just installed selenium. The path should look something like this:

...\yourPythonFolder\Lib\site-packages\selenium\webdriver\common

In this folder you need to replace the service.py file with the one included in the repository.
Either copy it in and replace it, or drag it into the folder to replace it. What this will do 
is it will slightly modify the source code of selenium to not show a detailed console window,
which may prove to be confusing to employees working on the training kiosk.



------------ 3. Configuring chromedriver ------------

To allow our script to control the chrome web browser, we need to place it in the same directory as our chrome installation. To find your chrome installation, 
look in your Program Files or Program Files(x86) folders. The path to your Chrome installation should look like the following:

C:\Program Files\Google\Chrome\Application

Copy and paste the chromedriver.exe file from the repository into this folder.



------------ 4. Configuring the script for your data directories ------------

Right click on the trainingKiosk.pyw and open it with your favorite text editor (or IDLE3 if you installed that with python in step 1). 

You should see early on in the file something that looks like this:
###############################################################################################################################################################
########################## EDIT THESE TWO LINES BELOW BASED ON YOUR USER DATA FOLDER LOCATION AND THE PROFILE YOU WANT TO LAUNCH CHROME WITH ##################
###############################################################################################################################################################
chrome_options.add_argument(r"--user-data-dir=C:\Users\You\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r'--profile-directory=Default') #e.g. Profile 3
###############################################################################################################################################################
###############################################################################################################################################################

Alter the code above to assign the "--user-data-dir" to the location of your User Data folder. For most people, all that would be is replacing the "You"
in the path with the name of your windows user account.

Additionally, you can alter the line below that to assign "--profile-directory" to the name of the Chrome user profile you want the script to launch.



------------ 5. Ready to go! ------------

At this point, you should be ready to go! Execute the trainingKiosk.bat file by double clicking it and you should have your kiosk that tracks user input
and issues session timeouts working. If you experience any issues, please leave an issue on the github repo webpage. 

One last bit of advice is that if you want this script to run at start up on your windows PC, do the following:

1. Go to the start menu and search for "task scheduler". Find the task scheduler in the search results and click it to open it.
2. Click "create basic task"
3. In the new window that opened, name the task something useful like "StartKiosk" and click "Next"
4. Click "when I log on", and then click "Next"
5. Click "Start a program", and then click "Next"
6. Type "trainingKiosk.bat" (no quotes) into the program to execute field, and then copy and paste the path to the repo in the "start in" field. Click "Next".
7. Finally, click finish. You should have the kiosk start the next time you log onto your PC!