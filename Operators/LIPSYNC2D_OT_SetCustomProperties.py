import os
from typing import Literal, cast

import bpy

from ..Core.LIPSYNC2D_SpritesheetNode import cgp_spriteratio_node_group, cgp_spritesheet_reader_node_group


class LIPSYNC2D_OT_SetCustomProperties(bpy.types.Operator):
    bl_idname = "object.set_lipsync_custom_properties"
    bl_label = "Set Lips Material"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and (not hasattr(obj, "lipsync2d_props") or "lip_sync_2d_sprite_sheet" not in obj.lipsync2d_props) #type: ignore

    def execute(self, context: bpy.types.Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        if context.active_object is None:
            return {'CANCELLED'}

        create_custom_prop(context.active_object)

        context.active_object.lipsync2d_props.lip_sync_2d_sprite_sheet = add_default_image_spritesheet() #type: ignore

        return {'FINISHED'}

def add_default_image_spritesheet():
    image = bpy.data.images.get("CGP_default_spritesheet_visemes")

    if image is None:
        spritesheet_path = os.path.join(os.path.dirname(__file__),"..", "Assets", "Images", "spritesheet_visemes.png")
        image = bpy.data.images.new("CGP_default_spritesheet_visemes", width=512, height=6144)
        image.source = 'FILE'
        image.filepath = spritesheet_path

    return image

def create_custom_prop(obj: bpy.types.Object):
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet = None # type: ignore
    obj.lipsync2d_props.lip_sync_2d_main_material = None # type: ignore
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet_columns = 1 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet_rows = 12 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet_sprite_scale = 1 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet_main_scale = 1 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet_index = 0 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_sprite_sheet_format = "VLINE" # type: ignore

    #TODO: Generate this from the phoneme dict
    obj.lipsync2d_props.lip_sync_2d_viseme_sil = 0 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_PP = 4 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_FF = 7 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_TH = 1 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_DD = 9 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_kk = 9 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_CH = 10 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_SS = 2 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_nn = 10 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_RR = 3 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_aa = 11 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_E = 8 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_ih = 6 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_oh = 5 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_ou = 5 # type: ignore
    obj.lipsync2d_props.lip_sync_2d_viseme_UNK = 0 # type: ignore


def add_spritesheet_node_to_mat(active_obj, material: bpy.types.Material, spritesheet_reader: bpy.types.ShaderNodeTree):
    if material.node_tree is None: return

    group = cast(bpy.types.ShaderNodeGroup,material.node_tree.nodes.new("ShaderNodeGroup"))
    group.name = "cgp_spritesheet_reader"
    principled = cast(bpy.types.ShaderNodeGroup,material.node_tree.nodes.new("ShaderNodeBsdfPrincipled"))
    mix_shader = material.node_tree.nodes.new("ShaderNodeMixShader")

    for node in material.node_tree.nodes:
        
        if node.bl_idname == "ShaderNodeOutputMaterial":
            x_offset = 800
            next_node = node

            # Quick & Dirty way to reposition nodes to prevent node stacking
            initial_output_node_loc = next_node.location.copy()
            next_node.location.x += principled.width + x_offset + x_offset/4

            mix_shader.location = initial_output_node_loc
            mix_shader.location.x += x_offset / 1.3 + x_offset/4

            principled.location = initial_output_node_loc
            principled.location.x += x_offset / 4 + x_offset/4
            principled.location.y -= principled.height

            group.location = initial_output_node_loc
            group.location.y -= group.height
            group.location.x += x_offset/4

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
                        
                        column_field = 'nodes["cgp_spritesheet_reader"].inputs[1].default_value'
                        rows_field = 'nodes["cgp_spritesheet_reader"].inputs[2].default_value'
                        index_field = 'nodes["cgp_spritesheet_reader"].inputs[0].default_value'
                        sprite_scale_field = 'nodes["cgp_spritesheet_reader"].inputs[3].default_value'
                        main_scale_field = 'nodes["cgp_spritesheet_reader"].inputs[4].default_value'

                        add_object_driver(material.node_tree, column_field, active_obj, 'lipsync2d_props.lip_sync_2d_sprite_sheet_columns')
                        add_object_driver(material.node_tree, rows_field, active_obj,'lipsync2d_props.lip_sync_2d_sprite_sheet_rows')
                        add_object_driver(material.node_tree, index_field, active_obj, 'lipsync2d_props.lip_sync_2d_sprite_sheet_index')
                        add_object_driver(material.node_tree, sprite_scale_field, active_obj, 'lipsync2d_props.lip_sync_2d_sprite_sheet_sprite_scale')
                        add_object_driver(material.node_tree, main_scale_field, active_obj, 'lipsync2d_props.lip_sync_2d_sprite_sheet_main_scale')

def link_nodes(node_tree: bpy.types.NodeTree, output_node: bpy.types.Node, input_node: bpy.types.Node, output_socket: int, input_socket: int):
    output = output_node.outputs[output_socket]
    input = input_node.inputs[input_socket]
    node_tree.links.new(input, output)


def create_spritesheet_nodes(context: bpy.types.Context, material: bpy.types.Material) -> bpy.types.ShaderNodeTree:
    
    node_sprite_ratio = bpy.data.node_groups.get("CGP_SpriteRatio")
    nodes_spritesheet_reader = cast(bpy.types.ShaderNodeTree,bpy.data.node_groups.get("cgp_spritesheet_reader"))

    if isinstance(nodes_spritesheet_reader, bpy.types.ShaderNodeTree): return nodes_spritesheet_reader.copy()
    
    #TODO: Here we could have an issue if node is found but is not a shadernodetree. See if we should delete it or not
    if node_sprite_ratio is None:
        node_sprite_ratio = cgp_spriteratio_node_group()
    if nodes_spritesheet_reader is None:
        nodes_spritesheet_reader = cast(bpy.types.ShaderNodeTree, cgp_spritesheet_reader_node_group(node_sprite_ratio, context.active_object.lipsync2d_props.lip_sync_2d_sprite_sheet)) # type: ignore

    return nodes_spritesheet_reader

def get_or_create_material(obj: bpy.types.Object, material_index: int) -> bpy.types.Material:
    if not obj or obj.type != 'MESH' or not isinstance(obj.data, bpy.types.Mesh):
        raise TypeError("Object must be a mesh")

    # If there's already a material in the first slot
    if obj.material_slots and material_index >= 0 and material_index < len(obj.material_slots) :
        mat = obj.material_slots[material_index].material
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


def add_object_driver(
    target: bpy.types.ID,
    target_property: str,
    ref_obj:  bpy.types.ID,
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
    var.targets[0].id = ref_obj
    var.type = 'SINGLE_PROP'
    driver.expression = expression