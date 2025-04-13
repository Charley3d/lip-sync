import os
from glob import glob
import tomlkit

def update_wheels():
    folder = "./wheels"
    files = os.listdir(folder)
    toml_path = "blender_manifest.toml"

    # file_list = [f for f in files if os.path.isfile(os.path.join(folder, f))]

    # for file in file_list:

    wheel_paths = glob("./wheels/*.whl")
    print(wheel_paths)
    clean = [path.replace("\\", "/") for path in wheel_paths]

    # Load the TOML file
    # Load the TOML file
    with open(toml_path, "r", encoding="utf-8") as f:
        toml_data = tomlkit.load(f)
    # Update the "wheels" entry
    toml_data["wheels"] = clean
    

    # Write back to the TOML file, preserving formatting and comments
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(toml_data))

update_wheels()