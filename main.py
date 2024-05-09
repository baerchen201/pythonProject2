import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello, World!")

        class ExampleButton(QtWidgets.QPushButton):
            def event(self, e: QtCore.QEvent) -> bool:
                if isinstance(e, QtGui.QMouseEvent):
                    print(e.button())
                return super().event(e)

        button = ExampleButton("Press Me!")

        # Set the central widget of the Window.
        self.setCentralWidget(button)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
