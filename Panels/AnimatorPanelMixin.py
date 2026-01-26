from typing import cast
import bpy

from ..LIPSYNC2D_Utils import get_package_name

from ..lipsync_types import BpyContext, BpyObject, BpyPropertyGroup, BpyUILayout


class AnimatorPanelMixin:
    def __init__(self, obj: BpyObject):

        self.package_name = get_package_name()
        self.prefs: bpy.types.AddonPreferences | None = None
        self.obj: BpyObject = obj
        lipsync_props = self.obj.lipsync2d_props  # type: ignore
        self.props: bpy.types.PropertyGroup = cast(BpyPropertyGroup, lipsync_props)

        if (
            self.package_name
            and bpy.context.preferences is not None
            and self.package_name in bpy.context.preferences.addons
        ):
            self.prefs = bpy.context.preferences.addons[self.package_name].preferences

        self.current_lang = self.prefs.current_lang if self.prefs is not None else None  # type: ignore
        self.is_model_installed = (
            True if self.current_lang not in ["", "none"] else False
        )

    def draw_animation_section(self, context: BpyContext, layout: BpyUILayout):
        raise NotImplementedError()

    def draw_visemes_section(self, context: BpyContext, layout: BpyUILayout):
        raise NotImplementedError()

    def draw_animator_section(self, context: BpyContext, layout: BpyUILayout):
        raise NotImplementedError()

    def draw_edit_section(self, context: BpyContext, layout: BpyUILayout):

        row = layout.row()
        row.label(text="Clean Up:")

        box = layout.box()
        row = box.row()
        row.label(text="Shader Editor:")
        row = box.row()
        row.operator("object.remove_lip_sync_node_groups")

        box = layout.box()
        row = box.row()
        row.label(text="Animation:")
        row = box.row()
        operator = row.operator("object.remove_lip_sync_animations", text="Remove SK")
        operator.animation_type = "SHAPEKEYS"  # type: ignore
        operator = row.operator("object.remove_lip_sync_animations", text="Remove SPT")
        operator.animation_type = "SPRITESHEET"  # type: ignore
        row = box.row()
        operator = row.operator(
            "object.remove_lip_sync_animations", text="Remove all Animations"
        )
        operator.animation_type = "ALL"  # type: ignore

        box = layout.box()
        row = box.row()
        row.prop(self.props, "lip_sync_2d_remove_animation_data")
        row.prop(self.props, "lip_sync_2d_remove_cgp_node_group")
        row = box.row()
        row.alert = True
        row.operator("object.remove_lip_sync_from_selection")

    def draw_baking_section(self, context: BpyContext, layout: BpyUILayout):
        if not self.is_model_installed:
            new_row = layout.row()
            new_row.label(
                text="Select a Language Model before Analyzing audio",
                icon="WARNING_LARGE",
            )

        new_row = layout.row()
        new_row.operator(
            "sound.cgp_analyze_audio", text="Bake audio", icon="SCRIPTPLUGINS"
        )
        new_row.enabled = self.is_model_installed

    def draw_bake_section(self, context: BpyContext, layout: BpyUILayout):
        panel_head, panel_body = layout.panel(
            "cgp_lipsync_bake_settings_dropdown", default_closed=True
        )
        panel_head.label(text="Bake Settings")

        if panel_body is not None:
            row = panel_body.row()
            row.label(text="Misc:")
            row = panel_body.row()
            row.prop(self.props, "lip_sync_2d_use_clear_keyframes")
            row = panel_body.row()
            row.label(text="Range:")
            row = panel_body.row()
            row.prop(self.props, "lip_sync_2d_use_bake_range")
            row = panel_body.row(align=True)
            row.prop(self.props, "lip_sync_2d_bake_start", text="Start")
            row.prop(self.props, "lip_sync_2d_bake_end", text="End")
            row.enabled = self.props.lip_sync_2d_use_bake_range  # type: ignore

            row = panel_body.row()
            row.prop(self.props, "lip_sync_2d_bake_channel")
