import os
import pyaudio

ICO_LOGO = os.path.dirname(__file__) + '/ico/record256.ico'
TITLE = '大胡子录屏 测试版 v0.1'
ABOUT_US_TEXT = '欢迎使用大胡子录屏软件。\n当前版本:测试版 v0.1。\n\n该软件基于GPL协议开源,不可用于任何商业用途。\n项目地址:  https://github.com/xiaomaodan110/bigbeard  \n\n如您对软件有任何宝贵的建议和其他问题,可加QQ群 582727724'
USER_CONFIG_PATH = os.path.dirname(__file__) + '/大胡子录屏配置文件.cfg'

# 录音配置
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "pqnwovqinoug.wav"
