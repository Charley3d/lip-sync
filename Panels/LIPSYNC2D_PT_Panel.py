import bpy

from .AnimatorPanelPoseAssetsStrategy import AnimatorPanelPoseAssetsStrategy

from .protocols import LIPSYNC2D_AnimatorPanel

from .AnimatorPanelSpriteSheetStrategy import AnimatorPanelSpriteSheetStrategy

from .AnimatorPanelShapeKeysStrategy import AnimatorPanelShapeKeysStrategy


class LIPSYNC2D_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the property editor"""

    bl_label = "Lip Sync"
    bl_idname = "LIPSYNC2D_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lip Sync"

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        self.animator_panel: LIPSYNC2D_AnimatorPanel | None = None

    def draw(self, context: bpy.types.Context):
        if self.layout is None:
            return
        if context.scene is None:
            return
        if context.preferences is None:
            return

        active_obj = context.active_object

        if active_obj is None or (
            active_obj.type != "MESH" and active_obj.type != "ARMATURE"
        ):
            self.layout.label(
                text="Please, select an Object with Mesh Data or an Armature",
                icon="INFO_LARGE",
            )
            return

        if not hasattr(active_obj, "lipsync2d_props"):
            self.layout.label(
                text="Something wrong happened. Try uninstall / reinstall Lip Sync Addon",
                icon="WARNING_LARGE",
            )
            return

        props = active_obj.lipsync2d_props  # type: ignore

        if props is None:
            return

        if props.lip_sync_2d_lips_type == "SHAPEKEYS":
            self.animator_panel = AnimatorPanelShapeKeysStrategy(active_obj)
        elif props.lip_sync_2d_lips_type == "SPRITESHEET":
            self.animator_panel = AnimatorPanelSpriteSheetStrategy(active_obj)
        elif props.lip_sync_2d_lips_type == "POSEASSETS":
            self.animator_panel = AnimatorPanelPoseAssetsStrategy(active_obj)

        layout = self.layout

        if (
            context.active_object is None
            or not hasattr(context.active_object, "lipsync2d_props")
            or context.active_object.lipsync2d_props.lip_sync_2d_initialized == False  # type: ignore
        ):
            row = layout.row(align=True)
            row.operator(
                "object.set_lipsync_custom_properties", text="Add Lip Sync on Selection"
            )
            return

        row = layout.row(align=True)
        row.label(text="Animation type")
        row.prop(props, "lip_sync_2d_lips_type", text="")

        if self.animator_panel is None:
            return

        layout.separator()
        self.animator_panel.draw_animator_section(context, layout)
        self.animator_panel.draw_visemes_section(context, layout)
        self.animator_panel.draw_animation_section(context, layout)
        self.animator_panel.draw_bake_section(context, layout)
        layout.separator()
        self.animator_panel.draw_baking_section(context, layout)
