from typing import List, Tuple


# This cache is required as a workaround for character encoding issue
# when using dynamic EnumProperty items (https://docs.blender.org/api/master/bpy.props.html#bpy.props.EnumProperty).
# Do not remove it otherwise non ascii characters will be displayed as Mojibake (https://github.com/Charley3d/lip-sync/issues/14)
STRING_CACHE = {}


def intern_enum_items(items: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
    """Cache strings to prevent memory issues"""

    def intern_string(s):
        if not isinstance(s, str):
            return s
        global STRING_CACHE
        if s not in STRING_CACHE:
            STRING_CACHE[s] = s
        return STRING_CACHE[s]

    return [tuple(intern_string(s) for s in item) for item in items]
