import pandas as pd
import numpy as np
import sounddevice as sd
import time


"""This simple program converts text to morse codes and vice versa
It can read from a file , could also take a manual input
It plays the sound of the morse code if you choose to"""


# --------------------------Generates sound for morse elements-------------------------------------#
def play_sound(frequency, duration, samplerate):
    t = np.linspace(0, duration, int(samplerate * duration), False)
    sound = 0.5 * np.sin(2 * np.pi * frequency * t)

    sd.play(sound, samplerate)
    sd.wait()


def play_dot():
    frequency = 1000
    duration = 0.1
    samplerate = 44100
    play_sound(frequency, duration, samplerate)


def play_dash():
    frequency = 1000
    duration = 0.3
    samplerate = 44100
    play_sound(frequency, duration, samplerate)


# ----------------------------FETCHING TABLE DATA FROM WEBSITE TO GET MORSE CODE REFERENCE------------------------#


# url = input("Enter website:  ")
#
# r = requests.get(url)
# print(r)
# df_list = pd.read_html(r.text)
# df_sliced_list = df_list[:4]
# print(df_sliced_list)
#
# for lst in df_sliced_list:
#     print(lst.columns)
#     df = pd.DataFrame(lst)
#     df.to_csv("morse_code_reference", index=False, mode='a')


# -------------------------------------MISCELLANEOUS FUNCTIONS -------------------------------------------- #

#  Choose how you want to read your text or morse code and get the target text to convert
def get_target():
    input_mode = input("Enter input mode (Type 1 for manual, 2 for file.): ")
    while input_mode not in ['1', '2']:
        input_mode = input("Invalid input. Please enter input mode again (1. manual, 2. file): ")
    if input_mode == "1":
        print(
            "Use / as words seperator and space as element seperator for morse codes e.g -- -.-- / -... --- -.-- representing 'my boy'")
        target = input("Enter a Text or Morse Code: ")
    elif input_mode == "2":
        file = input("Enter the file name: ")
        try:
            with open(file, "r") as target:
                target = target.read()
        except FileNotFoundError:
            print(f"Error: {file} not found.")
            get_target()
    return target


# Represent the welcome message as an ASCII Art
def draw_text_to_morse(action):
    print(" ____________ ____________")
    print("|  ________  |  ________  |")
    print("| |        | | |        | |")
    print("| | Welcome | | Enter any |")
    if action == "1":
        print("| |  to     | |  text     |")
        print("| | Text    | | you want  |")
        print("| |  to     | |   to      |")
        print("| | Morse   | | convert   |")
    elif action == "2":
        print("| |  to     | |   morse   |")
        print("| | Morse   | | you want  |")
        print("| |  to     | |     to    |")
        print("| | Text    | |  convert  |")
    print("| | Conver- | |           |")
    print("| | ter     | |           |")
    print("|____________|____________|")


# -------------------------------------TEXT TO MORSE CONVERTER & MORSE TO TEXT CONVERTER-----------------------------#


def text_to_morse_converter(reference_dict, morse_sound_dict, text):
    morse_code = ""
    for ch in text:
        if ch.isalpha():
            ch = ch.upper()
        elif ch == " ":
            morse_code += '/ '  # Separate words with /
            continue
        morse_code += reference_dict.get(ch, "") + " "
    print(morse_code)

    # Sound
    if input("Do you want to play the morse code?(type 'yes' or 'no'): ") == "yes":
        for elem in morse_code.replace(" ", ""):  # replaces spaces with null to avoid key error
            if elem == "/":
                time.sleep(1)  # sleep for 1 seconds before another word
                continue
            elif elem in [".", "-"]:
                morse_sound_dict[elem]()


def morse_to_text_converter(reference_dict, morse_sound_dict, morse_code):
    text = ""
    for words in morse_code.split("/"):
        for elem in words.split():
            text += reference_dict.get(elem, "")
        text += " "
        time.sleep(1)
    print(text)

    # Sound
    if text.replace(" ", ""):  # Checks if there the morse_code produced a valid text
        if input("Do you want to play the morse code?(type 'yes' or 'no'): ") == "yes":
            for elem in morse_code.replace(" ", ""):  # replaces spaces with null to avoid key error
                if elem == "/":
                    time.sleep(1)  # sleep for 1 seconds before another word
                    continue
                elif elem in [".", "-"]:
                    morse_sound_dict[elem]()
    else:
        print("No Valid Morse Code was given!")


# -------------------------------------     START    -------------------------------------------------------#
try:
    reference = pd.read_csv("morse_code_reference")
    reference = reference.to_dict(orient="records")
    choice = input("Type 1 for Text to Morse Converter , Type 2 for Morse to Text Converter: ")
    if choice == "1":
        references = {record["Character"]: record["Morse"] for record in reference}
        morse_sounds = {".": play_dot, "-": play_dash}
        draw_text_to_morse(choice)
        text_to_morse_converter(references, morse_sounds, get_target())
    elif choice == "2":
        references = {record["Morse"]: record["Character"] for record in reference}
        print(references)
        morse_sounds = {".": play_dot, "-": play_dash}
        draw_text_to_morse(choice)
        morse_to_text_converter(references, morse_sounds, get_target())
except Exception as e:
    print(f"An error occurred:  {e}")
