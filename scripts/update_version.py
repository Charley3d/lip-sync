import sys
from tomlkit import parse, dumps  # type: ignore

version = sys.argv[1]
toml_path = "blender_manifest.toml"

with open(toml_path, "r", encoding="utf-8") as f:
    doc = parse(f.read())

doc["version"] = version

with open(toml_path, "w", encoding="utf-8") as f:
    f.write(dumps(doc))
