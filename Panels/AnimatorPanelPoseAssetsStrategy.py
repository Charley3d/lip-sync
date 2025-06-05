import bpy

from ..lipsync_types import BpyObject
from .AnimatorPanelMixin import AnimatorPanelMixin
from ..Core.phoneme_to_viseme import viseme_items_mpeg4_v2 as viseme_items
from ..lipsync_types import BpyContext, BpyUILayout


class AnimatorPanelPoseAssetsStrategy(AnimatorPanelMixin):
    def __init__(self, obj: BpyObject):
        super().__init__(obj)
        if not isinstance(obj.data, bpy.types.Mesh):
            return

    def draw_animator_section(self, context: BpyContext, layout: BpyUILayout):
        panel_header, panel_body = layout.panel(
            "vpg_lipsync_animator_dropdown", default_closed=False
        )

        panel_header.label(text="Rig Settings")

        if panel_body is not None:
            row = panel_body.row()
            row.label(text="Rig Type")

            row = panel_body.row(align=True)
            row.prop(self.props, "lip_sync_2d_rig_type_basic", toggle=True)
            row.prop(self.props, "lip_sync_2d_rig_type_advanced", toggle=True)
            panel_body.separator(factor=1)

    def draw_animation_section(self, context: BpyContext, layout: BpyUILayout):
        panel_header, panel_body = layout.panel(
            "cgp_lipsync_animation_dropdown", default_closed=False
        )
        panel_header.label(text="Animation Settings")
        if panel_body is not None:
            row = panel_body.row()
            row.label(text="Motion:")
            row = panel_body.row()
            row.prop(self.props, "lip_sync_2d_close_motion_duration")

            self.draw_thresholds(self.props, panel_body)

    def draw_visemes_section(self, context: BpyContext, layout: BpyUILayout):
        panel_head, panel_body = layout.panel(
            "cgp_lipsync_viseme_dropdown", default_closed=True
        )
        panel_head.label(text="Viseme Settings")
        if panel_body is not None:
            row = panel_body.row(align=True)
            row.label(text="Viseme")
            row.label(text="Pose")

            visemes = viseme_items(None, None)

            for i, viseme in enumerate(visemes):
                lang_code = list(viseme)[0]
                row = panel_body.row(align=True)
                row.label(text=f"{lang_code}")
                row.prop(self.props, f"lip_sync_2d_viseme_pose_{lang_code}", text="")

            panel_body.separator()
            row = panel_body.row(align=True)
            row.operator("lipsync2d.refresh_pose_assets")
            panel_body.separator()

    def draw_thresholds(self, props, layout):
        row = layout.row()
        row.label(text="Thresholds:")
        data_list = ["lip_sync_2d_in_between_threshold", "lip_sync_2d_sil_threshold"]
        row = layout.row()
        for data in data_list:
            row.prop(props, data)

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

    def draw_edit_section(self, context: BpyContext, layout: BpyUILayout):

        row = layout.row()
        row.label(text="Clean Up:")

        box = layout.box()
        row = box.row()
        row.label(text="Animation:")
        row = box.row()
        operator = row.operator(
            "object.remove_lip_sync_animations", text="Remove Pose Animation"
        )
        operator.animation_type = "POSEASSETS"  # type: ignore
        row = box.row()
        operator = row.operator(
            "object.remove_lip_sync_animations", text="Remove all Animations"
        )
        operator.animation_type = "ALL"  # type: ignore

        box = layout.box()
        row = box.row()
        row.prop(self.props, "lip_sync_2d_remove_animation_data")
        row = box.row()
        row.alert = True
        row.operator("object.remove_lip_sync_from_selection")
