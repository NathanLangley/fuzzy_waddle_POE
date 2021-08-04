import os
from pathlib import Path
import sys
import pyautogui
import ctypes
from Helper.Window import WindowRect, GameWindow
from Helper.functions import is_admin, add_guas, guas
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PySide2.QtCore import QFile
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
import cv2 as cv
import numpy as np



TIME_FOR_MOVE = .1              #Constant controlling how fast the mouse moves to destinations should always be modified by guassian


class GUI(QWidget):
    def __init__(self, file, name):
        super(GUI, self).__init__()
        self.file = file
        self.name = name
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / self.file)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
        self.setWindowIcon(QIcon('C:\\Users\\LSI Setup\\Pictures\\icon.png'))
        ui_file.close()                                                       

                                                                             #Anything tied to a button or ui element will use the format of _function_name():
        if(self.file == "POEGUI/form.ui"):                                   #can manage what gets loaded for each window object could be accomplished with polymorphism but 
            self.window.grabWin.clicked.connect(self._pull_screen)           #thats a lot more code for this simple case especially since the current plan is 1 or 2 additional windows
            self.window.grabImg.clicked.connect(self._grab_frame)
            self.window.reloadUI.clicked.connect(self._load_ui)
            self.window.loadFile.clicked.connect(self._load_file)

        self._load_ui()

    def console(self, text):
        self.window.Output.appendPlainText(text)


            

#/////////////////////////////////////////////////////////////////////////////// Button Functions Below

    def _load_ui(self):
        try:
            self.mainWin = GameWindow(self.name)
            self.console(self.mainWin.window_info)
        except Exception:
            self.mainWin = None
            self.console("No window found need to reload object")

    def _load_file(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self, dir = "/", filter = ("Image Files (*.png *.jpg *.bmp)"))
            self.console(filename + ' - Loaded')
        except:
            pass

    def _pull_screen(self):
        if is_admin():
            try:
                self.mainWin.move_to_foreground()
                self.mainWin.rect.update()
                pyautogui.moveTo(self.mainWin.rect.center()[0] + guas(20), self.mainWin.rect.center()[1] + guas(20), TIME_FOR_MOVE + guas(.05), pyautogui.easeOutQuad)
            except:
                self.console("Error, probably no window found")

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    def _grab_frame(self):
        try:
            cv.imshow('', self.mainWin.grab_frame())
        except:
             self.console("Error, probably no window found")
