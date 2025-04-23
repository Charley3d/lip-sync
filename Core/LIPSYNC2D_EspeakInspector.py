import os
import pathlib
import platform
import zipfile
from typing import cast

import bpy
from phonemizer.backend import EspeakBackend

from ..LIPSYNC2D_Utils import get_package_name


class LIPSYNC2D_EspeakInspector():
    @staticmethod
    def unzip_binaries() -> None:
        plat = str.lower(platform.system())
        espeak_archive_path = LIPSYNC2D_EspeakInspector.get_espeak_archive_path()
        espeak_data_archive_path = LIPSYNC2D_EspeakInspector.get_espeak_data_archive_path()
        espeak_extraction_path = LIPSYNC2D_EspeakInspector.get_espeak_extraction_path()
        
        try:
            with zipfile.ZipFile(espeak_archive_path, 'r') as zip_ref:
                zip_ref.extractall(espeak_extraction_path)
                
            with zipfile.ZipFile(espeak_data_archive_path, 'r') as zip_ref:
                zip_ref.extractall(espeak_extraction_path) 


        except FileNotFoundError:
            raise FileNotFoundError(f"Input archive '{espeak_archive_path}' not found")
        except zipfile.BadZipFile:
            raise Exception(f"The file '{espeak_archive_path}' is not a valid zip archive")
        except Exception as e:
            raise Exception(f"Error during archive extraction: {e}")

    @staticmethod
    def set_espeak_backend():
        plat = str.lower(platform.system())
        espeak_extraction_path = LIPSYNC2D_EspeakInspector.get_espeak_extraction_path()
        output_path = pathlib.Path(espeak_extraction_path)
        if plat == "windows":
            EspeakBackend.set_library(output_path / "libespeak-ng.dll")
        elif plat == "linux":
            EspeakBackend.set_library(output_path / "libespeak-ng.so")
        elif plat == "darwin":
            EspeakBackend.set_library(output_path / "libespeak-ng.dylib")
        else:
            raise Exception(f"Unsupported platform: {plat}")

        os.environ["ESPEAK_DATA_PATH"] = str(output_path / "espeak-ng-data")
    
    @staticmethod
    def get_espeak_archive_path() -> pathlib.Path:
        plat = str.lower(platform.system())
        script_dir = pathlib.Path(__file__).parent  # Get the directory where the script is located
        archive_path = script_dir / ".." / "Assets" / "Archives" / plat / f"espeak-ng-{plat}.zip"

        return archive_path

    @staticmethod
    def get_espeak_data_archive_path() -> pathlib.Path:
        script_dir = pathlib.Path(__file__).parent  # Get the directory where the script is located
        archive_path = script_dir / ".." / "Assets" / "Archives" / "common" / "espeak-ng-data.zip"

        return archive_path
    
    @staticmethod
    def get_espeak_extraction_path() -> pathlib.Path:
        package_name = cast(str, get_package_name())
        plat = str.lower(platform.system())

        try:
            user_extension_bin_dir = bpy.utils.extension_path_user(package_name, path=f"bin/{plat}", create=True)
            user_extension_bin_path = pathlib.Path(user_extension_bin_dir)
        except Exception as e:
            raise Exception("Error while trying to get User Extension Path")

        return user_extension_bin_path
    
    
    @staticmethod
    def get_espeak_filepath() -> pathlib.Path:
        plat = str.lower(platform.system())
        espeak_path = LIPSYNC2D_EspeakInspector.get_espeak_extraction_path()

        if plat == "windows":
            return espeak_path / "libespeak-ng.dll"
        elif plat == "linux":
            return espeak_path / "libespeak-ng.so"
        elif plat == "darwin":
            return espeak_path / "libespeak-ng.dylib"
        
        # Fallback to linux lib
        return espeak_path / "libespeak-ng.so"
        

    @staticmethod
    def is_espeak_already_extracted() -> bool:
        espeak_filepath = LIPSYNC2D_EspeakInspector.get_espeak_filepath()
        return espeak_filepath.is_file()
