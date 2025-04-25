import pathlib
import sys

from vosk import MODEL_DIRS, Model


def install_model(lang: str, vosk_cache: str) -> None:
    """
    Download and/or Installs the specified language model for speech recognition. This function ensures
    the target directory for the model exists and initializes the model using the
    provided language and cache directory.

    :param lang: The language code for the model to be installed.
    :param vosk_cache: The directory path where the model should be cached.
    :return: None
    """
    MODEL_DIRS[3] = pathlib.Path(vosk_cache)
    model_path = MODEL_DIRS[3]

    if not model_path.exists():
        model_path.mkdir(parents=True, exist_ok=True)

    Model(lang=lang)


args = sys.argv[1:]
lang = args[0]
vosk_cache = args[1]

install_model(args[0], args[1])