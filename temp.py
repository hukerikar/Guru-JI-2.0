import streamlit as st
import speech_recognition as sr
from happytransformer import HappyTextToText, TTSettings
import pyttsx3

# Initialize pyttsx3
engine = pyttsx3.init()
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
            filename = "speech_output.txt"
            with open(filename, "w") as file:
                file.write(text)
            st.write("Speech saved to", filename)

        except sr.UnknownValueError:
            st.write("Sorry, could not understand audio.")
        except sr.RequestError as e:
            st.write("Error:", e)

# Function to perform grammar correction
def grammar_checker(file_path):
    def read_text_from_file(file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text

    def save_text_to_file(text, filename):
        with open(filename, "w") as file:
            file.write(text)
        st.write("Corrected text saved to", filename)

    happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
    args = TTSettings(num_beams=5, min_length=1)
    input_text = read_text_from_file(file_path)

    corrected_text = happy_tt.generate_text("grammar: " + input_text, args=args).text
    # engine.say(corrected_text)
    # engine.runAndWait()
    error_count = corrected_text.count("ERROR")

    corrected_file_path = "corrected_text.txt"
    save_text_to_file(corrected_text, corrected_file_path)

    st.write("Corrected Text:")
    st.write(corrected_text)
    return corrected_text

# Function to count changes between original and corrected text
def count_changes(original_file_path, corrected_file_path):
    with open(original_file_path, 'r') as file:
        original_text = file.read().split()
    with open(corrected_file_path, 'r') as file:
        corrected_text = file.read().split()
    total_words = len(corrected_text)
    special_characters = ['?', '.', '!', ',', ';']
    change_count = 0
    change_details = []  
    for original_word, corrected_word in zip(original_text, corrected_text):
        if original_word in special_characters or corrected_word in special_characters:
            continue
        original_word_lower = original_word.lower()
        corrected_word_lower = corrected_word.lower()
        if original_word_lower == corrected_word_lower:
            continue
        change_count += 1
        change_details.append(f"Change identified: Original '{original_word}' -> Corrected '{corrected_word}'")
    with open("error.txt", "w") as error_file:
        error_file.write(f"{change_count}")
    st.write(change_details)
    return change_count

# Streamlit UI
def main():
    st.title("Speech-to-Text and Grammar Correction")
    st.write("This app listens to your speech, saves it to a file, performs grammar correction, and counts changes.")

    if st.button("Start Speech Recognition"):
        listen_and_save_text()

    file_path = "speech_output.txt"
    corrected_text = grammar_checker(file_path)

    original_file_path = "speech_output.txt"
    corrected_file_path = "corrected_text.txt"
  
    num_changes = count_changes(original_file_path, corrected_file_path)
    st.write("Total Grammatical Error :", num_changes)

if __name__ == "__main__":
    main()
