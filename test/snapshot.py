"""测试文件, 不涉及项目功能
    测试截屏实现方式"""
# # ----------------------------------------------------------
# PIL
import cv2
import os
from PIL import ImageGrab
import numpy as np
from ctypes import windll

user32 = windll.user32
user32.SetProcessDPIAware()

# window_size = user32.get_window_info()

if os.path.exists('xx.jpg'):
    os.remove('xx.jpg')

# captureImage = ImageGrab.grab((0,0,int(1920*1.25),int(1080*1.25)))
captureImage = ImageGrab.grab()
width, height = captureImage.size
img = cv2.cvtColor(np.asarray(captureImage), cv2.COLOR_RGB2BGR)
cv2.imwrite('./xx.png', img)
cv2.waitKey(0)

# # ----------------------------------------------------------
# # PYQT5
# import sys
# from PyQt5.QtWidgets import *
# app = QApplication(sys.argv)
# screen = QApplication.primaryScreen()
# img = screen.grabWindow(QApplication.desktop().winId()).toImage()
# img.save("./screenshot.jpg")

# # ----------------------------------------------------------
# mss
# from mss import mss
# from PIL import Image
# def capture_screenshot():
#     # Capture entire screen
#     with mss() as sct:
#         monitor = sct.monitors[1]
#         sct_img = sct.grab(monitor)
#         # Convert to PIL/Pillow Image
#         return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

# img = capture_screenshot()
# img.show()

# # ----------------------------------------------------------
# # pywin32
# import win32gui, win32ui, win32con, win32api
# hwin = win32gui.GetDesktopWindow()
# width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
# height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
# left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
# top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
# hwindc = win32gui.GetWindowDC(hwin)
# srcdc = win32ui.CreateDCFromHandle(hwindc)
# memdc = srcdc.CreateCompatibleDC()
# bmp = win32ui.CreateBitmap()
# w = int(1920)
# h = int(1080)
# bmp.CreateCompatibleBitmap(srcdc, w, h)
# memdc.SelectObject(bmp)
# memdc.BitBlt((0, 0), (w, h), srcdc, (left, top), win32con.SRCCOPY)
# bmp.SaveBitmapFile(memdc, 'screenshot.bmp')

# # ----------------------------------------------------------
# # pyautogui
# import pyautogui,os
# if os.path.exists('xx.jpg'):
#     os.remove('xx.jpg')
# myScreenshot = pyautogui.screenshot()
# myScreenshot.save(r'xx.png')