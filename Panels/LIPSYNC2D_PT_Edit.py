import bpy

from ..Panels.AnimatorPanelShapeKeysStrategy import AnimatorPanelShapeKeysStrategy
from ..Panels.AnimatorPanelSpriteSheetStrategy import AnimatorPanelSpriteSheetStrategy


class LIPSYNC2D_PT_Edit(bpy.types.Panel):
    bl_idname = "LIPSYNC2D_PT_Edit"
    bl_label = "Quick Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lip Sync"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context: bpy.types.Context):
        if self.layout is None:
            return
        if context.scene is None:
            return
        if context.preferences is None:
            return

        active_obj = context.active_object

        if active_obj is None or active_obj.type != "MESH":
            self.layout.label(
                text="Please, select an Object with Mesh Data", icon="INFO_LARGE"
            )
            return

        if not hasattr(active_obj, "lipsync2d_props"):
            self.layout.label(
                text="Something wrong happened. Try uninstall / reinstall Lip Sync Addon",
                icon="WARNING_LARGE",
            )
            return

        if "lip_sync_2d_initialized" not in context.active_object.lipsync2d_props:  # type: ignore
            self.layout.label(text="Press on Add Lip Sync to start", icon="INFO_LARGE")
            return

        props = active_obj.lipsync2d_props  # type: ignore

        if props is None:
            return

        if props.lip_sync_2d_lips_type == "SHAPEKEYS":
            self.animator_panel = AnimatorPanelShapeKeysStrategy(active_obj)
        elif props.lip_sync_2d_lips_type == "SPRITESHEET":
            self.animator_panel = AnimatorPanelSpriteSheetStrategy(active_obj)

        if self.animator_panel is None:
            return

        self.animator_panel.draw_edit_section(context, self.layout)
