import json
import os
import threading
from pathlib import Path
from re import match
from typing import Callable

import bpy
import requests
from vosk import MODEL_DIRS, MODEL_LIST_URL, Model

from ..Core.LIPSYNC2D_BlenderThread import LIPSYNC2D_BlenderThread
from ..Core.LIPSYNC2D_VoskHelper import LIPSYNC2D_VoskHelper
from ..LIPSYNC2D_Utils import get_package_name


class LIPSYNC2D_AP_Preferences(bpy.types.AddonPreferences):
    bl_idname = get_package_name() # type: ignore

    current_lang: bpy.props.EnumProperty(name="Lip Sync Lang", items=LIPSYNC2D_VoskHelper.get_available_languages, update=LIPSYNC2D_VoskHelper.install_model, default=0) # type: ignore
    is_downloading: bpy.props.BoolProperty(name="Download Status", default=False) # type: ignore

    def draw(self, context):
        layout = self.layout

        LIPSYNC2D_AP_Preferences.draw_online_access_warning(layout)

        row = layout.row(align=True)
        row.label(text="Language Model")
        row.prop(self, "current_lang", text="") 
        
        LIPSYNC2D_AP_Preferences.draw_model_state(row, self.current_lang)
        LIPSYNC2D_AP_Preferences.draw_fetch_list_ops(layout)

    @staticmethod
    @LIPSYNC2D_VoskHelper.patchmodellang("ua", "uk")
    @LIPSYNC2D_VoskHelper.setextensionpath
    def draw_model_state(row: bpy.types.UILayout, current_lang: str) -> None:
        """
        Updates the UI to display the current status of the selected language model.

        :param row: bpy.types.UILayout
            The UI layout row on which the display updates are made.
        :param current_lang: str
            The currently selected language code for the model.
        :return: None
        """
        prefs = bpy.context.preferences.addons[get_package_name()].preferences # type: ignore

        if prefs is None:
            return

        installed = ""
        if current_lang != "none":
            directory = MODEL_DIRS[3] if len(MODEL_DIRS) >= 4 else None

            if directory is not None and Path(directory).exists():
                model_file_list = os.listdir(directory)
                model_file = [model for model in model_file_list if match(f"vosk-model(-small)?-{current_lang}", model) and os.path.isdir(os.path.join(directory, model))]
                if model_file:
                    installed = " Installed"
                    row.enabled = True
                elif prefs.is_downloading: #type: ignore
                    installed = " Downloading..."
                    row.enabled = False
            elif prefs.is_downloading: #type: ignore
                    installed = " Downloading..."
                    row.enabled = False


        row.label(text=installed)

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
        row.operator("lipsync2d.downloadlist", text="Reload Models List")
        row.enabled = bpy.app.online_access

