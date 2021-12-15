Hello! This is a guide to setting up this training kiosk software on your machine (with specific use in google chrome).

This is a python script and small batch file that work together to open google chrome in fullscreen (or kiosk mode, whichever suits your requirements)
and keeps track of user input. Whenever no input is received for a given period of time, the session times out, and the browser is restarted to its 
home URL. This little project is being used to manage machines that employees use to watch training videos.

Features:
-Launch chrome in kiosk mode
-Session timeout from no user activity
-Batch files and scheduled tasks which keep this script running
-If a new chrome window is opened that the script isn't controlling, the script exits the window and opens its own chrome window

------------   Contents   ------------
1. Installing python
2. Installing and configuring the dependencies
3. Configuring chromedriver
4. Configuring the script for your data directories
5. Finishing touches (other adjustments you can make)
--------------------------------------



------------ 1. Installing Python ------------

This script runs in python, so you will need to install python on your machine in order for it to work.
The repository comes with an installer for python 3.10, as of 12/8/21. Launch this python installer and follow
the instructions in the wizard to get python installed with recommended settings. Where prompted in the wizard, 
disable the path length limit.

Remember where you installed python! We will need that information in the next step.



------------ 2. Installing and configuring the dependencies ------------

Pip:
To install packages, we'll need pip. Pip is python's package installer and is a recursive acronym: Pip Installs Packages!
Pip should have come with your python installation, but in order to use it in the command line, we will need to add it 
to your path. To do this, go to the start menu and type "path" (no quotes). An option should come up that says 
"Edit system environment variables". Click on it and a window should pop up.

In this new window, click on environment variables in the bottom right hand corner and yet another window should come up.
In this new, new window, look to find an option in the system variable list on the bottom half of the window labeled
"path". Select it and then click edit. Click new to add another path to your set of path variables. A text input box should 
pop up where you should enter the following path:

...\yourPythonFolder\Scripts

Mine looked like this:
C:\Users\Training\AppData\Local\Programs\Python\Python310\Scripts

While we're here let's add python to our path:

...\yourPythonFolder

This is just so that the commandline knows what we're asking for when we ask to execute python code from it.

Then click ok to save it! You should have pip set up now. To get a pulse from pip, open a command line and enter pip -V to 
see if it's there. If it is, it should give you the version of pip. You may have to restart your computer at this point for
the environment variable changes to take effect.

Install dependencies:
This repository comes with a handy little file called "installDependencies.bat" which runs a suite of commands in the 
command prompt to get you all of the dependencies you need to run this kiosk script. Simply doubleclick on the 
file to run it, and then you'll get some messages in the command prompt that will tell you about the installation.
After you've verified all of the dependencies have been successfully installed, do the following to configure them:

Selenium: 
In the folder where you installed python, we need to navigate to where we just installed selenium. 
The path should look something like this:

...\yourPythonFolder\Lib\site-packages\selenium\webdriver\common

In this folder you need to replace the service.py file with the one included in the repository.
Either copy it in and replace it, or drag it into the folder to replace it. What this will do 
is it will slightly modify the source code of selenium to not show a detailed console window,
which may prove to be confusing to employees working on the training kiosk.

Plyer:
An adjustment you ought to make to get plyer's notifications to show up while windows is in full screen
is to navigate to the "focus assist" setting in your computer's start menu. Turn both of the options labeled
"when I'm playing a game" and "when I'm in fullscreen mode" off.




------------ 3. Configuring chromedriver ------------

To allow our script to control the chrome web browser, we need to place it in the same directory as our chrome installation. To find your chrome installation, 
look in your Program Files or Program Files(x86) folders. The path to your Chrome installation should look like the following:

C:\Program Files\Google\Chrome\Application

Copy and paste the chromedriver.exe file from the repository into this folder. Currently, this version of chromedriver.exe works with chrome 96. If chrome
is updated, you may need to get a newer version of chromedriver.



------------ 4. Configuring the script for your data directories ------------

Right click on the trainingKiosk.pyw and open it with your favorite text editor (or IDLE3 if you installed that with python in step 1). 

You should see early on in the file something that looks like this:

chrome_options.add_argument(r"--user-data-dir=C:\Users\You\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r'--profile-directory=Default') #e.g. Profile 3

Alter the code above to assign the "--user-data-dir" to the location of your User Data folder. For most people, all that would be is replacing the "You"
in the path with the name of your windows user account.

Additionally, you can alter the line below that to assign "--profile-directory" to the name of the Chrome user profile you want the script to launch.



------------ 5. Finishing touches ------------

At this point, you should be fully functional! Execute the trainingKiosk.bat file by double clicking it and you should have your kiosk that tracks user input
and issues session timeouts working. If you experience any issues, please leave an issue on the github repo webpage. 

Some other configurations you may want to make (we want these for the loeb electric training kiosks):

*If you want this script to run at start up on your windows PC, do the following:

1. Go to the start menu and search for "task scheduler". Find the task scheduler in the search results and click it to open it.
2. Click "create basic task"
3. In the new window that opened, name the task something useful like "StartKiosk" and click "Next"
4. Click "when I log on", and then click "Next"
5. Click "Start a program", and then click "Next"
6. Type "trainingKiosk.bat" (no quotes) into the program to execute field, and then copy and paste the path to the repo in the "start in" field. Click "Next".
7. Finally, click finish. You should have the kiosk start the next time you log onto your PC!

*If you want windows to check to see if this script is running, and if it isn't to start it up:

1. Go to the start menu and bring up the task scheduler again as described above.
2. Click "create task"
3. In the new window that opened, give your task a good name like "RelaunchKiosk" and click "Next"
4. Make the action of this new task to be to start a program, and type "cmd" (no quotes). Additionally, 
you should enter the directory of where the relauncKiosk.bat (the path to the repo) is contained in the "start in" box. Now, here's the important one:
Enter the following into the arguments:
/C start "" /MIN C:\...\loebTrainingKiosk\relaunchKiosk.bat
Where the ... is the path to the kiosk repo. This will start the relaunchKiosk.bat as minimized so it won't be annoying and pop up in front of you
every five minutes.
5. Set the task to recur daily, every 5 minutes. Make sure this triggers at a time in the near future so you can start seeing the trigger working.
6. Click okay to save the task.

*If you would like the see the tabs in chrome's kiosk mode, download the following chrome extension to the profile
that you'll be using this kiosk software with:
https://chrome.google.com/webstore/detail/fullscreen-tab-bar/hlackdnjlfblchoenkpcbbophehmeijb?hl=en-US