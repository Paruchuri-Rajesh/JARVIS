import speech_recognition as sr
import webbrowser
import pyttsx3
import re
import requests
from pytube import Search
from openai import OpenAI
from gtts import gTTS
import pygame 
import os



engine=pyttsx3.init()
newsapi="your newsapi key"
searchlink="https://www.google.com/search?q={}}&rlz=1C1CHBF_enIN1016IN1016&oq=apple+10+pro+max&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyCAgFEAAYFhgeMggIBhAAGBYYHjIICAcQABgWGB4yCAgIEAAYFhgeMggICRAAGBYYHtIBCDYwOTNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts=gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiprocess(c):
    client = OpenAI(
    api_key="your_openai_Apikey")
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a Virtual assistant named jarvis skilled in general tasks like Alexa dn Google cloud.Give short responses please"},
        {
            "role": "user",
            "content": c
        }
    ]
)
    return completion.choices[0].message.content



def process(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")  
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")  
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")  
    elif "open Instagram" in c.lower():
        webbrowser.open("https://instagram.com")  
    elif "play" in c.lower():
        songs = re.search(r"(?i)^play\s+(.*)", c)  
        song=songs.group(1).strip()
        search=Search(song)
        if search.results:
          first_video = search.results[0]  # Get the first result
          video_url = first_video.watch_url
          speak(f"playing: {song}") 
          webbrowser.open(video_url)  # Open in default browser

        else:
            speak("No results found.")
        #  search=Search.results[0] 
        #  link=search.watch_url
        #  link=f"https://www.youtube.com/results?search_query={song}"
        # #  link=musicLibrary.music[song.lower()]
        #  webbrowser.open(link)


    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}") 
        if r.status_code==200:
            print(f"printing the raw text{r.text}")
            data=r.json()
            print(data)
            articles=data.get('articles',[])
            speak("I am only reading out the titles for you")
            for article in articles:
               speak(article['title'])
    elif "search" in c.lower():
        searches = re.search(r"(?i)^play\s+(.*)", c)  
        search=searches.group(1).strip() 
        link=searchlink.format(search)
    else:
        output=aiprocess(c)
        speak(output)


if __name__=="__main__":
    speak("Intializing  Jarvis ")
    while True:
        r=sr.Recognizer()
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source,timeout=10,phrase_time_limit=5)
            word=r.recognize_google(audio)
            if "jarvis" in word.lower():
                speak("At your service sir")
                    #listen to command
                with sr.Microphone() as source:
                    print("Jarvis Active")
                    audio=r.listen(source,timeout=10,phrase_time_limit=5)
                    command=r.recognize_google(audio)
                    print(command)
                    process(command)


        except Exception as e:
                print("Error; {}".format(e))

