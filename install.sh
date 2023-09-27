#!/bin/bash

# it is assumed that pip is already installed

# the following line installs the required packages for the GUI from the PyQt5 library
sudo apt install  -y matchbox-keyboard python3-pyqt5  qtvirtualkeyboard-plugin  qml-module-qtquick2  qml-module-qtquick-controls  qml-module-qtquick-layouts  qml-module-qtquick-virtualkeyboard  qml-module-qtquick-window2  qml-module-qtquick-localstorage

# the following line installs from pip, the pyqt5 and GPIO libraries plus the requirements for google and vosk
# https://www.tutorialspoint.com/pyqt5/pyqt5_quick_guide.htm
# https://raspberrytips.com/raspberry-pi-gpio-pins/
pip install -r requirements.txt


# the following creates a desktop icon from which to launch the application

# download the sarco icon
picture_url="https://yoursite.com/your_image.png"
destination_folder=/home/pi/voicepass-raspigui
new_picture_name=your_icon.png
wget -O "$destination_folder/$new_picture_name" "$picture_url"

# Check if wget was successful
if [ $? -eq 0 ]; then
    echo "Picture downloaded and saved successfully."
else
    echo "Failed to download the picture."
fi

source_folder=/home/pi/voicepass-raspigui/desktop_icon
desktop_entry_file=program
destination_folder=/home/pi/Desktop

# Check if the source folder exists
if [ -d "$source_folder" ]; then
    # Check if the desktop entry file exists in the source folder
    if [ -f "$source_folder/$desktop_entry_file" ]; then
        # Copy the desktop entry file to the Desktop folder
        cp "$source_folder/$desktop_entry_file" "$destination_folder"
        if [ $? -eq 0 ]; then
            echo "Desktop entry file copied to Desktop successfully."
        else
            echo "Failed to copy the desktop entry file."
        fi
    else
        echo "Desktop entry file not found in the source folder."
    fi
else
    echo "Source folder not found."
fi