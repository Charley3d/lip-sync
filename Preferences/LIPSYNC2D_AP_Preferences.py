import os
import threading
from pathlib import Path
from re import match

import bpy
import requests
from vosk import MODEL_DIRS, MODEL_LIST_URL, Model

from ..Core.LIPSYNC2D_VoskWrapper import setextensionpath
from ..LIPSYNC2D_Utils import get_package_name


def online_available_langs():
    """
    Fetches the available language models for lip-syncing from an online source.

    :return: list[tuple[str, str, str]]
        A list of tuples representing the available languages. Each tuple contains:
        - Internal language code
        - Display name
        - A brief description (e.g., ('none', '-- None --', 'No selection')).
    """
    response = requests.get(MODEL_LIST_URL)

    all_langs = [(l["lang"], l["lang_text"]) for l in response.json() if
                 l["lang"] != "all" and l["obsolete"] == "false" and l['type'] == 'small']
    all_langs.sort(key=lambda x: x[1])
    all_langs = [('none', "-- None --", "No selection"), ] + all_langs

    enum_items = [(list(l)[0], list(l)[1], list(l)[0]) for l in all_langs]

    return enum_items


def install_model(self, context):
    """
    Installs the selected language model for lip-syncing asynchronously.

    :param self: bpy.types.AddonPreferences
        The current add-on preferences where the language selection is made.
    :param context: bpy.types.Context
        The Blender context.
    """
    if self.current_lang == "none":
        return
    
    @setextensionpath
    def install_model_thread():
        """
        Executes the model installation process in a separate thread.
    
        This function initializes the installation of the selected Vosk model
        by using the language code provided in the add-on preferences.
        """
        Model(lang=self.current_lang)

    threading.Thread(target=install_model_thread).start()

class LIPSYNC2D_AP_Preferences(bpy.types.AddonPreferences):
    bl_idname = get_package_name() # type: ignore

    available_langs = online_available_langs()
    current_lang: bpy.props.EnumProperty(name="Lip Sync Lang", items=available_langs, update=install_model, default=0) # type: ignore

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.label(text="Language Model")
        row.prop(self, "current_lang", text="") 
        
        draw_model_state(row, self.current_lang)

def patchmodellang(bad_code:str, good_code:str):
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


@patchmodellang("ua", "uk")
@setextensionpath
def draw_model_state(row: bpy.types.UILayout, current_lang: str) -> None:
    """
    Updates the UI to display the current status of the selected language model.

    :param row: bpy.types.UILayout
        The UI layout row on which the display updates are made.
    :param current_lang: str
        The currently selected language code for the model.
    :return: None
    """
    installed = ""
    if current_lang != "none":
        directory = MODEL_DIRS[3] if len(MODEL_DIRS) >= 4 else None
        if directory is not None and Path(directory).exists():
            model_file_list = os.listdir(directory)
            model_file = [model for model in model_file_list if match(f"vosk-model(-small)?-{current_lang}", model)]
            if model_file != []:
                installed = " Installed"
                row.enabled = True
                
            else:
                installed = " Downloading..."
                row.enabled = False
        else:
                installed = " Downloading..."
                row.enabled = False
    row.label(text=installed)



