import os

from windows_funcs import (
    _na,
    kill_process as _kill_process,
    kill_processes_by_name as _kill_processes_by_name,
    toggle_cursor as _toggle_cursor,
)

get_screen_size = _na

hide_cursor = _na
show_cursor = _na

toggle_cursor = _toggle_cursor

get_taskbar_height = _na
get_taskbar_position = _na

kill_processes_by_name = _kill_processes_by_name
kill_process = _kill_process


def is_admin() -> bool:
    return os.geteuid() == 0
