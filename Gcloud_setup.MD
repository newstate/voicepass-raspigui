Read the official docs here:
https://cloud.google.com/speech-to-text/docs/
https://cloud.google.com/speech-to-text/docs/transcribe-client-libraries


How to prepare the speech to text service in Google Cloud.

1. Set up a google cloud project.

2. Add a billing account to the project.

3. Enable cloud speech to text API.

4. Set up a service account for text to speech.

5. Generate keys for using the service account and download the json file.


Prepare a (local development/production) environment (on raspberry pi for example).

1. Create a virtual environment (conda or venv) with Python 3.9

  conda create -n *“myenv”* python=3.9 ipython

2. Install google cloud CLI

  https://cloud.google.com/sdk/docs/install

  command not found? export the directory to your PATH

3. Set up application default credentials (authenticate with the gcloud CLI)

  https://cloud.google.com/docs/authentication/provide-credentials-adc

  set environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the json file
  check your env variables using printenv

  https://cloud.google.com/speech-to-text/docs/error-messages

4. pip install google-cloud-speech

5. Test initiating client library

  https://cloud.google.com/storage/docs/reference/libraries

6. Test basic transcription request

  https://cloud.google.com/speech-to-text/docs/transcribe-client-libraries
  

**for streaming audio**

7. pip install pyaudio.

  These are python bindings for portaudio system library. If you get errors, try reinstalling portaudio.

8. enable quota for your google cloud project

  gcloud auth application-default set-quota-project *your-google-cloud-project-name*

  https://cloud.google.com/docs/quota

9. In the example script set StreamingRecognitionConfig(…, single_utterance=True, …) for voice commands

  https://cloud.google.com/speech-to-text/docs/transcribe-streaming-audio
  

**for raspberry pi**

10. connect audio input device (bluetooth or regular headset)
