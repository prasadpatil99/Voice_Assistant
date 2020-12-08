

# Import libraries
import time
import pyttsx3                            
import datetime
import wikipedia
import webbrowser
import subprocess
import speech_recognition as sr  

# Set default browser for operations
mozilla_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(mozilla_path))
webbrowser = webbrowser.get('firefox')

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices')         
engine.setProperty('voices', voices[0].id)

# To make assistant audible when statements are given
def speak(audio):                           
    engine.say(audio) 
    engine.runAndWait()   # just 'say' command won't work unless this is interpreted
    
# For greetings according to time
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Hello Sir, Good Morning")

    elif hour >= 12 and hour <= 16:
        speak("Hello sir, Good Afternoon")

    else:
        speak("Hello Sir, Good Evening")
    
    speak("What can I do for you?") 
    
    
# To recognize command
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 150
        r.pause_threshold = 1
        audio = r.listen(source)  
                                                      
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')   # recognizing command through google's api
        print("User said: {} \n".format(query))
        
    except Exception:
        print("Say that again please..")
        return "None"
    return query

# For different functionalities
def instructions(query):

    if ('wikipedia' in query):                                
        speak('Searching for the wikipedia...')
        query = query.replace('wikipedia', "")  
        try:             
            results = wikipedia.summary(query, sentences=2)         
            speak("Acording to wikipedia")
            print(results)
            speak(results)
        except Exception:
            print("Sorry sir, didn't find the appropriate results")
            speak("Sorry sir, didn't find the appropriate results")
            repeat()
        
    elif (('mail' in query) or ('email' in query)):
        webbrowser.open("mail.google.com")

    elif (('youtube' in query) or ('google' in query) or ('stackoverflow' in query)):
        if (('search for' in query) and ('for' in query)):
            splitted = query.split()
            indx = splitted.index('for')
        else:
            splitted = query.split()
            indx = splitted.index('search')                    
        splitted = splitted[indx+1:]
        search=" ".join(splitted)
        print(search)
        if('youtube' in query):   
            web = 'youtube'
        elif('google' in query):
            web = 'google'
        elif('stackoverflow' in query):
            web = 'stackoverflow'
        webbrowser.open("https://www."+web+".com/search?q="+search)         
            
    elif ('calculation' in query):
        splitted = query.split()
        indx = splitted.index('calculation')
        splitted = splitted[indx+1:]
        query="".join(splitted)
        print(query)
        webbrowser.open("https://duckduckgo.com/?q="+query)
          
    elif (('headlines' in query) or ('news' in query)):
        if (('about' in query) and ('of' in query)):
            splitted = query.split()
            indx = splitted.index('about')
            splitted = splitted[indx+1:]
            query=" ".join(splitted)
            webbrowser.open("https://timesofindia.indiatimes.com/topic/"+query)
        else:
            webbrowser.open("https://timesofindia.indiatimes.com/")  
            
    elif (('stock' in query) or ('share' in query)):
        webbrowser.open("https://in.tradingview.com/symbols/NSE-NIFTY/")
        
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M")    
        speak("Sir, the time is {}".format(strTime))
        print("Sir, the time is {}".format(strTime))
        
    elif (('stop' in query) or ('thanks' in query)):
        quit

    elif "log off" in query or "sign out" in query:
        speak("Ok , your pc will be log off, make sure you have exitted from all applications")
        subprocess.call(["shutdown", "/l"])

    else:
        speak("Sorry sir I couldn't get you")
        repeat()

# To repeat if query doesn't get execute at first
def repeat():
    
    speak('Do you need any other help?')
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 150
        audio = r.listen(source)
         
    try:
        query = r.recognize_google(audio, language='en-in')

    except Exception:
        speak("Sorry sir try again later")
        return quit
    
    if "yes" in query:
        speak('What help do you need sir')
        query = command().lower()  
        instructions(query)
        
    elif "wait" in query:
        speak('Ok Sir I am waiting')
        time.sleep(5)                   # to wait for 5 sec
        speak('What help you need sir go ahead I am listening')
        query = command().lower()
        instructions(query)
        
    else:
        speak('Ok, Thank you sir')
        print('Ok, Thank you sir')
        quit

# Main function
if __name__=="__main__" : 
    
    greet()
    query = command().lower()
    instructions(query)
          
    
    
