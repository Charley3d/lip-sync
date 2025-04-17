import bpy


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
        description="Sprite Index. Start at 0, from Bottom Left to Top Right)",
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

    #TODO: Generate this from the phoneme dict
    lip_sync_2d_viseme_sil: bpy.props.IntProperty(name="Viseme sil", description="Silence or mouth at rest (neutral position)", min=0, max=99, default=0) #type: ignore
    lip_sync_2d_viseme_PP: bpy.props.IntProperty(name="Viseme PP", description="Closed lips as in \"pop\" or \"map\"", min=0, max=99, default=1) #type: ignore
    lip_sync_2d_viseme_FF: bpy.props.IntProperty(name="Viseme FF", description="Top teeth over bottom lip, like \"fish\" or \"fifty\"", min=0, max=99, default=2) #type: ignore
    lip_sync_2d_viseme_TH: bpy.props.IntProperty(name="Viseme TH", description="Tongue between teeth, like \"think\" or \"that\"", min=0, max=99, default=3) #type: ignore
    lip_sync_2d_viseme_DD: bpy.props.IntProperty(name="Viseme DD", description="Tongue touches roof of mouth, as in \"dog\" or \"add\"", min=0, max=99, default=4) #type: ignore
    lip_sync_2d_viseme_kk: bpy.props.IntProperty(name="Viseme kk", description="Back of the tongue against the soft palate, like \"cook\" or \"kick\"", min=0, max=99, default=5) #type: ignore
    lip_sync_2d_viseme_CH: bpy.props.IntProperty(name="Viseme CH", description="Teeth clenched with lips slightly apart, like \"chew\" or \"church\"", min=0, max=99, default=6) #type: ignore
    lip_sync_2d_viseme_SS: bpy.props.IntProperty(name="Viseme SS", description="Lips apart, teeth close together, for \"see\" or \"snake\"", min=0, max=99, default=7) #type: ignore
    lip_sync_2d_viseme_nn: bpy.props.IntProperty(name="Viseme nn", description="Tongue on roof of mouth, nasal sound like \"no\" or \"none\"", min=0, max=99, default=8) #type: ignore
    lip_sync_2d_viseme_RR: bpy.props.IntProperty(name="Viseme RR", description="Rounded lips and retracted tongue, as in \"red\" or \"arrow\"", min=0, max=99, default=9) #type: ignore
    lip_sync_2d_viseme_aa: bpy.props.IntProperty(name="Viseme aa", description="Wide open mouth, like \"cat\" or \"flat\"", min=0, max=99, default=10) #type: ignore
    lip_sync_2d_viseme_E: bpy.props.IntProperty(name="Viseme E", description="Slightly open mouth with spread lips, like \"bed\" or \"pen\"", min=0, max=99, default=11) #type: ignore
    lip_sync_2d_viseme_ih: bpy.props.IntProperty(name="Viseme ih", description="Slightly open mouth, tongue high, like \"bit\" or \"hit\"", min=0, max=99, default=12) #type: ignore
    lip_sync_2d_viseme_oh: bpy.props.IntProperty(name="Viseme oh", description="Rounded lips, mouth less open, like \"bought\" or \"saw\"", min=0, max=99, default=13) #type: ignore
    lip_sync_2d_viseme_ou: bpy.props.IntProperty(name="Viseme ou", description="Tight rounded lips, like \"boot\" or \"you\"", min=0, max=99, default=14) #type: ignore
    lip_sync_2d_viseme_UNK: bpy.props.IntProperty(name="Viseme UNK", description="Default lips if phoneme is unknown", min=0, max=99, default=0) #type: ignore
