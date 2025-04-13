import bpy

from .phoneme_to_viseme import viseme_items_arkit as viseme_items

def update_sprite_sheet(self, context: bpy.types.Context):
    obj = context.active_object
    mat: bpy.types.Material = obj.lipsync2d_props.lip_sync_2d_main_material # type: ignore

    if mat is None or mat.node_tree is None or mat.node_tree.nodes is None: return

    group_node = mat.node_tree.nodes.get("cgp_spritesheet_reader")

    if not isinstance(group_node, bpy.types.ShaderNodeGroup) or group_node.node_tree is None or group_node.node_tree.nodes is None: return

    image_node = group_node.node_tree.nodes.get("CGP_LipSyncSpritesheet")

    if not isinstance(image_node, bpy.types.ShaderNodeTexImage): return

    image_node.image = self.lip_sync_2d_sprite_sheet
    
    return None


class LIPSYNC2D_PG_CustomProperties(bpy.types.PropertyGroup):
    lip_sync_2d_sprite_sheet: bpy.props.PointerProperty(
        name="Sprite Sheet",
        description="The name of the addon to reload",
        type=bpy.types.Image,
        update=update_sprite_sheet
    ) # type: ignore
    lip_sync_2d_main_material: bpy.props.PointerProperty(
        name="Main Material",
        description="Material containing Spritesheet",
        type=bpy.types.Material
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
    # lip_sync_2d_visemes: bpy.props.EnumProperty( # type: ignore
    #     name="Viseme",
    #     description="Select a viseme shape",
    #     items=viseme_items
    # )
    lip_sync_2d_viseme_0: bpy.props.EnumProperty(name="Viseme 0", items=viseme_items, default=0) #type: ignore
    lip_sync_2d_viseme_1: bpy.props.EnumProperty(name="Viseme 1", items=viseme_items, default=1) #type: ignore
    lip_sync_2d_viseme_2: bpy.props.EnumProperty(name="Viseme 2", items=viseme_items, default=2) #type: ignore
    lip_sync_2d_viseme_3: bpy.props.EnumProperty(name="Viseme 3", items=viseme_items, default=3) #type: ignore
    lip_sync_2d_viseme_4: bpy.props.EnumProperty(name="Viseme 4", items=viseme_items, default=4) #type: ignore
    lip_sync_2d_viseme_5: bpy.props.EnumProperty(name="Viseme 5", items=viseme_items, default=5) #type: ignore
    lip_sync_2d_viseme_6: bpy.props.EnumProperty(name="Viseme 6", items=viseme_items, default=6) #type: ignore
    lip_sync_2d_viseme_7: bpy.props.EnumProperty(name="Viseme 7", items=viseme_items, default=7) #type: ignore
    lip_sync_2d_viseme_8: bpy.props.EnumProperty(name="Viseme 8", items=viseme_items, default=8) #type: ignore
    lip_sync_2d_viseme_9: bpy.props.EnumProperty(name="Viseme 9", items=viseme_items, default=9) #type: ignore
    lip_sync_2d_viseme_10: bpy.props.EnumProperty(name="Viseme 10", items=viseme_items, default=10) #type: ignore
    lip_sync_2d_viseme_11: bpy.props.EnumProperty(name="Viseme 11", items=viseme_items, default=11) #type: ignore
    lip_sync_2d_viseme_12: bpy.props.EnumProperty(name="Viseme 12", items=viseme_items, default=12) #type: ignore
    # lip_sync_2d_espeak_path: bpy.props.StringProperty(name="Espeak library (.dll/.so/.dylib)", subtype='FILE_PATH') #type: ignore