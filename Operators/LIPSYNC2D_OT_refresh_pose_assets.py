from pathlib import Path
from typing import Literal
import bpy


class LIPSYNC2D_OT_refresh_pose_assets(bpy.types.Operator):
    bl_idname = "lipsync2d.refresh_pose_assets"
    bl_label = "Refresh Pose Assets"
    bl_description = "Only use this if your Asset Poses are not shown.\nIt will load all Pose Assets from your assets libraries into your current .blend."

    def execute(
        self, context
    ) -> set[
        Literal["RUNNING_MODAL", "CANCELLED", "FINISHED", "PASS_THROUGH", "INTERFACE"]
    ]:
        self.load_pose_assets_from_libraries()

        # Count loaded pose assets
        pose_asset_count = sum(1 for action in bpy.data.actions if action.asset_data)
        self.report({"INFO"}, f"Loaded {pose_asset_count} pose assets")

        return {"FINISHED"}

    def load_pose_assets_from_libraries(self):
        """Load pose assets from all configured asset libraries using bpy.data.libraries.load"""

        # Get asset library preferences
        prefs = bpy.context.preferences
        if prefs is None:
            return

        filepaths = prefs.filepaths
        asset_libraries = filepaths.asset_libraries

        for asset_library in asset_libraries:
            library_path = Path(asset_library.path)

            if not library_path.exists():
                continue

            # Find all .blend files in the library
            blend_files = [fp for fp in library_path.rglob("*.blend") if fp.is_file()]

            for blend_file in blend_files:
                try:
                    # Load only assets from the file
                    with bpy.data.libraries.load(str(blend_file), assets_only=True) as (
                        data_from,
                        data_to,
                    ):
                        # Load all actions that are assets (pose assets)
                        data_to.actions = data_from.actions

                except Exception as e:
                    continue
