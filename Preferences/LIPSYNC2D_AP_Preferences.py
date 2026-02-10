import os
from pathlib import Path
from re import match
from typing import Literal

import bpy
from vosk import MODEL_DIRS

from ..lipsync_types import BpyContext

from ..Core.LIPSYNC2D_VoskHelper import LIPSYNC2D_VoskHelper
from ..LIPSYNC2D_Utils import get_package_name


class LIPSYNC2D_AP_Preferences(bpy.types.AddonPreferences):
    bl_idname = get_package_name() # type: ignore

    current_lang: bpy.props.EnumProperty(name="Lip Sync Lang", items=LIPSYNC2D_VoskHelper.get_available_languages, default=0) # type: ignore
    is_downloading: bpy.props.BoolProperty(name="Download Status", default=False) # type: ignore
    download_progress: bpy.props.FloatProperty(name="Download Progress", default=0.0, min=0.0, max=100.0) # type: ignore

    def draw(self, context):
        layout = self.layout
        
        # Check for orphaned download state (e.g., after Blender restart)
        if self.is_downloading and LIPSYNC2D_VoskHelper.worker_proc is None:
            self.is_downloading = False
            self.download_progress = 0.0
            LIPSYNC2D_VoskHelper.reset_download_state()

        LIPSYNC2D_AP_Preferences.draw_online_access_warning(layout)

        row = layout.row(align=True)
        # Use sub-layout for property to control enabled state independently
        sub = row.row(align=True)
        sub.enabled = not self.is_downloading
        sub.prop(self, "current_lang", text="") 
        
        current_lang = self.current_lang
        if current_lang != "none":
            # Check if model installed
            prefs = context.preferences.addons[get_package_name()].preferences
            cache_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
            model_path = cache_path / current_lang

            if (not model_path.exists() or not model_path.is_dir()) and not self.is_downloading:
                row.operator("wm.lipsync_install_model", text="", icon="IMPORT")
        
        LIPSYNC2D_AP_Preferences.draw_model_state(row)
        LIPSYNC2D_AP_Preferences.draw_fetch_list_ops(layout)

    @staticmethod
    @LIPSYNC2D_VoskHelper.setextensionpath
    def draw_model_state(row: bpy.types.UILayout) -> None:
        """
        Updates the UI to display the current status of the selected language model.

        :param row: bpy.types.UILayout
            The UI layout row on which the display updates are made.
        :param current_lang: str
            The currently selected language code for the model.
        :return: None
        """
        

        installed = ""
        model_status = LIPSYNC2D_AP_Preferences.get_model_state()

        if model_status == "INSTALLED":
            installed = " Installed"
            row.enabled = True
        elif model_status == "DOWNLOADING":
            # Get progress percentage
            prefs = bpy.context.preferences.addons[get_package_name()].preferences # type: ignore
            progress = getattr(prefs, "download_progress", 0.0)
            installed = f" Downloading... {int(progress)}%"
            row.label(text=installed)
            row.enabled = True
            row.operator("wm.lipsync_cancel_download", text="", icon="X")
        else:
            row.label(text=installed)

    @staticmethod
    @LIPSYNC2D_VoskHelper.setextensionpath
    def get_model_state() -> Literal["INSTALLED", "DOWNLOADING", ""]:
        directory = MODEL_DIRS[3] if len(MODEL_DIRS) >= 4 else None
        result = ""

        prefs = bpy.context.preferences.addons[get_package_name()].preferences # type: ignore

        if prefs is None:
            return result
        
        current_lang = LIPSYNC2D_AP_Preferences.get_current_lang_code()

        if current_lang != "none":
            if directory is not None and Path(directory).exists():
                model_file_list = os.listdir(directory)
                model_file = [model for model in model_file_list if match(f"vosk-model(-small)?-{current_lang}", model) and os.path.isdir(os.path.join(directory, model))]
                if model_file:
                    result = "INSTALLED"
                elif prefs.is_downloading: #type: ignore
                    result = "DOWNLOADING"
            elif prefs.is_downloading: #type: ignore
                    result = "DOWNLOADING"
        
        return result


    @staticmethod
    def draw_online_access_warning(layout: bpy.types.UILayout) -> None:
        if not bpy.app.online_access:
            row = layout.row(align=False)
            row.label(text="Blender Online Access is required")
            row = layout.row(align=True)
            row.label(text="You will only see models in cache")
            row = layout.row(align=True)
            row.label(text="1. Enable Online Access: Preferences > System > Network")
            row = layout.row(align=True)
            row.label(text="2. Reload List: Preferences > Add-ons > Lip Sync > Reload")

    @staticmethod
    def draw_fetch_list_ops(layout: bpy.types.UILayout) -> None:
        row = layout.row()
        row.operator("wm.lipsync_download_list", text="Reload Models List")
        row.enabled = bpy.app.online_access

    @staticmethod
    def get_current_lang_code() -> str:
        prefs = bpy.context.preferences.addons[get_package_name()].preferences # type: ignore
        return prefs.current_lang

