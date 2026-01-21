import bpy

from .Operators.LIPSYNC2D_OT_refresh_pose_assets import LIPSYNC2D_OT_refresh_pose_assets


from .Core.LIPSYNC2D_EspeakInspector import LIPSYNC2D_EspeakInspector
from .Core.LIPSYNC2D_VoskHelper import LIPSYNC2D_VoskHelper
from .Operators.LIPSYNC2D_OT_AnalyzeAudio import LIPSYNC2D_OT_AnalyzeAudio
from .Operators.LIPSYNC2D_OT_DownloadModelsList import LIPSYNC2D_OT_DownloadModelsList
from .Operators.LIPSYNC2D_OT_RemoveAnimations import LIPSYNC2D_OT_RemoveAnimations
from .Operators.LIPSYNC2D_OT_RemoveLipSync import LIPSYNC2D_OT_RemoveLipSync
from .Operators.LIPSYNC2D_OT_RemoveNodeGroups import LIPSYNC2D_OT_RemoveNodeGroups
from .Operators.LIPSYNC2D_OT_SetCustomProperties import LIPSYNC2D_OT_SetCustomProperties
from .Operators.LIPSYNC2D_OT_SetMouthArea import LIPSYNC2D_OT_SetMouthArea
from .Panels.LIPSYNC2D_PT_Panel import LIPSYNC2D_PT_Panel
from .Panels.LIPSYNC2D_PT_Settings import LIPSYNC2D_PT_Settings
from .Panels.LIPSYNC2D_PT_Edit import LIPSYNC2D_PT_Edit
from .Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from .Properties.LIPSYNC2D_PG_CustomProperties import LIPSYNC2D_PG_CustomProperties


def register():
    if not LIPSYNC2D_EspeakInspector.is_espeak_already_extracted():
        LIPSYNC2D_EspeakInspector.unzip_binaries()
    LIPSYNC2D_EspeakInspector.set_espeak_backend()
    if bpy.app.online_access:
        LIPSYNC2D_VoskHelper.cache_online_langs_list()
    bpy.utils.register_class(LIPSYNC2D_AP_Preferences)
    bpy.utils.register_class(LIPSYNC2D_PG_CustomProperties)
    bpy.utils.register_class(LIPSYNC2D_PT_Settings)
    bpy.utils.register_class(LIPSYNC2D_PT_Panel)
    bpy.utils.register_class(LIPSYNC2D_OT_SetMouthArea)
    bpy.utils.register_class(LIPSYNC2D_OT_SetCustomProperties)
    bpy.utils.register_class(LIPSYNC2D_OT_AnalyzeAudio)
    bpy.utils.register_class(LIPSYNC2D_OT_DownloadModelsList)
    bpy.utils.register_class(LIPSYNC2D_OT_RemoveLipSync)
    bpy.utils.register_class(LIPSYNC2D_OT_RemoveNodeGroups)
    bpy.utils.register_class(LIPSYNC2D_PT_Edit)
    bpy.utils.register_class(LIPSYNC2D_OT_RemoveAnimations)
    bpy.utils.register_class(LIPSYNC2D_OT_refresh_pose_assets)
    bpy.types.Object.lipsync2d_props = bpy.props.PointerProperty(
        type=LIPSYNC2D_PG_CustomProperties,
        override={'LIBRARY_OVERRIDABLE'}
    )  # type: ignore


def unregister():
    bpy.utils.unregister_class(LIPSYNC2D_PG_CustomProperties)
    bpy.utils.unregister_class(LIPSYNC2D_PT_Panel)
    bpy.utils.unregister_class(LIPSYNC2D_OT_SetMouthArea)
    bpy.utils.unregister_class(LIPSYNC2D_OT_SetCustomProperties)
    bpy.utils.unregister_class(LIPSYNC2D_OT_AnalyzeAudio)
    bpy.utils.unregister_class(LIPSYNC2D_AP_Preferences)
    bpy.utils.unregister_class(LIPSYNC2D_PT_Settings)
    bpy.utils.unregister_class(LIPSYNC2D_OT_DownloadModelsList)
    bpy.utils.unregister_class(LIPSYNC2D_OT_RemoveLipSync)
    bpy.utils.unregister_class(LIPSYNC2D_OT_RemoveNodeGroups)
    bpy.utils.unregister_class(LIPSYNC2D_PT_Edit)
    bpy.utils.unregister_class(LIPSYNC2D_OT_RemoveAnimations)
    bpy.utils.unregister_class(LIPSYNC2D_OT_refresh_pose_assets)
    del bpy.types.Object.lipsync2d_props  # type: ignore


if __name__ == "__main__":
    register()
