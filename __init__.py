import bpy

from .LIPSYNC2D_PG_CustomProperties import LIPSYNC2D_PG_CustomProperties
from .LIPSYNC2D_OT_UpdateMaterial import LIPSYNC2D_OT_UpdateMaterial
from .LIPSYNC2D_OT_SetMouthArea import LIPSYNC2D_OT_SetMouthArea
from .LIPSYNC2D_PT_Panel import LIPSYNC2D_PT_Panel


def register():
    bpy.utils.register_class(LIPSYNC2D_PG_CustomProperties)
    bpy.utils.register_class(LIPSYNC2D_PT_Panel)
    bpy.utils.register_class(LIPSYNC2D_OT_SetMouthArea)
    bpy.utils.register_class(LIPSYNC2D_OT_UpdateMaterial)
    bpy.types.Object.lipsync2d_props = bpy.props.PointerProperty(type=LIPSYNC2D_PG_CustomProperties) # type: ignore
    bpy.types.Scene.lipsync2d_props = bpy.props.PointerProperty(type=LIPSYNC2D_PG_CustomProperties) # type: ignore

def unregister():
    bpy.utils.unregister_class(LIPSYNC2D_PG_CustomProperties)
    bpy.utils.unregister_class(LIPSYNC2D_PT_Panel)
    bpy.utils.unregister_class(LIPSYNC2D_OT_SetMouthArea)
    bpy.utils.unregister_class(LIPSYNC2D_OT_UpdateMaterial)
    del bpy.types.Scene.lipsync2d_props # type: ignore
    del bpy.types.Object.lipsync2d_props # type: ignore


if __name__ == "__main__":
    register()
