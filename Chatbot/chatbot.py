import json
import difflib
import sys, string, os, re, win32api
from difflib import get_close_matches
import time
from datetime import datetime as dt
#data=json.load(open('chat.json'))
app=json.load(open('app.json'))
import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")
def store(key,value):
    with open('chat.json','rb+') as file:
        file.seek(-2,2)
        file.write(",\"".encode("utf-8")+key+"\":[\"".encode("utf-8")+value+"\"]}\n".encode("utf-8"))
        file.close()

def appstore(key,value):
    with open('app.json','rb+') as file:
        file.seek(-2,2)
        file.write(",\"".encode("utf-8")+key+"\":[\"\\".encode("utf-8")+"\"".encode("utf-8"))
        for x in value.decode("utf-8"):
            if x=="\\":
                #print(x.unicode("utf-8"))
                file.write("\\".encode("utf-8"))
            file.write(x.encode("utf-8"))
        file.write("\\".encode("utf-8")+"\"\"]}\n".encode("utf-8"))
        file.close()

def find_file(word,root_folder, rex):
    beg=dt.now().second
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            end=dt.now().second
            if end-beg >= 10:
                print("Max: file not found")
                speak.Speak('file not found')
                return
            result = rex.search(f)
            if result:
                appstore(word.encode('utf-8'),os.path.join(root,f).encode('utf-8'))
                print (os.path.join(root, f))
                return
                    # if you want to find only one

def find_file_in_all_drives(word,file_name):
    #create a regular expression for the file
    rex = re.compile(file_name)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        find_file(word,drive, rex )
#find_file_in_all_drives("open chatbot","chatbot.py" )

def name(n,s):
    p=0
    k=0
    cn=""
    for x in n:
        if p==s:
            cn=cn+x
            k=k+1
        if x==" ":
            p=p+1

    return (cn)



print("\nHi! I am Max.. Why don't you tell me your name?")
speak.Speak("Hi! I am Max.. Why don't you tell me your name?")
while True:
    user=input("\nUser: ")
    if user != "":
        break
#user=input("User: ")
w=0
for x in user:
    if x== " ":
        w=w+1
if w ==0:
    print("\nMax: Nice to meet you "+user)
    speak.Speak("\nNice to meet you "+user)
else:
    user=name(user,w)
    print("\nMax: Nice to meet you "+user)
    speak.Speak("\nNice to meet you"+user)

a=[]
i=0
while True:
    with open("app.json") as appdata:
        app=json.load(appdata)
    with open("chat.json") as chatdata:
        data=json.load(chatdata)
    j=0
    while True:
        word=input("\n"+user+": ")
        if word != "":
            break
    wordl=word.lower()

    if wordl=="bye" or wordl=="exit":
        print("\nMax: Good Bye :)")
        speak.Speak("Good Bye")
        exit()

    if len(get_close_matches(wordl,data.keys())) > 0:
        w=get_close_matches(wordl,data.keys())[0]
    else:
        w=wordl


    if "open" in w:
        if w not in app:
            z=0
            for x in w:
                if x== " ":
                    z=z+1
            ap=name(w,z)
            find_file_in_all_drives(w,ap)
            appdata.close()
        app=json.load(open('app.json'))
        if w in app:
            print("\nMax: Opening...")
            speak.Speak("Opening")
        #os.chdir(app[w][0])
            os.system(app[w][0])
    elif w not in data and w not in app:
        wordb=w.encode('utf-8')
        print("\nMax: Help me to learn!\nWhat would you say if I have said it?\n")
        speak.Speak("Help me to learn!\nWhat would you say if I have said it?")
        value=input("\n"+user+": ")
        valueb=value.encode('utf-8')
        store(wordb,valueb)
        print("\nMax: Thanks for helping! I am a good learner.")
        speak.Speak("Thanks for helping! I am a good learner.")


    else:
        for z in a:
            if w in a:
                j=j+1
        try:
            print('\nMax: '+data[w][j])
            speak.Speak(data[w][j])
        except IndexError:
            j=0
            print('\nMax: '+data[w][j])
            speak.Speak(data[w][j])
        a.append(w)
        a[i]=w
        i=i+1
    chatdata.close()
