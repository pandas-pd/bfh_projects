#https://www.tinkerforge.com/de/doc/Software/Bricklets/LoadCellV2_Bricklet_Python.html#load-cell-v2-bricklet-python-examples

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_load_cell_v2 import BrickletLoadCellV2
from tinkerforge.ip_connection import Error as E
import json
import view


class Brick():

    def __init__(self):

        try:
            self.host : str         = "localhost"
            self.port : int         = 4223
            self.uid_master : str   = "6fX3k4"
            self.uid_load : str     = "KhY"

            self.ipcon = IPConnection() # Create IP connection
            self.lc = BrickletLoadCellV2(self.uid_load, self.ipcon) # Create device object

            self.ipcon.connect(self.host, self.port) # Connect to brickd

            #configs
            self.weight_limit = 1000 #[g]
            self.lc.set_moving_average(200)
            self.lc.set_configuration(rate = 1, gain = 0)

            #inital tara on bootup to set zero
            self.tara()
            self.scaled = False

        except:
            print("An Error has occured")
            exit()

    def _emergency_off(self, raw_weight : float):

        if raw_weight > self.weight_limit:
            self.disconnect()
            Controller.brick = None #used to signale, that the brickelt is disconnected

    def _scaling(self, raw_input) -> float:
        """uses the calibration to calculte the calibrated weights"""

        f = open("calibration.json", "r", encoding = "utf-8")
        calibration = json.load(f)
        f.close()

        cal_0, raw_0 = calibration["cal_0"]["cal"], calibration["cal_0"]["raw"]
        cal_1, raw_1 = calibration["cal_1"]["cal"], calibration["cal_1"]["raw"]
        cal_2, raw_2 = calibration["cal_2"]["cal"], calibration["cal_2"]["raw"]

        if raw_input <= raw_1:
            a = (cal_1 - cal_0) / (raw_1 - raw_0)
            #b = raw_0 - (cal_0*a)
            b = cal_0 - (raw_0*a)
            scaled = a*raw_input + b

        elif raw_input > raw_1:
            a = (cal_2 - cal_1) / (raw_2 - raw_1)
            #b = raw_1 - (cal_1*a)
            b = cal_1 - (raw_1*a)
            scaled = a*raw_input + b

        """
        a = (cal_1 - cal_0) / (raw_1 - raw_0)
        b = raw_0 - (cal_0*a)
        scaled = a*raw_input + b
        print(f"\nsmall f\n{a}*{raw_input} + {b}")

        a = (cal_2 - cal_1) / (raw_2 - raw_1)
        b = raw_1 - (cal_1*a)
        scaled = a*raw_input + b
        print(f"\nbig f\n{a}*{raw_input} + {b}")

        scaled = 1
        """

        return scaled

    def _check_calibration(self) -> None:
        """sort cal_1 and cal_2 by value for _sclaing() function"""

        f = open("calibration.json", "r", encoding = "utf-8")
        config = json.load(f)
        f.close()

        cal_1 : float =     config["cal_1"]["cal"]
        cal_2 : float =     config["cal_2"]["cal"]

        if cal_2 < cal_1:

            new_config = {
                "cal_0" : {"cal" : config["cal_0"]["cal"], "raw" : config["cal_0"]["raw"]},
                "cal_1" : {"cal" : config["cal_2"]["cal"], "raw" : config["cal_2"]["raw"]},
                "cal_2" : {"cal" : config["cal_1"]["cal"], "raw" : config["cal_1"]["raw"]}
            }

            f = open("calibration.json", "w", encoding = "utf-8")
            json.dump(new_config,f)
            f.close()

        return

    def calibrate(self, calibration_index : int, calibration_weight : float, raw_weight : float) -> None:
        """calibration_index = 0,1,2
        calibration_Weight = [g] / float """

        #load current config
        f = open("calibration.json", "r", encoding = "utf-8")
        config = json.load(f)
        f.close()

        #assing new calibrations
        config[f"cal_{calibration_index}"]["cal"] = calibration_weight
        config[f"cal_{calibration_index}"]["raw"] = raw_weight

        #save new calibration values
        f = open("calibration.json", "w", encoding = "utf-8")
        json.dump(config,f)
        f.close()

        if calibration_index < 2:
            self.scaled = False

        elif calibration_index == 2:
            self._check_calibration()
            self.scaled = True

        return

    def tara(self) -> None:
        self.lc.tare()
        return

    def get_meassurement(self) -> float:
        """
        smooth: if value should be smoothed, takes longer to calculate
        method: "mean", "median"
        period: relevat period for smoothing
        """

        try:
            raw_weight : float = self.lc.get_weight()
            self._emergency_off(raw_weight = raw_weight)

            if self.scaled:
                scaled_weight = self._scaling(raw_weight)
            else:
                scaled_weight = raw_weight

        except E:
            scaled_weight = None

        return scaled_weight

    def disconnect(self) -> None:
        self.ipcon.disconnect()
        return

class Controller():

    brick       = None
    test_mode   = None

    def recieve(message : object = None) -> dict:
        """fromat:  {"on": True, "tara": False, "calibrate": False, "calibration_weight": None, "calibration_index": None}
        if message = None, the currenct meassurement will get returned"""

        if message is None and Controller.brick is not None:
            weight : float = Controller.brick.get_meassurement()
            answer = Controller.send(weight = weight)

        elif message is not None: #used to get weight
            answer = Controller.callback(message)

        else:
            answer = Controller.send() #when emergency turn off, this will trigger

        return answer

    def send(weight : float = None) -> dict:
        """format: {weight: int, on: True}"""

        if Controller.brick is None:
            message : dict = {
                "weight"    : None,
                "on"        : False,
            }

        elif Controller.brick is not None and weight is None:
            message : dict = {
                "weight"    : None,
                "on"        : True,
            }

        else:
            message : dict = {
                "weight"    : weight,
                "on"        : True,
            }

        return message

    def callback(message : dict) -> dict:

        if message["on"] and Controller.brick is None:

            if not Controller.test_mode:

                Controller.brick = Brick()
            
        elif not message["on"] and Controller.brick is not None:
            Controller.brick.disconnect()
            Controller.brick = None

        elif message["tara"]:
            Controller.brick.tara()

        elif message["calibrate"]:

            response = Controller.recieve()
            raw = response["weight"]

            Controller.brick.calibrate(
                calibration_index   = message["calibration_index"],
                calibration_weight  = message["calibration_weight"],
                raw_weight          = raw,
            )

        answer : dict = Controller.send()

        return answer

if __name__ == '__main__':

    Controller.test_mode = False # set False for live mode
    view.Run.run(Controller.test_mode)