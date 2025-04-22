import os
import shutil
import zipfile
from collections import defaultdict
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





def handle_duplicate_wheels(directory: str):
    """
    Find and handle duplicate .whl files in the given directory and its subdirectories.
    Keeps files in ./wheels/common and removes duplicates. If a file is not in ./wheels/common,
    moves one to ./wheels/common and deletes the others.

    :param directory: str: The path to the directory to search for .whl files.
    :return: None
    """
    # Path to the common directory
    common_path = os.path.join(directory, "common")
    # Create the common directory if it doesn't exist
    os.makedirs(common_path, exist_ok=True)

    # Dictionary to store .whl filenames and their paths
    files_dict = defaultdict(list)

    # Traverse the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            print(f"Processing file: {file}")

            # Check if the file is a .whl file
            if file.endswith(".whl"):
                # Store the file and its full path in the dictionary
                full_path = os.path.join(root, file)
                files_dict[file].append(full_path)

    # Handle duplicates (files with more than one associated path)
    for file, paths in files_dict.items():
        if len(paths) > 1:  # Check if there are duplicates
            print(f"\nDuplicate found for: {file}")
            print("Locations:")
            for path in paths:
                print(f" - {path}")

            # Check if the file already exists in the common directory
            common_file_path = os.path.join(common_path, file)
            if os.path.exists(common_file_path):
                # Remove all duplicates, as the file already exists in common
                print(f"File already in common directory: {common_file_path}")
                for path in paths:
                    if path != common_file_path:
                        print(f"Removing duplicate: {path}")
                        os.remove(path)
            else:
                # Move one file to common and remove the others
                print(f"Moving one copy to common directory: {common_file_path}")
                shutil.move(paths[0], common_file_path)  # Move the first file to common
                for path in paths[1:]:
                    print(f"Removing duplicate: {path}")
                    os.remove(path)
        else:
            print(f"No duplicates for: {file}")


if __name__ == "__main__":
    update_wheels()
