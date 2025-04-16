import ctypes
import ctypes.util
import os
import pathlib
import platform
import zipfile
from typing import cast

import bpy
from phonemizer.backend import EspeakBackend

from ..LIPSYNC2D_Utils import get_package_name


class LIPSYNC2D_EspeakInspector():

    def try_find_library(self):
        lib = self.find_library()

        if lib is None:
            raise FileNotFoundError("Espeak lib not found")
        
        path = self.find_library_path(lib)

        if path is None:
            raise Exception("Error during import")
        
        return path

    def find_library(self) -> str | None:
        library = (
                ctypes.util.find_library('espeak-ng') or
                ctypes.util.find_library('espeak'))
        
        if library is None and platform.system() == "Windows":
            library = self.find_windows_library()
        
        return library
    
    def find_library_path(self, library: str):
        espeak = ctypes.cdll.LoadLibrary(str(library))
        path = pathlib.Path(espeak._name).resolve()

        if not path.is_file(): return None
        
        return str(path)
    
    def find_windows_library(self) -> str | None:
        drives = self.get_windows_drives()
        lib = None

        for drive in drives:
            dll_path = os.path.join(f"{drive}Program Files","eSpeak NG", "libespeak-ng.dll")

            if os.path.isfile(dll_path):
                lib = dll_path
                
                break

        return lib
    
    def get_windows_drives(self):
        buffer = ctypes.create_unicode_buffer(256)
        ctypes.windll.kernel32.GetLogicalDriveStringsW(256, buffer)
        drives = buffer.value.split('\x00')
        return [d for d in drives if d]

    @staticmethod
    def unzip_binaries():
        plat = str.lower(platform.system())

        script_dir = pathlib.Path(__file__).parent  # Get the directory where the script is located
        input_archive = script_dir / ".." / "Assets" / "Archives" / plat / f"espeak-ng-{plat}.zip"
        package_name = cast(str, get_package_name())

        try:
            output_dir = bpy.utils.extension_path_user(package_name, path=f"bin/{plat}", create=True)
            with zipfile.ZipFile(input_archive, 'r') as zip_ref:
                zip_ref.extractall(output_dir)  # Extract all files to the output directory

        except FileNotFoundError:
            raise FileNotFoundError(f"Input archive '{input_archive}' not found")
        except zipfile.BadZipFile:
            raise Exception(f"The file '{input_archive}' is not a valid zip archive")
        except Exception as e:
            raise Exception(f"Error during archive extraction: {e}")

        if plat == "windows":
            EspeakBackend.set_library(pathlib.Path(output_dir) / "libespeak-ng.dll")
        elif plat == "linux":
            EspeakBackend.set_library(pathlib.Path(output_dir) / "libespeak-ng.so")
        elif plat == "darwin":
            EspeakBackend.set_library(pathlib.Path(output_dir) / "libespeak-ng.dylib")
        else:
            raise Exception(f"Unsupported platform: {plat}")
