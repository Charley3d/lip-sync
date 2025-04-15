import bpy

from .Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from .Operators.LIPSYNC2D_OT_AnalyzeAudio import LIPSYNC2D_OT_AnalyzeAudio
from .Properties.LIPSYNC2D_PG_CustomProperties import LIPSYNC2D_PG_CustomProperties
from .Operators.LIPSYNC2D_OT_UpdateMaterial import LIPSYNC2D_OT_UpdateMaterial
from .Operators.LIPSYNC2D_OT_SetMouthArea import LIPSYNC2D_OT_SetMouthArea
from .Panels.LIPSYNC2D_PT_Panel import LIPSYNC2D_PT_Panel
from .Operators.LIPSYNC2D_OT_FindEspeak import LIPSYNC2D_OT_FindEspeak
from .Panels.LIPSYNC2D_PT_Settings import LIPSYNC2D_PT_Settings


def register():
    bpy.utils.register_class(LIPSYNC2D_AP_Preferences)
    bpy.utils.register_class(LIPSYNC2D_PG_CustomProperties)
    bpy.utils.register_class(LIPSYNC2D_PT_Panel)
    bpy.utils.register_class(LIPSYNC2D_OT_SetMouthArea)
    bpy.utils.register_class(LIPSYNC2D_OT_UpdateMaterial)
    bpy.utils.register_class(LIPSYNC2D_OT_AnalyzeAudio)
    bpy.utils.register_class(LIPSYNC2D_OT_FindEspeak)
    bpy.utils.register_class(LIPSYNC2D_PT_Settings)
    bpy.types.Object.lipsync2d_props = bpy.props.PointerProperty(type=LIPSYNC2D_PG_CustomProperties) # type: ignore

def unregister():
    bpy.utils.unregister_class(LIPSYNC2D_PG_CustomProperties)
    bpy.utils.unregister_class(LIPSYNC2D_PT_Panel)
    bpy.utils.unregister_class(LIPSYNC2D_OT_SetMouthArea)
    bpy.utils.unregister_class(LIPSYNC2D_OT_UpdateMaterial)
    bpy.utils.unregister_class(LIPSYNC2D_OT_AnalyzeAudio)
    bpy.utils.unregister_class(LIPSYNC2D_OT_FindEspeak)
    bpy.utils.unregister_class(LIPSYNC2D_AP_Preferences)
    bpy.utils.unregister_class(LIPSYNC2D_PT_Settings)
    del bpy.types.Object.lipsync2d_props # type: ignore


if __name__ == "__main__":
    register()
