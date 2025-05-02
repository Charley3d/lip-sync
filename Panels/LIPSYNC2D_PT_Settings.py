import platform

import bpy

from ..LIPSYNC2D_Utils import get_package_name
from ..Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences


class LIPSYNC2D_PT_Settings(bpy.types.Panel):
    bl_idname="LIPSYNC2D_PT_Settings"
    bl_label="Quick Setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lip Sync'

    platform = platform.system()

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        prefs = context.preferences.addons[get_package_name()].preferences # type: ignore
        if not layout or prefs is None:
            return

        self.draw_espeak_model_settings(layout, prefs)

    def draw_espeak_model_settings(self, layout: bpy.types.UILayout, prefs: bpy.types.AddonPreferences):
        LIPSYNC2D_AP_Preferences.draw_online_access_warning(layout)
        row = layout.row()
        row.label(text="Language Model")
        row.prop(prefs, "current_lang", text="")
        LIPSYNC2D_AP_Preferences.draw_model_state(row) #type: ignore

