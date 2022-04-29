import requests
import speech_recognition as sr
import subprocess
from gtts import gTTS

#sender = input("What's your name?\n")

bot_message = ""
message = ""

while bot_message != "Bye!" or bot_message != "Thanks":

    r = sr.Recognizer()
    with sr.Microphone(sample_rate=16000) as source:
        print("Speak anything...\n")
        audio = r.listen(source)
        try:
            message = r.recognize_google(audio)
            print("You said: {}".format(message))
        except:
            print("Sorry, I could not recognize your voice")
    if len(message) == 0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})
    
    print("Bot says, ")
    #print(r.text)
    for i in r.json():
        bot_message = i['text']
        print(bot_message)
        if "buttons" in i:
            for j in i['buttons']:
                print(j['title'])

    myobj = gTTS(text=bot_message)
    myobj.save("welcome.mp3")
    print("saved")
    subprocess.call(['mpg321', "welcome.mp3", '--play-and-exit'])
