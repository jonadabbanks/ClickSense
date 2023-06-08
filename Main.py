from pynput import mouse, keyboard
import pygetwindow as gw
from datetime import datetime
import sys
import shutil
import os
import subprocess
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QRect
import win32gui
from PyQt5.QtGui import QPixmap



previous_window_name = ""
start_time = datetime.now()  # Initialize start_time with current time

def format_duration(duration):
    if duration < 60:
        return "{:.2f} seconds".format(duration)
    elif duration < 3600:
        minutes = duration // 60
        seconds = duration % 60
        return "{:.0f} minutes {:.2f} seconds".format(minutes, seconds)
    else:
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = (duration % 3600) % 60
        return "{:.0f} hours {:.0f} minutes {:.2f} seconds".format(hours, minutes, seconds)


def get_window_name():
    hwnd = win32gui.GetForegroundWindow()
    window_name = win32gui.GetWindowText(hwnd)
    return window_name





def get_element_name(x, y):
    element = gw.getWindowsAt(x, y)
    if element:
        return element[0].title
    return None





def on_click(x, y, button, pressed):
    global previous_window_name, start_time

    if pressed:
        window_name = get_window_name()
        current_time = datetime.now()

        if window_name != previous_window_name:
            if previous_window_name:
                duration = (current_time - start_time).total_seconds()
                timestamp = current_time.strftime("%Y-%m-%d %I:%M:%S %p")
                formatted_duration = format_duration(duration)
                click_info = 'Window: {0}\nTime: {1}\nTotal Time Spent: {2}\n\n'.format(previous_window_name, timestamp, formatted_duration)
                with open("clicks.txt", "a", encoding="utf-8") as file:
                    file.write(click_info)

            start_time = current_time
            previous_window_name = window_name


def on_press(key):
    global listener, app, window, label
    if key == keyboard.Key.f7:
        if listener is None:
            # Start the listener
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            window.setStyleSheet("background-color: #c3e6cb;")  # Set border-radius to add rounded corners
            
            label.setText("Recording is active")
            print("Listener started.")
            window.show()  # Show the window when F7 key is pressed

            time.sleep(5)  # Pause execution for 5 seconds

            window.close()  # Close the window after 5 seconds
        else:
            # Stop the listener
            listener.stop()
            listener = None
            window.setStyleSheet("background-color: #deb0b1")
            label.setText("Recording is inactive")
            print("Listener stopped.")
            window.show()  # Show the window when F1 key is pressed

            time.sleep(5)  # Pause execution for 5 seconds

            window.close()  # Close the window after 5 seconds

    elif key == keyboard.Key.f8:
        try:
            # Copy the file to the user's document folder
            shutil.copy2("clicks.txt", os.path.expanduser("~\\Documents\\clicks.txt"))
            # Open the copied file with Notepad
            subprocess.Popen(["notepad.exe", os.path.expanduser("~\\Documents\\clicks.txt")])
        except Exception as e:
            print("An error occurred while copying or opening the file:", str(e))
    # Initialize the listener variable
listener = None

# Create the PyQt5 application and window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Click Recorder")
window.setWindowFlag(Qt.Tool) 
window.setGeometry(100, 0, 200, 50)  # Adjust the window position and size
window.setWindowFlag(Qt.FramelessWindowHint)  # Remove window frame
window.setAttribute(Qt.WA_TranslucentBackground)  # Enable transparent background
window.setWindowFlag(Qt.WindowStaysOnTopHint)  # Set the window to stay on top
label = QLabel("Recording is inactive", window)
label.setAlignment(Qt.AlignCenter)
label.setGeometry(QRect(0, 0, 200, 50))  # Adjust the position and size of the label


# Create a QLabel for the logo
logo_label = QLabel(window)
logo_label.setGeometry(5, 5, 40, 40)  # Adjust the position and size of the logo
logo_pixmap = QPixmap("img/logo.png")  # added the clicksense logo
logo_label.setPixmap(logo_pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))




listener = mouse.Listener(on_click=on_click)
listener.start()
window.setStyleSheet("background-color: #c3e6cb;")  # Set border-radius to add rounded corners
label.setText("Recording is active")
print("Listener started.") #start recording once the app is started.






# Create a keyboard listener to handle the shortcut
keyboard_listener = keyboard.Listener(on_press=on_press)



try:
    # Start the keyboard listener
    keyboard_listener.start()
    

    # Start the PyQt5 application event loop
    sys.exit(app.exec_())
except Exception as e:
    print("An error occurred:", str(e))
