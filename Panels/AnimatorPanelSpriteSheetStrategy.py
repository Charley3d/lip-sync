from .AnimatorPanelMixin import AnimatorPanelMixin
from ..Core.phoneme_to_viseme import viseme_items_mpeg4_v2 as viseme_items
from ..lipsync_types import BpyContext, BpyUILayout


class AnimatorPanelSpriteSheetStrategy(AnimatorPanelMixin):
    def draw_animator_section(self, context: BpyContext, layout: BpyUILayout):
        panel_header, panel_body = layout.panel(
            "cgp_lipsync_animator_dropdown", default_closed=False
        )
        panel_header.label(text="Sprite Sheet Settings")
        if panel_body is not None:
            row = panel_body.row()
            row.label(text="Area")

            row = panel_body.row()
            row.label(
                text="Go in Edit Mode to define Mouth Area",
                icon="INFO_LARGE",
            )

            row = panel_body.row()
            row.operator("mesh.set_lips_area", text="Set Mouth Area")
            panel_body.separator(factor=1)

            row = panel_body.row()
            row.label(text="Select your Sprite sheet")
            panel_body.template_ID_preview(
                self.props,
                "lip_sync_2d_sprite_sheet",
                rows=2,
                cols=6,
                open="image.open",
            )

            panel_body.separator(factor=1)

            row = panel_body.row(align=True)
            row.label(text="Spritesheet Format")
            row.prop(self.props, "lip_sync_2d_sprite_sheet_format", text="")

            panel_body.separator(factor=1)

            row = panel_body.row(align=True)
            if self.props["lip_sync_2d_sprite_sheet_format"] == 3:
                row.prop(self.props, "lip_sync_2d_sprite_sheet_rows")
            elif self.props["lip_sync_2d_sprite_sheet_format"] == 2:
                row.prop(self.props, "lip_sync_2d_sprite_sheet_columns")
            elif self.props["lip_sync_2d_sprite_sheet_format"] == 0:
                row.prop(self.props, "lip_sync_2d_sprite_sheet_rows")
            elif self.props["lip_sync_2d_sprite_sheet_format"] == 1:
                row.prop(self.props, "lip_sync_2d_sprite_sheet_columns")
                row.prop(self.props, "lip_sync_2d_sprite_sheet_rows")

            row = panel_body.row()
            row.prop(self.props, "lip_sync_2d_sprite_sheet_index")

            panel_body.separator(factor=1)

            row = panel_body.row()
            row.label(text="Scale")
            row = panel_body.row(align=True)
            row.prop(self.props, "lip_sync_2d_sprite_sheet_sprite_scale")
            row.prop(self.props, "lip_sync_2d_sprite_sheet_main_scale", text="Main")
        
    def draw_animation_section(self, context: BpyContext, layout: BpyUILayout):
        panel_header, panel_body = layout.panel(
            "cgp_lipsync_animation_dropdown", default_closed=True
        )
        panel_header.label(text="Animation Settings")
        if panel_body is not None:
            self.draw_thresholds(self.props, panel_body)

    def draw_visemes_section(self, context: BpyContext, layout: BpyUILayout):
        panel_head, panel_body = layout.panel(
            "cgp_lipsync_viseme_dropdown", default_closed=True
        )
        panel_head.label(text="Viseme Settings")
        if panel_body is not None:
            row = panel_body.row(align=True)
            row.label(text="Viseme")
            row.label(text="Image index")

            visemes = viseme_items(None, None)

            for i, viseme in enumerate(visemes):
                lang_code = list(viseme)[0]
                row = panel_body.row(align=True)
                row.label(text=f"{lang_code}")
                row.prop(self.props, f"lip_sync_2d_viseme_{lang_code}", text="")

    def draw_thresholds(self, props, layout):
        row = layout.row()
        row.label(text="Thresholds:")
        data_list = [
            "lip_sync_2d_sps_in_between_threshold",
            "lip_sync_2d_sps_sil_threshold",
        ]
        row = layout.row()
        for data in data_list:
            row.prop(props, data)
