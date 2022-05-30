import sys
from tkinter import HORIZONTAL, Grid
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from numpy import full
from pip import main
from recording import *
from win_handle import minimize_window
from config import *
import datetime
import filedialogs
import glo

glo._init()  # 初始化全局变量
glo.set_value('RECORD_STATUS_FLAG', 0)  # 0即停止录制状态  1是正在录制状态  2是暂停录制状态'


class MainWindow(QMainWindow):
    """
        界面类, 使用PyQt5绘制界面
    """

    def __init__(self):
        super().__init__()
        # 全局载入qss文件
        # with open(os.path.dirname(__file__) + './sr_viewer.qss',
        #           'r',
        #           encoding='utf-8') as f:
        #     self.setStyleSheet(f.read())
        self.setStyleSheet("""
            QPlainTextEdit { background: #fffff0 } 
            QLabel{color:#000000;font-size:16px;}
        """)
        self.initUI()  # 绘制界面

    def initUI(self):
        #设置窗口的位置和大小,x y w h
        # self.setGeometry(300, 300, 300, 220)
        #设置窗口的标题
        self.setWindowTitle(TITLE)
        # 设置图标
        self.setWindowIcon(QIcon(ICO_LOGO))
        # 调整窗口大小
        self.resize(420, 350)
        # 选项卡
        self.tabwidget = QTabWidget(self)
        # self.tabwidget.setTabPosition(2) 设置选项卡所处位置
        self.tabwidget.resize(420, 350)
        self.tab_record = QWidget()
        self.tab_gif = QWidget()
        self.tab_shortcuts = QWidget()
        self.tab_aboutus = QWidget()

        self.tabwidget.addTab(self.tab_record, '录屏')
        self.tabwidget.addTab(self.tab_gif, '制作gif')
        self.tabwidget.addTab(self.tab_shortcuts, '快捷键')
        self.tabwidget.addTab(self.tab_aboutus, '关于我们')

        # 录屏页面布局
        layout_record = QGridLayout(self.tab_record)
        record_label_mode = QLabel('录屏方式:')
        record_label_storage = QLabel('存储位置:')
        record_label_type = QLabel('视频格式:')
        # record_label_frame = QLabel('帧数:')
        record_label_intent = QLabel('显示范围:')
        record_label_definition = QLabel('清晰度:')
        record_label_screen_voice = QLabel('背景声音:')
        record_label_human_voice = QLabel('麦克风:')

        record_labels = [
            record_label_mode, record_label_storage, record_label_type,
            record_label_intent, record_label_definition,
            record_label_screen_voice, record_label_human_voice
        ]
        i, j = 0, 0
        for rl in record_labels:
            layout_record.addWidget(rl, *(i, j, 1, 1))
            # if rl == record_label_type:
            #     j = 2
            # else:
            i += 1
            j = 0

        self.record_input_mode_group = QButtonGroup(self.tab_record)
        record_input_mode_full = QRadioButton('全屏录制')
        record_input_mode_self = QRadioButton('自定义录制')
        record_input_mode_program = QRadioButton('程序窗口录制')
        self.record_input_mode_group.addButton(record_input_mode_full, 1)
        self.record_input_mode_group.addButton(record_input_mode_self, 2)
        self.record_input_mode_group.addButton(record_input_mode_program, 3)
        layout_record.addWidget(record_input_mode_full, *(0, 1))
        layout_record.addWidget(record_input_mode_self, *(0, 2))
        # layout_record.addWidget(record_input_mode_program, *(0, 3))
        record_input_mode_full.setChecked(True)
        record_input_mode_program.setCheckable(False)

        self.storage_path_text = QLineEdit(
            os.path.dirname(__file__) + '\\' +
            datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.avi')
        storage_path_select = QPushButton('选择')
        layout_record.addWidget(self.storage_path_text, *(1, 1, 1, 2))
        layout_record.addWidget(storage_path_select, *(1, 3))
        storage_path_select.clicked.connect(self.select_storage_path)

        self.record_type = QComboBox(self)
        self.record_type.addItem('avi')
        self.record_type.addItem('mp4')  # MP42/MP4V
        layout_record.addWidget(self.record_type, *(2, 1))
        self.record_type.currentIndexChanged.connect(
            self.change_storage_path_endwith)

        # self.record_frame = QComboBox(self)
        # self.record_frame.addItem('25')
        # self.record_frame.addItem('30')
        # self.record_frame.addItem('35')
        # layout_record.addWidget(self.record_frame, *(3, 1))

        self.record_intent = QComboBox(self)
        # self.record_intent.addItem('是')
        self.record_intent.addItem('否')
        layout_record.addWidget(self.record_intent, *(3, 1))

        self.record_definition = QComboBox(self)
        self.record_definition.addItem('高')
        layout_record.addWidget(self.record_definition, *(4, 1))

        self.has_bg_voice_group = QButtonGroup(self.tab_record)
        has_bg_voice_true = QRadioButton('是')
        has_bg_voice_false = QRadioButton('否')
        self.has_bg_voice_group.addButton(has_bg_voice_true, 1)
        self.has_bg_voice_group.addButton(has_bg_voice_false, 2)
        has_bg_voice_true.setCheckable(False)
        has_bg_voice_false.setChecked(True)
        layout_record.addWidget(has_bg_voice_true, *(5, 1))
        layout_record.addWidget(has_bg_voice_false, *(5, 2))

        self.has_human_voice_group = QButtonGroup(self.tab_record)
        has_human_voice_true = QRadioButton('是')
        has_human_voice_false = QRadioButton('否')
        self.has_human_voice_group.addButton(has_human_voice_true, 1)
        self.has_human_voice_group.addButton(has_human_voice_false, 2)
        has_human_voice_false.setChecked(True)
        layout_record.addWidget(has_human_voice_true, *(6, 1))
        layout_record.addWidget(has_human_voice_false, *(6, 2))

        self.btn_toggle_record = QPushButton("开始录制")
        layout_record.addWidget(self.btn_toggle_record, *(i, 1, 1, 2))
        self.btn_toggle_record.clicked.connect(self.toggle_record_status)

        self.btn_pause_record = QPushButton("暂停录制")
        self.btn_pause_record.setVisible(False)
        layout_record.addWidget(self.btn_pause_record, *(i, 3, 1, 1))
        self.btn_pause_record.clicked.connect(self.pause_record)

        # 制作gif页面布局
        layout_gif = QVBoxLayout(self.tab_gif)
        gif_text = QPlainTextEdit('功能开发中,敬请期待')
        layout_gif.addWidget(gif_text)

        # 快捷键页面布局
        layout_shortcuts = QVBoxLayout(self.tab_shortcuts)
        shorcuts_text = QPlainTextEdit('功能开发中,敬请期待')
        layout_shortcuts.addWidget(shorcuts_text)

        # 关于我们页面布局
        layout_aboutus = QVBoxLayout(self.tab_aboutus)
        aboutus_text = QPlainTextEdit(ABOUT_US_TEXT)
        layout_aboutus.addWidget(aboutus_text)

    def pause_record(self):
        if glo.get_value('RECORD_STATUS_FLAG') == 2:
            # 当点击继续录制时
            self.btn_pause_record.setText("暂停录制")
            self.btn_toggle_record.setText('结束录制')
            glo.set_value('RECORD_STATUS_FLAG', 1)
        else:
            # 当点击暂停录制时
            self.btn_toggle_record.setText('暂停中.直接结束录制')
            self.btn_pause_record.setText("继续录制")
            glo.set_value('RECORD_STATUS_FLAG', 2)

    def toggle_record_status(self):

        if glo.get_value('RECORD_STATUS_FLAG') == 0:
            # 点击开始录制后
            self.btn_toggle_record.setText('结束录制')
            self.btn_pause_record.setVisible(True)
            glo.set_value('RECORD_STATUS_FLAG', 1)
            self.work()
        elif glo.get_value('RECORD_STATUS_FLAG') == 1 or glo.get_value(
                'RECORD_STATUS_FLAG') == 2:
            # 点击结束录制或者直接结束录制时
            self.btn_toggle_record.setText('开始录制')
            # 每次结束录制后要修改下存储路径的 文件名，不然就跟上次重复了
            storage_path_main_list = self.storage_path_text.text().split(
                '\\')[:-1]
            storage_path_main = ''
            for s in storage_path_main_list:
                s = s + '\\'
                storage_path_main += s

            storage_path = storage_path_main + datetime.datetime.now(
            ).strftime('%Y%m%d%H%M%S') + '.' + self.record_type.currentText()
            self.storage_path_text.setText(storage_path)
            self.btn_pause_record.setVisible(False)
            glo.set_value('RECORD_STATUS_FLAG', 0)

    def work(self):
        """
            创建一个录屏的线程并启动
        """
        if self.record_input_mode_group.checkedButton(
        ) == self.record_input_mode_group.button(1):
            record_mode = 'full'
        elif self.record_input_mode_group.checkedButton(
        ) == self.record_input_mode_group.button(2):
            record_mode = 'self'
        else:
            record_mode = 'program'

        storage_path = self.storage_path_text.text()
        record_type = self.record_type.currentText()
        if record_type == 'mp4':
            record_type = 'mp4v'
        elif record_type == 'avi':
            record_type = 'XVID'
        else:
            raise Exception('record_type is wrong')
        # record_frame = int(self.record_frame.currentText())
        record_intent = self.record_intent.currentText()
        if record_intent == '是':
            record_intent = True
        else:
            record_intent = False

        if self.has_bg_voice_group.checkedButton(
        ) == self.has_bg_voice_group.button(1):
            has_bg_voice = True
        else:
            has_bg_voice = False

        if self.has_human_voice_group.checkedButton(
        ) == self.has_human_voice_group.button(1):
            has_human_voice = True
        else:
            has_human_voice = False

        self.workThread = WorkThread(record_mode, storage_path, record_type,
                                     record_intent, has_bg_voice,
                                     has_human_voice)
        self.workThread.start()

    def select_storage_path(self):
        """
            设置存储路径,注意要处理自己修改了视频名称这一特殊情况
        """
        storage_path_main = filedialogs.open_folder_dialog('选择文件夹路径', 'gbk')
        if storage_path_main is None:
            storage_path_main = os.path.dirname(__file__)
        storage_filename = self.storage_path_text.text().split('\\')[-1].split(
            '.')[0]
        try:
            if datetime.datetime.strptime(storage_filename,
                                          '%Y%m%d%H%M%S') != storage_filename:
                storage_path = storage_path_main + '\\' + storage_filename + '.' + self.record_type.currentText(
                )
            else:
                storage_path = storage_path_main + '\\' + datetime.datetime.now(
                ).strftime(
                    '%Y%m%d%H%M%S') + '.' + self.record_type.currentText()
        except:

            storage_path = storage_path_main + '\\' + storage_filename + '.' + self.record_type.currentText(
            )

        self.storage_path_text.setText(storage_path)

    def change_storage_path_endwith(self):
        storage_path = self.storage_path_text.text().split('.')[0]
        storage_path = storage_path + '.' + self.record_type.currentText()
        self.storage_path_text.setText(storage_path)


class WorkThread(QThread):
    """
        多线程
    """

    def __init__(self, record_mode, storage_path, record_type, record_intent,
                 has_bg_voice, has_human_voice) -> None:
        super(
            WorkThread,
            self).__init__()  # python3中等同于super().__init__() super主要用来解决多继承问题
        self.record_mode = record_mode
        self.storage_path = storage_path
        self.record_type = record_type
        # self.record_frame = record_frame
        self.record_intent = record_intent
        self.has_bg_voice = has_bg_voice
        self.has_human_voice = has_human_voice

    def run(self):
        ucfg = UserConfig(USER_CONFIG_PATH)
        if ucfg.get_value('conf', 'fps') == "8":
            revise_fps()
        if self.record_mode == 'self':
            # minimize_window()
            # fps,count,size,video_time,real_time,suggest_fps =
            if self.has_human_voice:
                Recording_with_human_voice(self.record_mode, self.storage_path,
                                           self.record_type,
                                           self.record_intent)
            else:
                Recording(self.record_mode, self.storage_path,
                          self.record_type, self.record_intent)
            # print(fps,count,size,video_time,real_time,suggest_fps)
        elif self.record_mode == 'full':
            # minimize_window()
            if self.has_human_voice:
                Recording_with_human_voice(self.record_mode, self.storage_path,
                                           self.record_type,
                                           self.record_intent)
            else:
                Recording(self.record_mode, self.storage_path,
                          self.record_type, self.record_intent)
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())