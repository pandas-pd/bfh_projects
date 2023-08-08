#!/usr/bin/env python3

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QSize, QThread, Signal
from PySide6.QtGui import QFont, QPalette, QMouseEvent, QColor, QAction, QGuiApplication, QImage
from PySide6.QtWidgets import QApplication, QWidget, QToolBar, QStatusBar, QMainWindow
import sys
from main import Controller
import time


 
class Colors():
    """
    All colors for the gui are saved here as qcolors, ready to use.
    """

    lavender_blush  = QColor(246,232,234)
    raisin_black    = QColor(34, 24, 28)
    jet_grey        = QColor(49, 47, 47)
    pine_green      = QColor(31, 112, 100)
    red             = QColor(188, 32, 65)
    brown           = QColor(86, 76, 85)
    light_blue      = QColor(91, 160 ,191)

    @staticmethod
    def color_yellow(item):

        item.setStyleSheet(f"color: rgb(253,191,110);")

    @staticmethod
    def color_green(item):

        item.setStyleSheet(f"color: rgb(31, 112, 100);")

    @staticmethod
    def color_red(item):

        item.setStyleSheet(f"color: rgb(188, 32, 65);")

    @staticmethod
    def color_brown(item):

        item.setStyleSheet(f"color: rgb(86, 76, 85);")

    @staticmethod
    def color_bg_light_blue(item):
        
        item.setStyleSheet(f"background-color: rgb(91, 160 ,191);")

    @staticmethod
    def color_bg_jet_grey(item):
        
        item.setStyleSheet(f"background-color: rgb(49, 47, 47);")

class MainWindow(QMainWindow):

    def __init__(self, test_mode):
        """
        Builds main window with menu.
        """
        super(MainWindow, self).__init__()
        self.controller     = None
        self.on             = False
        self.test_mode      = test_mode       

        self.height         = 400
        self.width          = 800
        palette             = self.palette()

        palette.setColor(QPalette.Window, Colors.jet_grey)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowTitle("Eichmeister Waage")


        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        ### SETUP INVISIBLE TOOLBAR ###

        toolbar = QToolBar("Main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        #self.addToolBar(toolbar) # keep invisible, acts as structure for menu

        ### SETUP UI LAYOUT ###
        
        self._init_ui()

        ### SETUP MENU ###

        self._init_menu()

        ### SETUP WORKER ###

        self.scale_worker = Scale_worker()
        self.scale_worker.scale = self
        self.scale_worker.start()
        self.scale_worker.scale_update.connect(self.update_display)

    def _init_ui(self):
        """
        Sets UI with fonts and alignments.
        """     
        self.setFont(QFont("Lato", 10))
        self.grid = QtWidgets.QGridLayout()

        self.tara_button   = QtWidgets.QPushButton("Tara")
        self.tara_button.clicked.connect(self.on_tara_click)

        self.on_off_button = QtWidgets.QPushButton("On")
        self.on_off_button.clicked.connect(self.on_on_off_click) 

        self.brand_label = QtWidgets.QLabel("EICHMEISTER WAAGE")
        Colors.color_yellow(self.brand_label)
        self.brand_label.setAlignment(Qt.AlignCenter)

        self.grams_label = QtWidgets.QLabel()
        self.grams_label.setAlignment(Qt.AlignRight)
        self.grams_label.setFont(QFont("Lato", 24))
        self.grams_label.setStyleSheet("margin : 16px")


        self.lcd_display = QtWidgets.QLCDNumber()
        self.lcd_display.display("")
        self.lcd_display.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcd_display.setDigitCount(8)

        self._populate_grid()

    def _populate_grid(self):

        """ Adds all widgets to grid. grid.addWidget(widget,row,column,row_span, column_span)"""
        self.grid.addWidget(self.lcd_display,0,0,2,3)
        self.grid.addWidget(self.grams_label, 0,2,1,1)
        self.grid.addWidget(self.on_off_button,2,0,1,1)
        self.grid.addWidget(self.brand_label,2,1,1,1)
        self.grid.addWidget(self.tara_button,2,2,1,1)
        self.centralWidget.setLayout(self.grid)

    def _init_menu(self) -> None:

        self.menu = self.menuBar()
        self.mode_menu = self.menu.addMenu("&Settings")
        self.toolbar = QToolBar("Main toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        #self.addToolBar(toolbar) # keep invisible, acts as structure for menu

        self.calibration_action = QAction("&Calibrate", self)
        self.calibration_action.setStatusTip("Starts calibration sequence")
        self.calibration_action.triggered.connect(self.on_calibrate_click)
        self.calibration_action.setCheckable(False)
        self.toolbar.addAction(self.calibration_action)

        self.mode_menu.addAction(self.calibration_action)

    def on_tara_click(self,e):

        self.scale_worker.send_to_scale({"on": True, "tara": True, "calibrate": False, "calibration_weight": None, "calibration_index": None})

    def on_on_off_click(self,e) -> None:

        if self.on:
            self.toggle_off()
            self.on = False
        else: 
            self.toggle_on()
            self.on = True

    def on_calibrate_click(self,e):

        if self.on:
            self.calibration_message_box("Please set the scale level and remove all weights. Then press ok.") 
            self.scale_worker.send_to_scale({"on": True, "tara": False, "calibrate": True, "calibration_weight": 0, "calibration_index": 0})
            input_one = Calibration_input_dialog(self,"Please put any weight between 0 and 500 grams on the scale (ideally 250 g).\n Enter the weight in the text field. Then press ok.")
            self.scale_worker.send_to_scale({"on": True, "tara": False, "calibrate": True, "calibration_weight": input_one.get_entered(), "calibration_index": 1})
            print(input_one.get_entered())
            input_two = Calibration_input_dialog(self,"Please put 500 grams on the scale and press ok.\n If you choose another weight, enter the weight in the text field.")
            print(input_two.get_entered())
            self.scale_worker.send_to_scale({"on": True, "tara": False, "calibrate": True, "calibration_weight": input_two.get_entered(), "calibration_index": 2})

        else:
            self.calibration_message_box("Please turn on the scale.") 

    def toggle_on(self) -> None:

        self.on_off_button.setText("Off")
        self.update_display("0000.00")
        Colors.color_bg_light_blue(self.lcd_display)

        self.grams_label.setText("grams")

        self.scale_worker.send_to_scale({"on": True, "tara": False, "calibrate": False, "calibration_weight": None, "calibration_index": None})
        

    def toggle_off(self) -> None:

        self.on_off_button.setText("On")
        self.lcd_display.display("")
        Colors.color_bg_jet_grey(self.lcd_display)

        self.grams_label.setText("")

        self.scale_worker.send_to_scale({"on": False, "tara": False, "calibrate": False, "calibration_weight": None, "calibration_index": None})

    def update_display(self,message) -> None:

        self.lcd_display.display(message)

    def calibration_message_box(self, message) -> None:

        message_box = QtWidgets.QMessageBox()
        message_box.setText(message)
        message_box.exec()


    def clear_all(self):
        """
        Used when switching modes. Removes all open widget from view.
        """
        children = []
        for i in range(self.count()):
            child = self.itemAt(i).widget()
            if child:
                children.append(child)

        for child in children:
            child.deleteLater()

class Scale_worker(QThread):
    """
    The scaling runs in a seperate thread,
    so the programm doesn't stall.
    """

    scale_update = Signal(str)
    scale = None 

    def run(self):
        """
        Run thread and and scale.
        """

        self.thread_active = True

        while self.thread_active:
            
            try:

                #turns scale on
                if not self.scale.on:
                    self.send_to_scale({"on": True, "tara": False, "calibrate": False, "calibration_weight": None, "calibration_index": None})

                #gets meassurment from scale
                if self.scale.on:
                    self.send_to_scale(None)

                if not self.scale.on:
                    self.scale_update.emit("")

            except Exception as e:
                print(e)

            time.sleep(0.01)
    
    def send_to_scale(self, message) -> None:

        response = Controller.recieve(message)

        if response["weight"] is not None:
            message = "{:.2f}".format(round(response["weight"],2))

        else:
            message = "----.--"

        self.scale_update.emit(message)

        if not response["on"]:
            if not self.scale.test_mode:
                self.scale_update.emit("")
                self.scale.toggle_off()
    
    def stop(self):
        """
        Close and exit video worker, when not needed anymore.
        """
        
        self.thread_active = False

        self.exit()



###### MESSAGE BOX SECTION ######

class Calibration_input_dialog():

    def __init__(self, widget, message) -> None:
        
        input_dialog = QtWidgets.QInputDialog
        text, ok = input_dialog.getText( widget,'Enter calibration weight', message )
        
        if text and ok:
            self.entered = float(str(text))

    def get_entered(self):
        return self.entered 
            
def set_window_center(self):
    """
    Used to display stuff dead center.
    """
    
    qr = self.frameGeometry() # geometry of the main window    
    cp = self.screen().availableGeometry().center() # center point of screen
    qr.moveCenter(cp)     # move rectangle's center point to screen's center point
    self.move(qr.topLeft())

class Run():
    
    def run(test_mode = False):

        app         = QApplication(sys.argv)
        window      = MainWindow(test_mode)

        window.show()
        set_window_center(window)

        app_run = app.exec()
   
        try:
            window.scale_worker.terminate() # terminate video worker before closing the window
        except:
            print("Qthread could not be terminated")

        sys.exit(app_run)

if __name__ == '__main__':

    #♣Run.run() #actually start this only over main.
    pass