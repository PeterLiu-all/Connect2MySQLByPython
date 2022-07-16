from time import time
from functools import wraps
from typing import *


class TimeKeeper:
    """
    该类用于监控并记录本模块各函数运行时间
    """

    def __init__(self) -> None:
        # 没有成员变量
        self.used_time = []  # 每一个函数运行时间的列表
        self.was_called = False  # 防止嵌套函数导致的重复记录
        self.delayed_time = 0  # 去除与用户交互的时间

    def calculate_used_time(self) -> str:
        # 计算所有运行时间
        used_time: float = 0
        for item in self.used_time:
            used_time += item
        return f"used_time:{used_time}s"

    def time_monitor(self, func: Callable):
        # 装饰器，将普通函数转换为被监控的函数
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            res = None
            if self.was_called == False:
                start_time = time()
                self.was_called = True
                res = func(*args, **kwargs)
                self.was_called = False
                in_process = time() - start_time - self.delayed_time
                self.delayed_time = 0
                self.used_time.append(in_process)
            else:
                res = func(*args, **kwargs)
            return res
        return wrapped_func


time_keeper = TimeKeeper()
