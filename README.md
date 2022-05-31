# BigBeard —— 大胡子录屏
## 项目介绍
BigBeard(大胡子录屏)是基于GPL协议开源的录屏软件项目。软件仅供个人学习交流使用, 永久免费, 不可用于任何商业用途。

该软件产生于个人居家隔离时期。因游戏录屏时找不到一款免费纯净且简约的录屏软件, 故萌生出自己开发的想法。开发前后耗时共3天, 完成了测试v0.1版, 现阶段软件功能较少, Bug较多, 不跨平台, 只支持windows10, 不适合正式长期使用。

严格来讲, BigBeard尚不能称之为一款软件, 现阶段只是个人练手性质的Demo, 并且个人水平有限, 也不擅长Python客户端开发, 代码较为冗杂混乱, 仅供大家批评交流使用, 同时欢迎大家参与。 

### 相关技术
项目使用Python 3.9.1开发, 向下兼容到Python 3.7。
涉及的主要第三方库有：
- PyQt5==5.15.6   实现UI界面
- opencv-python==4.5.5.64   图像处理
- pypiwin32==223  windows相关处理
- pynput==1.7.6  模拟键盘操作
- Pillow==9.1.1  图像处理
- PyAudio-0.2.11  音频处理

### 目录结构
- sr_viewer.py UI界面绘制和线程管理
- recording.py 录制的核心逻辑
- config.py 一些通用配置
- glo.py 用于跨模块全局变量的管理
- win_handle.py windows相关操作
- ico/* 存放logo图片
- pkg/* 存放用到的wheel
- sr_viewer.qss 全局pyqt5样式, 暂未使用
- test/* 一些测试代码

## 运行
1. 配置虚拟环境
```python
python -m venv venv
. venv/Scripts/activate  # 目前本项目只能运行在windows平台上
```
2. 安装依赖
```python
pip install -r requirements.txt

pip install pkg/PyAudio-0.2.11-cp39-cp39-win_amd64.whl
# 如果不是python3.9, 需要去下载对应版本的whl
# 下载地址: https://www.lfd.uci.edu/~gohlke/pythonlibs/
```
3. 运行
```
python sr_viewer.py
```
![](ico/%E6%BC%94%E7%A4%BA.jpg)
## 打包成exe
```python
pyinstaller.exe  -F -w  -i ico/record256.ico  -n 大胡子录屏  sr_viewer.py
```

## 开发日志
### 已完成事项
> 按时间顺序从前往后
- [新增]实现最核心的全屏录屏功能
- [新增]Logo和初步绘制界面
- [新增]显示存放视频文件的路径
- [新增]可设置存放视频文件路径
- [新增]可设置保存的视频格式,暂支持mp4和avi两种
- [新增]可设置生成视频的帧率(Deprecated)
- [重构]结束录制的功能
- [新增]暂停录制的功能
- [新增]绘制屏幕区域自定义录制的功能
- [修复]录屏被加速的问题(通过读写配置文件获得合适帧率)
- [修复]录屏清晰度的问题(windows自带播放器很清楚, 爱奇艺不清楚, 应该是爱奇艺软件bug, 待进一步观测)

### 待修复Bug
- 录屏时任务栏闪动(Unable to recurrence/复现条件:笔记本外接显示器)

### 下一阶段开发计划
- 屏幕声音抓取
- 麦克风声音抓取
- 自定义屏幕录制时显示一个框来标识范围(需要研究)
- 全屏录制时显示一个框来标识范围(需要研究)
- 录制结束后显示本次录制的相关信息
- 录屏保留一定数量的历史记录
- 录制时在屏幕顶部居中显示快捷操作按钮-停止录制/继续录制/暂停录制等
- 自定义屏幕录制时框选范围可以实时拖拽调节
- 实现录制某个窗口程序的界面
- 实现快捷键操作和自定义设置快捷键的功能
- 新增gif制作功能
- 优化UI界面

## 参与项目
直接发起合并即可
