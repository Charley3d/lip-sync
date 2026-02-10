import platform

import bpy

from ..LIPSYNC2D_Utils import get_package_name
from ..Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from ..Core.LIPSYNC2D_VoskHelper import LIPSYNC2D_VoskHelper


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
        row = layout.row()
        row.label(text="Language Model")
        
        row.prop(prefs, "current_lang", text="")
        
        if prefs.current_lang != "none":
            cache_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
            model_path = cache_path / prefs.current_lang
            
            if not model_path.exists() or not model_path.is_dir():
                row.operator("wm.lipsync_install_model", text="", icon="IMPORT")
                
        LIPSYNC2D_AP_Preferences.draw_model_state(row) #type: ignore

