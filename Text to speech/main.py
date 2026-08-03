from gtts import gTTS

text = "Welcome! This is a simple text-to-speech demonstration. If you can hear this clearly, the application is working correctly."

tts = gTTS(text=text, lang='en')

tts.save("voice.mp3")

print("Audio file 'voice.mp3' has been generated successfully.")
