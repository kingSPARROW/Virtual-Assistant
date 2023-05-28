#_____________________________________________________J.A.R.V.I.S________________________________________________________
#Python modules used for this programm
import sys
import speech_recognition as sr
import pyttsx3
import pywhatkit
import pywhatkit as kit
import datetime
import wikipedia
import pyjokes
import webbrowser
import time
import subprocess
import os
import cv2
import random
from requests import get
import smtplib
import psutil
import instaloader
import pyautogui
import PyPDF2
from Recordings import Record_Option
from PIL import ImageGrab
import pyaudio
import wave
import numpy as np 
from PhoneNumer import Phonenumber_location_tracker
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from JarvisUi import Ui_JarvisUI
from state import state
from pywikihow import search_wikihow
# import speedtest 
from pytube import YouTube
# import qrcode

#Set our engine to "Pyttsx3" which is used for text to speech in Python 
#and sapi5 is Microsoft speech application platform interface 
#we will be using this for text to speech function.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id) #index '0' for 'David'(male) voice index '1' for 'zira'(female) voice

def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        talk("Good morning")
    elif hour>=12 and hour<18:
        talk("Good Afternoon")
    else:
        talk("Good night")

#Main classs where all the functiona are present
class MainThread(QThread):
    # def __init__(self):
    #     super(MainThread,self).__init__()
    
    # def run(self):
    #     self.Intro()
    
    # #function that will take the querys  to convert voice into text
    # def take_query(self):
    #     try:
    #         listener = sr.Recognizer()
    #         with sr.Microphone() as source:

    #             print('Listening....')
    #             listener.pause_threshold = 1
    #             voice = listener.listen(source,timeout=4,phrase_time_limit=7)
    #             print("Recognizing...")
    #             query1 = listener.recognize_google(voice,language='en-in')
    #             query1 = query1.lower()  
    #             if 'Sparrow' in query1: 
    #                 query1 = query1.replace('Sparrow','')
                
    #         return query1
    #     except:
    #         return 'None'
    def __init__(self):
        super(MainThread,self).__init__()
    
    def run(self):
        self.run_sparrow()
    
    def STT(self):
        try:
            listener = sr.Recognizer()
            with sr.Microphone() as source:

                print('Listening....')
                listener.pause_threshold = 1
                voice = listener.listen(source,timeout=4,phrase_time_limit=7)
                print("Recognizing...")
                command1 = listener.recognize_google(voice,language='en-in')
                command1 = command1.lower()  
                if 'Sparrow' in command1: 
                    command1 = command1.replace('Sparrow','')
                
            return command1
        except:
            return 'None'
        
    #Jarvis querys controller 
    def run_sparrow(self):
        wish()
        self.talk('Hello boss I am Sparrow your assistant. please tell me how can i help you')
        
        while True:
            self.query =  self.STT() #Every time taking query after a task is done
            print(self.query)
            if ('play a song' in self.query) or ('youtube' in self.query) or ("download a song" in self.query) or ("download song" in self.query) : 
                #querys for opening youtube, playing a song in youtube, and download a song in youtube
                self.yt(self.query) #function is from line 555
            #Interaction querys with JARVIS
            elif ('your age' in self.query) or ('are you single'in self.query) or ('are you there' in self.query) or ('tell me something' in self.query) or ('thank you' in self.query) or ('in your free time' in self.query) or ('i love you' in self.query) or ('can you hear me' in self.query) or ('do you ever get tired' in self.query):
                self.Fun(self.query)
            elif 'time' in self.query : 
                self.Clock_time(self.query)
            elif (('hi' in self.query) and len(self.query)==2) or ((('hai' in self.query) or ('hey' in self.query)) and len(self.query)==3) or (('hello' in self.query) and len(self.query)==5):
                self.comum(self.query)
            elif ('what can you do' in self.query) or ('your name' in self.query) or ('my name' in self.query) or ('university name' in self.query):
                self.Fun(self.query)
            elif ('joke'in self.query) or ('date' in self.query):
                self.Fun(self.query)
            #schedule querys for remembering you what is the planns of the day
            elif ("college time table" in self.query) or ("schedule" in self.query):
                self.shedule() #function is present from 407
            #It will tell the day Eg : Today is wednesday
            elif ("today" in self.query):
                day = self.Cal_day()
                self.talk("Today is "+day)
            #commad for opening any weekly meeting links
            #Eg: I have kept a meeting my amFOSS club 
            #Note: the given link is fake!!
            elif ("meeting" in self.query):
                self.talk("Ok sir opening meeet")
                webbrowser.open("https://meeting/")
            #query if you don't want the JARVIS to spack until for a certain time
            #Note: I can be silent for max of 10mins
            # Eg: JARVIS keep quiet for 5 minutes 
            elif ('silence' in self.query) or ('silent' in self.query) or ('keep quiet' in self.query) or ('wait for' in self.query) :
                self.silenceTime(self.query)
            #query for opening your social media accounts in webrowser
            #Eg : JARVIS open facebook (or) JARVIS open social media facebook 
            elif ('facebook' in self.query) or ('whatsapp' in self.query) or ('instagram' in self.query) or ('twitter' in self.query) or ('discord' in self.query) or ('social media' in self.query):
                self.social(self.query)
            #query for opening your OTT platform accounts
            #Eg: open hotstart
            elif ('hotstar' in self.query) or ('prime' in self.query) or ('netflix' in self.query):
                self.OTT(self.query)
            #query for opening your online classes links
            elif ('online classes'in self.query):
                self.OnlineClasses(self.query)
            #query for opeing college websites
            elif ('open teams'in self.query) or ('open stream'in self.query) or ('open sharepoint'in self.query) or('open outlook'in self.query)or('open amrita portal'in self.query)or('open octave'in self.query):
                self.college(self.query)
            #query to search for something in wikipedia
            #Eg: what is meant by python in wikipedia (or) search for "_something_" in wikipedia
            elif ('wikipedia' in self.query) or ('what is meant by' in self.query) or ('tell me about' in self.query) or ('who the heck is' in self.query):
                self.B_S(self.query)
            #query for opening your browsers and search for information in google
            elif ('open google'in self.query) or ('open edge'in self.query) :
                self.brows(self.query)
            #query to open your google applications
            elif ('open gmail'in self.query) or('open maps'in self.query) or('open calender'in self.query) or('open documents'in self.query )or('open spredsheet'in self.query) or('open images'in self.query) or('open drive'in self.query) or('open news' in self.query):
                self.Google_Apps(self.query)
            #query to open your open-source accounts
            #you can add other if you have
            elif ('open github'in self.query) or ('open gitlab'in self.query) :
                self.open_source(self.query)
            #querys to open presentaion makeing tools like CANVA and GOOGLE SLIDES
            elif ('slides'in self.query) or ('canva'in self.query) :
                self.edit(self.query)
            #query to open desktop applications
            #It can open : caliculator, notepad,paint, teams(aka online classes), discord, spotify, ltspice,vscode(aka editor), steam, VLC media player
            elif ('open calculator'in self.query) or ('open notepad'in self.query) or ('open paint'in self.query) or ('open online classes'in self.query) or ('open discord'in self.query) or ('open ltspice'in self.query) or ('open editor'in self.query) or ('open spotify'in self.query) or ('open steam'in self.query) or ('open media player'in self.query):
                self.OpenApp(self.query)
            #query to close desktop applications
            #It can close : caliculator, notepad,paint, discord, spotify, ltspice,vscode(aka editor), steam, VLC media player
            elif ('close calculator'in self.query) or ('close notepad'in self.query) or ('close paint'in self.query) or ('close discord'in self.query) or ('close ltspice'in self.query) or ('close editor'in self.query) or ('close spotify'in self.query) or ('close steam'in self.query) or ('close media player'in self.query):
                self.CloseApp(self.query)
            #query for opening shopping websites 
            #NOTE: you can add as many websites
            elif ('flipkart'in self.query) or ('amazon'in self.query) :
                self.shopping(self.query)
            #query for asking your current location
            elif ('where i am' in self.query) or ('where we are' in self.query):
                self.locaiton()
            #query for opening query prompt 
            #Eg: jarvis open query prompt
            elif ('query prompt'in self.query) :
                self.talk('Opening query prompt')
                os.system('start cmd')
            #query for opening an instagram profile and downloading the profile pictures of the profile
            #Eg: jarvis open a profile on instagram 
            elif ('instagram profile' in self.query) or("profile on instagram" in self.query):
                self.Instagram_Pro()
            #query for opening taking screenshot
            #Eg: jarvis take a screenshot
            elif ('take screenshot' in self.query)or ('screenshot' in self.query) or("take a screenshot" in self.query):
                self.scshot()
            #query for reading PDF
            #EG: Jarvis read pdf
            elif ("read pdf" in self.query) or ("pdf" in self.query):
                self.pdf_reader()
            #query for searching for a procedure how to do something
            #Eg:jarvis activate mod
            #   jarvis How to make a cake (or) jarvis how to convert int to string in programming 
            elif "activate mod" in self.query:
                self.How()
            #query for increaing the volume in the system
            #Eg: jarvis increase volume
            elif ("volume up" in self.query) or ("increase volume" in self.query):
                pyautogui.press("volumeup")
                self.talk('volume increased')
            #query for decreaseing the volume in the system
            #Eg: jarvis decrease volume
            elif ("volume down" in self.query) or ("decrease volume" in self.query):
                pyautogui.press("volumedown")
                self.talk('volume decreased')
            #query to mute the system sound
            #Eg: jarvis mute the sound
            elif ("volume mute" in self.query) or ("mute the sound" in self.query) :
                pyautogui.press("volumemute")
                self.talk('volume muted')
            #query for opening your mobile camera the description for using this is in the README file
            #Eg: Jarvis open mobile camera
            elif ("open mobile cam" in self.query):
                self.Mobilecamra()
            #query for opening your webcamera
            #Eg: jarvis open webcamera
            elif ('web cam'in self.query) :
                self.webCam()
            #query for creating a new contact
            elif("create a new contact" in self.query):
                self.AddContact()
            #query for searching for a contact
            elif("number in contacts" in self.query):
                self.NameIntheContDataBase(self.query)
            #query for displaying all contacts
            elif("display all the contacts" in self.query):
                self.Display()
            #query for checking covid status in India
            #Eg: jarvis check covid (or) corona status
            elif ("covid" in self.query) or  ("corona" in self.query):
                self.talk("Boss which state covid 19 status do you want to check")
                s = self.take_query()
                self.Covid(s)
            #query for screenRecording
            #Eg: Jarvis start Screen recording
            elif ("recording" in self.query) or ("screen recording" in self.query) or ("voice recording" in self.query):
                try:
                    self.talk("Boss press q key to stop recordings")
                    option = self.query
                    Record_Option(option=option)
                    self.talk("Boss recording is being saved")
                except:
                    self.talk("Boss an unexpected error occured couldn't start screen recording")
            #query for phone number tracker
            elif ("track" in self.query) or ("track a mobile number" in self.query):
                self.talk("Boss please enter the mobile number with country code")
                try:
                     location,servise_prover,lat,lng=Phonenumber_location_tracker()
                     self.talk(f"Boss the mobile number is from {location} and the service provider for the mobile number is {servise_prover}")
                     self.talk(f"latitude of that mobile nuber is {lat} and longitude of that mobile number is {lng}")
                     print(location,servise_prover)
                     print(f"Latitude : {lat} and Longitude : {lng}")
                     self.talk("Boss location of the mobile number is saved in Maps")
                except:
                     self.talk("Boss an unexpected error occured couldn't track the mobile number")
                    #  query for playing a dowloaded mp3 song in which is present in your system
            
            #Eg: Jarvis play music
            elif 'music' in self.query:
                try:
                    music_dir = 'E:\\music' #change the song path directory if you have songs in other directory
                    songs = os.listdir(music_dir)
                    for song in songs:
                        if song.endswith('.mp3'):
                            os.startfile(os.path.join(music_dir, song))
                except:
                    self.talk("Boss an unexpected error occured")
            #query for knowing your system IP address
            #Eg: jarvis check my ip address
            elif 'ip address' in self.query:
                ip = get('https://api.ipify.org').text
                print(f"your IP address is {ip}")
                self.talk(f"your IP address is {ip}")
            #query for seading a whatsapp group and individual message
            #Individual => Eg: send a message to sujith
            #group => Eg: send a message to school group NOTE: mention the name "group" otherwise jarvis cannot detect the name
            elif ('send a message' in self.query):
                self.whatsapp(self.query)
            #query for sending an email 
            #Eg: jarvis send email
            elif 'send email' in self.query:
                self.verifyMail()
            #query for checking the temperature in surroundings
            #jarvis check the surroundings temperature
            elif "temperature" in self.query:
                self.temperature()
            #query to generate the qr codes
            elif "create a qr code" in self.query:
                self.qrCodeGenerator()
            #query for checking internet speed
            #Eg: jarvis check my internet speed
            elif "internet speed" in self.query:
                self.InternetSpeed()
            #query to make the jarvis sleep
            #Eg: jarvis you can sleep now
            elif ("you can sleep" in self.query) or ("sleep now" in self.query):
                self.talk("Okay boss, I am going to sleep you can call me anytime.")
                break
            #query for waking the jarvis from sleep
            #jarvis wake up
            elif ("wake up" in self.query) or ("get up" in self.query):
                self.talk("boss, I am not sleeping, I am in online, what can I do for u")
            #query for exiting jarvis from the program
            #Eg: jarvis goodbye
            elif ("goodbye" in self.query) or ("get lost" in self.query):
                self.talk("Thanks for using me boss, have a good day")
                sys.exit()
            #query for knowing about your system condition
            #Eg: jarvis what is the system condition
            elif ('system condition' in self.query) or ('condition of the system' in self.query):
                self.talk("checking the system condition")
                self.condition()
            #query for knowing the latest news
            #Eg: jarvis tell me the news
            elif ('tell me news' in self.query) or ("the news" in self.query) or ("todays news" in self.query):
                self.talk("Please wait boss, featching the latest news")
                self.news()
            #query for shutting down the system
            #Eg: jarvis shutdown the system
            elif ('shutdown the system' in self.query) or ('down the system' in self.query):
                self.talk("Boss shutting down the system in 10 seconds")
                time.sleep(10)
                os.system("shutdown /s /t 5")
            #query for restarting the system
            #Eg: jarvis restart the system
            elif 'restart the system' in self.query:
                self.talk("Boss restarting the system in 10 seconds")
                time.sleep(10)
                os.system("shutdown /r /t 5")
            #query for make the system sleep
            #Eg: jarvis sleep the system
            elif 'sleep the system' in self.query:
                self.talk("Boss the system is going to sleep")
                os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
            
    #Intro msg
    def Intro(self):
        while True:
            self.permission = self.STT()
            print(self.permission)
            if ("wake up" in self.permission) or ("get up" in self.permission):
                self.run_sparrow()
            elif ("goodbye" in self.permission) or ("get lost" in self.permission):
                self.talk("Thanks for using me boss, have a good day")
                sys.exit()
                
    #Talk 
    def talk(self,text):
        engine.say(text)
        engine.runAndWait()

    #Wish
    def wish(self):
        hour = int(datetime.datetime.now().hour)
        t = time.strftime("%I:%M %p")
        day = self.Cal_day()
        print(t)
        if (hour>=0) and (hour <=12) and ('AM' in t):
            self.talk(f'Good morning boss, its {day} and the time is {t}')
        elif (hour >= 12) and (hour <= 16) and ('PM' in t):
            self.talk(f"good afternoon boss, its {day} and the time is {t}")
        else:
            self.talk(f"good evening boss, its {day} and the time is {t}")

    #Weather forecast
    def temperature(self):
        IP_Address = get('https://api.ipify.org').text
        url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
        geo_reqeust = get(url)
        geo_data = geo_reqeust.json()
        city = geo_data['city']
        search = f"temperature in {city}"
        url_1 = f"https://www.google.com/search?q={search}"
        r = get(url_1)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div",class_="BNeawe").text
        self.talk(f"current {search} is {temp}")
    
    # #qrCodeGenerator
    def qrCodeGenerator(self):
        self.talk(f"Boss enter the text/link that you want to keep in the qr code")
        input_Text_link = input("Enter the Text/Link : ")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=4,
        )
        QRfile_name = (str(datetime.datetime.now())).replace(" ","-")
        QRfile_name = QRfile_name.replace(":","-")
        QRfile_name = QRfile_name.replace(".","-")
        QRfile_name = QRfile_name+"-QR.png"
        qr.add_data(input_Text_link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"QRCodes\{QRfile_name}")
        self.talk(f"Boss the qr code has been generated")

    #Mobile camera
    def Mobilecamra(self):
        import urllib.request
        import numpy as np
        try:
            self.talk(f"Boss openinging mobile camera")
            URL = "http://_IP_Webcam_IP_address_/shot.jpg" #Discription for this is available in the README file
            while True:
                imag_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                img = cv2.imdecode(imag_arr,-1)
                cv2.imshow('IPWebcam',img)
                q = cv2.waitKey(1)
                if q == ord("q"):
                    self.talk(f"Boss closing mobile camera")
                    break
            cv2.destroyAllWindows()
        except Exception as e:
            print("Some error occured")

    #Web camera
    #NOTE to exit from the web camera press "ESC" key 
    def webCam(self):    
        self.talk('Opening camera')
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('web camera',img)
            k = cv2.waitKey(50)
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    
    #covid 
    def Covid(self,s):
        try:
            from covid_india import states
            details = states.getdata()
            if "check in" in s:
                s = s.replace("check in","").strip()
                print(s)
            elif "check" in s:
                s = s.replace("check","").strip()
                print(s)
            elif "tech" in s:
                s = s.replace("tech","").strip()
            s = state[s]
            ss = details[s]
            Total = ss["Total"]
            Active = ss["Active"]
            Cured = ss["Cured"]
            Death = ss["Death"]
            print(f"Boss the total cases in {s} are {Total}, the number of active cases are {Active}, and {Cured} people cured, and {Death} people are death")
            self.talk(f"Boss the total cases in {s} are {Total}, the number of active cases are {Active}, and {Cured} people cured, and {Death} people are death")
            time.sleep(5)
            self.talk("Boss do you want any information of other states")
            I = self.take_query()
            print(I)
            if ("check" in I):
                self.Covid(I)
            elif("no" in I):
                self.talk("Okay boss stay home stay safe")
            else:
                self.talk("Okay boss stay home stay safe")
        except:
            self.talk("Boss some error occured, please try again")
            self.talk("Boss do you want any information of other states")
            I = self.take_query()
            if("yes" in I):
                self.talk("boss, Which state covid status do u want to check")
                Sta = self.take_query()
                self.Covid(Sta)
            elif("no" in I):
                self.talk("Okay boss stay home stay safe")
            else:
                self.talk("Okay boss stay home stay safe")

    #Whatsapp
    def whatsapp(self,query):
        try:
            query = query.replace('send a message to','')
            query = query.strip()
            name,numberID,F = self.SearchCont(query)
            if F:
                print(numberID)
                self.talk(f'Boss, what message do you want to send to {name}')
                message = self.take_query()
                hour = int(datetime.datetime.now().hour)
                min = int(datetime.datetime.now().minute)
                print(hour,min)
                if "group" in query:
                    kit.sendwhatmsg_to_group(numberID,message,int(hour),int(min)+1)
                else:
                    kit.sendwhatmsg(numberID,message,int(hour),int(min)+1)
                self.talk("Boss message have been sent")
            if F==False:
                self.talk(f'Boss, the name not found in our data base, shall I add the contact')
                AddOrNot = self.take_query()
                print(AddOrNot)
                if ("yes" in AddOrNot) or ("add" in AddOrNot) or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                    self.AddContact()
                elif("no" in AddOrNot):
                    self.talk('Ok Boss')
        except:
            print("Error occured, please try again")

    
    #Add contacts
    def AddContact(self):
        self.talk(f'Boss, Enter the contact details')
        name = input("Enter the name :").lower()
        number = input("Enter the number :")
        NumberFormat = f'"{name}":"+91{number}"'
        ContFile = open("Contacts.txt", "a") 
        ContFile.write(f"{NumberFormat}\n")
        ContFile.close()
        self.talk(f'Boss, Contact Saved Successfully')

    #Search Contact
    def SearchCont(self,name):
        with open("Contacts.txt","r") as ContactsFile:
            for line in ContactsFile:
                if name in line:
                    print("Name Match Found")
                    s = line.split("\"")
                    return s[1],s[3],True
        return 0,0,False
    
    #Display all contacts
    def Display(self):
        ContactsFile = open("Contacts.txt","r")
        count=0
        for line in ContactsFile:
            count+=1
        ContactsFile.close()
        ContactsFile = open("Contacts.txt","r")
        self.talk(f"Boss displaying the {count} contacts stored in our data base")    
        for line in ContactsFile:
            s = line.split("\"")
            print("Name: "+s[1])
            print("Number: "+s[3])
        ContactsFile.close()

    #search contact
    def NameIntheContDataBase(self,query):
        line = query
        line = line.split("number in contacts")[0]
        if("tell me" in line):
            name = line.split("tell me")[1]
            name = name.strip()
        else:
            name= line.strip()
        name,number,bo = self.SearchCont(name)
        if bo:
            print(f"Contact Match Found in our data base with {name} and the mboile number is {number}")
            self.talk(f"Boss Contact Match Found in our data base with {name} and the mboile number is {number}")
        else:
            self.talk("Boss the name not found in our data base, shall I add the contact")
            AddOrNot = self.take_query()
            print(AddOrNot)
            if ("yes add it" in AddOrNot)or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                self.AddContact()
                self.talk(f'Boss, Contact Saved Successfully')
            elif("no" in AddOrNot) or ("don't add" in AddOrNot):
                self.talk('Ok Boss')

    #Internet spped
    def InternetSpeed(self):
        self.talk("Wait a few seconds boss, checking your internet speed")
        st = speedtest.Speedtest()
        dl = st.download()
        dl = dl/(1000000) #converting bytes to megabytes
        up = st.upload()
        up = up/(1000000)
        print(dl,up)
        self.talk(f"Boss, we have {dl} megabytes per second downloading speed and {up} megabytes per second uploading speed")
        
    #Search for a process how to do
    def How(self):
        self.talk("How to do mode is is activated")
        while True:
            self.talk("Please tell me what you want to know")
            how = self.take_query()
            try:
                if ("exit" in how) or("close" in how):
                    self.talk("Ok sir how to mode is closed")
                    break
                else:
                    max_result=1
                    how_to = search_wikihow(how,max_result)
                    assert len(how_to) == 1
                    how_to[0].print()
                    self.talk(how_to[0].summary)
            except Exception as e:
                self.talk("Sorry sir, I am not able to find this")

    #Communication querys
    def comum(self,query):
        print(query)
        if ('hi'in query) or('hai'in query) or ('hey'in query) or ('hello' in query) :
            self.talk("Hello boss what can I help for u")
        else :
            self.No_result_found()

    #Fun querys to interact with jarvis
    def Fun(self,query):
        print(query)
        if 'your name' in query:
            self.talk("My name is jarvis")
        elif 'my name' in query:
            self.talk("your name is Sujith")
        elif 'university name' in query:
            self.talk("you are studing in Amrita Vishwa Vidyapeetam, with batcheloe in Computer Science and Artificail Intelligence") 
        elif 'what can you do' in query:
            self.talk("I talk with you until you want to stop, I can say time, open your social media accounts,your open source accounts, open google browser,and I can also open your college websites, I can search for some thing in google and I can tell jokes")
        elif 'your age' in query:
            self.talk("I am very young that u")
        elif 'date' in query:
            self.talk('Sorry not intreseted, I am having headache, we will catch up some other time')
        elif 'are you single' in query:
            self.talk('No, I am in a relationship with wifi')
        elif 'joke' in query:
            self.talk(pyjokes.get_joke())
        elif 'are you there' in query:
            self.talk('Yes boss I am here')
        elif 'tell me something' in query:
            self.talk('boss, I don\'t have much to say, you only tell me someting i will give you the company')
        elif 'thank you' in query:
            self.talk('boss, I am here to help you..., your welcome')
        elif 'in your free time' in self.query:
            self.talk('boss, I will be listening to all your words')
        elif 'i love you' in query:
            self.talk('I love you too boss')
        elif 'can you hear me' in query:
            self.talk('Yes Boss, I can hear you')
        elif 'do you ever get tired' in query:
            self.talk('It would be impossible to tire of our conversation')
        else :
            self.No_result_found()

    #Social media accounts querys
    def social(self,query):
        print(query)
        if 'facebook' in query:
            self.talk('opening your facebook')
            webbrowser.open('https://www.facebook.com/')
        elif 'whatsapp' in query:
            self.talk('opening your whatsapp')
            webbrowser.open('https://web.whatsapp.com/')
        elif 'instagram' in query:
            self.talk('opening your instagram')
            webbrowser.open('https://www.instagram.com/')
        elif 'twitter' in query:
            self.talk('opening your twitter')
            webbrowser.open('https://twitter.com/Suj8_116')
        elif 'discord' in query:
            self.talk('opening your discord')
            webbrowser.open('https://discord.com/channels/@me')
        else :
            self.No_result_found()
        
    #clock querys
    def Clock_time(self,query):
        print(query)
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        self.talk("Current time is "+time)
    
    #calender day
    def Cal_day(self):
        day = datetime.datetime.today().weekday() + 1
        Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',4: 'Thursday', 5: 'Friday', 6: 'Saturday',7: 'Sunday'}
        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
            print(day_of_the_week)
        
        return day_of_the_week

    #shedule function for remembering todays plans
    #NOTE For example I have declared my college timetable you can declare anything you want
    def shedule(self):
        day = self.Cal_day().lower()
        self.talk("Boss today's shedule is")
        Week = {"monday" : "Boss from 9:00 to 9:50 you have Cultural class, from 10:00 to 11:50 you have mechanics class, from 12:00 to 2:00 you have brake, and today you have sensors lab from 2:00",
        "tuesday" : "Boss from 9:00 to 9:50 you have English class, from 10:00 to 10:50 you have break,from 11:00 to 12:50 you have ELectrical class, from 1:00 to 2:00 you have brake, and today you have biology lab from 2:00",
        "wednesday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Data structures class, from 11:00 to 11:50 you have mechanics class, from 12:00 to 12:50 you have cultural class, from 1:00 to 2:00 you have brake, and today you have Data structures lab from 2:00",
        "thrusday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Maths class, from 11:00 to 12:50 you have sensors class, from 1:00 to 2:00 you have brake, and today you have english lab from 2:00",
        "friday" : "Boss today you have a full day of classes from 9:00 to 9:50 you have Biology class, from 10:00 to 10:50 you have data structures class, from 11:00 to 12:50 you have Elements of computing class, from 1:00 to 2:00 you have brake, and today you have Electronics lab from 2:00",
        "saturday" : "Boss today you have a full day of classes from 9:00 to 11:50 you have maths lab, from 12:00 to 12:50 you have english class, from 1:00 to 2:00 you have brake, and today you have elements of computing lab from 2:00",
        "sunday":"Boss today is holiday but we can't say anything when they will bomb with any assisgnments"}
        if day in Week.keys():
            self.talk(Week[day])

    #college resources querys
    #NOTE Below are some dummy links replace with your college website links
    def college(self,query):
        print(query)
        if 'teams' in query:
            self.talk('opening your microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')
        elif 'stream' in query:
            self.talk('opening your microsoft stream')
            webbrowser.open('https://web.microsoftstream.com/')
        elif 'outlook' in query:
            self.talk('opening your microsoft school outlook')
            webbrowser.open('https://outlook.office.com/mail/')
        elif 'amrita portal' in query:
            self.talk('opening your amrita university management system')
            webbrowser.open('https://aumsam.amrita.edu/')
        elif 'octave' in query:
            self.talk('opening Octave online')
            webbrowser.open('https://octave-online.net/')
        else :
            self.No_result_found()
    
    #Online classes
    def OnlineClasses(self,query):
        print(query)
        #Keep as many "elif" statemets based on your subject Eg: I have kept a dummy links for JAVA and mechanics classes link of MS Teams
        if("java" in query):
            self.talk('opening DSA class in teams')
            webbrowser.open("https://teams.microsoft.com/java")
        elif("mechanics" in query):
            self.talk('opening mechanics class in teams')
            webbrowser.open("https://teams.microsoft.com/mechanics")
        elif 'online classes' in query:
            self.talk('opening your microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')

    #Brower Search querys
    def B_S(self,query):
        print(query)
        try:
            # ('what is meant by' in self.query) or ('tell me about' in self.query) or ('who the heck is' in self.query)
            if ('wikipedia' in query):
                target1 = query.replace('search for','')
                target1 = target1.replace('in wikipedia','')
            elif('what is meant by' in query):
                target1 = query.replace("what is meant by"," ")
            elif('tell me about' in query):
                target1 = query.replace("tell me about"," ")
            elif('who the heck is' in query):
                target1 = query.replace("who the heck is"," ")
            print("searching....")
            info = wikipedia.summary(target1,5)
            print(info)
            self.talk("according to wikipedia "+info)
        except :
            self.No_result_found()
        
    #Browser
    def brows(self,query):
        print(query)
        if 'google' in query:
            self.talk("Boss, what should I search on google..")
            S = self.take_query()#taking query for what to search in google
            webbrowser.open(f"{S}")
        elif 'edge' in query:
            self.talk('opening your Miscrosoft edge')
            os.startfile('..\\..\\MicrosoftEdge.exe')#path for your edge browser application
        else :
            self.No_result_found()

    #google applications selection
    #if there is any wrong with the URL's replace them with your browsers URL's
    def Google_Apps(self,query):
        print(query)
        if 'gmail' in query:
            self.talk('opening your google gmail')
            webbrowser.open('https://mail.google.com/mail/')
        elif 'maps' in query:
            self.talk('opening google maps')
            webbrowser.open('https://www.google.co.in/maps/')
        elif 'news' in query:
            self.talk('opening google news')
            webbrowser.open('https://news.google.com/')
        elif 'calender' in query:
            self.talk('opening google calender')
            webbrowser.open('https://calendar.google.com/calendar/')
        elif 'photos' in query:
            self.talk('opening your google photos')
            webbrowser.open('https://photos.google.com/')
        elif 'documents' in query:
            self.talk('opening your google documents')
            webbrowser.open('https://docs.google.com/document/')
        elif 'spreadsheet' in query:
            self.talk('opening your google spreadsheet')
            webbrowser.open('https://docs.google.com/spreadsheets/')
        else :
            self.No_result_found()
            
    #youtube
    def yt(self,query):
        print(query)
        if 'play' in query:
            self.talk("Boss can you please say the name of the song")
            song = self.take_query()
            if "play" in song:
                song = song.replace("play","")
            self.talk('playing '+song)
            print(f'playing {song}')
            pywhatkit.playonyt(song)
            print('playing')
        elif "download" in query:
            self.talk("Boss please enter the youtube video link which you want to download")
            link = input("Enter the YOUTUBE video link: ")
            yt=YouTube(link)
            yt.streams.get_highest_resolution().download()
            self.talk(f"Boss downloaded {yt.title} from the link you given into the main folder")
        elif 'youtube' in query:
            self.talk('opening your youtube')
            webbrowser.open('https://www.youtube.com/')
        else :
            self.No_result_found()
        
    #Opensource accounts
    def open_source(self,query):
        print(query)
        if 'github' in query:
            self.talk('opening your github')
            webbrowser.open('https://github.com/BolisettySujith')
        elif 'gitlab' in query:
            self.talk('opening your gitlab')
            webbrowser.open('https://gitlab.com/-/profile')
        else :
            self.No_result_found()

    #Photo shops
    def edit(self,query):
        print(query)
        if 'slides' in query:
            self.talk('opening your google slides')
            webbrowser.open('https://docs.google.com/presentation/')
        elif 'canva' in query:
            self.talk('opening your canva')
            webbrowser.open('https://www.canva.com/')
        else :
            self.No_result_found()

    #OTT 
    def OTT(self,query):
        print(query)
        if 'hotstar' in query:
            self.talk('opening your disney plus hotstar')
            webbrowser.open('https://www.hotstar.com/in')
        elif 'prime' in query:
            self.talk('opening your amazon prime videos')
            webbrowser.open('https://www.primevideo.com/')
        elif 'netflix' in query:
            self.talk('opening Netflix videos')
            webbrowser.open('https://www.netflix.com/')
        else :
            self.No_result_found()

    #PC allications
    #NOTE: place the correct path for the applications from your PC there may be some path errors so please check the applications places
    #if you don't have any mentioned applications delete the codes for that
    #I have placed applications path based on my PC path check while using which OS you are using and change according to it
    def OpenApp(self,query):
        print(query)
        if ('calculator'in query) :
            self.talk('Opening calculator')
            os.startfile('C:\\Windows\\System32\\calc.exe')
        elif ('paint'in query) :
            self.talk('Opening msPaint')
            os.startfile('c:\\Windows\\System32\\mspaint.exe')
        elif ('notepad'in query) :
            self.talk('Opening notepad')
            os.startfile('c:\\Windows\\System32\\notepad.exe')
        elif ('discord'in query) :
            self.talk('Opening discord')
            os.startfile('..\\..\\Discord.exe')
        elif ('editor'in query) :
            self.talk('Opening your Visual studio code')
            os.startfile('..\\..\\Code.exe')
        elif ('online classes'in query) :
            self.talk('Opening your Microsoft teams')
            webbrowser.open('https://teams.microsoft.com/')
        elif ('spotify'in query) :
            self.talk('Opening spotify')
            os.startfile('..\\..\\Spotify.exe')
        elif ('lt spice'in query) :
            self.talk('Opening lt spice')
            os.startfile("..\\..\\XVIIx64.exe")
        elif ('steam'in query) :
            self.talk('Opening steam')
            os.startfile("..\\..\\steam.exe")
        elif ('media player'in query) :
            self.talk('Opening VLC media player')
            os.startfile("C:\Program Files\VideoLAN\VLC\vlc.exe")
        else :
            self.No_result_found()
            
    #closeapplications function
    def CloseApp(self,query):
        print(query)
        if ('calculator'in query) :
            self.talk("okay boss, closeing caliculator")
            os.system("taskkill /f /im calc.exe")
        elif ('paint'in query) :
            self.talk("okay boss, closeing mspaint")
            os.system("taskkill /f /im mspaint.exe")
        elif ('notepad'in query) :
            self.talk("okay boss, closeing notepad")
            os.system("taskkill /f /im notepad.exe")
        elif ('discord'in query) :
            self.talk("okay boss, closeing discord")
            os.system("taskkill /f /im Discord.exe")
        elif ('editor'in query) :
            self.talk("okay boss, closeing vs code")
            os.system("taskkill /f /im Code.exe")
        elif ('spotify'in query) :
            self.talk("okay boss, closeing spotify")
            os.system("taskkill /f /im Spotify.exe")
        elif ('lt spice'in query) :
            self.talk("okay boss, closeing lt spice")
            os.system("taskkill /f /im XVIIx64.exe")
        elif ('steam'in query) :
            self.talk("okay boss, closeing steam")
            os.system("taskkill /f /im steam.exe")
        elif ('media player'in query) :
            self.talk("okay boss, closeing media player")
            os.system("taskkill /f /im vlc.exe")
        else :
            self.No_result_found()

    #Shopping links
    def shopping(self,query):
        print(query)
        if 'flipkart' in query:
            self.talk('Opening flipkart online shopping website')
            webbrowser.open("https://www.flipkart.com/")
        elif 'amazon' in query:
            self.talk('Opening amazon online shopping website')
            webbrowser.open("https://www.amazon.in/")
        else :
            self.No_result_found()

    #PDF reader
    def pdf_reader(self):
        self.talk("Boss enter the name of the book which you want to read")
        n = input("Enter the book name: ")
        n = n.strip()+".pdf"
        book_n = open(n,'rb')
        pdfReader = PyPDF2.PdfFileReader(book_n)
        pages = pdfReader.numPages
        self.talk(f"Boss there are total of {pages} in this book")
        self.talk("plsase enter the page number Which I nedd to read")
        num = int(input("Enter the page number: "))
        page = pdfReader.getPage(num)
        text = page.extractText()
        print(text)
        self.talk(text)

    #Time caliculating algorithm
    def silenceTime(self,query):
        print(query)
        x=0
        #caliculating the given time to seconds from the speech commnd string
        if ('10' in query) or ('ten' in query):x=600
        elif '1' in query or ('one' in query):x=60
        elif '2' in query or ('two' in query):x=120
        elif '3' in query or ('three' in query):x=180
        elif '4' in query or ('four' in query):x=240
        elif '5' in query or ('five' in query):x=300
        elif '6' in query or ('six' in query):x=360
        elif '7' in query or ('seven' in query):x=420
        elif '8' in query or ('eight' in query):x=480
        elif '9' in query or ('nine' in query):x=540
        self.silence(x)
        
    #Silence
    def silence(self,k):
        t = k
        s = "Ok boss I will be silent for "+str(t/60)+" minutes"
        self.talk(s)
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        self.talk("Boss "+str(k/60)+" minutes over")

    #Mail verification
    def verifyMail(self):
        try:
            self.talk("what should I say?")
            content = self.take_query()
            self.talk("To whom do u want to send the email?")
            to = self.take_query()
            self.SendEmail(to,content)
            self.talk("Email has been sent to "+str(to))
        except Exception as e:
            print(e)
            self.talk("Sorry sir I am not not able to send this email")
    
    #Email Sender
    def SendEmail(self,to,content):
        print(content)
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login("YOUR_MAIL_ID","PASWORD")
        server.sendmail("YOUR_MAIL_ID",to,content)
        server.close()

    #location
    def locaiton(self):
        self.talk("Wait boss, let me check")
        try:
            IP_Address = get('https://api.ipify.org').text
            print(IP_Address)
            url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
            print(url)
            geo_reqeust = get(url)
            geo_data = geo_reqeust.json()
            city = geo_data['city']
            state = geo_data['region']
            country = geo_data['country']
            tZ = geo_data['timezone']
            longitude = geo_data['longitude']
            latidute = geo_data['latitude']
            org = geo_data['organization_name']
            print(city+" "+state+" "+country+" "+tZ+" "+longitude+" "+latidute+" "+org)
            self.talk(f"Boss i am not sure, but i think we are in {city} city of {state} state of {country} country")
            self.talk(f"and boss, we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
        except Exception as e:
            self.talk("Sorry boss, due to network issue i am not able to find where we are.")
            pass

    #Instagram profile
    def Instagram_Pro(self):
        self.talk("Boss please enter the user name of Instagram: ")
        name = input("Enter username here: ")
        webbrowser.open(f"www.instagram.com/{name}")
        time.sleep(5)
        self.talk("Boss would you like to download the profile picture of this account.")
        cond = self.take_query()
        if('download' in cond):
            mod = instaloader.Instaloader()
            mod.download_profile(name,profile_pic_only=True)
            self.talk("I am done boss, profile picture is saved in your main folder. ")
        else:
            pass

    #ScreenShot
    def scshot(self):
        self.talk("Boss, please tell me the name for this screenshot file")
        name = self.STT()
        self.talk("Please boss hold the screen for few seconds, I am taking screenshot")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        self.talk("I am done boss, the screenshot is saved in main folder.")

    #News
    def news(self):
        MAIN_URL_= "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=ec1b19a9e1644f6284dc1f83c4fdde90"
        MAIN_PAGE_ = get(MAIN_URL_).json()
        articles = MAIN_PAGE_["articles"]
        headings=[]
        seq = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth'] #If you need more than ten you can extend it in the list
        for ar in articles:
            headings.append(ar['title'])
        for i in range(len(seq)):
            print(f"todays {seq[i]} news is: {headings[i]}")
            self.talk(f"todays {seq[i]} news is: {headings[i]}")
        self.talk("Boss I am done, I have read most of the latest news")

    #System condition
    def condition(self):
        usage = str(psutil.cpu_percent())
        self.talk("CPU is at"+usage+" percentage")
        battray = psutil.sensors_battery()
        percentage = battray.percent
        self.talk(f"Boss our system have {percentage} percentage Battery")
        if percentage >=75:
            self.talk(f"Boss we could have enough charging to continue our work")
        elif percentage >=40 and percentage <=75:
            self.talk(f"Boss we should connect out system to charging point to charge our battery")
        elif percentage >=15 and percentage <=30:
            self.talk(f"Boss we don't have enough power to work, please connect to charging")
        else:
            self.talk(f"Boss we have very low power, please connect to charging otherwise the system will shutdown very soon")
        
    #no result found
    def No_result_found(self):
        self.talk('Boss I couldn\'t understand, could you please say it again.')        

# startExecution = MainThread()
# class Main(QMainWindow):
#     cpath =""
    
#     def __init__(self,path):
#         self.cpath = path
#         super().__init__()
#         self.ui = Ui_JarvisUI(path=current_path)
#         self.ui.setupUi(self)
#         self.ui.pushButton_4.clicked.connect(self.startTask)
#         self.ui.pushButton_3.clicked.connect(self.close)
    
#     #NOTE make sure to place a correct path where you are keeping this gifs
#     def startTask(self):
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ironman1.gif")
#         self.ui.label_2.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ringJar.gif")
#         self.ui.label_3.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\circle.gif")
#         self.ui.label_4.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\lines1.gif")
#         self.ui.label_7.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ironman3.gif")
#         self.ui.label_8.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\circle.gif")
#         self.ui.label_9.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\powersource.gif")
#         self.ui.label_12.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\powersource.gif")
#         self.ui.label_13.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ironman3_flipped.gif")
#         self.ui.label_16.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\Sujith.gif")
#         self.ui.label_17.setMovie(self.ui.movie)
#         self.ui.movie.start()
#         timer = QTimer(self)
#         timer.timeout.connect(self.showTime)
#         timer.start(1000)
#         startExecution.start()
    
#     def showTime(self):
#         current_time = QTime.currentTime()
#         current_date = QDate.currentDate()
#         label_time = current_time.toString('hh:mm:ss')
#         label_date = current_date.toString(Qt.ISODate)
#         self.ui.textBrowser.setText(label_date)
#         self.ui.textBrowser_2.setText(label_time)

# current_path = os.getcwd()
# app = QApplication(sys.argv)
# Jarvis = Main(path=current_path)
# Jarvis.show()
# exit(app.exec_())


FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"JarvisUi.ui"))

startExecution = MainThread()
class Main(QMainWindow):
    def __init__(self,path,parent=None):
        super(Main,self).__init__(parent)
    
        self.cpath = path
        super().__init__()
        self.ui = Ui_JarvisUI(path=current_path)
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.startTask)
        self.ui.pushButton_3.clicked.connect(self.close)
    
    #NOTE make sure to place a correct path where you are keeping this gifs
    def startTask(self):
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ironman1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ringJar.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\circle.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\lines1.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ironman3.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\circle.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\powersource.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\powersource.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\ironman3_flipped.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"D:\\Project\\New folder\\UI\\Sujith.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()
    
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


current_path = os.getcwd()
app = QtWidgets.QApplication(sys.argv)
main = Main(path=current_path)
main.show()
exit(app.exec_())