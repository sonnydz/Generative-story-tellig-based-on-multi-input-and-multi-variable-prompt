import speech_recognition as sr
import pyttsx3
from time import sleep
import wikipedia as wiki

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            engine.say(ask)
            engine.runAndWait()
        audio = listener.listen(source)
        voice_data = ''
        try:
            voice_data = listener.recognize_google(audio)
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            print("Sorry, I am currently unable to access the Google API. Please check your internet connection.")
        return voice_data.lower()


while True:
    voice_data = record_audio("How can I help you?")
    print(f">> {voice_data}")
