import json
import bpy
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..Core.phoneme_to_viseme import viseme_items_mpeg4_v2

class LIPSYNC2D_OT_ExportMappings(bpy.types.Operator, ExportHelper):
    """Export Viseme Mappings to JSON"""
    bl_idname = "lipsync2d.export_mappings"
    bl_label = "Export Mappings"
    filename_ext = ".json"

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore

    def execute(self, context):
        obj = context.active_object
        if not obj or not hasattr(obj, "lipsync2d_props"):
            self.report({'ERROR'}, "No valid object selected")
            return {'CANCELLED'}

        props = obj.lipsync2d_props
        anim_type = props.lip_sync_2d_lips_type
        
        data = {
            "animation_type": anim_type,
            "mappings": []
        }

        visemes = viseme_items_mpeg4_v2(None, None)
        
        for v in visemes:
            viseme_id = v[0] # "sil", "PP", etc.
            mapping_value = None

            if anim_type == "SPRITESHEET":
                prop_name = f"lip_sync_2d_viseme_{viseme_id}"
                mapping_value = getattr(props, prop_name)
            elif anim_type == "SHAPEKEYS":
                prop_name = f"lip_sync_2d_viseme_shape_keys_{viseme_id}"
                mapping_value = getattr(props, prop_name)
            elif anim_type == "POSEASSETS":
                prop_name = f"lip_sync_2d_viseme_pose_{viseme_id}"
                action = getattr(props, prop_name)
                if action:
                    mapping_value = action.name
            
            if mapping_value is not None:
                data["mappings"].append({
                    "viseme": viseme_id,
                    "mapping": mapping_value
                })

        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self.report({'INFO'}, f"Mappings exported to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export mappings: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}


class LIPSYNC2D_OT_ImportMappings(bpy.types.Operator, ImportHelper):
    """Import Viseme Mappings from JSON"""
    bl_idname = "lipsync2d.import_mappings"
    bl_label = "Import Mappings"
    filename_ext = ".json"

    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    ) # type: ignore

    create_missing: bpy.props.BoolProperty(
        name="Create Missing",
        description="Create missing Shape Keys or Actions if they don't exist",
        default=False,
    ) # type: ignore

    def execute(self, context):
        obj = context.active_object
        if not obj or not hasattr(obj, "lipsync2d_props"):
            self.report({'ERROR'}, "No valid object selected")
            return {'CANCELLED'}

        props = obj.lipsync2d_props
        current_anim_type = props.lip_sync_2d_lips_type

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to read file: {str(e)}")
            return {'CANCELLED'}

        file_anim_type = data.get("animation_type")
        if file_anim_type != current_anim_type:
            self.report({'ERROR'}, f"Animation type mismatch. File: {file_anim_type}, Object: {current_anim_type}")
            return {'CANCELLED'}

        mappings = data.get("mappings", [])
        
        # Helper to check if property exists on the object (for version compatibility)
        def prop_exists(prop_name):
            return hasattr(props, prop_name)

        loaded_count = 0
        skipped_count = 0
        created_count = 0

        for item in mappings:
            viseme_id = item.get("viseme")
            mapping_value = item.get("mapping")

            if not viseme_id:
                continue

            if current_anim_type == "SPRITESHEET":
                prop_name = f"lip_sync_2d_viseme_{viseme_id}"
                if prop_exists(prop_name):
                    setattr(props, prop_name, int(mapping_value))
                    loaded_count += 1
                else:
                    self.report({'INFO'}, f"Skipped '{viseme_id}': Property '{prop_name}' not found.")
                    skipped_count += 1

            elif current_anim_type == "SHAPEKEYS":
                prop_name = f"lip_sync_2d_viseme_shape_keys_{viseme_id}"
                if prop_exists(prop_name):
                    # Check if shape key exists on the mesh or if it is "NONE"
                    if mapping_value == "NONE":
                        setattr(props, prop_name, mapping_value)
                        loaded_count += 1
                    elif obj.data and obj.data.shape_keys and mapping_value in obj.data.shape_keys.key_blocks:
                        setattr(props, prop_name, mapping_value)
                        loaded_count += 1
                    elif self.create_missing:
                        # Ensure Basis key exists first
                        if not obj.data.shape_keys:
                            obj.shape_key_add(name="Basis")
                        
                        obj.shape_key_add(name=mapping_value)
                        # We need to refresh the EnumProperty somehow or just set the string if it allows (usually it stores string index)
                        # For now, just setting the string property should work if the Enum updates dynamically or if it's a StringProperty storage.
                        # However, for EnumProperty backed by a function, setting the string *should* work if the item is now in the list.
                        # Since we just added it to key_blocks, it should be valid.
                        setattr(props, prop_name, mapping_value)
                        created_count += 1
                        loaded_count += 1
                    else:
                        self.report({'INFO'}, f"Skipped '{viseme_id}': Shape Key '{mapping_value}' not found on object.")
                        skipped_count += 1
                else:
                    self.report({'INFO'}, f"Skipped '{viseme_id}': Property '{prop_name}' not found.")
                    skipped_count += 1

            elif current_anim_type == "POSEASSETS":
                prop_name = f"lip_sync_2d_viseme_pose_{viseme_id}"
                if prop_exists(prop_name):
                    if mapping_value == "None" or not mapping_value:
                        setattr(props, prop_name, None)
                        loaded_count += 1
                    else:
                        # Check if Action exists in bpy.data.actions
                        action = bpy.data.actions.get(mapping_value)
                        if action:
                            setattr(props, prop_name, action)
                            loaded_count += 1
                        elif self.create_missing:
                            new_action = bpy.data.actions.new(name=mapping_value)
                            # Mark as asset so it appears in the filtered dropdowns
                            new_action.asset_mark()
                            setattr(props, prop_name, new_action)
                            created_count += 1
                            loaded_count += 1
                        else:
                            self.report({'INFO'}, f"Skipped '{viseme_id}': Action '{mapping_value}' not found in blend file.")
                            skipped_count += 1
                else:
                    self.report({'INFO'}, f"Skipped '{viseme_id}': Property '{prop_name}' not found.")
                    skipped_count += 1

        self.report({'INFO'}, f"Imported {loaded_count} mappings. Created {created_count} missing items. Skipped {skipped_count}.")
        return {'FINISHED'}
