import os
import bpy
from .LIPSYNC2D_EspeakInspector import LIPSYNC2D_EspeakInspector
from phonemizer.backend import EspeakBackend

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


class LIPSYNC2D_AP_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__ # type: ignore
    espeak_inspector = LIPSYNC2D_EspeakInspector()
    espeak_path: bpy.props.StringProperty(name="Path to espeak lib file",subtype='FILE_PATH', default="", update=update_espeak_lib) # type: ignore

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="This addon needs espeak-ng library.")
        
        # if platform.system() is not 'Windows':
        row = layout.row()
        row.operator("lib.find_espeak_lib", text="Find Lib on my System")
 
        row = layout.row()
        row.label(text="Espeak path (.dll / .so / .dylib)")
        row.prop(self, "espeak_path", text="")


