from __future__ import print_function
import os.path
from wsgiref import headers

import pyttsx3
import datetime
import pyaudio
import pywhatkit
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import re
import requests
import random
import string
from bs4 import BeautifulSoup
from urllib.request import urlopen
import subprocess
import json
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning sir")

    elif hour>=12 and hour<18:
        speak('Good Afternoon sir')

    else:
        speak('Good Evening sir')

    speak("this is your Ai assistant Jarvis how can i help you")
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        print(e)
        print("Say that again please...")   #Say that again will be printed in case of improper voice
        return "None" #None string will be returned
    return query

def start():
    wishMe()
    while True:
        query= takeCommand().lower()
        # logic for executing tasks based on query
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query = query.replace('wikipedia','')
            results = wikipedia.summary(query, sentences = 2)
            speak('accouding to wikipedia')
            speak(results)

        elif 'open youtube' in query:
            webbrowser.get(chrome_path).open('youtube.com')

        elif 'open google' in query:
            webbrowser.get(chrome_path).open('google.com')

        elif 'open stackoverflow' in query:
            webbrowser.get(chrome_path).open('stackoverflow.com')

        elif 'open github' in query:
            webbrowser.get(chrome_path).open('github.com')

        elif 'open facebook' in query:
            webbrowser.get(chrome_path).open('facebook.com')
        elif 'play' in query:
            pywhatkit.playonyt(query)
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f"sir, the time is {strTime}")
        elif "rap" in query:
            speak('''Just waking up in the morning gotta thank God
                    I don't know but today seems kinda odd
                    No barking from the dogs, no smog
                    And momma cooked a breakfast with no hog
                    I got my grub on, but didn't pig out
                    Finally got a call from a girl want to dig out
                    Hooked it up on later as I hit the do'
                    Thinking will i live another twenty fo'
                    I gotta go cause I got me a drop top
                    And if I hit the switch, I can make the ass drop
                    Had to stop at a red light
                    Looking in my mirror not a jacker in sight
                    And everything is alright
                    I got a beep from Kim and she can fuck all night
                    Called up the homies and I'm askin' y'all
                    Which park, are y'all playin' basketball?
                    Get me on the court and I'm trouble
                    Last week fucked around and got a triple double
                    Freaking brothers every way like M.J.
                    I can't believe, today was a good day''')
        elif 'story' in query:
            speak("once upon a time there was a boy abhinav")
        elif 'on google' in query:
            pywhatkit.search(query)
        elif 'shut down my computer' in query:
            pywhatkit.shutdown(time=20)
        elif 'open code' in query:
            path = "C:\\Users\\astitva\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe"
            os.startfile(path)

        elif 'joke' in query.lower():
            res = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})

            if res.status_code == requests.codes.ok:
                speak(str(res.json()['joke']))
            else:
                speak('oops!I ran out of jokes')

        elif 'news' in query.lower():
            try:
                news_url = "https://news.google.com/news/rss"
                Client = urlopen(news_url)
                xml_page = Client.read()
                Client.close()
                soup_page = BeautifulSoup(xml_page, "html.parser")
                news_list = soup_page.findAll("item")
                for news in news_list[:5]:
                    speak(news.title.text)
            except Exception as e:
                print(e)



        elif 'tell me about' in query.lower():
            reg_ex = re.search('tell me about (.*)', query)
            try:
                if reg_ex:
                    topic = reg_ex.group(1)
                    print(wikipedia.summary(topic, sentences=3))
                    speak(wikipedia.summary(topic, sentences=3))
            except Exception as e:
                speak(e)



        elif 'search' in query.lower():
            reg_ex = re.search('search (.+)', query)
            if reg_ex:
                subject = reg_ex.group(1)
                url = 'https://www.google.com/search?q=' + subject
                webbrowser.open(url)
                speak('Searching for ' + subject + ' on Google.')



        elif 'current weather' in query.lower():
            api_key = "api key"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak("which city sir")
            city_name = takeCommand()
            complete_url = base_url + "q=" + city_name + "&appid=" + api_key
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature (in kelvin unit) = " +
                      str(current_temperature) +
                      "\n atmospheric pressure (in hPa unit) = " +
                      str(current_pressure) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
            else:
                speak(" City Not Found ")
        elif 'make a note' in query.lower():

            speak("What would you like me to write down?")
            note_text = takeCommand()
            note(note_text)
            speak("I've made a note of that.")


        elif 'videos about' in query.lower():
            reg_ex = re.search('videos (.+)', query)
            if reg_ex:
                videosAbout = reg_ex.group(1)
                url = 'https://www.youtube.com/results?q=' + videosAbout
                try:
                    source_code = requests.get(url, headers=headers, timeout=15)
                    plain_text = source_code.text
                    soup = BeautifulSoup(plain_text, "html.parser")
                    songs = soup.findAll('div', {'class': 'yt-lockup-video'})
                    song = songs[0].contents[0].contents[0].contents[0]
                    hit = song['href']
                    webbrowser.open('https://www.youtube.com' + hit)
                    speak('Playing ' + videosAbout + ' on Youtube.')
                except Exception as e:
                    webbrowser.open(url)
                    speak('Searching for ' + videosAbout + ' on Youtube.')
        elif "who are you" in query.lower() or 'where are you' in query.lower() or 'what are you' in query.lower():
            setReplies = [' I am ' + "belvix" + 'In your system' + 'I am an example of AI']
            speak(setReplies)

        elif 'hello' in query.lower() or 'hey' in query.lower():
            speak('hey')

        elif 'bye' in query.lower():
            speak("bye have a better day ahead")

        elif 'create a password' in query.lower() or 'give me a password' in query.lower():
            sep = ""
            random.choice(string.ascii_letters)
            password = []
            let1 = random.randint(1, 9)
            let2 = random.randint(1, 9)
            let3 = random.choice(string.ascii_letters)
            let4 = random.randint(1, 9)
            let5 = random.choice(string.ascii_letters)
            let6 = random.choice(string.ascii_letters)
            let7 = random.randint(1, 9)
            let8 = random.choice(string.ascii_letters)
            let9 = random.randint(1, 9)
            let10 = random.randint(1, 9)
            let11 = random.choice(string.ascii_letters)
            let12 = random.randint(1, 9)
            let13 = random.choice(string.ascii_letters)
            let14 = random.choice(string.ascii_letters)
            let15 = random.randint(1, 9)
            let16 = random.choice(string.ascii_letters)
            print(let1, let2, let3, let4, let5, let6, let7, let8, let9, let10, let11, let12, let13, let14, let15, let16,
                  sep="")
start()
