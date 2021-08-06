import sys
from PySide2.QtWidgets import QApplication
from GUI import GUI
import os

#Used for PyInstaller to make a single exe file including the form
#link to stack overflow found on
#https://stackoverflow.com/questions/13946650/pyinstaller-2-0-bundle-file-as-onefile

#pyinstaller --onefile --add-data="C:\Users\LSI Setup\source\repos\POE\POE\;." "C:\Users\LSI Setup\source\repos\POE\POE\main.py"
#change filespaths but that may work for building into an exe it leaves some.py files in with the way the path is setup but not important right now.

#when building the .exe change main to a .pyw file to suppress console output








    

if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    widget = GUI("POEGUI/form.ui", "POE")
    widget.window.show()
    sys.exit(app.exec_())
