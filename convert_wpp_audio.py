import speech_recognition as sr
import json
from datetime import datetime
import os
from pydub import AudioSegment

# Initialize Recognizer
UserVoiceRecognizer = sr.Recognizer()

# Optionally, ask for the preferred language
language_code = input("Enter the language code (e.g., 'en-US' for English, 'pt-BR' for Brazilian Portuguese): ")

# File to save recognized entries
json_file_path = 'recognized_texts_wpp.json'

# Ensure the JSON file exists; if not, create an empty one
if not os.path.exists(json_file_path):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump([], json_file)

# Load existing recognized entries from the JSON file with error handling
try:
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        recognized_entries = json.load(json_file)
except (json.JSONDecodeError, FileNotFoundError):
    # If the file is empty or not found, start with an empty list
    recognized_entries = []

# Folder path where the m4a files are stored
audio_folder_path = './audios'

# Function to process audio files
def process_m4a_file(m4a_file_path):
    all_recognized_texts = []  # Reset for each session
    keyword_detected = False  # Flag for keyword detection

    # Convert M4A to WAV using pydub
    try:
        audio = AudioSegment.from_file(m4a_file_path, format="m4a")
        wav_file_path = "temp_audio.wav"
        audio.export(wav_file_path, format="wav")
    except Exception as e:
        print(f"Error converting M4A to WAV: {e}")
        return

    try:
        with sr.AudioFile(wav_file_path) as source:
            audio_data = UserVoiceRecognizer.record(source)

            # Recognize speech using Google API
            try:
                recognized_text = UserVoiceRecognizer.recognize_google(audio_data, language=language_code)
                recognized_text = recognized_text.lower()
                print("Recognized Text:", recognized_text)

                # Append recognized text to the list
                all_recognized_texts.append(recognized_text)

                # Check for keywords ("água" and "esgoto")
                if "agua" in recognized_text or "água" in recognized_text or "esgoto" in recognized_text:
                    print("Keyword detected.")
                    keyword_detected = True

            except sr.UnknownValueError:
                print("Audio is unintelligible or no voice detected.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    except Exception as e:
        print(f"Error processing audio file: {e}")

    # If a keyword is detected, save the session
    if keyword_detected:
        print('Keyword detected; saving recognized texts.')

        # Create an entry with recognized texts and timestamp
        final_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recognized_texts": all_recognized_texts  # Save all recognized texts in one session
        }

        # Append the new entry to recognized_entries
        recognized_entries.append(final_entry)

        # Save the updated recognized entries to the JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(recognized_entries, json_file, ensure_ascii=False, indent=4)
        print(f"Session data saved to {json_file_path}.")

# Get the list of all m4a files from the /audios folder
m4a_files = [f for f in os.listdir(audio_folder_path) if f.endswith('.m4a')]

# Process each M4A file in the folder
for m4a_file in m4a_files:
    file_path = os.path.join(audio_folder_path, m4a_file)
    print(f"Processing file: {file_path}")
    process_m4a_file(file_path)

print("All files processed.")
