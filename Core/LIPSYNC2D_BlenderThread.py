import queue
from typing import Callable

from .LIPSYNC2D_SingletonMeta import SingletonMeta


class LIPSYNC2D_BlenderThread(metaclass=SingletonMeta):
    execution_queue= queue.Queue()

    @classmethod
    def run_in_main_thread(cls, func: Callable) -> None:
        cls.execution_queue.put(func)

    @classmethod
    def execute_queued_functions(cls):
        while not cls.execution_queue.empty():
            func = cls.execution_queue.get()
            func()
        return 1.0


