# types.py
from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from bpy.types import (
        Action,
        UILayout,
        ActionKeyframeStrip,
        Context,
        RenderSettings,
        Object,
        PropertyGroup,
        Operator,
        ShapeKey,
        ActionSlot,
        Mesh,
        ActionChannelbag,
        Armature,
    )

# Export commonly used types
BpyContext: TypeAlias = "Context"
BpyObject: TypeAlias = "Object"
BpyRenderSettings: TypeAlias = "RenderSettings"
BpyPropertyGroup: TypeAlias = "PropertyGroup"
BpyOperator: TypeAlias = "Operator"
BpyShapeKey: TypeAlias = "ShapeKey"
BpyActionSlot: TypeAlias = "ActionSlot"
BpyMesh: TypeAlias = "Mesh"
BpyAction: TypeAlias = "Action"
BpyActionKeyframeStrip: TypeAlias = "ActionKeyframeStrip"
BpyUILayout: TypeAlias = "UILayout"
BpyActionChannelbag: TypeAlias = "ActionChannelbag"
BpyArmature: TypeAlias = "Armature"
