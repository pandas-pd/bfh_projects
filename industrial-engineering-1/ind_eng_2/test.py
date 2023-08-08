from main import Controller
import time
import tkinter as tk

answer = Controller.recieve(message = {"on": True, "tara": False, "calibrate": False})
print(answer)

"""
for index, config in zip([0,1,2],[0,250,20]):
    input(f"Press enter for index {index}")
    answer = Controller.recieve({"on": True, "tara": False, "calibrate": True, "calibration_weight": config, "calibration_index": index})
    print(answer)
"""

for i in range(10000):
    print (Controller.recieve(), end = "\r")

exit()

Controller.recieve({"on": True, "tara": True, "calibrate": False})

for i in range(3000):
    print (Controller.recieve(), end = "\r")

answer = Controller.recieve(message = {"on": False, "tara": False, "calibrate": False})
print(answer)