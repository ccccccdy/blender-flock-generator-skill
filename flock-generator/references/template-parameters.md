# Distilled FlockGenerator Template Parameters

Source asset: `assets/FlockGenerator_v1.0.blend`, distilled from the user-provided original blend asset.

## Source Objects

- Straight-flight templates: `flock_crows_curve`, `flock_doves_curve`, `flock_seagulls_curve`.
- Circling templates: `flock_crows_circle`, `flock_doves_circle`, `flock_seagulls_circle`.
- Bird meshes: `crow_01_body`, `crow_01_wing`, `dove_01_body`, `dove_01_wing`, `seagull_01_body`, `seagull_01_wing`.
- Node group: `FlockGenerator`.

## Geometry Node Socket Map

| Socket | Meaning |
|---|---|
| `Socket_25` | Count |
| `Socket_34` | Random Seed |
| `Socket_10` | Flight Speed |
| `Socket_14` | Start Second |
| `Socket_22` | Loop |
| `Socket_13` | Show Flight Paths |
| `Socket_15` | Spread Along Paths |
| `Socket_9` | Spread Paths |
| `Socket_18` | Vertical Waviness |
| `Socket_19` | Vertical Intensity |
| `Socket_20` | Horizontal Waviness |
| `Socket_21` | Horizontal Intensity |
| `Socket_28` | Outliers Percentage |
| `Socket_27` | Outliers Range |
| `Socket_31` | Path Resolution |
| `Socket_6` | Body object |
| `Socket_7` | Wing object |
| `Socket_29` | Scale |
| `Socket_30` | Scale Variation |
| `Socket_3` | Flap Speed |
| `Socket_26` | Wing Range |
| `Socket_32` | Wing Angle Offset |
| `Socket_23` | Glide |
| `Socket_5` | Glide Frequency |

## Baseline Values

| Template | Mode | Count | Seed | Speed | Start | Spread Paths | Vertical Waviness | Vertical Intensity | Horizontal Waviness | Horizontal Intensity | Outliers Range | Flap Speed | Wing Range | Wing Offset | Glide | Glide Frequency |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| `flock_crows_curve` | straight | 50 | 50 | 10.0 | 0.0 | 2.0 | 0.1 | 2.0 | 0.2 | 3.0 | 20.0 | 0.187 | 1.5 | 0.1 | true | 0.2 |
| `flock_crows_circle` | circle | 50 | 50 | 10.0 | -10.0 | 2.0 | 0.1 | 2.0 | 0.2 | 3.0 | 20.0 | 0.187 | 1.5 | 0.1 | true | 0.2 |
| `flock_doves_curve` | straight | 100 | 25 | 10.0 | 0.0 | 1.0 | 0.276 | 1.472 | 0.226 | 7.3 | 20.0 | 0.29 | 1.982 | 0.0 | false | 0.5 |
| `flock_doves_circle` | circle | 100 | 25 | 10.0 | -10.0 | 1.0 | 0.276 | 1.472 | 0.226 | 7.3 | 20.0 | 0.29 | 1.982 | 0.0 | false | 0.5 |
| `flock_seagulls_curve` | straight | 50 | 50 | 6.0 | 0.0 | 2.0 | 0.5 | 1.0 | 0.2 | 3.0 | 40.0 | 0.15 | 1.5 | 0.0 | true | 0.8 |
| `flock_seagulls_circle` | circle | 50 | 50 | 6.0 | -10.0 | 5.0 | 0.5 | 1.0 | 0.2 | 3.0 | 40.0 | 0.15 | 1.5 | 0.0 | true | 0.8 |

Shared baseline values: `Loop=true`, `Show Flight Paths=true`, `Spread Along Paths=3.0`, `Outliers Percentage=0.25`, `Path Resolution=1.0`, `Scale=1.0`, `Scale Variation=0.25`.
