import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    print("Listening...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, 3, 4)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }


    print("Transcribing Audio...")

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def main():
    r = sr.Recognizer()
    print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=3)
    while(True):
        response = recognize_speech_from_mic(r, mic)

        if response["success"]:
            print(response["transcription"])

            if response["transcription"] == "exit":
                break
        else:
            print("Unable to transcribe audio")

def runLoop():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=3)
    while (True):
        response = recognize_speech_from_mic(r, mic)

        if response["success"]:
            print(response["transcription"])
        else:
            print("Unable to transcribe audio")

if __name__ == "__main__":
    main()