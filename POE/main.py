import sys
from PySide2.QtWidgets import QApplication
from GUI import GUI


    

if __name__ == "__main__":
    app = QApplication([])
    widget = GUI("POEGUI/form.ui", "PLC")
    widget.show()
    sys.exit(app.exec_())
