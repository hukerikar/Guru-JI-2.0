import random
from difflib import SequenceMatcher
import speech_recognition as sr
import pyttsx3
import streamlit as st

# Initialize pyttsx3

# Define the questions and answers in dictionary format
questions_and_answers = {
    "What is Difference between analog and digital signals? ": {
        "Answer": "Analog signals are continuous signals that vary smoothly over time, while digital signals are discrete signals that have specific, distinct values at each point in time.\nExample of analog signal: The sound produced by a human voice.\nExample of digital signal: Binary data transmitted over a computer network."
    },
    "Explain Designing a basic electronic circuit to amplify a signal": {
        "Answer": "A basic electronic circuit to amplify a signal typically involves using a transistor or an operational amplifier (op-amp) in combination with resistors and capacitors.\nThe transistor or op-amp amplifies the input signal, and the resistors and capacitors are used to set the gain and frequency response of the amplifier."
    },
    "What is Purpose of modulation in telecommunications and difference between AM and FM modulation": {
        "Answer": "Modulation is the process of encoding information onto a carrier signal for transmission.\nAM (Amplitude Modulation) changes the amplitude of the carrier signal to encode information, while FM (Frequency Modulation) changes the frequency of the carrier signal.\nAM modulation is more susceptible to noise but has a simpler demodulation process, while FM modulation is less susceptible to noise but requires more bandwidth."
    },
    "What are Operation of common electronic components (resistors, capacitors, transistors)": {
        "Answer": "Resistors: Resistors limit the flow of electric current and are commonly used to control voltage and current levels in electronic circuits.\nCapacitors: Capacitors store electric charge and are used to filter signals, smooth voltage fluctuations, and block DC signals while allowing AC signals to pass.\nTransistors: Transistors are semiconductor devices used as amplifiers, switches, and signal modulators in electronic circuits. They control the flow of current between two terminals based on the voltage applied to a third terminal."
    },
    "What is Nyquist theorem and its relation to sampling in digital signal processing ?": {
        "Answer": "The Nyquist theorem states that to accurately reconstruct a continuous signal from its samples, the sampling frequency must be at least twice the highest frequency component of the signal.\nIn digital signal processing, Nyquist theorem ensures that the sampling rate is sufficient to capture all frequency components of the analog signal without aliasing."
    },
    "Explain Calculation of bandwidth of a communication system and its importance": {
        "Answer": "The bandwidth of a communication system is the range of frequencies over which the system can transmit signals.\nBandwidth is typically calculated as the difference between the highest and lowest frequencies in the signal.\nBandwidth is important because it determines the data transmission rate and the amount of information that can be transmitted over the communication channel."
    },
    "Explain Concept of feedback in electronic circuits and its significance in amplifier design": {
        "Answer": "Feedback is the process of routing a portion of the output signal of an amplifier back to its input.\nFeedback helps stabilize the amplifier's gain, improve frequency response, reduce distortion, and increase bandwidth.\nThere are two types of feedback: positive feedback, which increases the gain, and negative feedback, which reduces the gain."
    },
    "What are Types of filters used in signal processing and their frequency response differences ?": {
        "Answer": "Common types of filters include low-pass, high-pass, band-pass, and band-stop filters.\nLow-pass filters allow frequencies below a certain cutoff frequency to pass through and attenuate higher frequencies.\nHigh-pass filters allow frequencies above a certain cutoff frequency to pass through and attenuate lower frequencies.\nBand-pass filters allow a specific range of frequencies to pass through and attenuate frequencies outside that range.\nBand-stop filters (also known as notch filters) attenuate a specific range of frequencies while allowing frequencies outside that range to pass through."
    },
    "Explain Troubleshooting common problems in electronic circuits (short circuits or open circuits)": {
        "Answer": "To troubleshoot a short circuit, identify and isolate the shorted component or connection and repair or replace it.\nTo troubleshoot an open circuit, check for broken or disconnected wires or components and repair or replace them."
    },
    "What are Principles behind wireless communication technologies such as Wi-Fi and Bluetooth and how they operate ?": {
        "Answer": "Wi-Fi and Bluetooth are both wireless communication technologies that use radio waves to transmit data over short distances.\nWi-Fi operates in the 2.4 GHz and 5 GHz frequency bands and is designed for high-speed data transmission over longer distances.\nBluetooth operates in the 2.4 GHz frequency band and is designed for short-range communication between devices such as smartphones, headphones, and smart speakers.\nBoth Wi-Fi and Bluetooth use modulation techniques to encode data onto radio waves and employ protocols for establishing connections, managing data transmission, and ensuring security."
    }
}

# Function to listen to speech and save text
def listen_and_save_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            st.write("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            st.write("You said:", text)
            return text
        except sr.UnknownValueError:
            st.write("Sorry, could not understand audio.")
            return ""
        except sr.RequestError as e:
            st.write("Error:", e)
            return ""

# Function to speak the question
def speak_question(question):
    st.write(question)
    engine = pyttsx3.init()
    engine.say(question)
    engine.runAndWait()
    engine = None
def calculate_similarity_score(expected_answer, user_answer):
    return SequenceMatcher(None, expected_answer, user_answer).ratio() * 100

# Get user's answer using speech recognition
def main():
    st.title("Interview App")

    # Start interview button
    if st.button("Start Interview"):
        st.write("Welcome to the interview!")

        # Randomly select a question
        random_question = random.choice(list(questions_and_answers.keys()))

        # Speak the randomly selected question
        speak_question(random_question)
        st.write("Question:", random_question)
        # Get the expected answer for the selected question
        expected_answer = questions_and_answers[random_question]["Answer"]
        # Get user's answer using speech recognition
        user_answer = listen_and_save_text()
        # Stop interview button
        st.write("Interview stopped.")
        # Calculate similarity score between user's answer and expected answer
        similarity_score = calculate_similarity_score(expected_answer, user_answer)
        # Display the similarity score
        st.write("Similarity Score:", round(similarity_score, 2), "%")


if __name__ == "__main__":
    main()
