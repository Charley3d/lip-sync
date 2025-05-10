import bpy

class LIPSYNC2D_Timeline:
  @staticmethod
  def get_fps_range() -> int:
      if bpy.context.scene is None:
          return -1

      return bpy.context.scene.frame_end - bpy.context.scene.frame_start

  @staticmethod
  def get_frame_start():
      if bpy.context.scene is None:
          return -1

      return bpy.context.scene.frame_start
  
  @staticmethod
  def get_frame_end():
      if bpy.context.scene is None:
          return -1

      return bpy.context.scene.frame_end