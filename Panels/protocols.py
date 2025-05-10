from typing import Protocol

from ..lipsync_types import BpyContext, BpyUILayout


class LIPSYNC2D_AnimatorPanel(Protocol):
    def draw_animation_section(self, context: BpyContext, layout: BpyUILayout):
        pass

    def draw_visemes_section(self, context: BpyContext, layout: BpyUILayout):
        pass

    def draw_edit_section(self, context: BpyContext, layout: BpyUILayout):
        pass

    def draw_baking_section(self, context: BpyContext, layout: BpyUILayout):
        pass

    def draw_animator_section(self, context: BpyContext, layout: BpyUILayout):
        pass

    def draw_bake_section(self, context: BpyContext, layout: BpyUILayout):
        pass
