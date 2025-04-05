# type: ignore
import bpy

#initialize CGP_SpriteRatio node group
def spriteratio_node_group():

    spriteratio = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "CGP_SpriteRatio")

    spriteratio.color_tag = 'NONE'
    spriteratio.description = ""
    spriteratio.default_group_node_width = 140
    

    #spriteratio interface
    #Socket Vector
    vector_socket = spriteratio.interface.new_socket(name = "Vector", in_out='OUTPUT', socket_type = 'NodeSocketVector')
    vector_socket.default_value = (0.0, 0.0, 0.0)
    vector_socket.min_value = -3.4028234663852886e+38
    vector_socket.max_value = 3.4028234663852886e+38
    vector_socket.subtype = 'NONE'
    vector_socket.attribute_domain = 'POINT'

    #Socket X
    x_socket = spriteratio.interface.new_socket(name = "X", in_out='INPUT', socket_type = 'NodeSocketFloat')
    x_socket.default_value = 0.0
    x_socket.min_value = -10000.0
    x_socket.max_value = 10000.0
    x_socket.subtype = 'NONE'
    x_socket.attribute_domain = 'POINT'

    #Socket Y
    y_socket = spriteratio.interface.new_socket(name = "Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
    y_socket.default_value = 0.0
    y_socket.min_value = -10000.0
    y_socket.max_value = 10000.0
    y_socket.subtype = 'NONE'
    y_socket.attribute_domain = 'POINT'


    #initialize spriteratio nodes
    #node Group Output
    group_output = spriteratio.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Group Input
    group_input = spriteratio.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Vector Math.002
    vector_math_002 = spriteratio.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'NORMALIZE'

    #node Combine XYZ
    combine_xyz = spriteratio.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    #Z
    combine_xyz.inputs[2].default_value = 1.0


    #Set locations
    group_output.location = (268.53369140625, 0.0)
    group_input.location = (-278.5335693359375, 0.0)
    vector_math_002.location = (78.53369140625, -0.07513427734375)
    combine_xyz.location = (-78.5335693359375, 0.0751953125)

    #Set dimensions
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    vector_math_002.width, vector_math_002.height = 140.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0

    #initialize spriteratio links
    #combine_xyz.Vector -> vector_math_002.Vector
    spriteratio.links.new(combine_xyz.outputs[0], vector_math_002.inputs[0])
    #group_input.X -> combine_xyz.X
    spriteratio.links.new(group_input.outputs[0], combine_xyz.inputs[0])
    #group_input.Y -> combine_xyz.Y
    spriteratio.links.new(group_input.outputs[1], combine_xyz.inputs[1])
    #vector_math_002.Vector -> group_output.Vector
    spriteratio.links.new(vector_math_002.outputs[0], group_output.inputs[0])
    return spriteratio

# spriteratio = spriteratio_node_group()

#initialize cgp_spritesheet_reader node group
def cgp_spritesheet_reader_node_group(spriteratio, sprite_image):

    cgp_spritesheet_reader = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = "cgp_spritesheet_reader")

    cgp_spritesheet_reader.color_tag = 'NONE'
    cgp_spritesheet_reader.description = ""
    cgp_spritesheet_reader.default_group_node_width = 193
    

    #cgp_spritesheet_reader interface
    #Socket Sprite
    sprite_socket = cgp_spritesheet_reader.interface.new_socket(name = "Sprite", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    sprite_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    sprite_socket.attribute_domain = 'POINT'

    #Socket Mix
    mix_socket = cgp_spritesheet_reader.interface.new_socket(name = "Mix", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
    mix_socket.default_value = 0.0
    mix_socket.min_value = -3.4028234663852886e+38
    mix_socket.max_value = 3.4028234663852886e+38
    mix_socket.subtype = 'NONE'
    mix_socket.attribute_domain = 'POINT'

    #Socket Specular
    specular_socket = cgp_spritesheet_reader.interface.new_socket(name = "Specular", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    specular_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    specular_socket.attribute_domain = 'POINT'

    #Socket Roughness
    roughness_socket = cgp_spritesheet_reader.interface.new_socket(name = "Roughness", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    roughness_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    roughness_socket.attribute_domain = 'POINT'

    #Socket Sprite Index
    sprite_index_socket = cgp_spritesheet_reader.interface.new_socket(name = "Sprite Index", in_out='INPUT', socket_type = 'NodeSocketFloat')
    sprite_index_socket.default_value = 0.0
    sprite_index_socket.min_value = -10000.0
    sprite_index_socket.max_value = 10000.0
    sprite_index_socket.subtype = 'NONE'
    sprite_index_socket.attribute_domain = 'POINT'

    #Socket Columns
    columns_socket = cgp_spritesheet_reader.interface.new_socket(name = "Columns", in_out='INPUT', socket_type = 'NodeSocketFloat')
    columns_socket.default_value = 1.0
    columns_socket.min_value = -3.4028234663852886e+38
    columns_socket.max_value = 3.4028234663852886e+38
    columns_socket.subtype = 'NONE'
    columns_socket.attribute_domain = 'POINT'

    #Socket Rows
    rows_socket = cgp_spritesheet_reader.interface.new_socket(name = "Rows", in_out='INPUT', socket_type = 'NodeSocketFloat')
    rows_socket.default_value = 1.0
    rows_socket.min_value = -3.4028234663852886e+38
    rows_socket.max_value = 3.4028234663852886e+38
    rows_socket.subtype = 'NONE'
    rows_socket.attribute_domain = 'POINT'

    #Socket Image Scale
    image_scale_socket = cgp_spritesheet_reader.interface.new_socket(name = "Image Scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
    image_scale_socket.default_value = 1.0
    image_scale_socket.min_value = -10000.0
    image_scale_socket.max_value = 10000.0
    image_scale_socket.subtype = 'NONE'
    image_scale_socket.attribute_domain = 'POINT'

    #Socket Main Scale
    main_scale_socket = cgp_spritesheet_reader.interface.new_socket(name = "Main Scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
    main_scale_socket.default_value = 1.0
    main_scale_socket.min_value = -3.4028234663852886e+38
    main_scale_socket.max_value = 3.4028234663852886e+38
    main_scale_socket.subtype = 'NONE'
    main_scale_socket.attribute_domain = 'POINT'

    #Socket Main Offset
    main_offset_socket = cgp_spritesheet_reader.interface.new_socket(name = "Main Offset", in_out='INPUT', socket_type = 'NodeSocketVector')
    main_offset_socket.default_value = (0.0, 0.0, 0.0)
    main_offset_socket.min_value = -10000.0
    main_offset_socket.max_value = 10000.0
    main_offset_socket.subtype = 'NONE'
    main_offset_socket.attribute_domain = 'POINT'


    #initialize cgp_spritesheet_reader nodes
    #node Group Output
    group_output_1 = cgp_spritesheet_reader.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True

    #node Group Input
    group_input_1 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_1.name = "Group Input"
    group_input_1.outputs[3].hide = True
    group_input_1.outputs[4].hide = True
    group_input_1.outputs[5].hide = True
    group_input_1.outputs[6].hide = True

    #node Frame
    frame = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame.label = "Position & Scale Mask"
    frame.name = "Frame"
    frame.use_custom_color = True
    frame.color = (0.15378153324127197, 0.2822643518447876, 0.43038833141326904)
    frame.label_size = 42
    frame.shrink = False

    #node Separate XYZ
    separate_xyz = cgp_spritesheet_reader.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    #node Mapping.001
    mapping_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeMapping")
    mapping_001.name = "Mapping.001"
    mapping_001.vector_type = 'VECTOR'
    #Rotation
    mapping_001.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Combine XYZ.001
    combine_xyz_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.label = "ForceCenter"
    combine_xyz_001.name = "Combine XYZ.001"
    #Z
    combine_xyz_001.inputs[2].default_value = 0.0

    #node Math.002
    math_002 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'LESS_THAN'
    math_002.use_clamp = False

    #node Math.003
    math_003 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'GREATER_THAN'
    math_003.use_clamp = False
    #Value_001
    math_003.inputs[1].default_value = 0.0

    #node Math.004
    math_004 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'MINIMUM'
    math_004.use_clamp = False

    #node Reroute
    reroute = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketFloat"
    #node Reroute.001
    reroute_001 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketFloat"
    #node Math.005
    math_005 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'LESS_THAN'
    math_005.use_clamp = False

    #node Math.006
    math_006 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'GREATER_THAN'
    math_006.use_clamp = False
    #Value_001
    math_006.inputs[1].default_value = 0.0

    #node Math.007
    math_007 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'MINIMUM'
    math_007.use_clamp = False

    #node Reroute.002
    reroute_002 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketFloat"
    #node Reroute.003
    reroute_003 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.socket_idname = "NodeSocketFloat"
    #node Reroute.004
    reroute_004 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.socket_idname = "NodeSocketFloat"
    #node Math.008
    math_008 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'MINIMUM'
    math_008.use_clamp = False

    #node Value.003
    value_003 = cgp_spritesheet_reader.nodes.new("ShaderNodeValue")
    value_003.label = "X Total"
    value_003.name = "Value.003"

    value_003.outputs[0].default_value = 1.0
    #node Value.004
    value_004 = cgp_spritesheet_reader.nodes.new("ShaderNodeValue")
    value_004.label = "Y Total"
    value_004.name = "Value.004"

    value_004.outputs[0].default_value = 1.0
    #node Math.009
    math_009 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'DIVIDE'
    math_009.use_clamp = False
    #Value
    math_009.inputs[0].default_value = 1.0

    #node Math.010
    math_010 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'DIVIDE'
    math_010.use_clamp = False
    #Value
    math_010.inputs[0].default_value = 1.0

    #node Frame.001
    frame_001 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_001.label = "Width Ratio"
    frame_001.name = "Frame.001"
    frame_001.use_custom_color = True
    frame_001.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    frame_001.label_size = 20
    frame_001.shrink = True

    #node Frame.002
    frame_002 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_002.label = "Height Ratio"
    frame_002.name = "Frame.002"
    frame_002.use_custom_color = True
    frame_002.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    frame_002.label_size = 20
    frame_002.shrink = True

    #node Reroute.005
    reroute_005 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.socket_idname = "NodeSocketFloat"
    #node UV Map
    uv_map = cgp_spritesheet_reader.nodes.new("ShaderNodeUVMap")
    uv_map.name = "UV Map"
    uv_map.from_instancer = False
    uv_map.uv_map = "Mouth"

    #node Image Texture.001
    image_texture_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeTexImage")
    image_texture_001.name = "Image Texture.001"
    image_texture_001.extension = 'CLIP'
    if sprite_image and sprite_image.name in bpy.data.images:
        image_texture_001.image = sprite_image
    image_texture_001.image_user.frame_current = 0
    image_texture_001.image_user.frame_duration = 1
    image_texture_001.image_user.frame_offset = -1
    image_texture_001.image_user.frame_start = 1
    image_texture_001.image_user.tile = 0
    image_texture_001.image_user.use_auto_refresh = False
    image_texture_001.image_user.use_cyclic = False
    image_texture_001.interpolation = 'Cubic'
    image_texture_001.projection = 'FLAT'
    image_texture_001.projection_blend = 0.0

    #node Attribute.002
    attribute_002 = cgp_spritesheet_reader.nodes.new("ShaderNodeAttribute")
    attribute_002.name = "Attribute.002"
    attribute_002.attribute_name = "Mouth"
    attribute_002.attribute_type = 'GEOMETRY'

    #node Math.011
    math_011 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_011.label = "Apply Main Scale"
    math_011.name = "Math.011"
    math_011.operation = 'DIVIDE'
    math_011.use_clamp = False

    #node Math.012
    math_012 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.operation = 'MINIMUM'
    math_012.use_clamp = True

    #node Combine XYZ.003
    combine_xyz_003 = cgp_spritesheet_reader.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_003.label = "ImageOffset"
    combine_xyz_003.name = "Combine XYZ.003"
    #Z
    combine_xyz_003.inputs[2].default_value = 0.0

    #node Color Ramp
    color_ramp = cgp_spritesheet_reader.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'CONSTANT'

    #initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.0
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.39545515179634094)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    #node Invert Color
    invert_color = cgp_spritesheet_reader.nodes.new("ShaderNodeInvert")
    invert_color.name = "Invert Color"
    #Fac
    invert_color.inputs[0].default_value = 1.0

    #node Mapping.003
    mapping_003 = cgp_spritesheet_reader.nodes.new("ShaderNodeMapping")
    mapping_003.name = "Mapping.003"
    mapping_003.vector_type = 'VECTOR'
    #Rotation
    mapping_003.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Vector Math.006
    vector_math_006 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'ADD'

    #node Math.022
    math_022 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_022.label = "Apply Image Scale"
    math_022.name = "Math.022"
    math_022.operation = 'DIVIDE'
    math_022.use_clamp = False

    #node Reroute.010
    reroute_010 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.socket_idname = "NodeSocketFloat"
    #node Math
    math = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math.label = "Invert Image Scale"
    math.name = "Math"
    math.operation = 'DIVIDE'
    math.use_clamp = False
    #Value
    math.inputs[0].default_value = 1.0

    #node Vector Math
    vector_math = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'SUBTRACT'

    #node Math.013
    math_013 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_013.label = "Apply Main Scale"
    math_013.name = "Math.013"
    math_013.operation = 'MULTIPLY'
    math_013.use_clamp = False

    #node Vector Math.001
    vector_math_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'ADD'

    #node Reroute.011
    reroute_011 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.socket_idname = "NodeSocketFloat"
    #node Math.001
    math_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'SUBTRACT'
    math_001.use_clamp = False
    #Value
    math_001.inputs[0].default_value = 1.0

    #node Math.014
    math_014 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.operation = 'DIVIDE'
    math_014.use_clamp = False
    #Value_001
    math_014.inputs[1].default_value = 2.0

    #node Frame.003
    frame_003 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_003.label = "Keep Mouth in middle"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    #node Math.024
    math_024 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_024.label = "Apply Image Scale"
    math_024.name = "Math.024"
    math_024.operation = 'DIVIDE'
    math_024.use_clamp = False

    #node Math.015
    math_015 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_015.label = "Apply Main Scale"
    math_015.name = "Math.015"
    math_015.operation = 'MULTIPLY'
    math_015.use_clamp = False

    #node Reroute.012
    reroute_012 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.socket_idname = "NodeSocketFloat"
    #node Reroute.014
    reroute_014 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.socket_idname = "NodeSocketFloat"
    #node Math.023
    math_023 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.operation = 'DIVIDE'
    math_023.use_clamp = False

    #node Math.028
    math_028 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_028.name = "Math.028"
    math_028.operation = 'TRUNC'
    math_028.use_clamp = False

    #node Math.029
    math_029 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_029.name = "Math.029"
    math_029.operation = 'DIVIDE'
    math_029.use_clamp = False
    #Value
    math_029.inputs[0].default_value = 1.0

    #node Math.030
    math_030 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_030.name = "Math.030"
    math_030.operation = 'MULTIPLY'
    math_030.use_clamp = False

    #node Math.026
    math_026 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_026.name = "Math.026"
    math_026.operation = 'TRUNC'
    math_026.use_clamp = False

    #node Math.027
    math_027 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_027.name = "Math.027"
    math_027.operation = 'MULTIPLY'
    math_027.use_clamp = False

    #node Math.031
    math_031 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_031.name = "Math.031"
    math_031.operation = 'DIVIDE'
    math_031.use_clamp = False
    #Value
    math_031.inputs[0].default_value = 1.0

    #node Math.032
    math_032 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_032.name = "Math.032"
    math_032.operation = 'MODULO'
    math_032.use_clamp = False

    #node Reroute.007
    reroute_007 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.socket_idname = "NodeSocketFloat"
    #node Map Range.001
    map_range_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.clamp = True
    map_range_001.data_type = 'FLOAT'
    map_range_001.interpolation_type = 'LINEAR'
    #From Min
    map_range_001.inputs[1].default_value = 0.0
    #To Min
    map_range_001.inputs[3].default_value = 0.0

    #node Math.025
    math_025 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_025.name = "Math.025"
    math_025.operation = 'MULTIPLY_ADD'
    math_025.use_clamp = False
    #Value_002
    math_025.inputs[2].default_value = -1.0

    #node Group Input.001
    group_input_001 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[4].hide = True
    group_input_001.outputs[5].hide = True
    group_input_001.outputs[6].hide = True

    #node Group Input.002
    group_input_002 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True

    #node Reroute.017
    reroute_017 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_017.name = "Reroute.017"
    reroute_017.socket_idname = "NodeSocketFloat"
    #node Vector Math.007
    vector_math_007 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'MULTIPLY'

    #node Group Input.003
    group_input_003 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[4].hide = True
    group_input_003.outputs[5].hide = True
    group_input_003.outputs[6].hide = True

    #node Group Input.004
    group_input_004 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True

    #node Group Input.005
    group_input_005 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[4].hide = True
    group_input_005.outputs[5].hide = True
    group_input_005.outputs[6].hide = True

    #node Group Input.006
    group_input_006 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[0].hide = True
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[3].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True
    group_input_006.outputs[6].hide = True

    #node Math.033
    math_033 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_033.name = "Math.033"
    math_033.operation = 'MULTIPLY'
    math_033.use_clamp = False

    #node Group Input.007
    group_input_007 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_007.name = "Group Input.007"
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    group_input_007.outputs[5].hide = True
    group_input_007.outputs[6].hide = True

    #node Math.016
    math_016 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.operation = 'GREATER_THAN'
    math_016.use_clamp = False
    #Value_001
    math_016.inputs[1].default_value = 1.0

    #node Math.017
    math_017 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_017.name = "Math.017"
    math_017.operation = 'TRUNC'
    math_017.use_clamp = False

    #node Group
    group = cgp_spritesheet_reader.nodes.new("ShaderNodeGroup")
    group.name = "Group"
    group.node_tree = spriteratio

    #node Group Input.008
    group_input_008 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_008.name = "Group Input.008"
    group_input_008.outputs[0].hide = True
    group_input_008.outputs[3].hide = True
    group_input_008.outputs[4].hide = True
    group_input_008.outputs[5].hide = True
    group_input_008.outputs[6].hide = True

    #node Group.001
    group_001 = cgp_spritesheet_reader.nodes.new("ShaderNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = spriteratio

    #node Vector Math.002
    vector_math_002_1 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_002_1.label = "Apply Image Ratio"
    vector_math_002_1.name = "Vector Math.002"
    vector_math_002_1.operation = 'MULTIPLY'

    #node Group Input.011
    group_input_011 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_011.name = "Group Input.011"
    group_input_011.outputs[0].hide = True
    group_input_011.outputs[1].hide = True
    group_input_011.outputs[2].hide = True
    group_input_011.outputs[3].hide = True
    group_input_011.outputs[4].hide = True
    group_input_011.outputs[6].hide = True

    #node Group Input.012
    group_input_012 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_012.name = "Group Input.012"
    group_input_012.outputs[0].hide = True
    group_input_012.outputs[1].hide = True
    group_input_012.outputs[2].hide = True
    group_input_012.outputs[3].hide = True
    group_input_012.outputs[4].hide = True
    group_input_012.outputs[6].hide = True

    #node Vector Math.008
    vector_math_008 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'SUBTRACT'

    #node Math.034
    math_034 = cgp_spritesheet_reader.nodes.new("ShaderNodeMath")
    math_034.name = "Math.034"
    math_034.operation = 'DIVIDE'
    math_034.use_clamp = False
    #Value
    math_034.inputs[0].default_value = 1.0

    #node Vector Math.009
    vector_math_009 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'MULTIPLY'

    #node Vector Math.010
    vector_math_010 = cgp_spritesheet_reader.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'SUBTRACT'

    #node Frame.004
    frame_004 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_004.label = "Find Y index"
    frame_004.name = "Frame.004"
    frame_004.use_custom_color = True
    frame_004.color = (0.29359620809555054, 0.47468459606170654, 0.21658125519752502)
    frame_004.label_size = 42
    frame_004.shrink = False

    #node Frame.005
    frame_005 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_005.label = "Find X index"
    frame_005.name = "Frame.005"
    frame_005.use_custom_color = True
    frame_005.color = (0.29360729455947876, 0.47467735409736633, 0.21658824384212494)
    frame_005.label_size = 38
    frame_005.shrink = False

    #node Frame.006
    frame_006 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_006.label = "Image Scale"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True

    #node Reroute.006
    reroute_006 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.socket_idname = "NodeSocketFloat"
    #node Reroute.008
    reroute_008 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.socket_idname = "NodeSocketFloat"
    #node Reroute.009
    reroute_009 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.socket_idname = "NodeSocketFloat"
    #node Reroute.016
    reroute_016 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_016.name = "Reroute.016"
    reroute_016.socket_idname = "NodeSocketFloat"
    #node Reroute.018
    reroute_018 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_018.name = "Reroute.018"
    reroute_018.socket_idname = "NodeSocketFloat"
    #node Reroute.021
    reroute_021 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_021.name = "Reroute.021"
    reroute_021.socket_idname = "NodeSocketVector"
    #node Reroute.022
    reroute_022 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_022.name = "Reroute.022"
    reroute_022.socket_idname = "NodeSocketVector"
    #node Reroute.019
    reroute_019 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_019.name = "Reroute.019"
    reroute_019.socket_idname = "NodeSocketVector"
    #node Reroute.020
    reroute_020 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    reroute_020.socket_idname = "NodeSocketVector"
    #node Reroute.023
    reroute_023 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_023.name = "Reroute.023"
    reroute_023.socket_idname = "NodeSocketVector"
    #node Reroute.013
    reroute_013 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.socket_idname = "NodeSocketFloat"
    #node Reroute.015
    reroute_015 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_015.name = "Reroute.015"
    reroute_015.socket_idname = "NodeSocketFloat"
    #node Reroute.024
    reroute_024 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_024.name = "Reroute.024"
    reroute_024.socket_idname = "NodeSocketVector"
    #node Reroute.025
    reroute_025 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_025.name = "Reroute.025"
    reroute_025.socket_idname = "NodeSocketVector"
    #node Group Input.009
    group_input_009 = cgp_spritesheet_reader.nodes.new("NodeGroupInput")
    group_input_009.name = "Group Input.009"
    group_input_009.outputs[0].hide = True
    group_input_009.outputs[1].hide = True
    group_input_009.outputs[2].hide = True
    group_input_009.outputs[3].hide = True
    group_input_009.outputs[5].hide = True
    group_input_009.outputs[6].hide = True

    #node Reroute.026
    reroute_026 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_026.name = "Reroute.026"
    reroute_026.socket_idname = "NodeSocketVector"
    #node Reroute.027
    reroute_027 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_027.name = "Reroute.027"
    reroute_027.socket_idname = "NodeSocketVector"
    #node Reroute.028
    reroute_028 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_028.name = "Reroute.028"
    reroute_028.socket_idname = "NodeSocketColor"
    #node Reroute.029
    reroute_029 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_029.name = "Reroute.029"
    reroute_029.socket_idname = "NodeSocketColor"
    #node Reroute.030
    reroute_030 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_030.name = "Reroute.030"
    reroute_030.socket_idname = "NodeSocketColor"
    #node Reroute.031
    reroute_031 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_031.name = "Reroute.031"
    reroute_031.socket_idname = "NodeSocketColor"
    #node Reroute.032
    reroute_032 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_032.name = "Reroute.032"
    reroute_032.socket_idname = "NodeSocketColor"
    #node Reroute.033
    reroute_033 = cgp_spritesheet_reader.nodes.new("NodeReroute")
    reroute_033.name = "Reroute.033"
    reroute_033.socket_idname = "NodeSocketColor"
    #node Frame.007
    frame_007 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_007.label = "Position & Scale Image"
    frame_007.name = "Frame.007"
    frame_007.use_custom_color = True
    frame_007.color = (0.1537686288356781, 0.28227511048316956, 0.43037357926368713)
    frame_007.label_size = 43
    frame_007.shrink = False

    #node Frame.008
    frame_008 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_008.label = "Add Main Offset"
    frame_008.name = "Frame.008"
    frame_008.label_size = 24
    frame_008.shrink = False

    #node Frame.009
    frame_009 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_009.label = "Apply Scales"
    frame_009.name = "Frame.009"
    frame_009.use_custom_color = True
    frame_009.color = (0.4050571024417877, 0.16369223594665527, 0.2130303531885147)
    frame_009.label_size = 33
    frame_009.shrink = False

    #node Frame.010
    frame_010 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_010.label = "Apply Scales"
    frame_010.name = "Frame.010"
    frame_010.use_custom_color = True
    frame_010.color = (0.40505117177963257, 0.16370615363121033, 0.2130207121372223)
    frame_010.label_size = 33
    frame_010.shrink = True

    #node Frame.011
    frame_011 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_011.label = "Specular & Roughness"
    frame_011.name = "Frame.011"
    frame_011.label_size = 38
    frame_011.shrink = False

    #node Frame.012
    frame_012 = cgp_spritesheet_reader.nodes.new("NodeFrame")
    frame_012.label = "Clamp Index"
    frame_012.name = "Frame.012"
    frame_012.label_size = 39
    frame_012.shrink = False

    #Set parents
    separate_xyz.parent = frame
    mapping_001.parent = frame
    combine_xyz_001.parent = frame_003
    math_002.parent = frame
    math_003.parent = frame
    math_004.parent = frame
    reroute.parent = frame
    reroute_001.parent = frame
    math_005.parent = frame
    math_006.parent = frame
    math_007.parent = frame
    reroute_002.parent = frame
    reroute_003.parent = frame
    reroute_004.parent = frame
    math_008.parent = frame
    value_003.parent = frame_001
    value_004.parent = frame_002
    math_009.parent = frame_001
    math_010.parent = frame_002
    frame_001.parent = frame
    frame_002.parent = frame
    reroute_005.parent = frame
    uv_map.parent = frame
    image_texture_001.parent = frame_007
    attribute_002.parent = frame_007
    math_011.parent = frame_007
    color_ramp.parent = frame_011
    invert_color.parent = frame_011
    mapping_003.parent = frame_007
    vector_math_006.parent = frame_007
    math_022.parent = frame_009
    math.parent = frame_006
    vector_math.parent = frame_007
    math_013.parent = frame_009
    math_001.parent = frame_003
    math_014.parent = frame_003
    math_024.parent = frame_010
    math_015.parent = frame_010
    math_023.parent = frame_004
    math_028.parent = frame_004
    math_029.parent = frame_004
    math_030.parent = frame_004
    math_026.parent = frame_005
    math_027.parent = frame_005
    math_031.parent = frame_005
    math_032.parent = frame_005
    map_range_001.parent = frame_012
    math_025.parent = frame_012
    group_input_001.parent = frame_006
    vector_math_007.parent = frame_007
    group_input_003.parent = frame_007
    group_input_004.parent = frame_005
    group_input_005.parent = frame_005
    group_input_006.parent = frame_004
    math_033.parent = frame_004
    group_input_007.parent = frame_004
    math_016.parent = frame_004
    math_017.parent = frame_004
    group.parent = frame_007
    group_input_008.parent = frame_008
    group_001.parent = frame_008
    group_input_011.parent = frame_008
    group_input_012.parent = frame
    vector_math_008.parent = frame
    math_034.parent = frame
    vector_math_009.parent = frame_008
    vector_math_010.parent = frame
    reroute_006.parent = frame_009
    reroute_008.parent = frame_010
    reroute_023.parent = frame_008
    group_input_009.parent = frame_003
    reroute_028.parent = frame_011
    reroute_029.parent = frame_011
    reroute_030.parent = frame_011
    reroute_031.parent = frame_011

    #Set locations
    group_output_1.location = (3720.0, 740.0)
    group_input_1.location = (-4415.060546875, -24.059814453125)
    frame.location = (500.0, 252.5)
    separate_xyz.location = (686.036865234375, -489.8516845703125)
    mapping_001.location = (502.601318359375, -497.6370849609375)
    combine_xyz_001.location = (346.3048095703125, -41.10009765625)
    math_002.location = (704.05126953125, -82.52813720703125)
    math_003.location = (698.7685546875, -261.3013916015625)
    math_004.location = (884.71875, -132.24591064453125)
    reroute.location = (599.8408203125, -190.18243408203125)
    reroute_001.location = (599.8408203125, -532.8446044921875)
    math_005.location = (1116.777099609375, -915.7269287109375)
    math_006.location = (1098.0, -1112.5)
    math_007.location = (1297.444580078125, -965.4451904296875)
    reroute_002.location = (1018.135498046875, -1023.3812255859375)
    reroute_003.location = (1018.0, -1222.5)
    reroute_004.location = (1018.135498046875, -556.3814697265625)
    math_008.location = (1538.0, -532.5)
    value_003.location = (29.57373046875, -67.7200927734375)
    value_004.location = (29.78369140625, -116.2166748046875)
    math_009.location = (260.9111328125, -40.21002197265625)
    math_010.location = (257.951171875, -40.0462646484375)
    frame_001.location = (80.0, -141.5)
    frame_002.location = (518.0, -972.5)
    reroute_005.location = (599.8408203125, -364.7384033203125)
    uv_map.location = (29.726806640625, -591.9075927734375)
    image_texture_001.location = (1270.0, -261.0)
    attribute_002.location = (230.0, -85.0)
    math_011.location = (230.0, -425.0)
    math_012.location = (2700.0, 520.0)
    combine_xyz_003.location = (-860.0, 440.0)
    color_ramp.location = (30.0, -78.75)
    invert_color.location = (490.0, -418.75)
    mapping_003.location = (1050.0, -321.0)
    vector_math_006.location = (870.0, -341.0)
    math_022.location = (30.0, -90.0)
    reroute_010.location = (-1860.0, 640.0)
    math.location = (29.9453125, -39.6527099609375)
    vector_math.location = (230.0, -721.0)
    math_013.location = (310.0, -90.0)
    vector_math_001.location = (80.0, -320.0)
    reroute_011.location = (-1520.0, 40.0)
    math_001.location = (29.5362548828125, -42.138916015625)
    math_014.location = (181.7032470703125, -39.8486328125)
    frame_003.location = (-840.0, -20.0)
    math_024.location = (30.0, -116.25)
    math_015.location = (370.0, -56.25)
    reroute_012.location = (-1860.0, 330.0)
    reroute_014.location = (-1860.0, -450.0)
    math_023.location = (272.53173828125, -95.82254028320312)
    math_028.location = (430.0, -95.0)
    math_029.location = (274.7841796875, -275.1216125488281)
    math_030.location = (650.0, -175.0)
    math_026.location = (30.0, -96.25)
    math_027.location = (510.0, -96.25)
    math_031.location = (270.0, -336.25)
    math_032.location = (270.0, -76.25)
    reroute_007.location = (-3402.95166015625, 37.15393829345703)
    map_range_001.location = (340.30322265625, -95.10816955566406)
    math_025.location = (29.61474609375, -240.17730712890625)
    group_input_001.location = (30.0, -208.0)
    group_input_002.location = (-1720.0, 80.0)
    reroute_017.location = (-1520.0, -180.0)
    vector_math_007.location = (430.0, -85.0)
    group_input_003.location = (30.0, -325.0)
    group_input_004.location = (270.0, -236.25)
    group_input_005.location = (270.0, -496.25)
    group_input_006.location = (30.0, -255.0)
    math_033.location = (1030.0, -195.0)
    group_input_007.location = (650.0, -655.0)
    math_016.location = (650.0, -355.0)
    math_017.location = (650.0, -515.0)
    group.location = (230.0, -285.0)
    group_input_008.location = (30.0, -100.0)
    group_001.location = (190.0, -60.0)
    vector_math_002_1.location = (-160.0, -220.0)
    group_input_011.location = (510.0, -240.0)
    group_input_012.location = (232.45361328125, -609.7247314453125)
    vector_math_008.location = (230.095458984375, -472.186767578125)
    math_034.location = (218.0, -692.5)
    vector_math_009.location = (510.0, -100.0)
    vector_math_010.location = (34.726806640625, -451.9076232910156)
    frame_004.location = (-3180.0, -200.0)
    frame_005.location = (-3190.0, 516.25)
    frame_006.location = (-2380.0, 720.0)
    reroute_006.location = (270.0, -220.0)
    reroute_008.location = (290.0, -188.25)
    reroute_009.location = (300.0, 20.0)
    reroute_016.location = (300.0, 606.0)
    reroute_018.location = (300.0, -540.0)
    reroute_021.location = (-280.0, -100.0)
    reroute_022.location = (-280.0, -300.0)
    reroute_019.location = (-280.0, -500.0)
    reroute_020.location = (-280.0, -320.0)
    reroute_023.location = (390.0, -180.0)
    reroute_013.location = (-1000.0, 360.0)
    reroute_015.location = (-1000.0, -294.0)
    reroute_024.location = (260.0, 340.0)
    reroute_025.location = (260.0, -354.0)
    group_input_009.location = (29.5362548828125, -205.138916015625)
    reroute_026.location = (442.0, -302.0)
    reroute_027.location = (440.0, -112.0)
    reroute_028.location = (370.0, -118.75)
    reroute_029.location = (370.0, -498.75)
    reroute_030.location = (510.0, -118.75)
    reroute_031.location = (510.0, -398.75)
    reroute_032.location = (2440.0, 840.0)
    reroute_033.location = (2440.0, 720.0)
    frame_007.location = (500.0, 1175.0)
    frame_008.location = (-670.0, -400.0)
    frame_009.location = (-1790.0, 550.0)
    frame_010.location = (-1810.0, -203.75)
    frame_011.location = (2610.0, 1098.75)
    frame_012.location = (-3977.0, 168.0)

    #Set dimensions
    group_output_1.width, group_output_1.height = 140.0, 100.0
    group_input_1.width, group_input_1.height = 140.0, 100.0
    frame.width, frame.height = 1708.0, 1290.5
    separate_xyz.width, separate_xyz.height = 140.0, 100.0
    mapping_001.width, mapping_001.height = 140.0, 100.0
    combine_xyz_001.width, combine_xyz_001.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    reroute.width, reroute.height = 10.0, 100.0
    reroute_001.width, reroute_001.height = 10.0, 100.0
    math_005.width, math_005.height = 140.0, 100.0
    math_006.width, math_006.height = 140.0, 100.0
    math_007.width, math_007.height = 140.0, 100.0
    reroute_002.width, reroute_002.height = 10.0, 100.0
    reroute_003.width, reroute_003.height = 10.0, 100.0
    reroute_004.width, reroute_004.height = 10.0, 100.0
    math_008.width, math_008.height = 140.0, 100.0
    value_003.width, value_003.height = 140.0, 100.0
    value_004.width, value_004.height = 140.0, 100.0
    math_009.width, math_009.height = 140.0, 100.0
    math_010.width, math_010.height = 140.0, 100.0
    frame_001.width, frame_001.height = 431.0, 218.0
    frame_002.width, frame_002.height = 428.0, 225.0
    reroute_005.width, reroute_005.height = 10.0, 100.0
    uv_map.width, uv_map.height = 150.0, 100.0
    image_texture_001.width, image_texture_001.height = 240.0, 100.0
    attribute_002.width, attribute_002.height = 140.0, 100.0
    math_011.width, math_011.height = 140.0, 100.0
    math_012.width, math_012.height = 140.0, 100.0
    combine_xyz_003.width, combine_xyz_003.height = 140.0, 100.0
    color_ramp.width, color_ramp.height = 240.0, 100.0
    invert_color.width, invert_color.height = 140.0, 100.0
    mapping_003.width, mapping_003.height = 140.0, 100.0
    vector_math_006.width, vector_math_006.height = 140.0, 100.0
    math_022.width, math_022.height = 140.0, 100.0
    reroute_010.width, reroute_010.height = 10.0, 100.0
    math.width, math.height = 140.0, 100.0
    vector_math.width, vector_math.height = 140.0, 100.0
    math_013.width, math_013.height = 140.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    reroute_011.width, reroute_011.height = 10.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    math_014.width, math_014.height = 140.0, 100.0
    frame_003.width, frame_003.height = 516.0, 287.0
    math_024.width, math_024.height = 140.0, 100.0
    math_015.width, math_015.height = 140.0, 100.0
    reroute_012.width, reroute_012.height = 10.0, 100.0
    reroute_014.width, reroute_014.height = 10.0, 100.0
    math_023.width, math_023.height = 140.0, 100.0
    math_028.width, math_028.height = 140.0, 100.0
    math_029.width, math_029.height = 140.0, 100.0
    math_030.width, math_030.height = 140.0, 100.0
    math_026.width, math_026.height = 140.0, 100.0
    math_027.width, math_027.height = 140.0, 100.0
    math_031.width, math_031.height = 140.0, 100.0
    math_032.width, math_032.height = 140.0, 100.0
    reroute_007.width, reroute_007.height = 10.0, 100.0
    map_range_001.width, map_range_001.height = 140.0, 100.0
    math_025.width, math_025.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    reroute_017.width, reroute_017.height = 10.0, 100.0
    vector_math_007.width, vector_math_007.height = 140.0, 100.0
    group_input_003.width, group_input_003.height = 140.0, 100.0
    group_input_004.width, group_input_004.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 140.0, 100.0
    group_input_006.width, group_input_006.height = 140.0, 100.0
    math_033.width, math_033.height = 140.0, 100.0
    group_input_007.width, group_input_007.height = 140.0, 100.0
    math_016.width, math_016.height = 140.0, 100.0
    math_017.width, math_017.height = 140.0, 100.0
    group.width, group.height = 140.0, 100.0
    group_input_008.width, group_input_008.height = 140.0, 100.0
    group_001.width, group_001.height = 140.0, 100.0
    vector_math_002_1.width, vector_math_002_1.height = 140.0, 100.0
    group_input_011.width, group_input_011.height = 140.0, 100.0
    group_input_012.width, group_input_012.height = 140.0, 100.0
    vector_math_008.width, vector_math_008.height = 140.0, 100.0
    math_034.width, math_034.height = 140.0, 100.0
    vector_math_009.width, vector_math_009.height = 140.0, 100.0
    vector_math_010.width, vector_math_010.height = 140.0, 100.0
    frame_004.width, frame_004.height = 1200.0, 781.0
    frame_005.width, frame_005.height = 680.0, 578.25
    frame_006.width, frame_006.height = 200.0, 290.0
    reroute_006.width, reroute_006.height = 10.0, 100.0
    reroute_008.width, reroute_008.height = 10.0, 100.0
    reroute_009.width, reroute_009.height = 10.0, 100.0
    reroute_016.width, reroute_016.height = 10.0, 100.0
    reroute_018.width, reroute_018.height = 10.0, 100.0
    reroute_021.width, reroute_021.height = 10.0, 100.0
    reroute_022.width, reroute_022.height = 10.0, 100.0
    reroute_019.width, reroute_019.height = 10.0, 100.0
    reroute_020.width, reroute_020.height = 10.0, 100.0
    reroute_023.width, reroute_023.height = 10.0, 100.0
    reroute_013.width, reroute_013.height = 10.0, 100.0
    reroute_015.width, reroute_015.height = 10.0, 100.0
    reroute_024.width, reroute_024.height = 10.0, 100.0
    reroute_025.width, reroute_025.height = 10.0, 100.0
    group_input_009.width, group_input_009.height = 140.0, 100.0
    reroute_026.width, reroute_026.height = 10.0, 100.0
    reroute_027.width, reroute_027.height = 10.0, 100.0
    reroute_028.width, reroute_028.height = 10.0, 100.0
    reroute_029.width, reroute_029.height = 10.0, 100.0
    reroute_030.width, reroute_030.height = 10.0, 100.0
    reroute_031.width, reroute_031.height = 10.0, 100.0
    reroute_032.width, reroute_032.height = 10.0, 100.0
    reroute_033.width, reroute_033.height = 10.0, 100.0
    frame_007.width, frame_007.height = 1540.0, 876.0
    frame_008.width, frame_008.height = 680.0, 322.0
    frame_009.width, frame_009.height = 480.0, 268.0
    frame_010.width, frame_010.height = 540.0, 294.25
    frame_011.width, frame_011.height = 660.0, 545.75
    frame_012.width, frame_012.height = 510.0, 438.0

    #initialize cgp_spritesheet_reader links
    #math_022.Value -> math_013.Value
    cgp_spritesheet_reader.links.new(math_022.outputs[0], math_013.inputs[0])
    #reroute_001.Output -> reroute_005.Input
    cgp_spritesheet_reader.links.new(reroute_001.outputs[0], reroute_005.inputs[0])
    #map_range_001.Result -> reroute_007.Input
    cgp_spritesheet_reader.links.new(map_range_001.outputs[0], reroute_007.inputs[0])
    #vector_math.Vector -> vector_math_006.Vector
    cgp_spritesheet_reader.links.new(vector_math.outputs[0], vector_math_006.inputs[1])
    #reroute_007.Output -> math_023.Value
    cgp_spritesheet_reader.links.new(reroute_007.outputs[0], math_023.inputs[0])
    #math_011.Value -> mapping_003.Scale
    cgp_spritesheet_reader.links.new(math_011.outputs[0], mapping_003.inputs[3])
    #math_028.Value -> math_030.Value
    cgp_spritesheet_reader.links.new(math_028.outputs[0], math_030.inputs[0])
    #math_014.Value -> combine_xyz_001.Y
    cgp_spritesheet_reader.links.new(math_014.outputs[0], combine_xyz_001.inputs[1])
    #reroute_002.Output -> math_005.Value
    cgp_spritesheet_reader.links.new(reroute_002.outputs[0], math_005.inputs[0])
    #reroute_012.Output -> math_022.Value
    cgp_spritesheet_reader.links.new(reroute_012.outputs[0], math_022.inputs[1])
    #math_027.Value -> math_022.Value
    cgp_spritesheet_reader.links.new(math_027.outputs[0], math_022.inputs[0])
    #math_024.Value -> math_015.Value
    cgp_spritesheet_reader.links.new(math_024.outputs[0], math_015.inputs[0])
    #reroute_010.Output -> math_011.Value
    cgp_spritesheet_reader.links.new(reroute_010.outputs[0], math_011.inputs[0])
    #mapping_003.Vector -> image_texture_001.Vector
    cgp_spritesheet_reader.links.new(mapping_003.outputs[0], image_texture_001.inputs[0])
    #separate_xyz.Y -> reroute_004.Input
    cgp_spritesheet_reader.links.new(separate_xyz.outputs[1], reroute_004.inputs[0])
    #math_008.Value -> math_012.Value
    cgp_spritesheet_reader.links.new(math_008.outputs[0], math_012.inputs[1])
    #math_007.Value -> math_008.Value
    cgp_spritesheet_reader.links.new(math_007.outputs[0], math_008.inputs[1])
    #math_010.Value -> math_005.Value
    cgp_spritesheet_reader.links.new(math_010.outputs[0], math_005.inputs[1])
    #math_004.Value -> math_008.Value
    cgp_spritesheet_reader.links.new(math_004.outputs[0], math_008.inputs[0])
    #reroute_008.Output -> math_015.Value
    cgp_spritesheet_reader.links.new(reroute_008.outputs[0], math_015.inputs[1])
    #mapping_001.Vector -> separate_xyz.Vector
    cgp_spritesheet_reader.links.new(mapping_001.outputs[0], separate_xyz.inputs[0])
    #reroute_005.Output -> math_003.Value
    cgp_spritesheet_reader.links.new(reroute_005.outputs[0], math_003.inputs[0])
    #reroute.Output -> math_002.Value
    cgp_spritesheet_reader.links.new(reroute.outputs[0], math_002.inputs[0])
    #reroute_012.Output -> reroute_014.Input
    cgp_spritesheet_reader.links.new(reroute_012.outputs[0], reroute_014.inputs[0])
    #math_009.Value -> math_002.Value
    cgp_spritesheet_reader.links.new(math_009.outputs[0], math_002.inputs[1])
    #value_004.Value -> math_010.Value
    cgp_spritesheet_reader.links.new(value_004.outputs[0], math_010.inputs[1])
    #reroute_032.Output -> color_ramp.Fac
    cgp_spritesheet_reader.links.new(reroute_032.outputs[0], color_ramp.inputs[0])
    #reroute_007.Output -> math_026.Value
    cgp_spritesheet_reader.links.new(reroute_007.outputs[0], math_026.inputs[0])
    #reroute_016.Output -> math_011.Value
    cgp_spritesheet_reader.links.new(reroute_016.outputs[0], math_011.inputs[1])
    #reroute_002.Output -> reroute_003.Input
    cgp_spritesheet_reader.links.new(reroute_002.outputs[0], reroute_003.inputs[0])
    #separate_xyz.X -> reroute_001.Input
    cgp_spritesheet_reader.links.new(separate_xyz.outputs[0], reroute_001.inputs[0])
    #reroute_029.Output -> invert_color.Color
    cgp_spritesheet_reader.links.new(reroute_029.outputs[0], invert_color.inputs[1])
    #math_032.Value -> math_027.Value
    cgp_spritesheet_reader.links.new(math_032.outputs[0], math_027.inputs[0])
    #math_033.Value -> math_024.Value
    cgp_spritesheet_reader.links.new(math_033.outputs[0], math_024.inputs[0])
    #math_006.Value -> math_007.Value
    cgp_spritesheet_reader.links.new(math_006.outputs[0], math_007.inputs[1])
    #math_014.Value -> combine_xyz_001.X
    cgp_spritesheet_reader.links.new(math_014.outputs[0], combine_xyz_001.inputs[0])
    #math_001.Value -> math_014.Value
    cgp_spritesheet_reader.links.new(math_001.outputs[0], math_014.inputs[0])
    #vector_math_007.Vector -> vector_math_006.Vector
    cgp_spritesheet_reader.links.new(vector_math_007.outputs[0], vector_math_006.inputs[0])
    #reroute_010.Output -> reroute_012.Input
    cgp_spritesheet_reader.links.new(reroute_010.outputs[0], reroute_012.inputs[0])
    #reroute_014.Output -> math_024.Value
    cgp_spritesheet_reader.links.new(reroute_014.outputs[0], math_024.inputs[1])
    #combine_xyz_003.Vector -> vector_math.Vector
    cgp_spritesheet_reader.links.new(combine_xyz_003.outputs[0], vector_math.inputs[0])
    #group_input_1.Rows -> math_025.Value
    cgp_spritesheet_reader.links.new(group_input_1.outputs[2], math_025.inputs[1])
    #image_texture_001.Alpha -> math_012.Value
    cgp_spritesheet_reader.links.new(image_texture_001.outputs[1], math_012.inputs[0])
    #vector_math_006.Vector -> mapping_003.Vector
    cgp_spritesheet_reader.links.new(vector_math_006.outputs[0], mapping_003.inputs[0])
    #math_003.Value -> math_004.Value
    cgp_spritesheet_reader.links.new(math_003.outputs[0], math_004.inputs[1])
    #value_003.Value -> math_009.Value
    cgp_spritesheet_reader.links.new(value_003.outputs[0], math_009.inputs[1])
    #math_023.Value -> math_028.Value
    cgp_spritesheet_reader.links.new(math_023.outputs[0], math_028.inputs[0])
    #math_002.Value -> math_004.Value
    cgp_spritesheet_reader.links.new(math_002.outputs[0], math_004.inputs[0])
    #reroute_005.Output -> reroute.Input
    cgp_spritesheet_reader.links.new(reroute_005.outputs[0], reroute.inputs[0])
    #reroute_003.Output -> math_006.Value
    cgp_spritesheet_reader.links.new(reroute_003.outputs[0], math_006.inputs[0])
    #math_025.Value -> map_range_001.To Max
    cgp_spritesheet_reader.links.new(math_025.outputs[0], map_range_001.inputs[4])
    #math_025.Value -> map_range_001.From Max
    cgp_spritesheet_reader.links.new(math_025.outputs[0], map_range_001.inputs[2])
    #reroute_006.Output -> math_013.Value
    cgp_spritesheet_reader.links.new(reroute_006.outputs[0], math_013.inputs[1])
    #math_031.Value -> math_027.Value
    cgp_spritesheet_reader.links.new(math_031.outputs[0], math_027.inputs[1])
    #reroute_004.Output -> reroute_002.Input
    cgp_spritesheet_reader.links.new(reroute_004.outputs[0], reroute_002.inputs[0])
    #math_005.Value -> math_007.Value
    cgp_spritesheet_reader.links.new(math_005.outputs[0], math_007.inputs[0])
    #math_026.Value -> math_032.Value
    cgp_spritesheet_reader.links.new(math_026.outputs[0], math_032.inputs[0])
    #reroute_024.Output -> vector_math.Vector
    cgp_spritesheet_reader.links.new(reroute_024.outputs[0], vector_math.inputs[1])
    #math.Value -> reroute_010.Input
    cgp_spritesheet_reader.links.new(math.outputs[0], reroute_010.inputs[0])
    #math_029.Value -> math_030.Value
    cgp_spritesheet_reader.links.new(math_029.outputs[0], math_030.inputs[1])
    #reroute_033.Output -> group_output_1.Sprite
    cgp_spritesheet_reader.links.new(reroute_033.outputs[0], group_output_1.inputs[0])
    #math_012.Value -> group_output_1.Mix
    cgp_spritesheet_reader.links.new(math_012.outputs[0], group_output_1.inputs[1])
    #reroute_031.Output -> group_output_1.Specular
    cgp_spritesheet_reader.links.new(reroute_031.outputs[0], group_output_1.inputs[2])
    #invert_color.Color -> group_output_1.Roughness
    cgp_spritesheet_reader.links.new(invert_color.outputs[0], group_output_1.inputs[3])
    #group_input_1.Sprite Index -> map_range_001.Value
    cgp_spritesheet_reader.links.new(group_input_1.outputs[0], map_range_001.inputs[0])
    #group_input_001.Image Scale -> math.Value
    cgp_spritesheet_reader.links.new(group_input_001.outputs[3], math.inputs[1])
    #attribute_002.Vector -> vector_math_007.Vector
    cgp_spritesheet_reader.links.new(attribute_002.outputs[1], vector_math_007.inputs[0])
    #group.Vector -> vector_math_007.Vector
    cgp_spritesheet_reader.links.new(group.outputs[0], vector_math_007.inputs[1])
    #math_013.Value -> combine_xyz_003.X
    cgp_spritesheet_reader.links.new(math_013.outputs[0], combine_xyz_003.inputs[0])
    #group_input_1.Columns -> math_025.Value
    cgp_spritesheet_reader.links.new(group_input_1.outputs[1], math_025.inputs[0])
    #group_input_004.Columns -> math_032.Value
    cgp_spritesheet_reader.links.new(group_input_004.outputs[1], math_032.inputs[1])
    #group_input_005.Columns -> math_031.Value
    cgp_spritesheet_reader.links.new(group_input_005.outputs[1], math_031.inputs[1])
    #group_input_006.Rows -> math_023.Value
    cgp_spritesheet_reader.links.new(group_input_006.outputs[2], math_023.inputs[1])
    #group_input_006.Rows -> math_029.Value
    cgp_spritesheet_reader.links.new(group_input_006.outputs[2], math_029.inputs[1])
    #math_030.Value -> math_033.Value
    cgp_spritesheet_reader.links.new(math_030.outputs[0], math_033.inputs[0])
    #math_017.Value -> math_016.Value
    cgp_spritesheet_reader.links.new(math_017.outputs[0], math_016.inputs[0])
    #group_input_007.Rows -> math_017.Value
    cgp_spritesheet_reader.links.new(group_input_007.outputs[2], math_017.inputs[0])
    #math_016.Value -> math_033.Value
    cgp_spritesheet_reader.links.new(math_016.outputs[0], math_033.inputs[1])
    #group_input_003.Rows -> group.X
    cgp_spritesheet_reader.links.new(group_input_003.outputs[2], group.inputs[0])
    #group_input_003.Columns -> group.Y
    cgp_spritesheet_reader.links.new(group_input_003.outputs[1], group.inputs[1])
    #group_input_008.Rows -> group_001.X
    cgp_spritesheet_reader.links.new(group_input_008.outputs[2], group_001.inputs[0])
    #group_input_008.Columns -> group_001.Y
    cgp_spritesheet_reader.links.new(group_input_008.outputs[1], group_001.inputs[1])
    #reroute_022.Output -> vector_math_002_1.Vector
    cgp_spritesheet_reader.links.new(reroute_022.outputs[0], vector_math_002_1.inputs[0])
    #reroute_020.Output -> vector_math_002_1.Vector
    cgp_spritesheet_reader.links.new(reroute_020.outputs[0], vector_math_002_1.inputs[1])
    #reroute_013.Output -> combine_xyz_003.Y
    cgp_spritesheet_reader.links.new(reroute_013.outputs[0], combine_xyz_003.inputs[1])
    #vector_math_010.Vector -> vector_math_008.Vector
    cgp_spritesheet_reader.links.new(vector_math_010.outputs[0], vector_math_008.inputs[0])
    #reroute_018.Output -> math_034.Value
    cgp_spritesheet_reader.links.new(reroute_018.outputs[0], math_034.inputs[1])
    #vector_math_008.Vector -> mapping_001.Vector
    cgp_spritesheet_reader.links.new(vector_math_008.outputs[0], mapping_001.inputs[0])
    #vector_math_009.Vector -> vector_math_001.Vector
    cgp_spritesheet_reader.links.new(vector_math_009.outputs[0], vector_math_001.inputs[1])
    #math_034.Value -> mapping_001.Scale
    cgp_spritesheet_reader.links.new(math_034.outputs[0], mapping_001.inputs[3])
    #group_input_012.Main Offset -> vector_math_008.Vector
    cgp_spritesheet_reader.links.new(group_input_012.outputs[5], vector_math_008.inputs[1])
    #uv_map.UV -> vector_math_010.Vector
    cgp_spritesheet_reader.links.new(uv_map.outputs[0], vector_math_010.inputs[0])
    #reroute_026.Output -> vector_math_010.Vector
    cgp_spritesheet_reader.links.new(reroute_026.outputs[0], vector_math_010.inputs[1])
    #vector_math_002_1.Vector -> vector_math_001.Vector
    cgp_spritesheet_reader.links.new(vector_math_002_1.outputs[0], vector_math_001.inputs[0])
    #reroute_011.Output -> reroute_006.Input
    cgp_spritesheet_reader.links.new(reroute_011.outputs[0], reroute_006.inputs[0])
    #reroute_017.Output -> reroute_008.Input
    cgp_spritesheet_reader.links.new(reroute_017.outputs[0], reroute_008.inputs[0])
    #reroute_011.Output -> reroute_009.Input
    cgp_spritesheet_reader.links.new(reroute_011.outputs[0], reroute_009.inputs[0])
    #reroute_009.Output -> reroute_016.Input
    cgp_spritesheet_reader.links.new(reroute_009.outputs[0], reroute_016.inputs[0])
    #reroute_009.Output -> reroute_018.Input
    cgp_spritesheet_reader.links.new(reroute_009.outputs[0], reroute_018.inputs[0])
    #combine_xyz_001.Vector -> reroute_021.Input
    cgp_spritesheet_reader.links.new(combine_xyz_001.outputs[0], reroute_021.inputs[0])
    #reroute_021.Output -> reroute_022.Input
    cgp_spritesheet_reader.links.new(reroute_021.outputs[0], reroute_022.inputs[0])
    #group_input_011.Main Offset -> vector_math_009.Vector
    cgp_spritesheet_reader.links.new(group_input_011.outputs[5], vector_math_009.inputs[1])
    #reroute_023.Output -> vector_math_009.Vector
    cgp_spritesheet_reader.links.new(reroute_023.outputs[0], vector_math_009.inputs[0])
    #group_001.Vector -> reroute_019.Input
    cgp_spritesheet_reader.links.new(group_001.outputs[0], reroute_019.inputs[0])
    #reroute_019.Output -> reroute_020.Input
    cgp_spritesheet_reader.links.new(reroute_019.outputs[0], reroute_020.inputs[0])
    #reroute_019.Output -> reroute_023.Input
    cgp_spritesheet_reader.links.new(reroute_019.outputs[0], reroute_023.inputs[0])
    #reroute_015.Output -> reroute_013.Input
    cgp_spritesheet_reader.links.new(reroute_015.outputs[0], reroute_013.inputs[0])
    #math_015.Value -> reroute_015.Input
    cgp_spritesheet_reader.links.new(math_015.outputs[0], reroute_015.inputs[0])
    #reroute_025.Output -> reroute_024.Input
    cgp_spritesheet_reader.links.new(reroute_025.outputs[0], reroute_024.inputs[0])
    #vector_math_001.Vector -> reroute_025.Input
    cgp_spritesheet_reader.links.new(vector_math_001.outputs[0], reroute_025.inputs[0])
    #group_input_009.Main Scale -> math_001.Value
    cgp_spritesheet_reader.links.new(group_input_009.outputs[4], math_001.inputs[1])
    #reroute_027.Output -> reroute_026.Input
    cgp_spritesheet_reader.links.new(reroute_027.outputs[0], reroute_026.inputs[0])
    #reroute_021.Output -> reroute_027.Input
    cgp_spritesheet_reader.links.new(reroute_021.outputs[0], reroute_027.inputs[0])
    #color_ramp.Color -> reroute_028.Input
    cgp_spritesheet_reader.links.new(color_ramp.outputs[0], reroute_028.inputs[0])
    #reroute_028.Output -> reroute_029.Input
    cgp_spritesheet_reader.links.new(reroute_028.outputs[0], reroute_029.inputs[0])
    #reroute_028.Output -> reroute_030.Input
    cgp_spritesheet_reader.links.new(reroute_028.outputs[0], reroute_030.inputs[0])
    #reroute_030.Output -> reroute_031.Input
    cgp_spritesheet_reader.links.new(reroute_030.outputs[0], reroute_031.inputs[0])
    #image_texture_001.Color -> reroute_032.Input
    cgp_spritesheet_reader.links.new(image_texture_001.outputs[0], reroute_032.inputs[0])
    #reroute_032.Output -> reroute_033.Input
    cgp_spritesheet_reader.links.new(reroute_032.outputs[0], reroute_033.inputs[0])
    #group_input_002.Main Scale -> reroute_011.Input
    cgp_spritesheet_reader.links.new(group_input_002.outputs[4], reroute_011.inputs[0])
    #reroute_011.Output -> reroute_017.Input
    cgp_spritesheet_reader.links.new(reroute_011.outputs[0], reroute_017.inputs[0])
    return cgp_spritesheet_reader

# cgp_spritesheet_reader = cgp_spritesheet_reader_node_group()

#initialize Mouth-v2 node group
def mouth_v2_node_group():

    mouth_v2 = mat.node_tree
    #start with a clean node tree
    for node in mouth_v2.nodes:
        mouth_v2.nodes.remove(node)
    mouth_v2.color_tag = 'NONE'
    mouth_v2.description = ""
    mouth_v2.default_group_node_width = 140
    

    #mouth_v2 interface

    #initialize mouth_v2 nodes
    #node Principled BSDF
    principled_bsdf = mouth_v2.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    #Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    #IOR
    principled_bsdf.inputs[3].default_value = 1.5
    #Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    #Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    #Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    #Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    #Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    #Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    #Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    #Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    #Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    #Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    #Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    #Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    #Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    #Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    #Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    #Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    #Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    #Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    #node Material Output
    material_output = mouth_v2.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    #Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Thickness
    material_output.inputs[3].default_value = 0.0

    #node Principled BSDF.001
    principled_bsdf_001 = mouth_v2.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf_001.name = "Principled BSDF.001"
    principled_bsdf_001.distribution = 'MULTI_GGX'
    principled_bsdf_001.subsurface_method = 'RANDOM_WALK'
    #Base Color
    principled_bsdf_001.inputs[0].default_value = (0.800133466720581, 0.36626043915748596, 0.07181036472320557, 1.0)
    #Metallic
    principled_bsdf_001.inputs[1].default_value = 0.0
    #Roughness
    principled_bsdf_001.inputs[2].default_value = 0.7954545021057129
    #IOR
    principled_bsdf_001.inputs[3].default_value = 1.5
    #Alpha
    principled_bsdf_001.inputs[4].default_value = 1.0
    #Normal
    principled_bsdf_001.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Diffuse Roughness
    principled_bsdf_001.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf_001.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf_001.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    #Subsurface Scale
    principled_bsdf_001.inputs[10].default_value = 0.05000000074505806
    #Subsurface Anisotropy
    principled_bsdf_001.inputs[12].default_value = 0.0
    #Specular IOR Level
    principled_bsdf_001.inputs[13].default_value = 0.5
    #Specular Tint
    principled_bsdf_001.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    #Anisotropic
    principled_bsdf_001.inputs[15].default_value = 0.0
    #Anisotropic Rotation
    principled_bsdf_001.inputs[16].default_value = 0.0
    #Tangent
    principled_bsdf_001.inputs[17].default_value = (0.0, 0.0, 0.0)
    #Transmission Weight
    principled_bsdf_001.inputs[18].default_value = 0.0
    #Coat Weight
    principled_bsdf_001.inputs[19].default_value = 0.0
    #Coat Roughness
    principled_bsdf_001.inputs[20].default_value = 0.029999999329447746
    #Coat IOR
    principled_bsdf_001.inputs[21].default_value = 1.5
    #Coat Tint
    principled_bsdf_001.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    #Coat Normal
    principled_bsdf_001.inputs[23].default_value = (0.0, 0.0, 0.0)
    #Sheen Weight
    principled_bsdf_001.inputs[24].default_value = 0.0
    #Sheen Roughness
    principled_bsdf_001.inputs[25].default_value = 0.5
    #Sheen Tint
    principled_bsdf_001.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Color
    principled_bsdf_001.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Strength
    principled_bsdf_001.inputs[28].default_value = 0.0
    #Thin Film Thickness
    principled_bsdf_001.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf_001.inputs[30].default_value = 1.3300000429153442

    #node Mix Shader
    mix_shader = mouth_v2.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    #node Group
    group_1 = mouth_v2.nodes.new("ShaderNodeGroup")
    group_1.name = "Group"
    group_1.node_tree = cgp_spritesheet_reader
    #Socket_5
    group_1.inputs[1].default_value = 9.0
    #Socket_6
    group_1.inputs[2].default_value = 1.0
    #Socket_7
    group_1.inputs[3].default_value = 0.9900000095367432
    #Socket_8
    group_1.inputs[4].default_value = 1.0
    #Socket_12
    group_1.inputs[5].default_value = (0.03999999910593033, 0.0, 0.0)

    #node Value
    value = mouth_v2.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0

    #Set locations
    principled_bsdf.location = (-366.04656982421875, -1293.2890625)
    material_output.location = (406.7846984863281, -1098.980712890625)
    principled_bsdf_001.location = (-397.0885314941406, -820.210693359375)
    mix_shader.location = (75.23101043701172, -1138.629638671875)
    group_1.location = (-941.168701171875, -1197.708984375)
    value.location = (-1420.0, -1320.0)

    #Set dimensions
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    material_output.width, material_output.height = 140.0, 100.0
    principled_bsdf_001.width, principled_bsdf_001.height = 240.0, 100.0
    mix_shader.width, mix_shader.height = 140.0, 100.0
    group_1.width, group_1.height = 210.59588623046875, 100.0
    value.width, value.height = 140.0, 100.0

    #initialize mouth_v2 links
    #principled_bsdf_001.BSDF -> mix_shader.Shader
    mouth_v2.links.new(principled_bsdf_001.outputs[0], mix_shader.inputs[1])
    #principled_bsdf.BSDF -> mix_shader.Shader
    mouth_v2.links.new(principled_bsdf.outputs[0], mix_shader.inputs[2])
    #group_1.Sprite -> principled_bsdf.Base Color
    mouth_v2.links.new(group_1.outputs[0], principled_bsdf.inputs[0])
    #group_1.Mix -> mix_shader.Fac
    mouth_v2.links.new(group_1.outputs[1], mix_shader.inputs[0])
    #group_1.Roughness -> principled_bsdf.Roughness
    mouth_v2.links.new(group_1.outputs[3], principled_bsdf.inputs[2])
    #group_1.Specular -> principled_bsdf.Specular IOR Level
    mouth_v2.links.new(group_1.outputs[2], principled_bsdf.inputs[13])
    #value.Value -> group_1.Sprite Index
    mouth_v2.links.new(value.outputs[0], group_1.inputs[0])
    #mix_shader.Shader -> material_output.Surface
    mouth_v2.links.new(mix_shader.outputs[0], material_output.inputs[0])
    return mouth_v2

# mouth_v2 = mouth_v2_node_group()

