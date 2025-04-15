import ctypes
import ctypes.util
import os
import pathlib
import platform


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

    