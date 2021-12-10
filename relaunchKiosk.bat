@ECHO OFF
TASKLIST | FINDSTR python.exe || start cmd /k CALL "C:\Users\Training\Documents\GitHub\loebTrainingKiosk\trainingKiosk.bat"
EXIT