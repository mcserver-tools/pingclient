"""Module containing console control functions"""

from ctypes import WinDLL, windll

def show_console():
    """Show the console window"""

    window_handle = windll.kernel32.GetConsoleWindow()
    # SW_SHOW = 5
    show_flag = 5
    WinDLL('user32', use_last_error=True).ShowWindow(window_handle, show_flag)

def hide_console():
    """Hide the console window"""

    window_handle = windll.kernel32.GetConsoleWindow()
    # SW_HIDE = 0
    hide_flag = 0
    WinDLL('user32', use_last_error=True).ShowWindow(window_handle, hide_flag)
