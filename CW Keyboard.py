import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
import rotaryio

# Przyciski do kropki i kreski
dot_button = DigitalInOut(board.GP28)
dot_button.direction = Direction.INPUT
dot_button.pull = Pull.UP

dash_button = DigitalInOut(board.GP29)
dash_button.direction = Direction.INPUT
dash_button.pull = Pull.UP

# Inicjalizacja klawiatury USB HID
keyboard = Keyboard(usb_hid.devices)

# Inicjalizacja enkodera
encoder = rotaryio.IncrementalEncoder(board.GP27, board.GP26)

# Alfabet Morse'a
morse_dict = {
    ".-": "a", "-...": "b", "-.-.": "c", "-..": "d", ".": "e", "..-.": "f",
    "--.": "g", "....": "h", "..": "i", ".---": "j", "-.-": "k", ".-..": "l",
    "--": "m", "-.": "n", "---": "o", ".--.": "p", "--.-": "q", ".-.": "r",
    "...": "s", "-": "t", "..-": "u", "...-": "v", ".--": "w", "-..-": "x",
    "-.--": "y", "--..": "z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6", "--...": "7",
    "---..": "8", "----.": "9", " ": " "
}

# Prędkość w WPM
min_wpm = 5
max_wpm = 50
wpm = 20  # Domyślna prędkość

# Obliczanie czasów w oparciu o WPM
def update_timings():
    global dot_duration, dash_duration, letter_space, word_space
    dot_duration = 1.2 / wpm  # Czas kropki
    dash_duration = dot_duration * 3  # Czas kreski
    letter_space = dot_duration * 3  # Czas odstępu między literami
    word_space = dot_duration * 7  # Czas odstępu między słowami
    print(f"Zaktualizowano czasy: WPM={wpm}, dot={dot_duration:.2f}, dash={dash_duration:.2f}")

update_timings()

# Wartości początkowe
signal = ""
last_signal_time = time.monotonic()
encoder_position = encoder.position
previous_encoder_position = encoder_position
letter_sent = False  # Czy litera została już wysłana
word_detected = False  # Czy wykryto koniec słowa

print("Program rozpoczął działanie...")

while True:
    current_time = time.monotonic()

    # Sprawdzanie przycisków
    if not dot_button.value:
        signal += "."
        print("Kropka")
        last_signal_time = current_time
        letter_sent = False  # Reset po nowym sygnale
        word_detected = False  # Reset wykrycia końca słowa
        time.sleep(dot_duration)

    elif not dash_button.value:
        signal += "-"
        print("Kreska")
        last_signal_time = current_time
        letter_sent = False  # Reset po nowym sygnale
        word_detected = False  # Reset wykrycia końca słowa
        time.sleep(dash_duration)

    # Sprawdzenie końca litery
    if signal and (current_time - last_signal_time > letter_space):
        if not letter_sent:
            if signal.strip() in morse_dict:
                letter = morse_dict[signal.strip()]
                print(f"Odebrano literę: {letter}")
                if letter.isalpha():
                    keyboard.press(ord(letter.lower()) - 93)  # Kod HID dla litery
                    keyboard.release_all()
                elif letter.isdigit():
                    digit_to_hid = {
                        "0": 0x27, "1": 0x1E, "2": 0x1F, "3": 0x20, "4": 0x21,
                        "5": 0x22, "6": 0x23, "7": 0x24, "8": 0x25, "9": 0x26
                    }
                    keyboard.press(digit_to_hid[letter])
                    keyboard.release_all()
            else:
                print(f"Nieznany kod: {signal.strip()}")
            signal = ""
            letter_sent = True  # Zablokuj ponowne wysyłanie litery

    # Sprawdzenie przerwy między słowami
    if not signal and (current_time - last_signal_time > word_space):
        if not word_detected:  # Wstaw spację tylko raz
            print("Dodajemy spację między słowami...")
            keyboard.press(0x2C)  # Kod HID dla spacji
            keyboard.release_all()
            word_detected = True  # Zablokuj kolejne spacje dla tej przerwy

    # Aktualizacja prędkości WPM przez enkoder
    encoder_position = encoder.position
    if encoder_position != previous_encoder_position:
        if encoder_position > previous_encoder_position:
            wpm = min(wpm + 1, max_wpm)
        else:
            wpm = max(wpm - 1, min_wpm)
        update_timings()
        previous_encoder_position = encoder_position

    time.sleep(0.01)
