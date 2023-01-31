import speech_recognition as sr

class Mic:
    def __init__(self):
        #   Initializing the recognizer class
        self.r = sr.Recognizer()
        self.speech_input = ""

    def listen(self):
        #   Using the laptop microphone as the source
        #   listens to what is said and stores in 'audio_text' variable
        with sr.Microphone() as source:
            print("Tell me your move")
            audio_text = self.r.listen(source)
            print("Got it, thanks")

            #   This bit is exception handling
            #   r (recognizer method) gives a request error when the API cannot be reached
        try:
            # using google speech recognition
            self.speech_input = self.r.recognize_google(audio_text)
            # print("You said: " + speech_input)
            # p1, p2 = map(int, speech_input.split(","))
            return self.speech_input
        except ValueError:
            print("Invalid input format. Please enter two integers separated by a comma.")
            return None
        except:
            print("Sorry, could you repeat that?")
            return None