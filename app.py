import streamlit as st
import speech_recognition as sr
from happytransformer import HappyTextToText, TTSettings
global change_count
change_count = 0

def listen_and_save_text():
    global change_count
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

def grammar_checker(file_path):
    global change_count

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

    error_count = corrected_text.count("ERROR")

    corrected_file_path = "corrected_text.txt"

    if error_count > 0:
        save_text_to_file(corrected_text, corrected_file_path)
        st.write("Corrected Text:")
        st.write(corrected_text)
        st.write("Number of grammatical errors:", error_count)
    else:
        st.write("No grammatical errors found.")
        st.write("Number of grammatical errors:", error_count)

    return corrected_text
def count_changes(original_file_path, corrected_file_path):
    global change_count

    with open(original_file_path, 'r') as file:
        original_text = file.read().split()

    with open(corrected_file_path, 'r') as file:
        corrected_text = file.read().split()
    total_words = len(corrected_text)
    st.write(f"Total number of words: {total_words}")

    special_characters = ['?', '.', '!', ',', ';']

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

    if change_count > 0:
        with open("error.txt", "w") as error_file:
            error_file.write(f"{change_count}")
        return change_count
    else:
        st.write("No changes found.")
        return 0

def main():
    st.title("HR Interview")

    if st.button("Start Interview"):
        st.title("Why should we hire you for our company")
        listen_and_save_text()
        filename = "speech_output.txt"
        grammar_checker(filename)
        original_file_path = "speech_output.txt"
        corrected_file_path = "corrected_text.txt"
        count_changes(original_file_path, corrected_file_path)

if __name__ == '__main__':
    main()
