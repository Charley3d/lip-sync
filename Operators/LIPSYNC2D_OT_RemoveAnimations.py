from typing import Literal
import bpy

from ..Core.constants import (
    ACTION_SUFFIX_NAME,
    SLOT_POSE_LIB_NAME,
    SLOT_SHAPE_KEY_NAME,
    SLOT_SPRITE_SHEET_NAME,
)

from ..lipsync_types import BpyContext


class LIPSYNC2D_OT_RemoveAnimations(bpy.types.Operator):
    bl_idname = "object.remove_lip_sync_animations"
    bl_label = "Remove Animations"
    bl_description = (
        "Remove Lip Sync Animation Data from your Object. "
        "\n"
        "\nSK: ShapeKeys Animation Data."
        "\nPose: Poses Animation Data."
        "\nSPT: Sprite Sheet Animation Data."
        "\nall: Remove the entire Action"
    )
    bl_options = {"UNDO"}

    animation_type: bpy.props.StringProperty(name="animation_type")  # type: ignore

    @classmethod
    def poll(cls, context: BpyContext) -> bool:
        return context.active_object is not None

    def execute(
        self, context: BpyContext
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        obj = context.active_object

        if obj is None:
            return {"FINISHED"}

        action = bpy.data.actions.get(f"{obj.name}-{ACTION_SUFFIX_NAME}")

        if action is not None:
            if self.animation_type == "ALL":
                bpy.data.actions.remove(action)
                self.report({"INFO"}, message="Animation successfully removed!")
                return {"FINISHED"}

            slots = []
            if self.animation_type == "SHAPEKEYS":
                slots = [action.slots.get(f"KE{SLOT_SHAPE_KEY_NAME}")]
            elif self.animation_type == "SPRITESHEET":
                slots = [action.slots.get(f"OB{SLOT_SPRITE_SHEET_NAME}")]
            elif self.animation_type == "POSELIB":
                slots = [action.slots.get(f"OB{SLOT_POSE_LIB_NAME}")]

            for slot in slots:
                if slot is not None:
                    action.slots.remove(slot)

            if all(slot is not None for slot in slots):
                self.report({"INFO"}, message="Animation successfully removed!")
            else:
                self.report({"WARNING"}, message="Slot not found.")

        else:
            self.report(
                {"WARNING"}, message="Action not found. Cannot remove Animation."
            )

        return {"FINISHED"}
