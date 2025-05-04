from typing import Literal

import bpy
from bpy.types import Context

from ..Core.constants import ACTION_SUFFIX_NAME
from .LIPSYNC2D_OT_RemoveNodeGroups import LIPSYNC2D_OT_RemoveNodeGroups


class LIPSYNC2D_OT_RemoveLipSync(bpy.types.Operator):
    bl_idname = "object.remove_lip_sync_from_selection"
    bl_label = "Remove Lip Sync"
    bl_description = "Remove all Lip Sync properties from the selection. All custom settings will be forever lost"
    bl_options = {"REGISTER", "UNDO"}

    def execute(
        self, context: Context
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        obj = context.active_object

        if obj is None:
            self.report(
                {"ERROR"},
                message="Lip Sync cannot be removed! Please, select an Active Object",
            )
            return {"FINISHED"}

        elif "lipsync2d_props" in obj:

            second_message = ""
            if obj.lipsync2d_props.lip_sync_2d_remove_animation_data:  # type: ignore
                action = bpy.data.actions.get(f"{obj.name}-{ACTION_SUFFIX_NAME}")

                if action is not None:
                    bpy.data.actions.remove(action)
                else:
                    second_message = f"Could not remove the Action. Try do it manually."

            if obj.lipsync2d_props.lip_sync_2d_remove_cgp_node_group:  # type: ignore
                LIPSYNC2D_OT_RemoveNodeGroups.remove_nodes_from_materials(obj)

            del obj["lipsync2d_props"]

            self.report(
                {"INFO"}, message=f"Lip Sync successfully removed! {second_message}"
            )

        return {"FINISHED"}
