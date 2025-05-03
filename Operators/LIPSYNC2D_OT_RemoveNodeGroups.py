from typing import Literal

import bpy

from .LIPSYNC2D_OT_SetCustomProperties import link_nodes
from ..lipsync_types import BpyContext, BpyObject


class LIPSYNC2D_OT_RemoveNodeGroups(bpy.types.Operator):
    bl_idname = "object.remove_lip_sync_node_groups"
    bl_label = "Remove Node Groups"
    bl_description = "Remove Lip Sync's node groups from Object's Materials"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: BpyContext) -> bool:
        return context.active_object is not None

    def execute(self, context: BpyContext) -> set[
        Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:

        obj = context.active_object

        if obj is None:
            self.report({'ERROR'}, message="Please, select an active object")
            return {'FINISHED'}

        message = LIPSYNC2D_OT_RemoveNodeGroups.remove_nodes_from_materials(obj)

        self.report({'INFO'}, message=message)
        return {'FINISHED'}

    @staticmethod
    def remove_nodes_from_materials(obj: BpyObject):
        materials = [m.material for m in obj.material_slots]
        prev_node = None
        next_node = None

        for m in materials:
            if m is None or m.node_tree is None:
                continue

            main_group = m.node_tree.nodes.get("cgp_main_group")

            if main_group:
                for input in main_group.inputs:
                    if input.name == "Shader":
                        links = input.links
                        if links and len(links) > 0:
                            prev_node = links[0].from_node

                for output in main_group.outputs:
                    if output.name == "Output":
                        links = output.links

                        if links and len(links) > 0:
                            next_node = links[0].to_node

                m.node_tree.nodes.remove(main_group)
                if prev_node and next_node and m.node_tree:
                    link_nodes(m.node_tree, prev_node, next_node, 0, 0)

        message = "Nodes successfully removed!" if prev_node and next_node else "Nodes were not found"
        return message
