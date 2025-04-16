import os
import zipfile
from glob import glob
import tomlkit

def update_wheels():
    folder = "./wheels"
    files = os.listdir(folder)
    toml_path = "blender_manifest.toml"

    wheel_paths = glob("./wheels/**/*.whl", recursive=True)


    print(wheel_paths)
    clean = [path.replace("\\", "/") for path in wheel_paths]

    # Load the TOML file
    with open(toml_path, "r", encoding="utf-8") as f:
        toml_data = tomlkit.load(f)
    # Update the "wheels" entry
    toml_data["wheels"] = clean
    

    # Write back to the TOML file, preserving formatting and comments
    with open(toml_path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(toml_data))

def build_addon():
    current_dir = os.getcwd()
    exclude_patterns = [
        '.venv',
        '.gitignore',
        '.git',
        '.idea',
        '__pycache__',
        'dist',
        'dev_tools.py'
    ]

    dist_dir = os.path.join(current_dir, "dist")

    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)

    with open("blender_manifest.toml", "r") as f:
        parsed = tomlkit.parse(f.read())
        version = parsed["version"]
        addon_id = parsed["id"]

    with zipfile.ZipFile(f"{current_dir}/dist/{addon_id}_{version}.zip", "w") as zip_file:
        for root, dirs, files in os.walk(f"{current_dir}"):
            dirs[:] = [d for d in dirs if os.path.relpath(os.path.join(root,d), current_dir) not in exclude_patterns]

            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), current_dir)
                # Skip files based on exclude patterns
                if any(file_path.startswith(pattern) or file_path in exclude_patterns for pattern in exclude_patterns):
                    continue

                # Add the file to the zip archive
                zip_file.write(os.path.join(root, file), file_path)

    print(f"Build complete. Addon file saved to {dist_dir}")



# update_wheels()