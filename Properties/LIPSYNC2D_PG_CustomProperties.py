from __future__ import annotations
from typing import cast

import bpy

from ..Utils.strings import intern_enum_items

from ..lipsync_types import BpyContext

from ..Core.phoneme_to_viseme import viseme_items_mpeg4_v2 as viseme_items


def update_rig_type_advanced(self, context):
    if self.lip_sync_2d_rig_type_advanced:
        self["lip_sync_2d_rig_type_basic"] = False
    self["lip_sync_2d_rig_type_advanced"] = True


def update_rig_type_basic(self, context):
    if self.lip_sync_2d_rig_type_basic:
        self["lip_sync_2d_rig_type_advanced"] = False
    self["lip_sync_2d_rig_type_basic"] = True


def update_sprite_sheet(self: bpy.types.bpy_struct, context: bpy.types.Context):
    obj = context.active_object
    mat: bpy.types.Material = obj.lipsync2d_props.lip_sync_2d_main_material  # type: ignore

    if mat is None or mat.node_tree is None or mat.node_tree.nodes is None:
        return

    main_group = cast(
        bpy.types.ShaderNodeGroup, mat.node_tree.nodes.get("cgp_main_group")
    )

    if main_group is None or main_group.node_tree is None:
        return

    group_node = main_group.node_tree.nodes.get("cgp_spritesheet_reader")

    if (
        not isinstance(group_node, bpy.types.ShaderNodeGroup)
        or group_node.node_tree is None
        or group_node.node_tree.nodes is None
    ):
        return

    image_node = group_node.node_tree.nodes.get("CGP_LipSyncSpritesheet")

    if not isinstance(image_node, bpy.types.ShaderNodeTexImage):
        return

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
    if "lip_sync_2d_sprite_sheet_format" not in self:
        return

    spritesheet_format = self["lip_sync_2d_sprite_sheet_format"]

    if spritesheet_format == 0:
        self["lip_sync_2d_sprite_sheet_columns"] = self["lip_sync_2d_sprite_sheet_rows"]


def shape_keys_list(self: bpy.types.bpy_struct, context: bpy.types.Context | None):
    result = [("NONE", "None", "None")]

    if context is None or context.active_object is None:
        return result

    active_obj = context.active_object

    if (
        not isinstance(active_obj.data, bpy.types.Mesh)
        or active_obj.data.shape_keys is None
    ):
        return result

    shape_keys = active_obj.data.shape_keys
    key_blocks = active_obj.data.shape_keys.key_blocks

    result = result + [
        (s.name, s.name, s.name) for s in key_blocks if s != shape_keys.reference_key
    ]

    return intern_enum_items(result)


def set_bake_end(self, value):
    if value < self.lip_sync_2d_bake_start:
        self["lip_sync_2d_bake_start"] = value

    self["lip_sync_2d_bake_end"] = value


def get_bake_end(self):
    try:
        return self["lip_sync_2d_bake_end"]
    except:
        return 0


def set_bake_start(self, value):
    if value > self.lip_sync_2d_bake_end:
        self["lip_sync_2d_bake_end"] = value

    self["lip_sync_2d_bake_start"] = value


def get_bake_start(self):
    try:
        return self["lip_sync_2d_bake_start"]
    except:
        return 0


def armature_prop_poll(self, obj):
    return obj.type == "ARMATURE"


def get_lip_sync_type_items(self, context: BpyContext | None):
    if context is None or context.active_object is None:
        return []

    items = [
        (
            "SPRITESHEET",
            "Sprite Sheet",
            "Use a Sprite Sheet containg all of your visemes",
        ),
        ("SHAPEKEYS", "Shape Keys", "Use your Shape Keys to animate mouth"),
    ]

    if context.active_object.type == "ARMATURE":
        items = [
            ("POSEASSETS", "Pose Assets", "Use Pose Library to animate mouth"),
        ]

    return items


def poll_pose_assets(self, obj: bpy.types.ID):
    return bool(obj.asset_data)


class LIPSYNC2D_PG_CustomProperties(bpy.types.PropertyGroup):
    lip_sync_2d_initialized: bpy.props.BoolProperty(
        name="Initilize Lip Sync",
        description="Initilize Lip Sync on selection",
        default=False,
    )  # type: ignore
    lip_sync_2d_sprite_sheet: bpy.props.PointerProperty(
        name="Sprite Sheet",
        description="The name of the addon to reload",
        type=bpy.types.Image,
        update=update_sprite_sheet,
    )  # type: ignore
    lip_sync_2d_main_material: bpy.props.PointerProperty(
        name="Main Material",
        description="Material containing Sprite sheet",
        type=bpy.types.Material,
    )  # type: ignore
    lip_sync_2d_sprite_sheet_columns: bpy.props.IntProperty(
        name="Columns", description="Total of columns in sprite sheet", default=1
    )  # type: ignore
    lip_sync_2d_sprite_sheet_rows: bpy.props.IntProperty(
        name="Rows",
        description="Total of rows in sprite sheet",
        update=update_sprite_sheet_rows,
        default=1,
    )  # type: ignore
    lip_sync_2d_sprite_sheet_sprite_scale: bpy.props.FloatProperty(
        name="Sprite",
        description="Adjust sprite scale so it fits in mouth area",
        default=1,
    )  # type: ignore
    lip_sync_2d_sprite_sheet_main_scale: bpy.props.FloatProperty(
        name="Lips", description="Adjust Lips scale", default=1
    )  # type: ignore
    lip_sync_2d_sprite_sheet_index: bpy.props.IntProperty(
        name="Sprite Index",
        description="Sprite Index. Start at 0, from Bottom Left to Top Right",
        default=1,
    )  # type: ignore
    lip_sync_2d_sprite_sheet_format: bpy.props.EnumProperty(
        name="Sprite sheet format",
        description="Sprite sheet format can be square, rectangle or line.",
        items=[
            (
                "SQUARE",
                "Square",
                "Sprites are placed in a square with same width and height",
            ),
            (
                "RECTANGLE",
                "Rectangle",
                "Sprites are placed in a rectangle with multiple columns and rows",
            ),
            ("HLINE", "Horizontal Line", "Sprites are placed horizontally"),
            ("VLINE", "Vertical Line", "Sprites are placed vertically"),
        ],
        update=update_sprite_sheet_format,
        default=3,
    )  # type: ignore

    lip_sync_2d_lips_type: bpy.props.EnumProperty(
        name="Animation type",
        description="What kind of animation will you use.",
        items=get_lip_sync_type_items,
        update=update_sprite_sheet_format,
        default=0,
    )  # type: ignore

    lip_sync_2d_in_between_threshold: bpy.props.FloatProperty(
        name="In between",
        description="Minimum time gap required between two keyframes. Keyframes added closer than this will be removed.",
        default=0.0417,
        subtype="TIME",
        unit="TIME_ABSOLUTE",
    )  # type: ignore

    lip_sync_2d_sil_threshold: bpy.props.FloatProperty(
        name="Silence",
        description="Minimum time gap between keyframes required to insert a silent interval.",
        default=0.22,
        subtype="TIME",
        unit="TIME_ABSOLUTE",
    )  # type: ignore

    lip_sync_2d_sps_in_between_threshold: bpy.props.FloatProperty(
        name="In between",
        description="Minimum time gap required between two keyframes. Keyframes added closer than this will be removed.",
        default=0.0417,
        subtype="TIME",
        unit="TIME_ABSOLUTE",
    )  # type: ignore

    lip_sync_2d_sps_sil_threshold: bpy.props.FloatProperty(
        name="Silence",
        description="Minimum time gap between keyframes required to insert a silent interval.",
        default=0.22,
        subtype="TIME",
        unit="TIME_ABSOLUTE",
    )  # type: ignore

    lip_sync_2d_close_motion_duration: bpy.props.FloatProperty(
        name="Lip Close Duration",
        description="Duration of lip-closing animation during silent intervals",
        default=0.2,
        subtype="TIME",
        unit="TIME_ABSOLUTE",
    )  # type: ignore

    lip_sync_2d_remove_animation_data: bpy.props.BoolProperty(
        name="Remove Animation",
        description="Also remove action, action slot and keyframes",
        default=True,
    )  # type: ignore

    lip_sync_2d_remove_cgp_node_group: bpy.props.BoolProperty(
        name="Remove Nodes",
        description="Also remove node groups from Object's Materials",
        default=True,
    )  # type: ignore

    lip_sync_2d_use_clear_keyframes: bpy.props.BoolProperty(
        name="Clear Keyframes",
        description="Clear Keyframes before Bake",
        default=True,
    )  # type: ignore

    lip_sync_2d_use_bake_range: bpy.props.BoolProperty(
        name="Use Range",
        description="Only bake between specified range",
        default=False,
    )  # type: ignore

    lip_sync_2d_debug_output: bpy.props.BoolProperty(
        name="Debug Output",
        description="Output phoneme and viseme data to a text block",
        default=False,
    )  # type: ignore

    lip_sync_2d_bake_start: bpy.props.IntProperty(
        name="Bake Start",
        description="Start Baking at this frame",
        default=1,
        min=0,
        set=set_bake_start,
        get=get_bake_start,
    )  # type: ignore

    lip_sync_2d_bake_end: bpy.props.IntProperty(
        name="Bake End",
        description="End Baking at this frame",
        default=250,
        min=0,
        set=set_bake_end,
        get=get_bake_end,
    )  # type: ignore

    lip_sync_2d_rig_type_basic: bpy.props.BoolProperty(
        name="Basic Rig",
        description=(
            "Rig with basic bones animation.\n"
            "As long as only basic bones are animated, this should be your default choice."
        ),
        default=True,
        update=update_rig_type_basic,
    )  # type: ignore

    lip_sync_2d_rig_type_advanced: bpy.props.BoolProperty(
        name="Advanced Rig",
        description=(
            "Rig with more complex animated elements like BBone or Custom Properties.\n"
            "Since this inserts keyframes on ALL of your animated properties, it will be slower.\n"
            "Only use this if Basic Rig is not working."
        ),
        update=update_rig_type_advanced,
    )  # type: ignore

    lip_sync_2d_prioritize_accuracy: bpy.props.BoolProperty(
        name="Prioritize Accuracy",
        description=(
            "Animate all important visemes regardless of timing constraints. "
            "Prevents critical mouth shapes (lip contact sounds like P, B, M, F, TH) "
            "from being skipped when they occur in rapid succession."
        ),
        default=False,
    )  # type: ignore

    @classmethod
    def register(cls):
        visemes = viseme_items(None, None)

        for v in visemes:
            enum_id, name, desc = v
            prop_name = f"lip_sync_2d_viseme_{enum_id}"
            setattr(
                cls,
                prop_name,
                bpy.props.IntProperty(
                    name=f"Viseme {name}", description=desc, min=0, max=99, default=-1
                ),  # type: ignore
            )

            prop_name = f"lip_sync_2d_viseme_shape_keys_{enum_id}"
            setattr(
                cls,
                prop_name,
                bpy.props.EnumProperty(
                    name=f"Viseme {name}",
                    description=desc,
                    items=shape_keys_list,
                    default=0,
                ),  # type: ignore
            )

            prop_name = f"lip_sync_2d_viseme_pose_{enum_id}"
            setattr(
                cls,
                prop_name,
                bpy.props.PointerProperty(
                    type=bpy.types.Action,
                    name=f"Viseme {name}",
                    description=desc,
                    poll=poll_pose_assets,
                ),
            )
