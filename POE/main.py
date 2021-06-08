# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import pyautogui
import ctypes
from Helper.Window import WindowRect, GameWindow
from Helper.functions import is_admin, add_log_guas, guas
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
import cv2 as cv
import numpy as np

TIME_FOR_MOVE = .1              #Constant controlling how fast the mouse moves to destinations should always be modified by guassian


class GUI(QWidget):
    def __init__(self, file):
        super(GUI, self).__init__()
        self.load_ui(file)

    def load_ui(self, file):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / file)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file, self)
        ui_file.close()
        self.mainWin = GameWindow("Stick")
        print(self.mainWin.window_info)

        if(file == "POEGUI/form.ui"):
            self.window.grabWin.clicked.connect(self._pull_screen)
            self.window.grabImg.clicked.connect(self._grab_frame)

    def _pull_screen(self):
        if is_admin():
            self.mainWin.move_to_foreground()
            self.mainWin.rect.update()
            pyautogui.moveTo(self.mainWin.rect.center()[0] + guas(20), self.mainWin.rect.center()[1] + guas(20), TIME_FOR_MOVE + guas(.05), pyautogui.easeOutQuad)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    def _grab_frame(self):
        cv.imshow('', self.mainWin.grab_frame())

if __name__ == "__main__":
    app = QApplication([])
    widget = GUI("POEGUI/form.ui")
    widget.show()
    sys.exit(app.exec_())
