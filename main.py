from __future__ import annotations

import os
import sys
from typing import Callable, Literal

try:
    from PyQt6.QtCore import Qt, QEvent, QRect
    from PyQt6.QtGui import QMouseEvent, QPixmap, QIcon
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
except ModuleNotFoundError as e:
    try:
        from tkinter import messagebox

        messagebox.showerror("Python module missing",
                             f"To run this program, you need to install the following python module: {e.name}\n"
                             f"\nYou can install it with the following command:\n\n\tpip install {e.name}", )
        raise SystemExit(1)
    except ModuleNotFoundError:
        print(e)
        print(f"Please install the required module with the following command:\n\tpip3 install {e.name}")
    except Exception as _e:
        print(e)
        print(_e)
    finally:
        raise SystemExit(1)

if os.name == "nt":
    import windows_funcs as funcs
else:
    app = QApplication([])
    msgbox = QMessageBox()
    msgbox.setIcon(QMessageBox.Icon.Critical)
    msgbox.setText("This program currently only runs on windows")
    msgbox.setInformativeText(f"Due to system limitations, this program cannot be run on your system [{os.name}].")
    msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
    msgbox.setDefaultButton(QMessageBox.StandardButton.Ok)
    msgbox.setWindowTitle("System Error")
    msgbox.setWindowIcon(QIcon("default_icon.png"))
    msgbox.exec()
    app.quit()
    raise SystemExit(1)


class SimpleMouseEvent:
    ACT_DOWN = QEvent.Type.MouseButtonPress
    ACT_UP = QEvent.Type.MouseButtonRelease

    BTN_LEFT = Qt.MouseButton.LeftButton
    BTN_RIGHT = Qt.MouseButton.RightButton
    BTN_MIDDLE = Qt.MouseButton.MiddleButton

    def __init__(
            self,
            btn: Literal[
                     Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton, Qt.MouseButton.MiddleButton, None] | int,
            action: Literal[QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, None] | int,
            a_pos: tuple[int, int] | tuple,
            r_pos: tuple[int, int] | tuple,
    ):
        self.button = btn
        self.action = action
        self.absolute_pos = a_pos
        self.relative_pos = r_pos

    def __str__(self) -> str:
        return (f"MouseEvent(button={self.str_button}, action={self.str_action}, absolute_pos={self.str_absolute_pos}"
                f", relative_pos={self.str_relative_pos})")

    @property
    def str_button(self) -> str:
        return {self.BTN_LEFT: "left", self.BTN_RIGHT: "right", self.BTN_MIDDLE: "middle", None: ""}[self.button]

    @property
    def str_action(self) -> str:
        return {self.ACT_DOWN: "down", self.ACT_UP: "up", None: ""}[self.action]

    @property
    def str_absolute_pos(self) -> str:
        return f"({self.absolute_pos[0]},{self.absolute_pos[1]})"

    @property
    def str_relative_pos(self) -> str:
        return f"({self.relative_pos[0]},{self.relative_pos[1]})"

    def from_event(event: QMouseEvent) -> SimpleMouseEvent:
        return SimpleMouseEvent(
            btn=event.button()
            if event.button() in [Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton, Qt.MouseButton.MiddleButton]
            else None,
            action=event.type()
            if event.type() in [QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease]
            else None,
            a_pos=(event.globalPosition().x(), event.globalPosition().y()),
            r_pos=(event.position().x(), event.position().y()),
        )


class ClickableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hooks: dict[int, Callable[[SimpleMouseEvent], bool | None]] = {}

    def event(self, e: QEvent) -> bool:
        if isinstance(e, QMouseEvent):
            for func in self._hooks.values():
                ret = func(SimpleMouseEvent.from_event(e))
                if ret is None:
                    continue
                if not ret:
                    return False
        return super().event(e)

    def hook_click(self, func: Callable[[SimpleMouseEvent], bool | None]) -> int:
        for i in range(len(self._hooks) + 1):
            if i not in self._hooks:
                self._hooks[i] = func
                return i

    def unhook_click(self, hook_id: int) -> Callable[[SimpleMouseEvent], bool | None]:
        return self._hooks.pop(hook_id)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello, World!")
        self.setWindowIcon(QIcon("default_icon.png"))
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.Tool)  # This prevents the window from appearing in the taskbar and Alt+Tab
        self.setWindowFlag(Qt.WindowType.WindowDoesNotAcceptFocus, True)  # This prevents the window from taking focus

        label = ClickableLabel(self)

        @label.hook_click
        def _(e: SimpleMouseEvent) -> bool:
            print(e)
            if e.button == SimpleMouseEvent.BTN_RIGHT and e.action == SimpleMouseEvent.ACT_UP:
                QApplication.quit()
                return False

        pixmap = QPixmap("img.png")
        label.setPixmap(pixmap)
        label.setToolTip("Right click to quit")
        self.size = (100, 100)
        self.size = (pixmap.width(), pixmap.height())
        self.setGeometry(QRect(50, funcs.get_taskbar_position() - self.size[1], self.size[0], self.size[1]))

        self.setCentralWidget(label)
        self.show()


app = QApplication(sys.argv)

window = MainWindow()

app.exec()
