import os
import threading
from pathlib import Path
from re import match

import bpy
import requests
from phonemizer.backend import EspeakBackend
from vosk import MODEL_DIRS, MODEL_LIST_URL, Model

from ..Core.LIPSYNC2D_EspeakInspector import LIPSYNC2D_EspeakInspector
from ..LIPSYNC2D_Utils import get_package_name


def update_espeak_lib(self, context: bpy.types.Context):
    espeak_path = self["espeak_path"]

    if espeak_path == "":
        return
    
    if not os.path.isfile(espeak_path):
        self["espeak_path"] = ""
        return
    
    espeak_inspector = LIPSYNC2D_EspeakInspector()

    try:
        lib_path = espeak_inspector.find_library_path(espeak_path)
    except Exception as e:
        self["espeak_path"] = ""
        return

    if lib_path is None:
        self["espeak_path"] = ""
        return

    EspeakBackend.set_library(espeak_path)

def online_available_langs():
    response = requests.get(MODEL_LIST_URL)

    all_langs = [(l["lang"], l["lang_text"]) for l in response.json() if l["lang"] != "all" and l["obsolete"] == "false" and l['type'] == 'small']
    all_langs.sort(key=lambda x: x[1])
    all_langs = [('none', "-- None --", "No selection"),] + all_langs

    enum_items = [(list(l)[0],list(l)[1],list(l)[0]) for l in all_langs]

    return enum_items

def install_model(self, context):
    if self.current_lang == "none":
        return
    
    def install_model_thread():
        if not MODEL_DIRS[3].exists():
            MODEL_DIRS[3].mkdir(parents=True, exist_ok=True)
        Model(lang=self.current_lang)

    threading.Thread(target=install_model_thread).start()

class LIPSYNC2D_AP_Preferences(bpy.types.AddonPreferences):
    bl_idname = get_package_name() # type: ignore
    espeak_inspector = LIPSYNC2D_EspeakInspector()
    espeak_path: bpy.props.StringProperty(name="Path to espeak lib file",subtype='FILE_PATH', default="", update=update_espeak_lib) # type: ignore
    available_langs = online_available_langs()
    current_lang: bpy.props.EnumProperty(name="Lip Sync Lang", items=available_langs, update=install_model, default=0) # type: ignore

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="This addon needs espeak-ng library.")
        
        row = layout.row()
        row.operator("lib.find_espeak_lib", text="Find Lib on my System")
 
        row = layout.row()
        row.label(text="Espeak path (.dll / .so / .dylib)")
        row.prop(self, "espeak_path", text="")

        row = layout.row(align=True)
        row.label(text="Language Model")
        row.prop(self, "current_lang", text="") 
        
        draw_model_state(row, self.current_lang)


def draw_model_state(row: bpy.types.UILayout, current_lang: str) -> None:
    installed = ""
    if current_lang != "none":
        for directory in MODEL_DIRS:
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



