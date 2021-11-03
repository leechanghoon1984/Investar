from pywinauto import application
import os, time

os.systme('taskkill /IM coStarter* /F /T')
os.systme('taskkill /IM CpStart* /F /T')
os.systme('taskkill /IM DibServer* /F /T')
os.system('wmic process where "name like \'%coStarter%'" call terminate')
os.system('wmic process where "name like \'%CpStart%'" call terminate')
os.system('wmic process where "name like \'%DibServer%'" call terminate')

time.sleep(5)
app = application.Application()
app.start('C:\CREON\STARTER\coStarter.exe /prj:cp '
    'id:CONAN /pwd:!ckdgns7 /autostart')
time.sleep(60)
