
import ctypes
import pyautogui
import os, sys, random
from collections import namedtuple
import numpy as np
import cv2 as cv
import time
import math





def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def add_log_guas(number, size):
    return number + np.random.normal(0, math.log(size,2))

def guas(number):
    return np.random.normal(0, number)