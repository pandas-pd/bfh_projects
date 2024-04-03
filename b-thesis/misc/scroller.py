import win32api
from win32con import *
import keyboard

#Scroll one up

import threading
from win32api import STD_INPUT_HANDLE
from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT


class Scroller():

    def main():
        pass
    
    def scroll(speed):

        #Scroll one down
        win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, -1, 0)

Scroller.main()