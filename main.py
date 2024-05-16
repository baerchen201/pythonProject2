from __future__ import annotations

import os
import sys
import threading
import time
from typing import Callable, Literal

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent, QImage
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

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
            btn={Qt.LeftButton: 0, Qt.RightButton: 1, Qt.MiddleButton: 2}.get(event.button(), None),
            action={QEvent.MouseButtonPress: 0, QEvent.MouseButtonRelease: 1}.get(event.type(), None),
            a_pos=(event.globalX(), event.globalY()),
            r_pos=(event.x(), event.y()),
        )


class ClickableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hooks: dict[int, Callable[[SimpleMouseEvent], bool]] = {}

    def event(self, e: QEvent) -> bool:
        if isinstance(e, QMouseEvent):
            for func in self._hooks.values():
                if not func(SimpleMouseEvent.from_event(e)):
                    return False
        return super().event(e)

    def hook_click(self, func: Callable[[SimpleMouseEvent], bool]) -> int:
        for i in range(len(self._hooks) + 1):
            if i not in self._hooks:
                self._hooks[i] = func
                return i

    def unhook_click(self, hook_id: int) -> Callable[[SimpleMouseEvent], bool]:
        return self._hooks.pop(hook_id)


class ClickableVideoWidget(QVideoWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hooks: dict[int, Callable[[SimpleMouseEvent], bool]] = {}

    def event(self, e: QEvent) -> bool:
        if isinstance(e, QMouseEvent):
            for func in self._hooks.values():
                if not func(SimpleMouseEvent.from_event(e)):
                    return False
        return super().event(e)

    def hook_click(self, func: Callable[[SimpleMouseEvent], bool]) -> int:
        for i in range(len(self._hooks) + 1):
            if i not in self._hooks:
                self._hooks[i] = func
                return i

    def unhook_click(self, hook_id: int) -> Callable[[SimpleMouseEvent], bool]:
        return self._hooks.pop(hook_id)


class AnimatedPixmap(QImage):
    def __init__(self, _frames: list[str | bytes | os.PathLike], _fps: float | None = None):
        super().__init__()
        self.fps = _fps
        self.current_frame = 0
        self.frames = []
        if len(_frames) == 0:
            raise ValueError(f"No animation frames")
        for frame in _frames:
            if isinstance(frame, str):
                with open(frame, "rb") as f:
                    frame = f.read()
            self.frames.append(frame)

    def _next_frame(self):
        time.sleep(1 / self.fps)
        self.next_frame()
        threading.Thread(target=self._next_frame).start()

    def next_frame(self, skip: int | None = 0):
        self.current_frame = (self.current_frame + skip + 1) % len(self.frames)
        print(self.current_frame, self.frames[self.current_frame])
        self.loadFromData(self.frames[self.current_frame])

    def resize_all(self, x: int, y: int):
        for frame in self.frames:
            pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello, World!")
        self.setWindowOpacity(0.5)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        label = ClickableLabel(self)

        @label.hook_click
        def _(e: SimpleMouseEvent) -> bool:
            print(e)
            if e.button == SimpleMouseEvent.BTN_LEFT and e.action == SimpleMouseEvent.ACT_DOWN:
                _switch()
                return True
            if e.button == SimpleMouseEvent.BTN_RIGHT:
                QApplication.quit()
                return False

        image = QImage("img.png")
        label.setToolTip("Leftclick to switch, Rightclick to quit")
        self.size = (100, 100)
        self.size = (image.width(), image.height())
        self.setGeometry(QtCore.QRect(50, funcs.get_taskbar_position() - self.size[1], self.size[0], self.size[1]))

        apixmap = AnimatedPixmap(["a1.png", "a2.png", "a3.png", "a2.png"])

        next_pixmap = apixmap

        def _switch():
            apixmap.next_frame()
            return
            nonlocal next_pixmap
            _ = next_pixmap
            next_pixmap = label.pixmap()
            label.setPixmap(_)

        widget = QImageWidget

        self.setCentralWidget(image)
        self.show()


app = QApplication(sys.argv)

window = MainWindow()

app.exec()
