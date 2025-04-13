import platform

import bpy
from bpy.types import Context

class LIPSYNC2D_PT_EspeakInstructions(bpy.types.Panel):
    bl_idname="LIPSYNC2D_PT_EspeakInstructions"
    bl_label="Espeak Instructions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id="LIPSYNC2D_PT_Panel"
    platform = platform.system()

    @classmethod
    def poll(cls, context: Context) -> bool:
        prefs = context.preferences.addons[__package__].preferences # type: ignore
        
        return prefs.espeak_path == ""

    def draw(self, context):
        if self.layout is None: return
        if context.scene is None: return
        if context.preferences is None: return
        
        prefs = context.preferences.addons[__package__].preferences # type: ignore
        layout = self.layout

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

        return