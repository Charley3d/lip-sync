from typing import Literal

import bpy
from bpy.types import Context

from .LIPSYNC2D_EspeakInspector import LIPSYNC2D_EspeakInspector


class LIPSYNC2D_OT_FindEspeak(bpy.types.Operator):
    bl_idname="lib.find_espeak_lib"
    bl_label="Find Espeak Lib"
    bl_options={'UNDO', 'REGISTER'}

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        prefs = context.preferences.addons[__package__].preferences # type: ignore
        espeak_inspector = LIPSYNC2D_EspeakInspector()
        
        try:
            espeak_path = espeak_inspector.try_find_library()
        except FileNotFoundError as e:
            self.report(type={'ERROR'}, message="Cannot find automatically library. Try to add it in your PATH or go find it manually with field below.")
            return {'FINISHED'}
        except Exception as e:
            self.report(type={'ERROR'}, message="Error while loading the file. Try to add file path manually.")
            return {'FINISHED'}

        
        prefs.espeak_path = espeak_path #type: ignore
        self.report({'INFO'}, message="Espeak library found!")
        return {'FINISHED'}