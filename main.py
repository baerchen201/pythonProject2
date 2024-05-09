import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

if os.name == "nt": import windows_funcs as funcs


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app: QApplication = app

        self.setWindowTitle("Hello, World!")
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.FramelessWindowHint)
        print(funcs.get_taskbar_height())
        self.size = (200, 100)
        self.setGeometry(50, funcs.get_screen_size()[1] - funcs.get_taskbar_height() - self.size[1], self.size[0],
                         self.size[1])
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        class ExampleButton(QPushButton):
            def window(self) -> MainWindow:
                return super().window()

            def event(self, e: QtCore.QEvent) -> bool:
                if isinstance(e, QtGui.QMouseEvent):
                    print(e.type())
                    if e.button() == Qt.MiddleButton and e.type() == Qt.MouseButtonPress:
                        self.window().app.quit()
                return super().event(e)

        button = ExampleButton("Middleclick to exit")

        # Set the central widget of the Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()
