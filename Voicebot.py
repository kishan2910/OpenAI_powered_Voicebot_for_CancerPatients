import re
import speech_recognition as sr
from datetime import datetime, time
import soundfile as sf
import openai
from gtts import gTTS
import playsound
from tempfile import NamedTemporaryFile

with open('./reportnum.text', 'r+') as file:
            content = file.read()
            global number
            number = int(content.strip())

def increment_number_in_file():
    
    try:
        with open('./reportnum.text', 'r+') as file:
            content = file.read()
            global number
            number = int(content.strip())
            incremented_number = number + 1
            file.seek(0)
            file.write(str(incremented_number))
            file.truncate()
        print("Number incremented in the file successfully.")
    except (IOError, ValueError):
        print("An error occurred while incrementing the number in the file.")


def save_string_to_file(content):
    global number
    file_path="./report"+str(number)+".txt"
    try:
        with open(file_path, 'a') as file:
            file.write(content)
        print("String saved to file successfully.")
    except IOError:
        print("An error occurred while saving the string to file.")

file_path = 'kala.text'
def clear_and_write(file_path, content):
    with open("./kala.text", 'w') as file:
        file.truncate(0)  # Clear the contents of the file
        file.write(content)  # Write new content

def append_sentence(file_path, sentence):
    with open("./kala.text", 'a') as file:
        file.write(sentence + '\n')             

openai.api_key = "XXXX" #change your OpenAI api information 
openai.organization = "XXXX"  #change your OpenAI api information 

word_set=["greetings", "How are You", "hi","hello"]
word_set_bye=["bye","See you", "takecare"]
word_set_func=["function","functions"]


def check(text,word_set):
    text = text.lower()
    
    pattern = r'[^\w\s]'
    text = re.sub(pattern, '', text)
    found=False
    print("Inside :",text)
    words = text.split()
    for word in word_set:
        if word in words:
            found=True
            return True
    return found

interacting=False
import datetime


greetingtext=" Hello ,  How may i help you ?"
byetext="It was nice talking to you ,I hope I was not too robotic for you!. Looking forward to meet you again."
functiontext="My functions include answering your questions."

text="What is  love ?"



def response(text):
    response = openai.Completion.create(
  model="text-davinci-003",
  prompt=f"Friend is a chatbot that provides helpful responses to questions:\n\nYou: How can I cope with the emotional challenges of being a cancer patient?\nFriend: It's completely understandable to feel overwhelmed emotionally as a cancer patient. One effective strategy is to seek support from a qualified therapist or counselor who specializes in helping individuals with cancer. They can provide you with valuable coping mechanisms and emotional support tailored to your specific needs.\nYou: What are some practical tips for managing the side effects of chemotherapy?\nFriend: Managing the side effects of chemotherapy can be challenging, but there are several things you can do to alleviate discomfort. Staying hydrated, maintaining a balanced diet, and getting plenty of rest can help your body cope better. It's also important to communicate any side effects you're experiencing to your healthcare team so they can provide appropriate interventions or adjustments to your treatment plan.\nYou: How can I find support groups for cancer patients?\nFriend: Connecting with others who are going through similar experiences can be incredibly valuable. You can start by reaching out to your healthcare provider or local cancer treatment centers to inquire about support groups in your area. There are also online communities and forums dedicated to cancer support where you can find a network of individuals who can relate to your journey.\nYou: What are some strategies for dealing with the fear of cancer recurrence?\nFriend: The fear of cancer recurrence is a common concern among cancer survivors. Engaging in self-care activities such as meditation, deep breathing exercises, or practicing mindfulness can help alleviate anxiety. It's also important to maintain regular follow-up appointments with your healthcare team and discuss any concerns you have. Remember, you are not alone, and seeking support from loved ones or joining survivorship programs can provide a sense of community and reassurance.\nYou: {text}\nFriend:",
  temperature=0.5,
  max_tokens=75,
  top_p=0.3,
  frequency_penalty=0.5,
  presence_penalty=0.0
)
    return response['choices'][0]['text']




recognizer = sr.Recognizer()
   
   
def speak(message):
    #print(message)
    tts = gTTS(message)
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    tts.save(filename)
    append_sentence(file_path, " \n RoboDoctor:"+message)
    playsound.playsound(filename)
    

        
mic = sr.Microphone()


mic = sr.Microphone()
r = sr.Recognizer()
r.energy_threshold = 400
r.pause_threshold=1.2
# Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
r.dynamic_energy_threshold = False
increment_number_in_file()
speak("I am on, you can speak now ")
while True:
    with mic as source:
        print("recording ....")
        r.adjust_for_ambient_noise(source,duration=0.25)
        try:
            audio = r.listen(source,phrase_time_limit=6)
            text = recognizer.recognize_google(audio)
            
            print("recorded")
        except sr.UnknownValueError:
            # speak("how can i help you ?")
            continue
    
  
    
    print(text)
    clear_and_write(file_path, " Patient:"+text+"\n ")
    
    
    if text == 'Thanks for watching!' or text == 'Thank you.'or text == '.' or text=="" or text==" " or text =="Thanks.":
        print("no recording.......")
        continue
    
    if check(text,word_set):
        interacting=True
        print("Check returend true",text)

        speak(greetingtext)
        continue
    if check(text,word_set_bye) and interacting:
    
        print("Check returend true",text)

        speak(byetext)
        interacting=False
        continue
    if check(text,word_set_func) and interacting:
    
        print("Check returend true",text)

        speak(functiontext)
        interacting=True
        continue
    
    if interacting==False:
        continue


    print("patient: ",text)
    user="\n Patient :"+text+"\n"
    save_string_to_file(user)
    print("getting Response ")
    res=response(text)
    res=res.replace(","," .  ")
    print("Response: "+res)
    robot=" \n Robo Doctor:"+res+"\n"
    save_string_to_file(robot)
    speak(res)

    print("spoken")

    
