"""windows操作"""

from pynput.keyboard import Key, Controller
import win32gui, win32api, win32con, win32ui


def win_rectangle():
    """未实现需求: 在windows桌面上画个矩形框, 且不影响桌面使用"""
    # 获取桌面的pyhandle
    win = win32gui.GetDesktopWindow()
    # left, top, right, bottom = win32gui.GetWindowRect(win)
    # print(left, top, right, bottom)
    # print(win)
    dc = win32gui.GetDC(win)

    # 尝试一: 没法调整线宽
    # win32gui.MoveToEx(dc,0,0)
    # win32gui.LineTo(dc,2560,0)
    # win32gui.LineTo(dc,2560,1440)
    # win32gui.LineTo(dc,0,1440)

    # 尝试二: 不知道为啥没用
    # win32gui.DrawEdge(dc,(10, 10, 10, 10),win32con.BDR_RAISEDINNER,win32con.BF_RECT)

    # 尝试三
    hPen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0,
                                                                 255))  # 定义框颜色
    win32gui.SelectObject(dc, hPen)
    hbrush = win32gui.GetStockObject(win32con.NULL_BRUSH)  # 定义透明画刷，这个很重要！！
    prebrush = win32gui.SelectObject(dc, hbrush)
    win32gui.Rectangle(dc, 0, 0, 2560, 1440)  # 左上到右下的坐标
    win32gui.SelectObject(dc, prebrush)


def minimize_window():
    """
        minimize_window函数是为了在运行时缩小窗口
        win+方向下 可以实现
        使用pynput库
    """
    keyboard = Controller()
    with keyboard.pressed(Key.cmd_l):
        keyboard.press(Key.down)
        keyboard.release(Key.down)


