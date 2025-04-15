import bpy

from ..LIPSYNC2D_Utils import get_package_name
from ..Core.phoneme_to_viseme import viseme_items_arkit_v2 as viseme_items_arkit

class LIPSYNC2D_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Lip Sync 2D"
    bl_idname = "LIPSYNC2D_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Lip Sync 2D'

    def draw(self, context: bpy.types.Context):
        if self.layout is None: return
        if context.scene is None: return
        if context.preferences is None: return

        package_name = get_package_name()
        prefs = context.preferences.addons[package_name].preferences # type: ignore
        active_obj = context.active_object

        if prefs.espeak_path == "":
            layout = self.layout
            box = layout.box()
            box.label(text="Please complete the Quick Setup process")
            return

        if active_obj is None:
            return

        if not hasattr(active_obj, "lipsync2d_props"):
            return
        
        props = active_obj.lipsync2d_props # type: ignore

        if props is None:
            return
        
        layout = self.layout

        if "lip_sync_2d_sprite_sheet" not in context.active_object.lipsync2d_props: # type: ignore
            row = layout.row(align=True)
            row.operator('mesh.set_lips_material', text="Add Spritesheet on Selection")

        if context.active_object is None or not hasattr(context.active_object,"lipsync2d_props") or "lip_sync_2d_sprite_sheet" not in context.active_object["lipsync2d_props"]: return
        
        is_model_installed = True if prefs.current_lang not in ["", "none"] else False

        row = layout.row()
        row.label(text="Select your Sprite sheet")
        row = layout.row()
        layout.template_ID_preview(props, "lip_sync_2d_sprite_sheet", rows=2, cols=6, open="image.open" )

        row = layout.row()
        row.label(text="Area - Edit Mode Only")
        row = layout.row()
        row.operator('mesh.set_lips_area', text="Set Mouth Area")
        row = layout.row()
        row.prop(props, "lip_sync_2d_sprite_sheet_index")

        panel_header, panel_body = layout.panel("cgp_lipsync_sprite_settings_dropdown", default_closed=True)
        panel_header.label(text="Spritesheet Settings")
        if panel_body is not None:
            row = panel_body.row()
            row.label(text="Spritesheet Format")
            row = panel_body.row(align=True)
            row.prop(props, "lip_sync_2d_sprite_sheet_format")
            row = panel_body.row(align=True)
            if props["lip_sync_2d_sprite_sheet_format"] == 3:
                row.prop(props, "lip_sync_2d_sprite_sheet_rows")
            elif props["lip_sync_2d_sprite_sheet_format"] == 2:
                row.prop(props, "lip_sync_2d_sprite_sheet_columns")
            elif props["lip_sync_2d_sprite_sheet_format"] == 0:
                row.prop(props, "lip_sync_2d_sprite_sheet_rows")
            elif props["lip_sync_2d_sprite_sheet_format"] == 1:
                row.prop(props, "lip_sync_2d_sprite_sheet_columns")
                row.prop(props, "lip_sync_2d_sprite_sheet_rows")

            row = panel_body.row()
            row.label(text="Scale")
            row = panel_body.row(align=True)
            row.prop(props, "lip_sync_2d_sprite_sheet_sprite_scale")
            row.prop(props, "lip_sync_2d_sprite_sheet_main_scale", text="Main")

        panel_header, panel_body = layout.panel("cgp_lipsync_sprite_audio_dropdown", default_closed=False)
        panel_header.label(text="Audio Analysis")
        if panel_body is not None:
            if not is_model_installed:
                row = layout.row()
                row.label(text="Select a Language Model before Analyzing audio")

            row = layout.row()
            row.operator("audio.cgp_analyze_audio", text="Analyze audio")
            row.enabled = is_model_installed


        if props.lip_sync_2d_sprite_sheet is not None:
            panel_head, panel_body = layout.panel("cgp_lipsync_viseme_dropdown", default_closed=True)
            panel_head.label(text="Viseme Settings")
            if panel_body is not None:
                row = panel_body.row()
                i = 0

                row = panel_body.row(align=True)
                row.label(text=f"Viseme")
                row.label(text=f"Image index")

                visemes = viseme_items_arkit(None, None)

                for i, viseme in enumerate(visemes):
                    lang_code = list(viseme)[0]
                    row = panel_body.row(align=True)
                    row.label(text=f"{lang_code}")
                    row.prop(props, f"lip_sync_2d_viseme_{lang_code}", text="")
            

