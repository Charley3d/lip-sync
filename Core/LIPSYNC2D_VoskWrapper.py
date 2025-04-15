import pathlib
from typing import cast
from vosk import Model, MODEL_DIRS

import bpy

from ..LIPSYNC2D_Utils import get_package_name

class LIPSYNC2D_VoskWrapper():
    def __init__(self) -> None:
        package_name = cast(str, get_package_name())
        MODEL_DIRS[3] = pathlib.Path(bpy.utils.extension_path_user(package_name, path="cache", create=True))

    def get_model(self, lang: str):
        if not MODEL_DIRS[3].exists():
            MODEL_DIRS[3].mkdir(parents=True, exist_ok=True)
        Model(lang=lang)

def extensionpath(func):
    def wrapper(*args, **kwargs):
        package_name = cast(str, get_package_name())
        MODEL_DIRS[3] = pathlib.Path(bpy.utils.extension_path_user(package_name, path="cache", create=True))

        if not MODEL_DIRS[3].exists():
            MODEL_DIRS[3].mkdir(parents=True, exist_ok=True)
            
        result = func(*args, **kwargs)
        return result
    return wrapper