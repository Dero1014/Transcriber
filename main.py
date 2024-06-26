import speech_recognition as sr
import sounddevice as sd
import wavio

# Recording settings 
fs = 44100  # Sample rate
seconds = int(input("Quote in seconds length: "))  # Duration of recording

# Speech recognizer setting
r = sr.Recognizer()

# File Setting
quotes = open("Quotes.txt", "w", buffering=1, encoding="utf-8")
counter = 0

try: 
    while True:

        # Recording
        print("Recording!")
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        wavio.write("output.wav", myrecording, fs ,sampwidth=2)

        # Transcribe
        with sr.AudioFile('output.wav') as source:
            audio = r.listen(source)
        print("Quote: ")
        try:
            quoteEN = r.recognize_google(audio, language="en-US")
            print("In English: " + quoteEN)
        except sr.UnknownValueError:
            print("Unrecognizable in English")
            quoteEN = 0
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        try:

            quoteHR = r.recognize_google(audio, language="hr-HR")
            print("In Croatian: " + quoteHR)
        except sr.UnknownValueError:
            print("Unrecognizable in Croatian")
            quoteHR = 0
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        # Save to text file
        if quoteHR != 0 or quoteEN != 0: 
            quotes.write(str(counter) + ": " + str(quoteEN) + " | " + str(quoteHR) + "\n")
            counter = counter + 1
        print("------------------------------------")

except KeyboardInterrupt:
    quotes.close()
    print("Text saved in file Quotes.txt")