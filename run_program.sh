#!/bin/bash
matchbox-keyboard &
cd /home/pi/voicepass-raspigui &
python /home/pi/voicepass-raspigui/main_vosk.py
