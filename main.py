from __future__ import annotations

import os
import sys
from typing import Callable, Literal

from PyQt6.QtCore import Qt, QEvent, QRect
from PyQt6.QtGui import QMouseEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

if os.name == "nt":
    import windows_funcs as funcs
else:
    raise SystemError("This program currently only runs on windows")


class SimpleMouseEvent:
    ACT_DOWN = 0
    ACT_UP = 1

    BTN_LEFT = 0
    BTN_RIGHT = 1
    BTN_MIDDLE = 2

    def __init__(
        self,
        btn: Literal[0, 1, 2, None] | int,
        action: Literal[0, 1, None] | int,
        a_pos: tuple[int, int] | tuple,
        r_pos: tuple[int, int] | tuple,
    ):
        self.button = btn
        self.action = action
        self.absolute_pos = a_pos
        self.relative_pos = r_pos

    def __str__(self) -> str:
        return f"MouseEvent(button={self.str_button}, action={self.str_action}, absolute_pos={self.str_absolute_pos}, relative_pos={self.str_relative_pos})"

    @property
    def str_button(self) -> str:
        return {0: "left", 1: "right", 2: "middle", None: ""}[self.button]

    @property
    def str_action(self) -> str:
        return {0: "down", 1: "up", None: ""}[self.action]

    @property
    def str_absolute_pos(self) -> str:
        return f"({self.absolute_pos[0]},{self.absolute_pos[1]})"

    @property
    def str_relative_pos(self) -> str:
        return f"({self.relative_pos[0]},{self.relative_pos[1]})"

    def from_event(event: QMouseEvent) -> SimpleMouseEvent:
        return SimpleMouseEvent(
            btn={Qt.MouseButton.LeftButton: 0, Qt.MouseButton.RightButton: 1, Qt.MouseButton.MiddleButton: 2}.get(
                event.button(), None
            ),
            action={QEvent.Type.MouseButtonPress: 0, QEvent.Type.MouseButtonRelease: 1}.get(event.type(), None),
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
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        label = ClickableLabel(self)

        @label.hook_click
        def _(e: SimpleMouseEvent) -> bool:
            print(e)
            if e.button == SimpleMouseEvent.BTN_RIGHT:
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
