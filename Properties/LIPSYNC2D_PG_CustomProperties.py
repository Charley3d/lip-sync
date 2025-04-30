import bpy

from ..Core.phoneme_to_viseme import viseme_items_mpeg4_v2 as viseme_items


def update_sprite_sheet(self: bpy.types.bpy_struct, context: bpy.types.Context):
    obj = context.active_object
    mat: bpy.types.Material = obj.lipsync2d_props.lip_sync_2d_main_material # type: ignore

    if mat is None or mat.node_tree is None or mat.node_tree.nodes is None: return

    group_node = mat.node_tree.nodes.get("cgp_spritesheet_reader")

    if not isinstance(group_node, bpy.types.ShaderNodeGroup) or group_node.node_tree is None or group_node.node_tree.nodes is None: return

    image_node = group_node.node_tree.nodes.get("CGP_LipSyncSpritesheet")

    if not isinstance(image_node, bpy.types.ShaderNodeTexImage): return

    image_node.image = self["lip_sync_2d_sprite_sheet"]
    
    return None

def update_sprite_sheet_format(self: bpy.types.bpy_struct, context: bpy.types.Context):
    spritesheet_format = self["lip_sync_2d_sprite_sheet_format"]


    if spritesheet_format == 0:
        self["lip_sync_2d_sprite_sheet_rows"] = self["lip_sync_2d_sprite_sheet_columns"]
    elif spritesheet_format == 2:
        self["lip_sync_2d_sprite_sheet_rows"] = 1
    elif spritesheet_format == 3:
        self["lip_sync_2d_sprite_sheet_columns"] = 1

def update_sprite_sheet_rows(self: bpy.types.bpy_struct, context: bpy.types.Context):
    if "lip_sync_2d_sprite_sheet_format" not in self: return
    
    spritesheet_format = self["lip_sync_2d_sprite_sheet_format"]

    if spritesheet_format == 0:
        self["lip_sync_2d_sprite_sheet_columns"] = self["lip_sync_2d_sprite_sheet_rows"]

def shape_keys_list(self:bpy.types.bpy_struct, context: bpy.types.Context | None):
        result = [("NONE", "None", "None")]
        
        if context is None or context.active_object is None: return result

        active_obj = context.active_object

        if not isinstance(active_obj.data, bpy.types.Mesh) or active_obj.data.shape_keys is None: return result
        shape_keys = active_obj.data.shape_keys.key_blocks

        result = result + [(s.name,s.name,s.name) for s in shape_keys]

        return result

class LIPSYNC2D_PG_CustomProperties(bpy.types.PropertyGroup):
    lip_sync_2d_sprite_sheet: bpy.props.PointerProperty(
        name="Sprite Sheet",
        description="The name of the addon to reload",
        type=bpy.types.Image,
        update=update_sprite_sheet
    ) # type: ignore
    lip_sync_2d_main_material: bpy.props.PointerProperty(
        name="Main Material",
        description="Material containing Sprite sheet",
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
        update=update_sprite_sheet_rows,
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
        description="Sprite Index. Start at 0, from Bottom Left to Top Right",
        default=1
    ) # type: ignore
    lip_sync_2d_sprite_sheet_format: bpy.props.EnumProperty(
        name="Sprite sheet format",
        description="Sprite sheet format can be square, rectangle or line.",
        items=[
            ("SQUARE", "Square", "Sprites are placed in a square with same width and height"),
            ("RECTANGLE", "Rectangle", "Sprites are placed in a rectangle with multiple columns and rows"),
            ("HLINE", "Horizontal Line", "Sprites are placed horizontally"),
            ("VLINE", "Vertical Line", "Sprites are placed vertically"),
        ],
        update=update_sprite_sheet_format,
        default=3
    )  # type: ignore

    lip_sync_2d_lips_type: bpy.props.EnumProperty(
        name="Lips type",
        description="What kind of animation will you use.",
        items=[
            ("SPRITESHEET", "Sprite Sheet", "Use a Sprite Sheet containg all of your visemes"),
            ("SHAPEKEYS", "Shape Keys (BETA)", "Use your Shape Keys to animate mouth"),
            # ("BONES", "Bones", "Use Bones position to animate mouth") Next release
        ],
        update=update_sprite_sheet_format,
        default=0
    )  # type: ignore

    lip_sync_2d_in_between_threshold: bpy.props.FloatProperty(
        name="In between Threshold",
        description="Minimum time to have between 2 Keyframes. Keyframe being added before this threshold will be removed",
        default=.0417,
        subtype="TIME",
        unit="TIME"
    ) # type: ignore

    lip_sync_2d_sil_threshold: bpy.props.FloatProperty(
        name="Silence Threshold",
        description="Minimum time to have between 2 Keyframes to consider having a \"Silence\"",
        default=.1,
        subtype="TIME",
        unit="TIME"
    ) # type: ignore

    @classmethod
    def register(cls):
        visemes = viseme_items(None, None)

        for v in visemes:
            enum_id, name, desc = v
            prop_name = f"lip_sync_2d_viseme_{enum_id}"
            setattr(cls, prop_name,
                    bpy.props.IntProperty(name=f"Viseme {name}", description=desc,
                                          min=0, max=99, default=0)  # type: ignore
                    )
            
            prop_name = f"lip_sync_2d_viseme_shape_keys_{enum_id}"
            setattr(cls, prop_name,
                    bpy.props.EnumProperty(name=f"Viseme {name}", 
                                           description=desc,
                                           items=shape_keys_list,
                                           default=0)  # type: ignore
                    )
    
