import functools
from typing import Literal, TypedDict, cast

import bmesh
import bpy
import mathutils


class ViewState(TypedDict):
    location: mathutils.Vector
    rotation: mathutils.Quaternion
    distance: float
    perspective: Literal['PERSP','ORTHO','CAMERA']

class LIPSYNC2D_OT_SetMouthArea(bpy.types.Operator):
    bl_idname="mesh.set_lips_area"
    bl_label ="Set Lips Area"
    bl_options ={'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.mode == 'EDIT' and obj.type == 'MESH'
    
    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        obj = bpy.context.active_object

        if obj and obj.mode == 'EDIT' and isinstance(obj.data, bpy.types.Mesh):
            
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)

            selected_faces_normals = sum([f.normal for f in bm.faces if f.select], mathutils.Vector())
            average_normal = selected_faces_normals.normalized()

            quat = average_normal.to_track_quat('Z', 'Y')

            view_state = align_view_to_selection(quat)

            if context.screen is not None and context.area is not None:
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                space_view3d = cast(bpy.types.SpaceView3D, space)
                                space_view3d.shading.type = "MATERIAL"

            if view_state is not None and context.area is not None:
                activate_area_info = get_area_identifier(context.area)
                bpy.app.timers.register(functools.partial(callback, activate_area_info, view_state), first_interval=.01)

        return {'FINISHED'}
    

def callback(activate_area_info:tuple[float, float, float, float, str], view_state: ViewState) -> None:
    obj = bpy.context.active_object
    if obj is None or not isinstance(obj.data, bpy.types.Mesh):
        return
    
    if bpy.context.window is None:
        return
    
    mesh = obj.data
    bm = bmesh.from_edit_mesh(mesh)
    selected_faces = [f for f in bm.faces if f.select]
    
    uv_layer = None
    uv_layer_name = 'Mouth'
    previous_active_uv = mesh.uv_layers.active_index
    
    if not uv_layer_name:
        return
    
    uv_layer = bm.loops.layers.uv.get(uv_layer_name)
    if uv_layer is None:
        uv_layer = bm.loops.layers.uv.new(uv_layer_name)
    
    if not uv_layer:
        raise Exception("No UV map found.")
        
    mesh = obj.data
    uv_index = mesh.uv_layers.find(uv_layer_name)
    if uv_index != -1:
        mesh.uv_layers.active_index = uv_index
    
    for area in bpy.context.window.screen.areas:
        if get_area_identifier(area) == activate_area_info:
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = bpy.context.copy()
                    override["area"] = area
                    override["region"] = region
                    if area.spaces.active is None:
                        break
                    space = cast( bpy.types.SpaceView3D, area.spaces.active)
                    override["space_data"] = space
                    override["region_data"] = space.region_3d

                    with bpy.context.temp_override(**override):
                        bpy.ops.uv.project_from_view(orthographic=True, scale_to_bounds=True)
                    #TODO: Unwrap unselected faces and move them out
                    unselected = [f for f in bm.faces if not f.select]
                    for e in bm.edges:
                        e.select_set(False)

                    for f in bm.faces:
                        f.select_set(False)

                    for v in bm.verts:
                        v.select_set(False)

                    for f in unselected:
                        f.select_set(True)
                    
                    bpy.ops.uv.unwrap()
                    
                    for face in unselected:
                        for loop in face.loops:
                            loop[uv_layer].uv = mathutils.Vector([-.1,0])
                            #TODO: Rotate uv island to cancel view rotation

                    for f in unselected:
                        f.select_set(False)

                    for f in selected_faces:
                        f.select_set(True)
                    
                    break
        
    mesh.uv_layers.active_index = previous_active_uv
    return None

def get_area_identifier(area: bpy.types.Area):
    return (area.x, area.y, area.width, area.height, area.type)

def save_view_state(region_3d: bpy.types.RegionView3D) -> ViewState:
    return {
        "location": region_3d.view_location.copy(),
        "rotation": region_3d.view_rotation.copy(),
        "distance": region_3d.view_distance,
        "perspective": region_3d.view_perspective,
    }

def restore_view_state(region_3d: bpy.types.RegionView3D, view_state: ViewState):
    region_3d.view_location = view_state["location"]
    region_3d.view_rotation = view_state["rotation"]
    region_3d.view_distance = view_state["distance"]
    region_3d.view_perspective = view_state["perspective"]


def align_view_to_selection(quat: mathutils.Quaternion) -> ViewState | None:
    if bpy.context.window is None:
        return None
    
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    space = cast(bpy.types.SpaceView3D, area.spaces.active)
                    region_3d = space.region_3d
                    if region_3d is None: break

                    view_state = save_view_state(region_3d)
                    region_3d.view_rotation = quat
                    return  view_state
    return None
