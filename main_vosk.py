# -*- coding: utf-8 -*-

# this imports the necessary libraries
import RPi.GPIO as GPIO
from configparser import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal

# this imports the libraries for speech recognition
import datetime
import time
import threading
from uuid import uuid4
# import pyttsx3 as tts
import speech_recognition
import os

import psutil
import json
import vosk
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue

# the following lines load the config file
config_object = ConfigParser()
config_object.read("/home/pi/voicepass-raspigui/config.ini")

# this matches the pin numbers to their functions
button = 20
lock = 21

# the following lines set up the GPIO pins
GPIO.setwarnings(False) # Ignore warning for now
GPIO.cleanup() # clean up at the end of your script
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(button , GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 20 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(lock, GPIO.OUT) # Set pin 21 to be an output pin and set initial value to be low (off)
GPIO.output(lock, True) # set output to high (on)

class Ui_MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(800, 320)
        # self.showFullScreen()
        self.timer = QtCore.QTimer()
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("background-color: rgb(35, 36, 37);")
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(-1, -1, 800, 480))
        self.stackedWidget.setStyleSheet("color: rgb(255, 255, 255)")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.label = QtWidgets.QLabel(self.page_1)
        self.label.setGeometry(QtCore.QRect(20, 30, 800, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.page_1)
        self.lineEdit.setGeometry(QtCore.QRect(22, 130, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        # self.lineEdit.setMaxLength(0) # Set the maximum length to 0 (unlimited)
        # self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        # self.lineEdit.setText("Please say 'Hello' to start.")
        self.pushButton = QtWidgets.QPushButton(self.page_1)
        self.pushButton.setGeometry(QtCore.QRect(20, 230, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 230, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(20, 29, 800, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeft)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(22, 130, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label_3 = QtWidgets.QLabel(self.page_3)
        self.label_3.setGeometry(QtCore.QRect(20, 29, 800, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("setStyleSheet color: rgb(255, 0, 0)")
        self.label_3.setAlignment(QtCore.Qt.AlignLeft)
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(22, 130, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.page_3)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 230, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.label_4 = QtWidgets.QLabel(self.page_4)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 800, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeft)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.page_4)
        self.label_5.setGeometry(QtCore.QRect(20, 120, 800, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(self.page_4)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 230, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_6 = QtWidgets.QLabel(self.page_4)
        self.label_6.setGeometry(QtCore.QRect(10, 170, 451, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.pushButton_5 = QtWidgets.QPushButton(self.page_5)
        self.pushButton_5.setGeometry(QtCore.QRect(338, 30, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.label_7 = QtWidgets.QLabel(self.page_6)
        self.label_7.setGeometry(QtCore.QRect(20, 110, 441, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.page_6)
        self.label_8.setGeometry(QtCore.QRect(50, 50, 51, 51))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("/home/pi/Documents/STT/voicepass-raspigui/wrong.png"))
        self.label_8.setObjectName("label_8")
        self.pushButton_6 = QtWidgets.QPushButton(self.page_6)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 220, 271, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.stackedWidget.addWidget(self.page_6)
        self.setCentralWidget(self.centralwidget)
        
        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(self.pageCode)
        self.pushButton.setAutoDefault(True)
        self.pushButton_2.clicked.connect(self.pageWho)
        self.pushButton_3.clicked.connect(self.pageWhere)
        self.pushButton_4.clicked.connect(self.pageYes)
        self.pushButton_5.clicked.connect(self.pageReset)
        self.pushButton_6.clicked.connect(self.backToPage)
        QtCore.QMetaObject.connectSlotsByName(self)
        GPIO.add_event_detect(button, GPIO.BOTH ,callback=self.on_gpio_event)
        
        self.lineEdit.returnPressed.connect(self.pushButton.click)
        self.lineEdit_2.returnPressed.connect(self.pushButton_2.click)
        self.lineEdit_3.returnPressed.connect(self.pushButton_3.click)

        self.current_state = 'hello'
        self.should_continue = True
        self.listen_thread = threading.Thread(target=self.listen_for_prompts)
        self.listen_thread.start()

        self.credentials = os.getenv("TEST_CREDENTIALS")
        # the following lines configure the speech recognition model to recognize certain words which we expect based on the set passphrases, names and locations
        self.preferred_words = ["something", "someone", "somewhere"]
        # Convert the preferred_words list to the JSON format Vosk expects
        self.preferred_phrases_json = json.dumps(self.preferred_words)

        # Initialize Vosk
        vosk.SetLogLevel(-1)  # This will reduce verbosity
        self.model_path = "/home/pi/.cache/vosk/vosk-model-small-en-us-0.15"  # Replace with the path to your Vosk model
        try:
            self.model = vosk.Model(self.model_path)
        except Exception as e:
            print(f"Error initializing Vosk model: {e}")
            exit(1)

        self.q = queue.Queue()
        self.recognizer = None
        self.audio_stream = None

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen_for_prompts(self):

        print("Speaking: Please say 'Hello' to start. Or type your passphrase.")
        os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/start.mp3")

        while self.should_continue:
            # Check if VLC is running so that we don't accidentally record the audio coming from the speaker
            vlc_running = "vlc" in (p.name() for p in psutil.process_iter())
            if not vlc_running:

                q = queue.Queue()

                def callback(indata, frames, time, status):
                    q.put(bytes(indata))

                device_info = sd.query_devices(None, "input")
                sample_rate = int(device_info["default_samplerate"])
                model = Model(self.model_path)

                start_time = time.time()  # Record the start time
                # print("The start time is: ", start_time)

                with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, device=None, dtype="int16", channels=1, callback=callback):
                    rec = KaldiRecognizer(model, sample_rate)

                    output = ""

                    os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/beep.wav")

                    while True:  # Start an infinite loop
                        data = q.get()
                        elapsed_time = time.time() - start_time  # Update elapsed_time at the beginning of the loop
                        if rec.AcceptWaveform(data):
                            output = eval(rec.Result())['text']
                            print("I heard: ")
                            print(output + "\n")
                        else:
                            # print(rec.PartialResult())
                            if self.current_state == 'hello':
                                self.label.setText(eval(rec.PartialResult())['partial'])
                            elif self.current_state == 'passphrase':
                                self.label.setText(eval(rec.PartialResult())['partial'])
                            elif self.current_state == 'name':
                                self.label_2.setText(eval(rec.PartialResult())['partial'])
                            elif self.current_state == 'location':
                                self.label_3.setText(eval(rec.PartialResult())['partial'])
                            elapsed_time = time.time() - start_time  # Update elapsed_time if no new data was transcribed
                        if elapsed_time > 6.0:  # Then break the loop if elapsed_time is more than 4 seconds.
                            print("Time to stop recording and start recognizing.")
                            break

                    # except Exception as e:
                    #     print("Error occurred: ", type(e).__name__, " - ", str(e))
                        
                    try:
                        if any(x in output.lower() for x in ["quit", "stop", "exit"]):
                            sys.exit(0)
                        
                        if self.current_state == 'hello':
                            if "hello" in output.lower():
                                text = "Please say the pass phrase."
                                self.label.setText(text)
                                print("Speaking:" + text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/passphrase.mp3")
                                self.current_state = 'passphrase'
                            else:
                                """If hello is not in the output, just do nothing. Keep waiting for the signal to start.
                                Let's assume that someone will start typing if they're uncapable of saying hello.
                                In the case that nothing is in the transcription we have to assume that they will be typing."""

                        elif self.current_state == 'passphrase':
                            if config_object["USERINFO"]['password'].lower() in output.lower():
                                text = "Please say your name."
                                print("Pass phrase correct.")
                                self.label_2.setText(text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/name.mp3")
                                self.current_state = 'name'
                                self.lineEdit.setText(config_object["USERINFO"]['password'].lower())
                                self.pushButton.clicked.emit()
                            else:
                                text = f"I heard {output}. Please say the pass phrase."
                                self.label.setText(text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/passphrase.mp3")
                        
                        elif self.current_state == 'name':
                            if config_object["USERINFO"]['username'].lower() in output.lower():
                                text = "Please say your location."
                                print("Name correct.")
                                self.label_3.setText(text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/location.mp3")
                                self.current_state = 'location'
                                self.lineEdit_2.setText(config_object["USERINFO"]['username'].lower())
                                self.pushButton_2.clicked.emit()
                            else:
                                text = f"I heard {output}. Please say your name."
                                self.label_2.setText(text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/name_else.mp3")
                        
                        elif self.current_state == 'location':
                            if config_object["USERINFO"]['where'].lower() in output.lower():
                                text = "If you wish to die say 'yes' and press the button."
                                print("Location correct.")
                                self.label_4.setText(text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/confirm.mp3")
                                self.current_state = 'confirmation'
                                self.lineEdit_3.setText(config_object["USERINFO"]['where'].lower())
                                self.pushButton_3.clicked.emit()
                            else:
                                text = f"I heard {output}. Please say your location."
                                self.label_3.setText(text)
                                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/location_else.mp3")

                        elif self.current_state == 'confirmation':
                            if any(x in output.lower() for x in ["yes", "I do", "I know"]):
                                print("Confirmation given.")
                                self.pushButton_4.clicked.emit()
                                self.should_continue = False
                            else:
                                # text = f"I heard {output}. Are you sure you wish to proceed?"
                                """ I think that we shouldn't leave people hanging once they get to this stage.
                                Either wait for their command for a set time or restart the process with an excuse.
                                But don't bug them about misheard words. 
                                So play the confirm_not audio when the program is reset."""
                                
                        start_time = time.time()
                        # print("The new start time is: ", start_time)
            
                    except Exception as e:
                        print(f"Error during transcription: {e}")
                        if self.current_state == 'hello':
                            """Do nothing while we wait for hello or a typed passphrase."""
                            # text = "I couldn't understand. Please say Hello."
                            # self.label.setText(text)
                        elif self.current_state == 'passphrase':
                            text = "I couldn't understand. Please say the pass phrase."
                            self.label.setText(text)
                            os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/passphrase_not.mp3")
                        elif self.current_state == 'name':
                            text = "I couldn't understand. Please say your name."
                            self.label_2.setText(text)
                            os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/name_not.mp3")
                        elif self.current_state == 'location':
                            text = "I couldn't understand. Please say your location."
                            self.label_3.setText(text)
                            os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/location_not.mp3")
                        elif self.current_state == 'confirmation':
                            """Do nothing while we wait for confirmation.
                            Only play the confirm_not audio when the program is reset."""
                            # text = "I couldn't understand. Are you sure you wish to proceed?"
                            # self.label_4.setText(text)
                            # synthesize_speech(text)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Program"))
        self.label.setText(_translate("MainWindow", "Please say 'Hello' to start or type your passphrase."))
        self.pushButton.setText(_translate("MainWindow", "Enter"))
        self.pushButton_2.setText(_translate("MainWindow", "Yes"))
        self.label_2.setText(_translate("MainWindow", "Who are you?"))
        self.label_3.setText(_translate("MainWindow", "Where are you?"))
        self.pushButton_3.setText(_translate("MainWindow", "Yes"))
        self.label_4.setText(_translate("MainWindow", "if you wish to proceed,"))
        self.label_5.setText(_translate("MainWindow", "press yes wishin the next "))
        self.pushButton_4.setText(_translate("MainWindow", "Yes"))
        self.label_6.setText(_translate("MainWindow", "10 seconds"))
        self.pushButton_5.setText(_translate("MainWindow", "Reset"))
        self.label_7.setText(_translate("MainWindow", "Wrong"))
        self.pushButton_6.setText(_translate("MainWindow", "OK"))


    @QtCore.pyqtSlot(int)
    def on_click(self):
        if self.stackedWidget.currentWidget() == self.page_4:
            self.timer.stop()
            GPIO.output(lock, False)
            self.stackedWidget.setCurrentIndex(4)

    def on_gpio_event(self,channel):
        button_state=GPIO.input(button)
        if button_state == 0:
            self.on_click()

    def pageCode(self):
        input_text = self.lineEdit.text().lower()
        password = config_object["USERINFO"]['password'].lower()
        print(f"Input text: {input_text}, Password: {password}")
        if password in input_text:
            self.stackedWidget.setCurrentIndex(1)
            self.lineEdit.clear()
            self.lineEdit_2.setFocus()
            if self.current_state != 'name':
                self.current_state = 'name'
                print("Playing speech from pageCode() function.")
                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/name.mp3")
        else:
            self.showWrong(0)

    def pageWho(self):
        input_text = self.lineEdit_2.text().lower()
        username = config_object["USERINFO"]['username'].lower()
        print(f"Input text: {input_text}, Username: {username}")
        if username in input_text:
            self.stackedWidget.setCurrentIndex(2)
            self.lineEdit_2.clear()
            self.lineEdit_3.setFocus()
            if self.current_state != 'location':
                self.current_state = 'location'
                print("Playing speech from pageWho() function.")
                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/location.mp3")
        else:
            self.showWrong(1)

    def pageWhere(self):
        input_text = self.lineEdit_3.text().lower()
        location = config_object["USERINFO"]['where'].lower()
        print(f"Input text: {input_text}, Location: {location}")
        if location in input_text:
            self.stackedWidget.setCurrentIndex(3)
            self.lineEdit_3.clear()
            if self.current_state != 'confirmation':
                self.current_state = 'confirmation'
                print("Playing speech from pageWhere() function.")
                os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/confirm.mp3")
            self.timer.timeout.connect(self.pageReset)
            self.timer.start(10000)
        else:
            self.showWrong(2)


    def pageYes(self):
        self.timer.stop()
        GPIO.output(lock, False)
        print("Mechanism activated.")
        self.should_continue = False
        self.stackedWidget.setCurrentIndex(4)

    def pageReset(self):
        """If the GPIO output lock was already True when coming to this page
        then the user failed to activate the mechanis in time.
        In that case play the confirm_not audio"""

        if GPIO.input(lock) == 1:
            os.system('cvlc --play-and-exit %s' % "/home/pi/voicepass-raspigui/audio/confirm_not.mp3")

        GPIO.output(lock, True)
        self.label.setText("Process completed. Please restart the program.")
        self.stackedWidget.setCurrentIndex(0)
        self.lineEdit.setFocus()
    
    def backToPage(self):
        self.stackedWidget.setCurrentIndex(self.indexpage)
        if self.indexpage == 0:    
            self.lineEdit.clear()
            self.lineEdit.setFocus()
        elif self.indexpage == 1:
            self.lineEdit_2.clear()
            self.lineEdit_2.setFocus()
        elif self.indexpage == 2:
            self.lineEdit_3.clear()
            self.lineEdit_3.setFocus()
    
    def showWrong(self, indexpage):
        self.stackedWidget.setCurrentIndex(5)
        self.indexpage = indexpage

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_E:
            if self.stackedWidget.currentWidget() == self.page_4: 
                self.pageYes()
            elif self.stackedWidget.currentWidget() == self.page_6:
                self.backToPage()                
        elif event.key() == Qt.Key_R:
            if self.stackedWidget.currentWidget() == self.page_5: 
                self.pageReset()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

