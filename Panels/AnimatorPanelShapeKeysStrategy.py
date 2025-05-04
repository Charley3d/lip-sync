import bpy

from ..lipsync_types import BpyObject
from .AnimatorPanelMixin import AnimatorPanelMixin
from ..Core.phoneme_to_viseme import viseme_items_mpeg4_v2 as viseme_items
from ..lipsync_types import BpyContext, BpyUILayout


class AnimatorPanelShapeKeysStrategy(AnimatorPanelMixin):
    def __init__(self, obj: BpyObject):
        super().__init__(obj)
        if not isinstance(obj.data, bpy.types.Mesh):
            return

        self.at_least_two_shape_keys = bool(
            (
                obj.data
                and obj.data.shape_keys
                and obj.data.shape_keys.key_blocks.__len__() > 1
            )
        )

        self.is_relative = bool(
            (obj.data and obj.data.shape_keys and obj.data.shape_keys.use_relative)
        )

    def draw_animation_section(self, context: BpyContext, layout: BpyUILayout):
        panel_header, panel_body = layout.panel(
            "cgp_lipsync_sprite_audio_dropdown", default_closed=False
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
            row.label(text="Shape Key")

            visemes = viseme_items(None, None)

            for i, viseme in enumerate(visemes):
                lang_code = list(viseme)[0]
                row = panel_body.row(align=True)
                row.label(text=f"{lang_code}")
                row.prop(
                    self.props, f"lip_sync_2d_viseme_shape_keys_{lang_code}", text=""
                )

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
        if not self.at_least_two_shape_keys:
            new_row = layout.row()
            new_row.label(
                text="Missing Shape Keys",
                icon="WARNING_LARGE",
            )

        if not self.is_relative:
            new_row = layout.row()
            new_row.label(
                text="Shape Keys have to be set to 'Relative'",
                icon="WARNING_LARGE",
            )

        new_row = layout.row()
        new_row.operator(
            "sound.cgp_analyze_audio", text="Bake audio", icon="SCRIPTPLUGINS"
        )
        new_row.enabled = (
            self.is_model_installed
            and self.at_least_two_shape_keys
            and self.is_relative
        )
