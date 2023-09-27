import os
import tempfile
from google.cloud import texttospeech_v1

def synthesize_speech_andsave(text, filename):
    # Create a client
    client = texttospeech_v1.TextToSpeechClient()

    # Initialize request argument(s)
    input_text = texttospeech_v1.SynthesisInput()
    input_text.text = text

    voice = texttospeech_v1.VoiceSelectionParams()
    voice.language_code = "en-GB"  # You can change this as per your requirement
    voice.name = "en-GB-Neural2-A" # The most neutral sounding voice I could find.

    audio_config = texttospeech_v1.AudioConfig()
    audio_config.audio_encoding = texttospeech_v1.AudioEncoding.MP3
    audio_config.pitch = -3  # To make the voice sound a bit more calm.
    audio_config.speaking_rate = 0.95 # Just to make sure the user catches the question correctly.

    request = texttospeech_v1.SynthesizeSpeechRequest(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )

    # Make the request
    response = client.synthesize_speech(request=request)

    # The response's audio_content is binary
    audio_content = response.audio_content

    # Create an mp3 file with the provided filename
    try:
        with open(filename, "wb") as out:
            out.write(audio_content)
            print(f"Audio content written to file {filename}")
        
        # Play the mp3 file with cvlc
        os.system('cvlc --play-and-exit %s' % filename)

    except IOError as io_error:
        # Handle any IOError exceptions that occur during file I/O
        print(f"Failed to write audio content to file {filename}. The error is {io_error}")

synthesize_speech_andsave("Please say 'Hello' to start. Or type your passphrase.", "/home/pi/voicepass-raspigui/audio/start.mp3")
synthesize_speech_andsave("Please say Hello.", "/home/pi/voicepass-raspigui/audio/hello.mp3")
synthesize_speech_andsave("Please say the pass phrase after the beep.", "/home/pi/voicepass-raspigui/audio/passphrase.mp3")
synthesize_speech_andsave("I heard something else. Please try saying your passphrase again.", "/home/pi/voicepass-raspigui/audio/passphrase_else.mp3")
synthesize_speech_andsave("I couldn't hear you. Please try saying your passphrase again.", "/home/pi/voicepass-raspigui/audio/passphrase_not.mp3")
synthesize_speech_andsave("Please say your name after the beep.", "/home/pi/voicepass-raspigui/audio/name.mp3")
synthesize_speech_andsave("I heard something else. Please try saying your name again.", "/home/pi/voicepass-raspigui/audio/name_else.mp3")
synthesize_speech_andsave("I couldn't hear you. Please try saying your name again.", "/home/pi/voicepass-raspigui/audio/name_not.mp3")
synthesize_speech_andsave("Please say your location after the beep.", "/home/pi/voicepass-raspigui/audio/location.mp3")
synthesize_speech_andsave("I heard something else. Please try saying your location again.", "/home/pi/voicepass-raspigui/audio/location_else.mp3")
synthesize_speech_andsave("I couldn't hear you. Please try saying your location again.", "/home/pi/voicepass-raspigui/audio/location_not.mp3")
synthesize_speech_andsave("If you wish to activate the mechanism say 'yes' after the beep.", "/home/pi/voicepass-raspigui/audio/confirm.mp3")
synthesize_speech_andsave("I'm sorry but I did not get a confirmation in time. Please answer the questions again whenever you're ready.", "/home/pi/voicepass-raspigui/audio/confirm_not.mp3")

