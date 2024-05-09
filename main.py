import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app: QApplication = app

        self.setWindowTitle("Hello, World!")
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.FramelessWindowHint)

        class ExampleButton(QPushButton):
            def window(self) -> MainWindow:
                return super().window()

            def event(self, e: QtCore.QEvent) -> bool:
                if isinstance(e, QtGui.QMouseEvent):
                    print(e.type())
                    if e.button() == Qt.MiddleButton and e.type() == Qt.MouseButtonPress:
                        self.window().destroy()
                        self.window().app.quit()
                return super().event(e)

        button = ExampleButton("Middleclick to exit")

        # Set the central widget of the Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()
