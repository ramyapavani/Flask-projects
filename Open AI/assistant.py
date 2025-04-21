import openai
import speech_recognition as sr
import pyttsx3

# Set your OpenAI API key here (replace with your actual key)
openai.api_key = "your_api_key"

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
    except sr.RequestError:
        return "Could not request results, please check your internet connection."

def chatbot_response(prompt):
    """Get AI response from OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Main loop
while True:
    print("Say something (or type 'exit' to quit)...")
    user_input = listen()
    print("You:", user_input)

    if user_input.lower() == "exit":
        speak("Goodbye, Wela!")
        break

    response = chatbot_response(user_input)
    print("Bot:", response)
    speak(response)
