# MyEpoc (Changed to WETMOS)
Django app for monitoring chronic obstructive pulmonary disease (COPD or EPOC in spanish) patients by receiving HTTP POST requests from an ESP32 that reads SpO2 levels and in return sends commands to control the flow of oxygen that the patient should receive (the ESP32 reads the commands through GET requests). 

## How to run
1. Set up a virtual environment and run *pip install -r requirements.txt* to install everything needed
2. Add a SECRET_SETTINGS.py file that contains the secret key of settings.py in MyEpoc folder
3. Create your own superuser using *python manage.py createsuperuser*

## What does it contain?
In order to access the web page, you'll need to log in using your superuser or another existing User
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/login.png" alt="Login Page" width="600" height="300"/>
</p>

After that, the homepage contains a basic description of how everything works. In addition, if logged in as a patient, there will also be a chat bubble available to communicate with medics.
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/chat_patient.png" alt="Patient view of chat" width="600" height="300"/>
</p>
The monitoring tab will allow the user to follow their treatment and check on their SpO2 levels.
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/monitor_patient.png" alt="Patient view of monitoring" width="600" height="300"/>
</p>
From the medic's point of view, there's also the option to change the oxygen flow.
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/monitor_medic.png" alt="Medic view of monitoring" width="600" height="300"/>
</p>
For the medics, there's also a tab to monitor every registered patient.
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/monitor_table.png" alt="Table of patients" width="600" height="300"/>
</p>
Another tab available for only medics is the settings page, this contains the option to edit and add new users (patients or medics) and attend chats requested by patients.
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/settings.png" alt="Settings" width="600" height="300"/>
</p>
Joining a chat room will show the following view.
<p align="center">
    <img src="https://github.com/Mauricio1812/MyEpoc/blob/master/docs/images/chat_medic.png" alt="Medic view of chat" width="600" height="300"/>
</p>
