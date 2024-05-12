import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

if os.name == "nt":
    import windows_funcs as funcs
else:
    raise SystemError("This program currently only runs on windows")


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app: QApplication = app

        self.setWindowTitle("Hello, World!")
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        class ExampleButton(QLabel):
            def event(self, e: QtCore.QEvent) -> bool:
                if isinstance(e, QtGui.QMouseEvent):
                    print(e.type())
                    if e.button() == Qt.MiddleButton and e.type() == Qt.MouseButtonPress:
                        QApplication.quit()
                        return True
                return super().event(e)

        label = ExampleButton(self)
        pixmap = QtGui.QPixmap("img.png")
        label.setPixmap(pixmap)
        self.size = (100, 100)
        self.size = (pixmap.width(), pixmap.height())
        self.setGeometry(QtCore.QRect(50, funcs.get_taskbar_position() - self.size[1], self.size[0], self.size[1]))

        self.setCentralWidget(label)
        self.show()


app = QApplication(sys.argv)

window = MainWindow(app)

app.exec()
