import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

# Convert text to speech
text = "Hello, I'm using pyttsx3 in Python 3 to generate speech."
engine.say(text)
engine.runAndWait()
