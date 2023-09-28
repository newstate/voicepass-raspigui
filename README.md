# voicepass-raspigui

This is code for creating voice-controlled password programs that can unlock physical devices or activate mechanisms using a raspberry pi microcontroller. The user needs to answer three questions before being asked to confirm that they would like to unlock or activate a mechanism. At that point the IO pin of the raspberry pi is switched whereby an attached device (using a relay) can be activated. It contains also a reset button that the user can press to reset the IO pin. A simple GUI is created with PyQt which can be controlled via touchscreen (scaled for this purpose) and virtual keyboard or via mouse and physical keyboard. The GUI displays the questions and feedback from the program when the user correctly or incorrectly answers the questions. The program can either run offline using the vosk library and Kaldi recognizer models or using google cloud services. The generated voice, either offline or online, is generated using google cloud text to speech.

The install.sh installs everything that is needed to run the program using a raspberry pi touchscreen or optionally a monitor and keyboard + mouse.

Note: The environment variable DISPLAY should be set to :0.0 to access a monitor (included in the .env file) And the display of the raspberry pi touchscreen might have to be rotated when fitting in a case.

The main_vosk.py runs the program offline. This is also what's been configured for the desktop shortcut.

create_audio.py is used to generate the spoken questions and feedback from the program. You can write your own questions here and generate them after setting up google cloud.

The config.ini file is used to set the passwords, codes or phrases that unlock the next page (PyQt widget) or set output pins to up/down, allowing for control of electrical physical locks or motors.

Read more about setting up google speech here [here](https://github.com/newstate/gcloud_stt/blob/master/Gcloud_setup.MD): 

The main_gcloud.py needs (stable and fast) internet connection and runs the lock program using speech recognition from google. 

Note: At the moment, the offline version has the most natural flow to it. The online version has some lag in sending audio to and from google's servers which slows down the program and makes it feel less natural.

Virtual or physical keyboard input works in both scripts.

After setting up Google Cloud yous should donwload your own .json file containing a private key to be able to use the google speech to text API. It's free up to 60 min per month. https://cloud.google.com/speech-to-text/pricing
