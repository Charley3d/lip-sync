from typing import Literal
import bpy
from bpy.types import Context

from ..Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_VoskHelper

class LIPSYNC2D_OT_DownloadModelsList(bpy.types.Operator):
    bl_idname = "lipsync2d.downloadlist"
    bl_label="Refresh Models List"
    bl_options={'UNDO', 'REGISTER'}
    bl_description="Reuires Online Access. Fetch a new models list. Use this if models list is empty / incomplete."

    def execute(self, context: Context) -> set[Literal['RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH', 'INTERFACE']]:
        try:
            LIPSYNC2D_VoskHelper.cache_online_langs_list()
        except:
            self.report({'ERROR'}, "Unable to fetch a new models list")

        self.report({'INFO'}, "New list has been downloaded!")
        return {'FINISHED'}