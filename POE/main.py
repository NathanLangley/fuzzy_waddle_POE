# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import pyautogui
import ctypes
from Helper.FindWindow import WindowRect, GameWindow, is_admin
from PySide2.QtWidgets import QApplication, QWidget, QPushButton
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader



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
            pyautogui.moveTo(mainWin.rect.center())
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

if __name__ == "__main__":
    app = QApplication([])
    widget = GUI("POEGUI/form.ui")
    widget.show()
    sys.exit(app.exec_())
