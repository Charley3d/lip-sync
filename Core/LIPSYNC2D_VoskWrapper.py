import pathlib
from typing import cast

import bpy
from vosk import MODEL_DIRS

from ..LIPSYNC2D_Utils import get_package_name


def setextensionpath(func):
    def wrapper(*args, **kwargs):
        package_name = cast(str, get_package_name())
        MODEL_DIRS[3] = pathlib.Path(bpy.utils.extension_path_user(package_name, path="cache", create=True))

        if not MODEL_DIRS[3].exists():
            MODEL_DIRS[3].mkdir(parents=True, exist_ok=True)
            
        result = func(*args, **kwargs)
        return result
    return wrapper