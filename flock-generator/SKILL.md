---
name: flock-generator
description: Create Blender bird flock scenes from the distilled FlockGenerator_v1.0 asset. Use when Codex needs to generate, duplicate, parameterize, or vary animated bird flock templates in Blender, especially when the user provides template_count/int, circling_count, and straight_count values for circling and straight-flight bird groups.
---

# Flock Generator

## Overview

Use this skill to create Blender bird flock templates from the bundled `FlockGenerator_v1.0` asset. The distilled generator exposes user inputs for total template count, circling flock count, straight-flight flock count, and bird species allocation for each flight mode; seeds, speed, spacing, waviness, scale, flap, and glide settings should be chosen from the source templates with small natural variations.

## Required Inputs

Collect these values before generating:

- `template_count` int: total flock template objects to create.
- `circling_count` int: number of templates using the `*_circle` flight path.
- `straight_count` int: number of templates using the `*_curve` flight path.
- `circling_species_counts` dict: how many circling/perching-flight templates use each bird species.
- `straight_species_counts` dict: how many straight-flight templates use each bird species.

Supported species keys:

- `seagull` / `海鸥`
- `dove` / `鸽子`
- `crow` / `乌鸦`

## Invocation UX

When the user invokes this skill without all required counts, ask for missing values before running Blender or modifying any file.

First ask for flight-mode counts:

```text
Please provide the bird flock counts: total template count, circling/perching-flight count, and straight-flight count.
```

Accept natural-language answers such as "12 total, 4 circling, 8 straight" and map them to `template_count=12`, `circling_count=4`, `straight_count=8`.

If the user provides only two values and one can be safely derived, infer the missing value and state the inference before generating. For example, if total is 12 and circling is 4, infer `straight_count=8`.

Then ask for species allocation by flight mode:

```text
For the circling/perching-flight flocks, how many should be seagulls, doves, and crows? For the straight-flight flocks, how many should be seagulls, doves, and crows?
```

Accept natural-language answers such as "circling: 2 seagulls, 1 dove, 1 crow; straight: 3 seagulls, 3 doves, 2 crows" and map them to:

```python
circling_species_counts={"seagull": 2, "dove": 1, "crow": 1}
straight_species_counts={"seagull": 3, "dove": 3, "crow": 2}
```

If a species allocation sum is smaller than that flight-mode count, fill the missing templates by cycling `crow`, `dove`, `seagull`. If a species allocation sum is larger, clamp in `crow`, `dove`, `seagull` order to the requested flight-mode count and state the normalization.

Normalize invalid input conservatively:

- If `template_count` is omitted, use `circling_count + straight_count` when both are present; otherwise ask for it.
- If `circling_count + straight_count` is smaller than `template_count`, fill the remainder with straight-flight templates.
- If `circling_count + straight_count` is larger than `template_count`, keep the requested ratio and clamp to `template_count`.
- Keep counts as non-negative integers.

## Blender Workflow

1. Ensure the bundled blend asset exists at `assets/FlockGenerator_v1.0.blend`.
2. Use `scripts/create_flock_scene.py` inside Blender, or copy its logic into `mcp__blender.execute_blender_code` when working through Blender MCP.
3. Append the required datablocks from the bundled blend: collection `Birds`, node group `FlockGenerator`, and the six source curve templates.
4. Duplicate only flock curve objects into the destination scene. Keep bird body/wing meshes available but hide them in a support collection.
5. Create exactly `template_count` flock templates, with exactly `circling_count` using circle templates and exactly `straight_count` using straight templates after normalization.
6. Assign source template variants from the requested species allocations. Use the `seagull`, `dove`, and `crow` templates from the bundled blend, varying seed and numeric sockets slightly.
7. Place circling templates in a single row along the X axis. Place straight-flight templates in a separate lane along the Z axis. Keep the straight-flight lane offset on Y so the two motion families are easy to inspect independently.
8. Set viewport-friendly defaults: show generated flock objects, hide raw source templates/support birds, keep flight paths visible unless the user asks for final render cleanup.
9. Verify with a Blender scene inspection or viewport screenshot.

## Distilled Behavior

Read `references/template-parameters.md` for the source socket map and baseline values. Keep the original relationship between bird species and motion style:

- Crow: darker, compact groups; medium wing range; gliding enabled in the original templates.
- Dove: denser groups; higher flap speed and wider horizontal intensity; gliding disabled.
- Seagull: slower speed, wider spread, frequent gliding.

Apply slight variation to these sockets only unless the user asks for manual controls:

- `Random Seed`: replace with a unique integer per generated template.
- `Count`: vary by about +/-15%, minimum 1.
- `Flight Speed`: vary by about +/-10%.
- `Spread Paths`, `Vertical Waviness`, `Vertical Intensity`, `Horizontal Waviness`, `Horizontal Intensity`, `Outliers Range`: vary by about +/-10%.
- `Scale`, `Scale Variation`, `Flap Speed`, `Wing Range`, `Glide Frequency`: vary by about +/-8%.
- `Start Second`: keep `0.0` for straight templates and around `-10.0` for circling templates, with up to +/-2 seconds offset.
- `Body`, `Wing`, `Loop`, `Glide`, and bird species identity should stay consistent with the chosen source template.

## Script Usage

Run inside Blender Python:

```python
exec(open(r"C:\Users\...\.codex\skills\flock-generator\scripts\create_flock_scene.py", encoding="utf-8").read())
create_flock_scene(
    template_count=12,
    circling_count=4,
    straight_count=8,
    circling_species_counts={"seagull": 2, "dove": 1, "crow": 1},
    straight_species_counts={"seagull": 3, "dove": 3, "crow": 2},
)
```

When using Blender MCP, execute the same file contents or import it from the absolute skill path, then call `create_flock_scene(...)` with the requested counts.

Default layout parameters:

- `circling_spacing_x=65.0`: distance between circling flock modules on X.
- `straight_spacing_z=35.0`: distance between straight-flight flock modules on Z.
- `straight_lane_y=-80.0`: Y offset for the straight-flight lane.
