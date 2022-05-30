from operator import length_hint
from tracemalloc import start
from turtle import heading, width
from PIL import ImageGrab
import numpy as np
import cv2
import os
from config import *
import glo
import time
import os
import configparser
from moviepy.editor import *
from moviepy.audio.fx import all
import pyaudio
import wave
# from ctypes import windll
# user32 = windll.user32
# user32.SetProcessDPIAware()


class UserConfig:

    def __init__(self, config_path):
        self.config_path = config_path
        self.init_configfile()
        self.conf = configparser.ConfigParser()
        self.conf.read(self.config_path)

    def init_configfile(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                f.write("[conf]\nfps=8")
        # 待处理，用户修改了配置文件怎么办

    def get_value(
        self,
        section,
        key,
    ):
        # 获取配置文件的信息
        return self.conf.get(section, key)

    def get_conf(self):
        return self.conf

    def write_or_update_value(self, section, key, value):
        self.conf.set(section, key, value)
        with open(self.config_path, 'w', encoding='utf-8') as fw:  # 循环写入
            self.conf.write(fw)


class Region:
    """需要完善的:
        1. 框选范围时背景的清晰度问题
        2. 确认范围的按键问题，支持鼠标
        3. 框选范围时支持拖曳调整，且支持一些辅助功能，如撤回等
    """

    def __init__(self):
        self.frame = ImageGrab.grab()
        self.img = ''
        self.point1 = ()
        self.point2 = ()

    def on_mouse(self, event, x, y, flags, param):
        img2 = self.img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
            self.point1 = (x, y)
            cv2.circle(img2, self.point1, 10, (0, 255, 0), thickness=2)
            cv2.imshow('image', img2)
        elif event == cv2.EVENT_MOUSEMOVE and (
                flags
                & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
            cv2.rectangle(img2, self.point1, (x, y), (255, 0, 0), thickness=2)
            cv2.imshow('image', img2)
        elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
            self.point2 = (x, y)
            cv2.rectangle(img2,
                          self.point1,
                          self.point2, (0, 0, 255),
                          thickness=2)
            cv2.imshow('image', img2)

    def select_roi(self):
        self.img = cv2.cvtColor(np.array(self.frame), cv2.COLOR_RGB2BGR)
        winname = 'image'
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN,
                              cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback(winname, self.on_mouse)
        cv2.putText(self.img,
                    "Press Space to continue", (200, 400),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 200, 0),
                    thickness=2)
        cv2.imshow(winname, self.img)
        while True:
            k = cv2.waitKey(0)
            if k == 32:
                break
        cv2.destroyAllWindows()
        try:
            return self.point1, self.point2
        except:
            return None


def revise_fps():
    ucfg = UserConfig(USER_CONFIG_PATH)
    storage_path = os.path.dirname(__file__) + '/test.avi'
    fps = Recording(storage_mode='full',
                    storage_path=storage_path,
                    storage_type='XVID',
                    record_intent=False,
                    get_fps_flag=True)
    ucfg.write_or_update_value('conf', 'fps', fps)
    if os.path.exists(storage_path):
        os.remove(storage_path)


def Recording(storage_mode='full',
              storage_path=os.path.dirname(__file__) + '/test.avi',
              storage_type='XVID',
              record_intent=False,
              get_fps_flag=False):
    if storage_mode == 'self':
        r = Region().select_roi()
        record_region = (r[0][0], r[0][1], r[1][0], r[1][1])  # 自定义录像的位置
    elif storage_mode == 'full':
        record_region = None

    ucfg = UserConfig(USER_CONFIG_PATH)
    fps = int(ucfg.get_value('conf', 'fps'))
    # 录屏核心代码
    image = ImageGrab.grab(record_region)  # 获取指定范围的屏幕对象
    width, height = image.size
    fourcc = cv2.VideoWriter_fourcc(*storage_type)
    # print(width,height)
    video = cv2.VideoWriter(storage_path, fourcc, fps, (width, height))
    start_time = time.time()
    n = 0
    while True:
        captureImage = ImageGrab.grab(record_region)
        frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
        video.write(frame)
        if get_fps_flag:
            n = n + 1
            if n > 20:
                break

        if glo.get_value('RECORD_STATUS_FLAG') == 0:
            break
        if glo.get_value('RECORD_STATUS_FLAG') == 2:
            exit_all = False
            # 暂停录制时跳入一层循环
            while True:
                # 等待退出该循环继续录制
                if glo.get_value('RECORD_STATUS_FLAG') == 1:
                    break
                if glo.get_value('RECORD_STATUS_FLAG') == 0:
                    # 如果等来了直接结束，就退两层循环
                    exit_all = True

                    break
            if exit_all:
                break
    final_time = time.time()

    video.release()
    cv2.destroyAllWindows()
    if get_fps_flag:
        return get_fps(storage_path, start_time, final_time)


def get_fps(storage_path, start_time, final_time):
    # get record information
    video_f = cv2.VideoCapture(storage_path)
    fps = video_f.get(cv2.CAP_PROP_FPS)
    count = video_f.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(video_f.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video_f.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    suggest_fps = int(fps * ((int(count) / fps) / (final_time - start_time)))
    # print(suggest_fps)
    # print('当前帧率=%.1f'%fps)
    # print('当前帧数=%.1f'%count)
    # print('分辨率',size)
    # print('视频时间=%.3f秒'%(int(count)/fps))
    # print('录制时间=%.3f秒'%(final_time-start_time))
    # print('推荐帧率=%.2f'%suggest_fps)
    video_f.release()
    cv2.destroyAllWindows()
    return str(suggest_fps)


def Recording_with_human_voice(storage_mode='full',
                               storage_path=os.path.dirname(__file__) +
                               '/test.avi',
                               storage_type='XVID',
                               record_intent=False,
                               get_fps_flag=False):
    if os.path.exists(WAVE_OUTPUT_FILENAME):
        os.remove(WAVE_OUTPUT_FILENAME)

    p = pyaudio.PyAudio()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    audio_record_flag = True

    def callback(in_data, frame_count, time_info, status):
        wf.writeframes(in_data)
        if audio_record_flag:
            return (in_data, pyaudio.paContinue)
        else:
            return (in_data, pyaudio.paComplete)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    stream_callback=callback)

    if storage_mode == 'self':
        r = Region().select_roi()
        record_region = (r[0][0], r[0][1], r[1][0], r[1][1])  # 自定义录像的位置
    elif storage_mode == 'full':
        record_region = None

    ucfg = UserConfig(USER_CONFIG_PATH)
    fps = int(ucfg.get_value('conf', 'fps'))
    # 录屏核心代码
    image = ImageGrab.grab(record_region)  # 获取指定范围的屏幕对象
    width, height = image.size
    fourcc = cv2.VideoWriter_fourcc(*storage_type)
    # print(width,height)
    video = cv2.VideoWriter(storage_path, fourcc, fps, (width, height))
    start_time = time.time()
    n = 0
    stream.start_stream()
    while True:
        captureImage = ImageGrab.grab(record_region)
        frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
        video.write(frame)
        if get_fps_flag:
            n = n + 1
            if n > 20:
                break

        if glo.get_value('RECORD_STATUS_FLAG') == 0:
            break
        if glo.get_value('RECORD_STATUS_FLAG') == 2:
            exit_all = False
            # 暂停录制时跳入一层循环
            while True:
                # 等待退出该循环继续录制
                if glo.get_value('RECORD_STATUS_FLAG') == 1:
                    break
                if glo.get_value('RECORD_STATUS_FLAG') == 0:
                    # 如果等来了直接结束，就退两层循环
                    exit_all = True

                    break
            if exit_all:
                break
    final_time = time.time()
    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()
    video.release()
    cv2.destroyAllWindows()

    audioclip = AudioFileClip(WAVE_OUTPUT_FILENAME)
    videoclip = VideoFileClip(storage_path)
    videoclip2 = videoclip.set_audio(audioclip)
    video = CompositeVideoClip([videoclip2])
    video.write_videofile(storage_path, codec='mpeg4')
    if os.path.exists(WAVE_OUTPUT_FILENAME):
        os.remove(WAVE_OUTPUT_FILENAME)

    if get_fps_flag:
        return get_fps(storage_path, start_time, final_time)


if __name__ == "__main__":
    glo._init()
    glo.set_value('RECORD_STATUS_FLAG', 1)
    revise_fps()