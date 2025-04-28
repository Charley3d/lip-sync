from ...lipsync_types import BpyRenderSettings

class LIPSYNC2D_TimeConversion:

    def __init__(self, render_settings: BpyRenderSettings):
        self.based_fps = render_settings.fps / render_settings.fps_base

    def time_to_frame(self, time: float) -> int:
        return round(time * self.based_fps)

    def frame_to_time(self, frame: int) -> int:
        return round(frame / self.based_fps)