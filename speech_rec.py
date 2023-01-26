import speech_recognition as sr
\
#   Initializing the recognizer class
r = sr.Recognizer()

#   Using the laptop microphone as the source
#   listens to what is said and stores in 'audio_text' variable
with sr.Microphone() as source:
    print("Tell me your move")
    audio_text = r.listen(source)
    print("Got it, thanks")

#   This bit is exception handling
#   r (recognizer method) gives a request error when the API cannot be reached
try:
    # using google speech recognition
    print("Text: "+r.recognize_google(audio_text))
except:
    print("Sorry, could you repeat that?")
