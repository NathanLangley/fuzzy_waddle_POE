import ctypes
import pyautogui
from enum import Enum
import os, sys, random
from collections import namedtuple
import numpy as np
import cv2 as cv
from mss import mss
import time
import math
from Helper.functions import is_admin
SW_RESTORE = 9
SW_NORMAL = 1


class user32_SW():
    SW_HIDE = 0
    SW_NORMAL = 1
    SW_SHOWMINIMIZED = 2
    SW_MAXIMIZE = 3
    SW_SHOWNOACTIVE = 4
    SW_SHOW = 5
    SW_MINIMIZE = 6
    SW_SHOWMINNOACTIVE = 7
    SW_SHOWNA = 8
    SW_RESTORE = 9
    SW_SHOWDEFAULT = 10
    SW_FORCEMINIMIZE = 11


#most of this code is pulled from an old window project I worked on with a friend it has been upated to be more generic in fulfilling what I need

user32 = ctypes.WinDLL('user32', use_last_error=True)

def check_zero(result, func, args):
    if not result:
        err = ctypes.get_last_error()
        if err:
            raise ctypes.WinError(err)
    return args

if not hasattr(ctypes.wintypes, 'LPDWORD'): # PY2
    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

WindowInfo = namedtuple('WindowInfo', 'pid title')

WNDENUMPROC = ctypes.WINFUNCTYPE(
    ctypes.wintypes.BOOL,
    ctypes.wintypes.HWND,    # _In_ hWnd
    ctypes.wintypes.LPARAM,) # _In_ lParam

user32.EnumWindows.errcheck = check_zero
user32.EnumWindows.argtypes = (
   WNDENUMPROC,      # _In_ lpEnumFunc
   ctypes.wintypes.LPARAM,) # _In_ lParam

user32.IsWindowVisible.argtypes = (
    ctypes.wintypes.HWND,) # _In_ hWnd

user32.GetWindowThreadProcessId.restype = ctypes.wintypes.DWORD
user32.GetWindowThreadProcessId.argtypes = (
  ctypes.wintypes.HWND,     # _In_      hWnd
  ctypes.wintypes.LPDWORD,) # _Out_opt_ lpdwProcessId

user32.GetWindowTextLengthW.errcheck = check_zero
user32.GetWindowTextLengthW.argtypes = (
  ctypes.wintypes.HWND,) # _In_ hWnd

user32.GetWindowTextW.errcheck = check_zero
user32.GetWindowTextW.argtypes = (
    ctypes.wintypes.HWND,   # _In_  hWnd
    ctypes.wintypes.LPWSTR, # _Out_ lpString
    ctypes.c_int,)   # _In_  nMaxCount

class GameWindow():
    def __init__(self, name):
        self.name = name

        self.window_info, self.window_handle = self.find_window()
        self.rect = WindowRect(self.window_handle)

    def move_to_foreground(self):
        user32.ShowWindow(self.window_handle, user32_SW.SW_RESTORE);
        user32.SetForegroundWindow(self.window_handle)
        time.sleep(0.1)

    def grab_frame(self):
        with mss() as sct:
            self.rect.update()
            monitor = {"top": self.rect.top, "left": self.rect.left, "width": self.rect.width, "height": self.rect.height}
            #monitor = (self.rect.left, self.rect.top, self.rect.right, self.rect.bottom)       #alternate form of grabframe
            return np.array(sct.grab(monitor))[:, :, :-1]

    def local_to_global(self, point):
        return np.array([point[0] + self.rect.left, point[1] + self.rect.top])

    def find_window(self):
        results = []
        @WNDENUMPROC
        def enum_proc(hWnd, lParam):
            pid = ctypes.wintypes.DWORD()
            tid = user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            if title.value.find(self.name) > -1:
                results.append((WindowInfo(pid.value, title.value), hWnd))
            return True
        user32.EnumWindows(enum_proc, 0)
        return None if len(results) == 0 else results[0]


class WindowRect():
    def __init__(self, window_handle):
        self.window_handle = window_handle
        self.update()

    def update(self):
        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(self.window_handle, ctypes.byref(rect))

        self.left = rect.left
        self.right = rect.right
        self.width = abs(rect.right - rect.left)

        self.top = rect.top
        self.bottom = rect.bottom
        self.height = abs(rect.bottom - rect.top)

    def center(self):
        x = int(self.left + self.width / 2)
        y = int(self.top + self.height / 2)
        print("{} {}".format(self.bottom, self.top))
        return (x, y)



 