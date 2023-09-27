import os
import tempfile
from google.cloud import texttospeech_v1

def synthesize_speech(text):
    # Create a client
    client = texttospeech_v1.TextToSpeechClient()

    # Initialize request argument(s)
    input_text = texttospeech_v1.SynthesisInput()
    input_text.text = text

    voice = texttospeech_v1.VoiceSelectionParams()
    voice.language_code = "en-GB"  # You can change this as per your requirement
    voice.name = "en-GB-Neural2-A" # this is an British English Female voice of the Neural type, see https://cloud.google.com/text-to-speech/docs/voices

    audio_config = texttospeech_v1.AudioConfig()
    audio_config.audio_encoding = texttospeech_v1.AudioEncoding.MP3
    audio_config.pitch = -6 # modify the pitch to be slightly lower for a more calming effect
    audio_config.speaking_rate = 0.75 # modify the speaking rate to be slightly slower for a more calming effect

    request = texttospeech_v1.SynthesizeSpeechRequest(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )

    # Make the request
    response = client.synthesize_speech(request=request)

    # The response's audio_content is binary.
    audio_content = response.audio_content

    # Create a temporary mp3 file
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        fp.write(audio_content)
        fp.flush()

        # Play the mp3 file with cvlc
        os.system('cvlc --play-and-exit %s' % fp.name)
