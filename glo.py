def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    # 定义一个全局变量
    _global_dict[key] = value


def get_value(key):
    # 获得一个全局变量
    try:
        return _global_dict[key]
    except:
        print('获取不到该变量')