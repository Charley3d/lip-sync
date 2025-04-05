from typing import Literal, cast

import bpy
from bpy.types import Context

from .LIPSYNC2D_SpritesheetNode import cgp_spritesheet_reader_node_group, spriteratio_node_group

class LIPSYNC2D_OT_UpdateMaterial(bpy.types.Operator):
    bl_idname = "mesh.set_lips_material"
    bl_label = "Set Lips Material"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        if context.active_object is None:
            return {'CANCELLED'}
        
        main_material = get_or_create_first_material(context.active_object)
        nodes_spritesheet_reader = create_spritesheet_nodes(context)

        if nodes_spritesheet_reader is None:
            return {'CANCELLED'}
        
        add_spritesheet_node_to_mat(main_material, nodes_spritesheet_reader)

        
        return {'FINISHED'}

def add_spritesheet_node_to_mat(material: bpy.types.Material, spritesheet_reader: bpy.types.ShaderNodeTree):
    if material.node_tree is None: return

    group = cast(bpy.types.ShaderNodeGroup,material.node_tree.nodes.new("ShaderNodeGroup"))
    group.name = "TEST"
    principled = cast(bpy.types.ShaderNodeGroup,material.node_tree.nodes.new("ShaderNodeBsdfPrincipled"))
    mix_shader = material.node_tree.nodes.new("ShaderNodeMixShader")

    for node in material.node_tree.nodes:
        
        if node.bl_idname == "ShaderNodeOutputMaterial":
            next_node = node
            inputs_name = node.inputs.keys()

            for input_name in inputs_name:
                if input_name == "Surface":
                    node_links = node.inputs[input_name].links
                    if node_links is None: continue

                    for link in node_links:
                        prev_node = link.from_node

                        if prev_node is None: return

                        group.node_tree = spritesheet_reader
                        material.node_tree.links.remove(link)

                        # Connect spritesheet Node to new Principled Node
                        link_nodes(material.node_tree, group, principled, 0, 0)
                        # Connect spritesheet Node Specular to new Principled Node
                        link_nodes(material.node_tree, group, principled, 2, 13)
                        # Connect spritesheet Node Roughness to new Principled Node
                        link_nodes(material.node_tree, group, principled, 3, 2)

                        # Connect spritesheet Node to Mix Node
                        link_nodes(material.node_tree, group, mix_shader,1, 0)
                        # Connect previous node to Mix Node
                        link_nodes(material.node_tree, prev_node, mix_shader, 0, 1)
                        # Connect new Principled BSDF to Mix Node
                        link_nodes(material.node_tree, principled, mix_shader, 0, 2)
                        # Connect Mix Shader to output
                        link_nodes(material.node_tree, mix_shader, next_node, 0, 0)
                        
                        column_field = 'nodes["TEST"].inputs[1].default_value'
                        rows_field = 'nodes["TEST"].inputs[2].default_value'
                        index_field = 'nodes["TEST"].inputs[0].default_value'
                        sprite_scale_field = 'nodes["TEST"].inputs[3].default_value'
                        main_scale_field = 'nodes["TEST"].inputs[4].default_value'
                        add_scene_driver(material.node_tree, column_field, 'lipsync2d_props.lip_sync_2d_sprite_sheet_columns')
                        add_scene_driver(material.node_tree, rows_field, 'lipsync2d_props.lip_sync_2d_sprite_sheet_rows')
                        add_scene_driver(material.node_tree, index_field, 'lipsync2d_props.lip_sync_2d_sprite_sheet_index')
                        add_scene_driver(material.node_tree, sprite_scale_field, 'lipsync2d_props.lip_sync_2d_sprite_sheet_sprite_scale')
                        add_scene_driver(material.node_tree, main_scale_field, 'lipsync2d_props.lip_sync_2d_sprite_sheet_main_scale')

def link_nodes(node_tree: bpy.types.NodeTree, output_node: bpy.types.Node, input_node: bpy.types.Node, output_socket: int, input_socket: int):
    output = output_node.outputs[output_socket]
    input = input_node.inputs[input_socket]
    node_tree.links.new(input, output)


def create_spritesheet_nodes(context) -> bpy.types.ShaderNodeTree | None:
    node_sprite_ratio = bpy.data.node_groups.get("CGP_SpriteRatio")
    nodes_spritesheet_reader = bpy.data.node_groups.get("cgp_spritesheet_reader")
    if not isinstance(nodes_spritesheet_reader, bpy.types.ShaderNodeTree): return

    if node_sprite_ratio is None:
        node_sprite_ratio = spriteratio_node_group()
    if nodes_spritesheet_reader is None:
        nodes_spritesheet_reader = cgp_spritesheet_reader_node_group(node_sprite_ratio, context.scene.lipsync2d_props.lip_sync_2d_sprite_sheet)

    return nodes_spritesheet_reader

def get_or_create_first_material(obj: bpy.types.Object) -> bpy.types.Material:
    if not obj or obj.type != 'MESH' or not isinstance(obj.data, bpy.types.Mesh):
        raise TypeError("Object must be a mesh")

    # If there's already a material in the first slot
    if obj.material_slots:
        mat = obj.material_slots[0].material
        if mat:
            return mat

    # No material? Create one
    new_mat = bpy.data.materials.new(name="CGP_LipsAutoMaterial")
    new_mat.use_nodes = True

    # Make sure there's at least one slot
    if not obj.material_slots:
        obj.data.materials.append(new_mat)
    else:
        obj.material_slots[0].material = new_mat

    return new_mat

def add_scene_driver(
    target: bpy.types.ID,
    target_property: str,
    data_path: str,
    expression: str = "var"
):
    """Add a driver to a node socket (input) inside a material."""

    fcurve = cast(bpy.types.FCurve, target.driver_add(target_property))
    driver = fcurve.driver
    if driver is None: return

    driver.type = 'SCRIPTED'
    var = driver.variables.new()
    var.name = "var"
    var.targets[0].data_path = data_path
    var.type = 'CONTEXT_PROP'
    var.targets[0].context_property = 'ACTIVE_SCENE'
    driver.expression = expression