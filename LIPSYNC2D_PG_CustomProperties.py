import bpy

class LIPSYNC2D_PG_CustomProperties(bpy.types.PropertyGroup):
    lip_sync_2d_sprite_sheet: bpy.props.PointerProperty(
        name="Sprite Sheet",
        description="The name of the addon to reload",
        type=bpy.types.Image
    ) # type: ignore
    lip_sync_2d_sprite_sheet_columns: bpy.props.IntProperty(
        name="Columns",
        description="Total of columns in sprite sheet",
        default=1
    ) # type: ignore
    lip_sync_2d_sprite_sheet_rows: bpy.props.IntProperty(
        name="Rows",
        description="Total of rows in sprite sheet",
        default=1
    ) # type: ignore
    lip_sync_2d_sprite_sheet_sprite_scale: bpy.props.FloatProperty(
        name="Sprite",
        description="Adjust sprite scale so it fits in mouth area",
        default=1
    ) # type: ignore
    lip_sync_2d_sprite_sheet_main_scale: bpy.props.FloatProperty(
        name="Lips",
        description="Adjust Lips scale",
        default=1
    ) # type: ignore
    lip_sync_2d_sprite_sheet_index: bpy.props.IntProperty(
        name="Sprite Index",
        description="Sprite Index. Start at 0, from Bottom Left to Top Right)",
        default=1
    ) # type: ignore