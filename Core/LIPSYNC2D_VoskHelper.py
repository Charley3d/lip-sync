import json
import os
import pathlib
import threading
from typing import Callable, Literal, cast
from vosk import MODEL_DIRS, MODEL_LIST_URL, Model

import bpy
import requests
from vosk import MODEL_DIRS

from .LIPSYNC2D_BlenderThread import LIPSYNC2D_BlenderThread

from ..LIPSYNC2D_Utils import get_package_name

class LIPSYNC2D_VoskHelper():

    @staticmethod
    def setextensionpath(func):
        def wrapper(*args, **kwargs):
            MODEL_DIRS[3] = LIPSYNC2D_VoskHelper.get_extension_path("cache")
            model_path = pathlib.Path(MODEL_DIRS[3])

            if not model_path.exists():
                model_path.mkdir(parents=True, exist_ok=True)
                
            result = func(*args, **kwargs)
            return result
        return wrapper


    @staticmethod
    def get_extension_path(subfolder: Literal['cache','tmp','bin', ''] = "") -> pathlib.Path:
        package_name = cast(str, get_package_name())
        return pathlib.Path(bpy.utils.extension_path_user(package_name, path=subfolder, create=True))
    

    @staticmethod
    def patchmodellang(bad_code:str, good_code:str) -> Callable:
        """
        A decorator for replacing an invalid language code with a valid one during function execution.
        
        :param bad_code: str
            The incorrect language code to be replaced.
        :param good_code: str
            The correct language code to use instead.
        :return: callable
            The wrapper function that performs the substitution.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                _, lang = args  # Your original unpacking logic
                if lang == bad_code:
                    lang = good_code
                
                args = (_, lang)
                result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def get_available_langs_online(use_cached_list = True) -> list[tuple[str, str, str]]:
        """
        List available language models for lip-syncing from a cached list..

        :return: list[tuple[str, str, str]]
            A list of tuples representing the available languages. Each tuple contains:
            - Internal language code
            - Display name
            - A brief description (e.g., ('none', '-- None --', 'No selection')).
        """
        langs_list = []
        all_langs = []
        cached_langs_list_file = LIPSYNC2D_VoskHelper.get_language_list_file()

        if use_cached_list and os.path.isfile(cached_langs_list_file):
            try:
                with open(cached_langs_list_file, "r", encoding="utf-8") as f:
                    langs_list = json.load(f)
            except Exception as e:
                raise Exception(f"Error while loading cached files index.{e}")

        if langs_list:
            all_langs = [(l["lang"], l["lang_text"]) for l in langs_list if
                        l["lang"] != "all" and l["obsolete"] == "false" and l['type'] == 'small']
            all_langs.sort(key=lambda x: x[1])

        all_langs = [('none', "-- None --", "No selection"), ] + all_langs

        enum_items = [(list(l)[0], list(l)[1], list(l)[0]) for l in all_langs]

        return enum_items

    @staticmethod
    def get_available_langs_offline() -> list[tuple[str, str, str]]:
        ext_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
        all_offline_langs = []

        if not ext_path.is_dir():
            return all_offline_langs

        cached_langs_list_file = ext_path / "languages_list.json"

        if cached_langs_list_file.is_file():
            try:
                with open(cached_langs_list_file, "r", encoding="utf-8") as f:
                    langs_list = json.load(f)
            except Exception as e:
                raise Exception(f"Error while loading cached files index. {e}")

            all_dir_names = {
                lang["name"]: (lang["lang"], lang["lang_text"], lang["lang"])
                for lang in langs_list
                if lang["type"] == "small" and lang["obsolete"] == "false"
            }

            all_offline_langs = [all_dir_names[pathlib.Path(model_dir).name] for model_dir in ext_path.iterdir() if
                                model_dir.is_dir() and pathlib.Path(model_dir).name in all_dir_names]

        all_offline_langs = [('none', "-- None --", "No selection")] + all_offline_langs
        return all_offline_langs

    @staticmethod
    def cache_online_langs_list() -> None:
        list_request = requests.get(MODEL_LIST_URL)
        if list_request:
            try:
                with open(LIPSYNC2D_VoskHelper.get_language_list_file(), "w", encoding="utf-8") as f:
                    full_list = list_request.json()
                    filter_list = [item for item in full_list if item["type"] == "small" and item["obsolete"] == "false"]
                    json.dump(filter_list, f, ensure_ascii=False)
            except Exception as e:
                raise Exception(f"Error while creating cached file index: {e}")

    @staticmethod
    def get_language_list_file() -> pathlib.Path:
        return LIPSYNC2D_VoskHelper.get_extension_path("cache") / "languages_list.json"

    @staticmethod
    def get_available_languages(_, context) -> list[tuple[str, str, str]]:
        available_langs = LIPSYNC2D_VoskHelper.get_available_langs_online() if bpy.app.online_access else LIPSYNC2D_VoskHelper.get_available_langs_offline()
        return available_langs

    @staticmethod
    def install_model(addon_prefs, context):
        """
        Installs the selected language model for lip-syncing asynchronously.

        :param self: bpy.types.AddonPreferences
            The current add-on preferences where the language selection is made.
        :param context: bpy.types.Context
            The Blender context.
        """
        if addon_prefs.current_lang == "none":
            return
        
        prefs = context.preferences.addons[get_package_name()].preferences # type: ignore
        prefs.is_downloading = True
        
        @LIPSYNC2D_VoskHelper.setextensionpath
        def install_model_thread() -> None:
            """
            Executes the model installation process in a separate thread.
        
            This function initializes the installation of the selected Vosk model
            by using the language code provided in the add-on preferences.
            """
            bthread = LIPSYNC2D_BlenderThread()
            bthread.run_in_main_thread(lambda: setattr(prefs, "is_downloading", False))
            Model(lang=addon_prefs.current_lang)
            bthread.execute_queued_functions()

        threading.Thread(target=install_model_thread).start()
