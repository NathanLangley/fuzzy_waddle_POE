
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

def add_guas(mean, variance):
    return np.random.normal(mean, math.sqrt(variance))

def guas(variance):
    return np.random.normal(0, math.sqrt(variance))