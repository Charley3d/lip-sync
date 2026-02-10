import json
import os
import pathlib
import subprocess
import sys
from typing import Callable, Literal, cast

import bpy
import requests
from vosk import MODEL_DIRS, MODEL_LIST_URL

from ..LIPSYNC2D_Utils import get_package_name


class LIPSYNC2D_VoskHelper():
    """
    Helper functions and utilities for lip-syncing using Vosk language models.

    This class offers tools for managing language models for lip-syncing in
    Blender. It includes methods for listing available languages, installing
    language models, managing cache, and more. The class primarily works with
    online and offline Vosk language models and facilitates usage within the
    Blender environment.

    :ivar worker_proc: Manages the subprocess handling asynchronous language model installation.
    :type worker_proc: subprocess.Popen | None
    :ivar excluded_lang: A list of language codes to exclude from model selection,
        such as unstable languages or ones causing caching issues.
    :type excluded_lang: list[str]
    """
    worker_proc: subprocess.Popen | None = None
    # Langs in this list won't show up in Language Model selection
    excluded_lang = [
        "kz",  # Unstable, throw ASSERTION_FAILED error
        "ua"
        # Vosk uses ua to identify Ukrainian but store a model named **-uk-**.zip preventing efficient caching and force model to be downloaded each time
    ]

    @staticmethod
    def setextensionpath(func):
        """
        A static method decorator that sets a predefined path for vosk Cache and ensures the directory exists.
        It wraps the given function, updating the vosk project-specific `MODEL_DIRS` mapping with the dynamically
        determined path for the extension cache directory. If the directory does not already exist, it will
        be created before the wrapped function executes.

        :param func: The function to be wrapped.
        :type func: Callable
        :return: Wrapped function that ensures the extension cache path is set and exists.
        :rtype: Callable
        """
        def wrapper(*args, **kwargs):
            MODEL_DIRS[3] = LIPSYNC2D_VoskHelper.get_extension_path("cache")
            model_path = pathlib.Path(MODEL_DIRS[3])

            if not model_path.exists():
                model_path.mkdir(parents=True, exist_ok=True)

            result = func(*args, **kwargs)
            return result

        return wrapper

    @staticmethod
    def get_extension_path(subfolder: Literal['cache', 'tmp', 'bin', ''] = "") -> pathlib.Path:
        """
        Gets the user-defined extension path for a specific subfolder associated with the package.

        This method retrieves the path where addon can store various elements. The subfolder
        argument allows specifying a specific subdirectory within the extension path to retrieve.
        If no subfolder is provided, the base extension path is returned. The path will automatically
        be created if it does not already exist. The result is returned as a `pathlib.Path` object.

        :param subfolder: One of the specified subfolder names ('cache', 'tmp', 'bin', or '')
                          indicating the subdirectory within the extension path to retrieve.
        :return: A `pathlib.Path` object pointing to the requested extension path.
        :rtype: pathlib.Path
        """
        package_name = cast(str, get_package_name())
        return pathlib.Path(bpy.utils.extension_path_user(package_name, path=subfolder, create=True))

    @staticmethod
    def get_available_langs_online() -> list[tuple[str, str, str]]:
        """
        This method retrieves a language list from a cached file, filters it based on predefined
        criteria, and returns it in a formatted tuple containing unique identifiers, language
        names, and additional data. Sorting is applied for better readability of the language options.

        :param cached_langs_list_file: The path to the cached languages list file, fetched from the class helper.
        :raises Exception: Raised when there is an error loading the cached file.
        :rtype: List[tuple[str, str, str]]
        :return: A list of tuples where each tuple contains three strings:
            - Language identifier
            - Display text for the language
            - Key representing the language
        """
        langs_list = []
        all_langs = []
        cached_langs_list_file = LIPSYNC2D_VoskHelper.get_language_list_file()

        if os.path.isfile(cached_langs_list_file):
            try:
                with open(cached_langs_list_file, "r", encoding="utf-8") as f:
                    langs_list = json.load(f)
            except Exception as e:
                raise Exception(f"Error while loading cached files index.{e}")

        if langs_list:
            cache_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
            
            # List should already be filtered. This is done as a safety measure.
            for l in langs_list:
                if l["lang"] == "all" or l["obsolete"] != "false" or l["lang"] in LIPSYNC2D_VoskHelper.excluded_lang:
                    continue
                
                name = l["name"]
                lang_text = l["lang_text"]
                size_text = l.get('size_text', 'Unknown')
                label = f"{lang_text} ({size_text})"
                
                # Check if installed
                model_path = cache_path / name
                if model_path.exists() and model_path.is_dir():
                    label = f"{label} - Installed"
                
                all_langs.append((name, label))

            all_langs.sort(key=lambda x: x[1])

        all_langs = [('none', "-- None --", "No selection"), ] + all_langs

        enum_items = [(list(l)[0], list(l)[1], list(l)[0]) for l in all_langs]

        return enum_items

    @staticmethod
    def get_available_langs_offline() -> list[tuple[str, str, str]]:
        """
        Returns a list of all available offline language models from the local cache directory
        along with their metadata. It checks the local extension path for cached language
        model directories and a JSON file containing language metadata. If a corresponding
        language model exists in both the cache and the metadata file, it is included in the
        list. A default 'none' option is always included at the beginning of the list.

        This method is useful for retrieving the available offline language models to
        be used in the application.

        :param ext_path: The path to the cache directory where language models are stored,
            as obtained by the `get_extension_path` method.
        :type ext_path: pathlib.Path

        :return: A list of tuples, where each tuple contains the following elements:
            - The code of the language model.
            - The display text for the language model.
            - A detailed label for the language model.
        :rtype: list[tuple[str, str, str]]

        :raises Exception: If the `languages_list.json` file is present but cannot be parsed
            as valid JSON, or an unexpected error occurs during the file reading or
            processing.

        """
        ext_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
        all_offline_langs = []

        if not ext_path.is_dir():
            return all_offline_langs

        cached_langs_list_file = ext_path / "languages_list.json"

        if cached_langs_list_file.is_file():
            try:
                with open(cached_langs_list_file, "r", encoding="utf-8") as f:
                    langs_list = json.load(f)
            except Exception as e:
                raise Exception(f"Error while loading cached files index. {e}")

            all_dir_names = {
                lang["name"]: (lang["name"], f"✔ {lang['lang_text']} ({lang.get('size_text', 'Unknown')})", lang["name"])
                for lang in langs_list
                if lang["obsolete"] == "false"
            }

            all_offline_langs = [all_dir_names[pathlib.Path(model_dir).name] for model_dir in ext_path.iterdir() if
                                 model_dir.is_dir() and pathlib.Path(model_dir).name in all_dir_names]

        all_offline_langs = [('none', "-- None --", "No selection")] + all_offline_langs
        return all_offline_langs

    @staticmethod
    def cache_online_langs_list() -> None:
        """
        Caches the list of online language models by fetching them from the specified URL and
        filtering the data. The filtered list is then stored in a local file for later use.

        This method retrieves the language model list via an HTTP GET request, processes it
        to filter models based on specified criteria, and writes the filtered list to a local
        file in JSON format. If any error occurs during the process, it raises an exception.

        :raises Exception: If there is an error while writing the filtered data to the file or
            during processing.
        :return: This method does not return any value.
        """
        list_request = requests.get(MODEL_LIST_URL)
        if list_request:
            try:
                with open(LIPSYNC2D_VoskHelper.get_language_list_file(), "w", encoding="utf-8") as f:
                    full_list = list_request.json()
                    filter_list = [item for item in full_list if
                                   item["obsolete"] == "false"]
                    json.dump(filter_list, f, ensure_ascii=False)
            except Exception as e:
                raise Exception(f"Error while creating cached file index: {e}")

    @staticmethod
    def get_language_list_file() -> pathlib.Path:
        """
        Gets the path to the languages list file.

        This method retrieves the path to the JSON file that contains the list of
        languages for the application. The file is stored under a 'cache' directory
        within the extension path.

        :return: The pathlib.Path object representing the location of the languages
            list JSON file.
        :rtype: pathlib.Path
        """
        return LIPSYNC2D_VoskHelper.get_extension_path("cache") / "languages_list.json"

    @staticmethod
    def get_available_languages(_, context) -> list[tuple[str, str, str]]:
        """
        Retrieve the list of available languages either online or offline.

        This method determines available languages based on the application's online
        connectivity. When online access is available, it returns the list of languages
        available online; otherwise, it retrieves the list of cached languages. Each language entry
        is represented by a tuple containing three string elements.

        :param _: Placeholder argument, not used in the method.
        :param context: Blender context providing information such as the current area,
                        screen, scene, etc.
        :return: A list of tuples representing the available languages. Each tuple consists
                 of three strings: the language code, a human-readable language name, and
                 additional language metadata.
        :rtype: list[tuple[str, str, str]]
        """
        available_langs = LIPSYNC2D_VoskHelper.get_available_langs_online() if bpy.app.online_access else LIPSYNC2D_VoskHelper.get_available_langs_offline()
        return available_langs

    @staticmethod
    def get_model_url(model_name: str) -> str | None:
        """
        Get the download URL for a specific model from the cached languages list.

        :param model_name: The name of the model to get the URL for
        :return: The download URL for the model, or None if not found
        :rtype: str | None
        """
        cached_langs_list_file = LIPSYNC2D_VoskHelper.get_language_list_file()
        
        if not os.path.isfile(cached_langs_list_file):
            return None
        
        try:
            with open(cached_langs_list_file, "r", encoding="utf-8") as f:
                langs_list = json.load(f)
                
            for lang in langs_list:
                if lang.get("name") == model_name:
                    return lang.get("url")
        except Exception:
            return None
        
        return None

    @staticmethod
    def install_model(addon_prefs, context) -> None:
        """
        Install a language model for use with the application. This method initializes the
        environment, sets up the necessary paths, and spawns a separate process to download
        language models asynchronously. It ensures that resources are correctly managed
        during the process.

        :param addon_prefs: An instance of the addon preferences containing the configuration
            settings. Includes current language and status of the download process.
        :type addon_prefs: AddonPreferences
        :param context: The Blender context in which this method is invoked. Provides access
            to the current state of Blender.
        :type context: bpy.types.Context
        :return: None. The method performs operations asynchronously and handles the
            results through callbacks.
        :rtype: NoneType
        """
        if addon_prefs.current_lang == "none":
            return

        # Get the model URL from the cached list
        model_url = LIPSYNC2D_VoskHelper.get_model_url(addon_prefs.current_lang)
        if not model_url:
            raise Exception(f"Could not find download URL for model: {addon_prefs.current_lang}")

        addon_prefs.is_downloading = True
        addon_prefs.download_progress = 0.0

        # Prepare env to ensure process can access to all modules
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join(sys.path)

        # Get custom cache path to change vosk default one
        vosk_cache_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
        
        # Create progress file path
        progress_file = LIPSYNC2D_VoskHelper.get_extension_path("tmp") / "download_progress.json"

        args = [model_url, addon_prefs.current_lang, str(vosk_cache_path), str(progress_file)]
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        worker_path = os.path.join(project_root, "Workers", "wrk_download_models.py")

        LIPSYNC2D_VoskHelper.worker_proc = subprocess.Popen(
            [sys.executable, worker_path, *args],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True)

        bpy.app.timers.register(LIPSYNC2D_VoskHelper.check_worker_finished)
        return

    @staticmethod
    def cancel_download() -> None:
        """
        Cancel the current download process.
        Terminates the worker process, cleans up partial files, and resets the download state.
        """
        if LIPSYNC2D_VoskHelper.worker_proc:
            try:
                LIPSYNC2D_VoskHelper.worker_proc.terminate()
                LIPSYNC2D_VoskHelper.worker_proc.wait(timeout=2)
            except Exception:
                try:
                    LIPSYNC2D_VoskHelper.worker_proc.kill()
                except Exception:
                    pass
            LIPSYNC2D_VoskHelper.worker_proc = None

        # Clean up the partial zip file
        all_preferences = bpy.context.preferences
        package_name = get_package_name()
        
        if package_name and all_preferences and all_preferences.addons:
            addon = all_preferences.addons.get(package_name)
            if addon and addon.preferences:
                current_lang = addon.preferences.current_lang
                if current_lang and current_lang != "none":
                    cache_path = LIPSYNC2D_VoskHelper.get_extension_path("cache")
                    zip_path = cache_path / f"{current_lang}.zip"
                    if zip_path.exists():
                        try:
                            os.remove(zip_path)
                        except Exception:
                            pass

        LIPSYNC2D_VoskHelper.reset_download_state()

    @staticmethod
    def reset_download_state() -> None:
        """
        Reset the download state to clear any stuck or orphaned download status.
        This is useful when a download was interrupted or Blender was closed mid-download.
        """
        all_preferences = bpy.context.preferences
        package_name = get_package_name()
        
        if package_name is None or all_preferences is None or all_preferences.addons is None:
            return
        
        addon = all_preferences.addons.get(package_name)
        
        if addon is None or addon.preferences is None:
            return
        
        addon.preferences.is_downloading = False
        addon.preferences.download_progress = 0.0
        
        # Clean up progress file if it exists
        progress_file = LIPSYNC2D_VoskHelper.get_extension_path("tmp") / "download_progress.json"
        if progress_file.exists():
            try:
                os.remove(progress_file)
            except Exception:
                pass

    @staticmethod
    def check_worker_finished() -> float | None:
        """
        Checks the state of the worker process for LIPSYNC2D_VoskHelper and updates
        related addon preferences if necessary. Also reads progress updates from
        the progress file and updates the UI.

        This method inspects the current state of the `worker_proc` attribute
        belonging to `LIPSYNC2D_VoskHelper`. If the process is still active,
        it reads the progress file and updates the download_progress property.
        If the process has completed execution, the method performs cleanup tasks,
        such as resetting the `worker_proc` to None, retrieving the associated
        addon preferences from Blender's context, and updating the `is_downloading`
        preference flag for the identified addon (if applicable).

        :returns: 0.5 if the worker process is still active (check every 0.5s); None otherwise.
        :rtype: float or None
        """
        if LIPSYNC2D_VoskHelper.worker_proc is None:
            # Check if we have an orphaned download state (Blender was restarted mid-download)
            all_preferences = bpy.context.preferences
            package_name = get_package_name()
            
            if package_name and all_preferences and all_preferences.addons:
                addon = all_preferences.addons.get(package_name)
                if addon and addon.preferences and addon.preferences.is_downloading:
                    # Reset orphaned download state
                    LIPSYNC2D_VoskHelper.reset_download_state()
            
            return None

        all_preferences = bpy.context.preferences
        package_name = get_package_name()

        if package_name is None or all_preferences is None or all_preferences.addons is None:
            return None

        addon = all_preferences.addons.get(package_name)

        if addon is None or addon.preferences is None:
            return None

        # Read progress from file
        progress_file = LIPSYNC2D_VoskHelper.get_extension_path("tmp") / "download_progress.json"
        if progress_file.exists():
            try:
                with open(progress_file, "r") as f:
                    progress_data = json.load(f)
                    addon.preferences.download_progress = progress_data.get("progress", 0.0)
            except Exception:
                pass  # Silently ignore read errors

        if LIPSYNC2D_VoskHelper.worker_proc.poll() is None:
            # Process still running, check again in 0.5 seconds
            return 0.5
        else:
            # Process finished
            LIPSYNC2D_VoskHelper.worker_proc = None
            addon.preferences.is_downloading = False
            addon.preferences.download_progress = 0.0
            
            # Clean up progress file
            if progress_file.exists():
                try:
                    os.remove(progress_file)
                except Exception:
                    pass

            return None
