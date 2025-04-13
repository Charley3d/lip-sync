import bpy

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
        
        prefs = context.preferences.addons[__package__].preferences # type: ignore

        if prefs.espeak_path == "":
            return

        if not hasattr(context.scene, "lipsync2d_props"):
            return
        
        if context.active_object is None:
            return
        
        props = context.active_object.lipsync2d_props # type: ignore

        if props is None:
            return
        
        layout = self.layout

        if "lip_sync_2d_sprite_sheet" not in context.active_object.lipsync2d_props: # type: ignore
            row = layout.row(align=True)
            row.operator('mesh.set_lips_material', text="Add Spritesheet on Selection")

        if context.active_object is None or not hasattr(context.active_object,"lipsync2d_props") or "lip_sync_2d_sprite_sheet" not in context.active_object["lipsync2d_props"]: return
        
        row = layout.row()
        row.label(text="Select your Sprite sheet")
        row = layout.row()
        layout.template_ID_preview(props, "lip_sync_2d_sprite_sheet", rows=2, cols=6, open="image.open" )

        row = layout.row()
        row.label(text="Area")
        row = layout.row()
        row.operator('mesh.set_lips_area', text="Set Mouth Area (Edit Mode)")

        row = layout.row()
        row.label(text="Spritesheet Size")
        row = layout.row(align=True)
        row.prop(props, "lip_sync_2d_sprite_sheet_columns")
        row.prop(props, "lip_sync_2d_sprite_sheet_rows")
        
        row = layout.row()
        row.label(text="Scale")
        row = layout.row(align=True)
        row.prop(props, "lip_sync_2d_sprite_sheet_sprite_scale")
        row.prop(props, "lip_sync_2d_sprite_sheet_main_scale")
        
        row = layout.row()
        row.prop(props, "lip_sync_2d_sprite_sheet_index")

        if props.lip_sync_2d_sprite_sheet is not None:
            row = layout.row()
            row.operator("audio.cgp_analyze_audio", text="Analyze audio")

            row = layout.row()
            i = 0

            row = layout.row(align=True)
            row.label(text=f"Image index")
            row.label(text=f"Viseme")
            while i < props.lip_sync_2d_sprite_sheet_columns * props.lip_sync_2d_sprite_sheet_rows:
                row = layout.row(align=True)
                row.label(text=f"{i}")
                row.prop(props, f"lip_sync_2d_viseme_{i}", text="")
                i += 1
