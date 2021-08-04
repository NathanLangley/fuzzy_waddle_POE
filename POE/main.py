import sys
from PySide2.QtWidgets import QApplication
from GUI import GUI
import os

#Used for PyInstaller to make a single exe file including the form
#link to stack overflow found on
#https://stackoverflow.com/questions/13946650/pyinstaller-2-0-bundle-file-as-onefile

#pyinstaller --onefile --add-data="C:\Users\LSI Setup\source\repos\POE\POE\;." "C:\Users\LSI Setup\source\repos\POE\POE\main.py"
#change filespaths but that may work for building into an exe it leaves some.py files in with the way the path is setup but not important right now.

filename = 'POEGUI\form.ui'
if hasattr(sys, '_MEIPASS'):
    # PyInstaller >= 1.6
    os.chdir(sys._MEIPASS)
    filename = os.path.join(sys._MEIPASS, filename)
elif '_MEIPASS2' in environ:
    # PyInstaller < 1.6 (tested on 1.5 only)
    os.chdir(environ['_MEIPASS2'])
    filename = os.path.join(environ['_MEIPASS2'], filename)
else:
    os.chdir(dirname(sys.argv[0]))
    filename = os.path.join(dirname(sys.argv[0]), filename)





    

if __name__ == "__main__":
    app = QApplication([])
    widget = GUI("POEGUI/form.ui", "PLC")
    widget.show()
    sys.exit(app.exec_())
