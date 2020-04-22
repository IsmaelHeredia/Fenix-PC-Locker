#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pip install keyboard
# pip install pynput
#
# Title : Fenix PC Locker 0.3
# Author : Ismael Heredia
# Date : 21/04/2020

import os, sys, keyboard
from pynput import mouse
from threading import Thread
import queue
import time, datetime

magic_key = "space" # Edit (a-z, space, page up, page down, esc, windows, f1 - f12, enter, up, down, left, right, del)
key = "ctrl+shift+" + magic_key

q1 = queue.Queue()
q2 = queue.Queue()

listener = mouse.Listener()

def write_log(filename,text):
    file = open(filename, "a")
    file.write(text + "\n")
    file.close()

def unlock():
    keyboard.unhook_all()
    listener.stop()

    q1.put("stop")
    q2.put("stop")

    print("[!] System unlocked")

    os._exit(0)

def blocked():
    keyboard.unhook_all()
    listener.stop()

    q1.put("stop")
    q2.put("stop")

    now = datetime.datetime.now()
    info = "[!] Intruder detected at : %d/%d/%d %d:%d:%d" % (now.day, now.month, now.year, now.hour, now.minute, now.second,)
    
    write_log("log_pc_locker.txt",info)

    print("[!] System locked")

    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0") # Game over
    os._exit(0)

def print_pressed_keys(e):
	line = ', '.join(str(code) for code in keyboard._pressed_events)
	if line:
		if line != "29" and line != "42" and line != "29, 42": # Control + Shift
		    blocked()

def on_move(x, y):
    blocked()

def on_click(x, y, button, pressed):
    if pressed:
        blocked()

def on_scroll(x, y, dx, dy):
    blocked()

def thread_keyboard():
    while True:
        try:
            item = q1.get(False)
            if item == "stop":
                break
        except queue.Empty:
            pass

        print("[+] Controlling keyboard")

        try:
            keyboard.add_hotkey(key, unlock)
            keyboard.hook(print_pressed_keys)
            keyboard.wait(key)
        except:
            pass

def thread_mouse():
    while True:
        try:
            item = q2.get(False)
            if item == "stop":
                break
        except queue.Empty:
            pass

        print("[+] Controlling mouse")

        listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
        listener.start()
        listener.join()

def main():
    Thread(target=thread_keyboard).start()
    Thread(target=thread_mouse).start()

if __name__ == "__main__":
    main()