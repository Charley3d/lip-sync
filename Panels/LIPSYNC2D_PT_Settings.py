import platform

import bpy

from ..LIPSYNC2D_Utils import get_package_name
from ..Preferences.LIPSYNC2D_AP_Preferences import draw_model_state

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

    def draw_espeak_instructions(self, layout: bpy.types.UILayout, prefs: bpy.types.Preferences):
        box = layout.box()
        box.label(text="This addon needs espeak-ng library.")

        layout.separator(factor=2)

        row = layout.row()
        row.operator("lib.find_espeak_lib", text="Find Lib on my System")
        row = layout.row()
        row.label(text='OR')
        row = layout.row()
        row.label(text="espeak-ng lib (.dll/.so/.dylib)")
        row.prop(prefs, "espeak_path", text="")

        layout.separator(factor=2)

        if self.platform == "Windows":
            panel_header, panel_body = layout.panel("cgp_windows_instruction", default_closed=True)
            panel_header.label(text="Instructions For Windows:")
            if panel_body is not None:
                box = panel_body.box()
                box.label(text="1- Download the latest release (.msi) and install it")
                box.label(text="2- Select the .dll file in installation folder")
                box.label(text="Download the .msi at the bottom of the Github page")
                windows_url_ops = box.operator("wm.url_open", text="Download Release")
                windows_url_ops.url = "https://github.com/espeak-ng/espeak-ng/releases/tag/1.52.0" # type: ignore

        if self.platform == "Darwin":
            panel_header, panel_body = layout.panel("cgp_mac_instruction", default_closed=True)
            panel_header.label(text="Instructions For Mac:")
            if panel_body is not None:
                box = panel_body.box()
                box.label(text="1- brew install espeak-ng")
                box.label(text="2- Select the .dylib file in installation folder")

        if self.platform == "Linux":
            panel_header, panel_body = layout.panel("cgp_linux_instruction", default_closed=True)
            panel_header.label(text="Instructions For Linux:")
            if panel_body is not None:
                box = panel_body.box()
                box.label(text="1- sudo apt-get install espeak-ng")
                box.label(text="2- Select the .so file in installation folder")

    def draw_espeak_model_settings(self, layout: bpy.types.UILayout, prefs: bpy.types.AddonPreferences):
        row = layout.row()
        row.label(text="Language Model")
        row.prop(prefs, "current_lang", text="")
        draw_model_state(row, prefs.current_lang) #type: ignore

