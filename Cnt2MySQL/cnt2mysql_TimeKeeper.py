from time import time
from functools import wraps
from typing import *

class TimeKeeper:
    """
    该类用于监控并记录本模块各函数运行时间
    """
    used_time = [] # 每一个函数运行时间的列表
    was_called = False # 防止嵌套函数导致的重复记录
    delayed_time = 0 # 去除与用户交互的时间
    def __init__(self) -> None:
        # 没有成员变量
        print("Nothing will be init for TimeKeeper's instance!")
        print(f"TimeKeeper.was_called:{TimeKeeper.was_called}")
        print(f"TimeKeeper.delayed_time:{TimeKeeper.delayed_time}")
        print(TimeKeeper.calculate_used_time())
    @staticmethod
    def calculate_used_time() -> str:
        # 计算所有运行时间
        used_time:float = 0
        for item in TimeKeeper.used_time:
            used_time += item
        return f"used_time:{used_time}"
    @staticmethod
    def time_keeper(func: Callable):
        # 装饰器，将普通函数转换为被监控的函数
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if TimeKeeper.was_called == False:
                start_time = time()
                TimeKeeper.was_called = True
                func(*args, **kwargs)
                TimeKeeper.was_called = False
                in_process = time() - start_time - TimeKeeper.delayed_time
                TimeKeeper.delayed_time = 0
                TimeKeeper.used_time.append(in_process)
            else: func(*args, **kwargs)
        return wrapped_func 
    

