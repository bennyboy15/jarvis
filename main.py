import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry sir, you are going to have to repeat that.")
            return ""
        except sr.RequestError:
            speak("Sorry sir, it appears my speech service is down at the moment.")
            return ""

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir!")
    else:
        speak("Good Evening!")
    speak("What do you need?")

def execute_command(command):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif 'play music' in command:
        music_dir = "C:\\Your\\Music\\Directory"  # Change this to your music folder
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
        speak("Playing music")
    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I'm not sure how to help with that.")

def execute_convo(voice_txt):
    completion = client.chat.completions.create(
        model= "gpt-4o",
        messages=[{
            "role": "user",
            "content": voice_txt
        }]
    )
    speak(completion.choices[0].message.content)

if __name__ == "__main__":
    greet()
    while True:
        user_command = listen()
        if user_command:
            print("COMMAND: ", user_command)
            #execute_command(user_command)
            execute_convo(user_command)
