# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import numpy as np
import pyautogui
import ctypes
from Helper.FindWindow import WindowRect, GameWindow
from Helper.functions import is_admin, add_log_guas, guas
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
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

        if(file == "POEGUI/form.ui"):
            self.window.pushButton.clicked.connect(self._pull_screen)

    def _pull_screen(self):
        if is_admin():
            mainWin = GameWindow("Stick")
            print(mainWin.window_info)
            mainWin.move_to_foreground()
            pyautogui.moveTo(mainWin.rect.center()[0] + guas(20), mainWin.rect.center()[1] + guas(20), TIME_FOR_MOVE + guas(.05), pyautogui.easeOutQuad)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

if __name__ == "__main__":
    app = QApplication([])
    widget = GUI("POEGUI/form.ui")
    widget.show()
    sys.exit(app.exec_())
