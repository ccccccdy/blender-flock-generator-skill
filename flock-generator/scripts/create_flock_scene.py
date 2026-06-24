import os
import random
from pathlib import Path

import bpy


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSET_BLEND = SKILL_DIR / "assets" / "FlockGenerator_v1.0.blend"

SOCKETS = {
    "count": "Socket_25",
    "seed": "Socket_34",
    "speed": "Socket_10",
    "start": "Socket_14",
    "loop": "Socket_22",
    "show_paths": "Socket_13",
    "spread_along": "Socket_15",
    "spread_paths": "Socket_9",
    "vertical_waviness": "Socket_18",
    "vertical_intensity": "Socket_19",
    "horizontal_waviness": "Socket_20",
    "horizontal_intensity": "Socket_21",
    "outliers_percentage": "Socket_28",
    "outliers_range": "Socket_27",
    "path_resolution": "Socket_31",
    "body": "Socket_6",
    "wing": "Socket_7",
    "scale": "Socket_29",
    "scale_variation": "Socket_30",
    "flap_speed": "Socket_3",
    "wing_range": "Socket_26",
    "wing_angle_offset": "Socket_32",
    "glide": "Socket_23",
    "glide_frequency": "Socket_5",
}

SOURCE_TEMPLATES = {
    "straight": {
        "crow": "flock_crows_curve",
        "dove": "flock_doves_curve",
        "seagull": "flock_seagulls_curve",
    },
    "circle": {
        "crow": "flock_crows_circle",
        "dove": "flock_doves_circle",
        "seagull": "flock_seagulls_circle",
    },
}

SUPPORT_COLLECTIONS = ["Birds"]
SOURCE_COLLECTIONS = ["Crow Flocks", "Dove Flocks", "Seagull Flocks"]
SPECIES_ORDER = ["crow", "dove", "seagull"]
SPECIES_ALIASES = {
    "crow": "crow",
    "crows": "crow",
    "乌鸦": "crow",
    "dove": "dove",
    "doves": "dove",
    "pigeon": "dove",
    "pigeons": "dove",
    "鸽子": "dove",
    "seagull": "seagull",
    "seagulls": "seagull",
    "gull": "seagull",
    "gulls": "seagull",
    "海鸥": "seagull",
}


def _append_collection_once(collection_name):
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    filepath = str(ASSET_BLEND / "Collection" / collection_name)
    directory = str(ASSET_BLEND / "Collection")
    bpy.ops.wm.append(filepath=filepath, directory=directory, filename=collection_name)
    return bpy.data.collections[collection_name]


def _append_node_group_once(node_group_name="FlockGenerator"):
    if node_group_name in bpy.data.node_groups:
        return bpy.data.node_groups[node_group_name]
    filepath = str(ASSET_BLEND / "NodeTree" / node_group_name)
    directory = str(ASSET_BLEND / "NodeTree")
    bpy.ops.wm.append(filepath=filepath, directory=directory, filename=node_group_name)
    return bpy.data.node_groups[node_group_name]


def _ensure_assets():
    if not ASSET_BLEND.exists():
        raise FileNotFoundError(f"Missing bundled flock asset: {ASSET_BLEND}")
    _append_node_group_once()
    for collection_name in SUPPORT_COLLECTIONS + SOURCE_COLLECTIONS:
        _append_collection_once(collection_name)


def _collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


def _hide_source_assets():
    for collection_name in SUPPORT_COLLECTIONS + SOURCE_COLLECTIONS:
        col = bpy.data.collections.get(collection_name)
        if not col:
            continue
        col.hide_viewport = True
        col.hide_render = True
        for obj in col.objects:
            obj.hide_set(True)
            obj.hide_render = True


def _normalized_counts(template_count, circling_count=0, straight_count=None):
    template_count = max(0, int(template_count))
    circling_count = max(0, int(circling_count or 0))
    if straight_count is None:
        straight_count = template_count - circling_count
    straight_count = max(0, int(straight_count))
    total = circling_count + straight_count
    if total == template_count:
        return circling_count, straight_count
    if total == 0:
        return 0, template_count
    if total < template_count:
        return circling_count, straight_count + (template_count - total)
    circle = round(template_count * circling_count / total)
    circle = max(0, min(template_count, circle))
    return circle, template_count - circle


def _species_key(value):
    key = str(value).strip().lower()
    if key not in SPECIES_ALIASES:
        raise ValueError(f"Unknown bird species: {value}. Use seagull, dove, or crow.")
    return SPECIES_ALIASES[key]


def _species_sequence(total_count, species_counts=None):
    total_count = max(0, int(total_count))
    if total_count == 0:
        return []
    if not species_counts:
        return [SPECIES_ORDER[index % len(SPECIES_ORDER)] for index in range(total_count)]

    normalized = {species: 0 for species in SPECIES_ORDER}
    for species, count in species_counts.items():
        normalized[_species_key(species)] += max(0, int(count))

    sequence = []
    for species in SPECIES_ORDER:
        sequence.extend([species] * normalized[species])

    if len(sequence) < total_count:
        missing = total_count - len(sequence)
        sequence.extend(SPECIES_ORDER[index % len(SPECIES_ORDER)] for index in range(missing))
    return sequence[:total_count]


def _copy_object_to_collection(source_obj, target_collection):
    obj = source_obj.copy()
    obj.data = source_obj.data.copy()
    obj.animation_data_clear()
    for collection in obj.users_collection:
        collection.objects.unlink(obj)
    target_collection.objects.link(obj)
    return obj


def _varied(value, rng, amount):
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return max(1, int(round(value * rng.uniform(1 - amount, 1 + amount))))
    return float(value) * rng.uniform(1 - amount, 1 + amount)


def _set_socket(modifier, socket_key, value):
    socket_id = SOCKETS[socket_key]
    if socket_id in modifier.keys():
        modifier[socket_id] = value


def _vary_modifier(obj, index, mode, rng):
    modifier = obj.modifiers.get("FlockGenerator")
    if not modifier:
        return
    _set_socket(modifier, "seed", rng.randint(1, 99999))
    if SOCKETS["count"] in modifier.keys():
        _set_socket(modifier, "count", _varied(int(modifier[SOCKETS["count"]]), rng, 0.15))
    for socket_key in [
        "speed",
        "spread_paths",
        "vertical_waviness",
        "vertical_intensity",
        "horizontal_waviness",
        "horizontal_intensity",
        "outliers_range",
    ]:
        socket_id = SOCKETS[socket_key]
        if socket_id in modifier.keys():
            _set_socket(modifier, socket_key, _varied(float(modifier[socket_id]), rng, 0.10))
    for socket_key in ["scale", "scale_variation", "flap_speed", "wing_range", "glide_frequency"]:
        socket_id = SOCKETS[socket_key]
        if socket_id in modifier.keys():
            _set_socket(modifier, socket_key, _varied(float(modifier[socket_id]), rng, 0.08))
    base_start = -10.0 if mode == "circle" else 0.0
    _set_socket(modifier, "start", base_start + rng.uniform(-2.0, 2.0))
    _set_socket(modifier, "show_paths", True)
    obj["flock_template_index"] = index
    obj["flock_mode"] = mode


def create_flock_scene(
    template_count,
    circling_count=0,
    straight_count=None,
    circling_species_counts=None,
    straight_species_counts=None,
    seed=1234,
    collection_name="Generated Bird Flocks",
    circling_spacing_x=65.0,
    straight_spacing_z=35.0,
    straight_lane_y=-80.0,
):
    """Create varied bird flock templates from the bundled FlockGenerator asset."""
    _ensure_assets()
    circle_count, line_count = _normalized_counts(template_count, circling_count, straight_count)
    rng = random.Random(seed)
    target_collection = _collection(collection_name)
    created = []
    circle_species = _species_sequence(circle_count, circling_species_counts)
    straight_species = _species_sequence(line_count, straight_species_counts)

    layout_plan = []
    for mode_index in range(circle_count):
        layout_plan.append(
            {
                "mode": "circle",
                "mode_index": mode_index,
                "species": circle_species[mode_index],
                "location": (mode_index * circling_spacing_x, 0.0, 0.0),
            }
        )
    for mode_index in range(line_count):
        layout_plan.append(
            {
                "mode": "straight",
                "mode_index": mode_index,
                "species": straight_species[mode_index],
                "location": (0.0, straight_lane_y, mode_index * straight_spacing_z),
            }
        )

    for index, item in enumerate(layout_plan, start=1):
        mode = item["mode"]
        species = item["species"]
        source_name = SOURCE_TEMPLATES[mode][species]
        source_obj = bpy.data.objects[source_name]
        obj = _copy_object_to_collection(source_obj, target_collection)
        obj.name = f"generated_{mode}_flock_{index:02d}_{source_name.replace('flock_', '')}"
        obj.location.x, obj.location.y, obj.location.z = item["location"]
        obj.rotation_euler.z = rng.uniform(-0.25, 0.25)
        obj.hide_set(False)
        obj.hide_render = False
        _vary_modifier(obj, index, mode, rng)
        obj["flock_species"] = species
        created.append(obj)
    _hide_source_assets()
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = max(bpy.context.scene.frame_end, 240)
    for obj in created:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = created[0] if created else None
    return created


if __name__ == "__main__":
    create_flock_scene(template_count=8, circling_count=3, straight_count=5)
