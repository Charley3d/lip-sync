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
        
        layout = self.layout

        

        if not hasattr(context.scene, "lipsync2d_props"):
            return
        
        props = context.scene.lipsync2d_props # type: ignore

        if props is None:
            return
        
        
        # Create a simple row.
        row = layout.row()
        row.label(text="Select your Sprite sheet")
        row = layout.row()
        layout.template_ID_preview(props, "lip_sync_2d_sprite_sheet", rows=2, cols=6, open="image.open" )
        
        row = layout.row()
        row.operator('mesh.set_lips_area', text="Set Mouth Area")

        row = layout.row(align=True)
        row.operator('mesh.set_lips_material', text="Add Spritesheet on Selection")

        
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
        
        