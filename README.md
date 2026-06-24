# blender鸟群生成skill

Codex skill for generating configurable Blender bird flocks with seagull, dove, and crow templates.

这是一个用于 Codex 的 Blender 鸟群生成 skill。它基于内置的 `FlockGenerator_v1.0.blend` 资产，在目标 Blender 文件中生成可配置的鸟群模板，包括盘旋/盘踞飞行和直飞两种飞行方式，并支持按鸟类分配海鸥、鸽子、乌鸦数量。

## 功能

- 生成指定总数的鸟群模板。
- 指定其中多少个为盘旋/盘踞飞行，多少个为直飞。
- 分别为盘旋/盘踞飞行和直飞指定鸟类数量：
  - 海鸥 / `seagull`
  - 鸽子 / `dove`
  - 乌鸦 / `crow`
- 盘旋/盘踞飞行鸟群沿 X 轴排开。
- 直飞鸟群沿 Z 轴排开，并放在独立 Y 轴车道，便于检查。
- 基于原始几何节点模板，对数量、速度、路径扰动、扑翼、滑翔等参数做轻微随机变化。

## 环境要求

使用这个 skill 的电脑需要具备：

- Codex，并支持本地 skills 目录。
- Blender，建议 Blender 5.0 或兼容版本。
- 能运行 Python / Blender Python。
- 如果通过 Codex 操作 Blender，建议配置好 Blender MCP 插件，或能用 Blender 后台命令执行 Python。
- Windows、macOS、Linux 均可使用，但脚本示例里的路径需要改成本机路径。

## 安装

把仓库里的 `flock-generator` 文件夹复制到 Codex skills 目录。

Windows 示例：

```text
C:\Users\你的用户名\.codex\skills\flock-generator
```

macOS / Linux 示例：

```text
~/.codex/skills/flock-generator
```

最终目录结构应类似：

```text
flock-generator/
├─ SKILL.md
├─ agents/
│  └─ openai.yaml
├─ assets/
│  └─ FlockGenerator_v1.0.blend
├─ references/
│  └─ template-parameters.md
└─ scripts/
   └─ create_flock_scene.py
```

## 调用时需要输入的数据

调用 `$flock-generator` 时，agent 会先询问：

```text
总鸟群模板数
盘旋/盘踞飞行数
直飞数
```

然后继续询问鸟类分配：

```text
盘旋/盘踞飞行鸟群：海鸥几个、鸽子几个、乌鸦几个？
直飞鸟群：海鸥几个、鸽子几个、乌鸦几个？
```

示例输入：

```text
总数 12，盘旋 4，直飞 8。
盘旋：海鸥 2，鸽子 1，乌鸦 1。
直飞：海鸥 3，鸽子 3，乌鸦 2。
```

对应脚本参数：

```python
create_flock_scene(
    template_count=12,
    circling_count=4,
    straight_count=8,
    circling_species_counts={"seagull": 2, "dove": 1, "crow": 1},
    straight_species_counts={"seagull": 3, "dove": 3, "crow": 2},
)
```

## 直接在 Blender Python 中使用

在 Blender Python 中执行：

```python
exec(open(r"C:\Users\你的用户名\.codex\skills\flock-generator\scripts\create_flock_scene.py", encoding="utf-8").read())

create_flock_scene(
    template_count=12,
    circling_count=4,
    straight_count=8,
    circling_species_counts={"seagull": 2, "dove": 1, "crow": 1},
    straight_species_counts={"seagull": 3, "dove": 3, "crow": 2},
)
```

## 文件说明

- `flock-generator/SKILL.md`：Codex skill 的主说明文件，定义触发场景、交互流程和使用规则。
- `flock-generator/assets/FlockGenerator_v1.0.blend`：运行时真正读取的 Blender 模板资产，包含鸟模型、曲线模板和 `FlockGenerator` 几何节点组。
- `flock-generator/scripts/create_flock_scene.py`：生成鸟群的 Blender Python 脚本。
- `flock-generator/references/template-parameters.md`：蒸馏出的节点 socket 和基线参数说明，主要给人和 Codex 阅读。
- `flock-generator/agents/openai.yaml`：Codex UI 元数据。

## 注意

- 运行时不依赖原始桌面路径里的 `FlockGenerator_v1.0（鸟群）.blend`，而是读取 skill 自带的 `assets/FlockGenerator_v1.0.blend`。
- 如果把这个 skill 分享给别人，需要包含整个 `flock-generator` 文件夹，尤其不能漏掉 `assets/FlockGenerator_v1.0.blend`。
- `.blend` 文件属于二进制资产，后续如果资产变大，建议为仓库启用 Git LFS。
