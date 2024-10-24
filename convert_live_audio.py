import speech_recognition as sr
import json
from datetime import datetime
import os

# The Recognizer is initialized.
UserVoiceRecognizer = sr.Recognizer()

# Optionally, ask for the preferred language
language_code = input("Enter the language code (e.g., 'en-US' for English, 'pt-BR' for Brazilian Portuguese): ")

# File to save recognized entries
json_file_path = 'recognized_texts.json'

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

while True:
    all_recognized_texts = []  # Reset for each session
    keyword_detected = False  # Flag for keyword detection

    try:
        with sr.Microphone() as UserVoiceInputSource:
            UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)

            print("Listening...")
            while True:  # Loop to continue listening until a KeyboardInterrupt occurs
                UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)

                # Recognize speech using the specified language
                try:
                    UserVoiceInput_converted_to_Text = UserVoiceRecognizer.recognize_google(UserVoiceInput, language=language_code)
                    UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.lower()
                    print("Recognized Text:", UserVoiceInput_converted_to_Text)

                    # Append the recognized text to the all_recognized_texts list
                    all_recognized_texts.append(UserVoiceInput_converted_to_Text)

                    # Check for keywords ("água" and "esgoto")
                    if "agua" in UserVoiceInput_converted_to_Text or "água" in UserVoiceInput_converted_to_Text or "esgoto" in UserVoiceInput_converted_to_Text:
                        print("Keyword detected.")
                        keyword_detected = True  # Set flag to indicate a keyword was detected
                        # Note: Do not break here; continue to listen

                except sr.UnknownValueError:
                    print("No User Voice detected OR unintelligible noises detected OR the recognized audio cannot be matched to text !!!")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

    except KeyboardInterrupt:
        # If we reached here, it means the user interrupted the session
        if keyword_detected:
            print('A KeyboardInterrupt encountered; Saving all recognized texts because a keyword was detected!')

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
            print("Session data saved to recognized_texts.json.")

        else:
            print("No keywords detected; no data saved.")

        exit(0)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
