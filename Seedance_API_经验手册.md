# Seedance API 经验手册

> 基于 2026.02.27 实战总结，含完整踩坑记录

---

## 1. 架构总览

```
素材准备 (nano-banana 生图)
    ↓
首帧确认 (人物+场景合成)
    ↓
seedance_video.py --chain --batch-size 1
    ↓
S01 首帧 → 生成视频 → 拿尾帧 → S02 首帧 → ... → S10
    ↓
ffmpeg concat → final_film.mp4
```

---

## 2. 认证与开通

### 认证方式

Ark 内容生成 API **不支持 AK/SK**，必须用 API Key：

```python
from volcenginesdkarkruntime import Ark
client = Ark(api_key="你的-api-key")
```

### 获取 API Key

火山方舟控制台 → API Key 管理 → 创建
https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

### 开通模型

拿到 key 后还需要单独开通模型，否则报 `ModelNotOpen`：

火山方舟控制台 → 模型广场 → 搜索 `seedance` → 逐个开通
https://console.volcengine.com/ark/region:ark+cn-beijing/model

---

## 3. 可用模型 (截至 2026.02)

| 模型 | Model ID | 核心能力 |
|------|----------|----------|
| **Seedance 1.5 Pro** | `doubao-seedance-1-5-pro-251215` | 文/图生视频 + **音频生成** + 首尾帧 + 草稿 |
| Seedance 1.0 Pro | `doubao-seedance-1-0-pro-250528` | 文/图生视频 + 首尾帧 |
| Seedance 1.0 Pro Fast | `doubao-seedance-1-0-pro-fast-251015` | 文/图生视频 + **参考图(1-4张)** |
| Seedance 1.0 Lite i2v | `doubao-seedance-1-0-lite-i2v-250428` | 图生视频(轻量) |
| Seedance 1.0 Lite t2v | `doubao-seedance-1-0-lite-t2v-250428` | 文生视频(轻量) |

**Seedance 2.0 暂不支持 API 调用**，仅控制台体验中心可用。

### 能力矩阵

| 能力 | 1.5 Pro | 1.0 Pro | 1.0 Fast | 1.0 Lite |
|------|---------|---------|----------|----------|
| 文生视频 | Y | Y | Y | t2v only |
| 图生视频(首帧) | Y | Y | Y | i2v only |
| 首尾帧控制 | Y | Y | Y | - |
| 音频生成 | **Y** | - | - | - |
| 草稿预览 | **Y** | - | - | - |
| 参考图(1-4) | - | - | **Y** | - |
| 返回末帧 | Y | Y | Y | - |
| 最大时长 | 12s | 12s | 12s | 12s |
| 分辨率 | 480p/720p/1080p | 同左 | 同左 | 同左 |

---

## 4. API 调用方式

### SDK 安装

```bash
pip install 'volcengine-python-sdk[ark]'
```

### 提交任务

```python
task = client.content_generation.tasks.create(
    model="doubao-seedance-1-5-pro-251215",
    content=[
        {"type": "text", "text": "你的提示词"},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/png;base64,..."},
            "role": "first_frame",   # first_frame / last_frame / reference_image
        },
    ],
    duration=12,            # 4-12 秒
    resolution="1080p",     # 480p / 720p / 1080p
    ratio="16:9",           # 16:9 / 4:3 / 1:1 / 3:4 / 9:16 / 21:9
    generate_audio=True,    # 仅 1.5 Pro
    return_last_frame=True, # 返回末帧用于续拍
    draft=False,            # 草稿模式, 仅 1.5 Pro, 强制 480p
    camera_fixed=False,     # 固定镜头
)
task_id = task.id
```

### 查询结果

```python
result = client.content_generation.tasks.get(task_id=task_id)
# result.status: "running" / "queued" / "succeeded" / "failed" / "cancelled"
# result.content.video_url: 视频下载地址
# result.content.last_frame_url: 末帧图片地址
# result.error.message: 失败原因
```

### content 数组中的 role 取值

| role | 用途 | 限制 |
|------|------|------|
| `first_frame` | 首帧图 | 1张 |
| `last_frame` | 尾帧图 | 1张, 需配合 first_frame |
| `reference_image` | 参考图 | 1-4张, 仅 1.0 Fast |

图片传递方式：`data:image/png;base64,{base64编码}`

---

## 5. 续拍链 (Chain Mode)

核心思路：每段视频的**尾帧**作为下一段的**首帧**，保证画面衔接。

```
S01(首帧图) → 视频 → 尾帧 → S02(首帧) → 视频 → 尾帧 → S03 ...
```

### 关键参数

- 所有镜头设 `return_last_frame=True`
- `--batch-size 1`（必须逐段串行，否则无法拿到上一段尾帧）
- 脚本自动下载尾帧 → 注入为下一段首帧

### 命令

```bash
python seedance_video.py --chain --batch-size 1
```

---

## 6. 首帧制作流程 (nano-banana)

### 步骤

1. **准备素材**：人物三视图 + 场景图 + 真人面部参考
2. **合成场景**：用 nano-banana 将人物放入场景，调整服饰/风化/氛围
3. **换脸**：用真人照片替换面部，保持一致性

### Prompt 经验

- **换脸时不要描述五官细节**，只说 "replace the face with the person from the second photo"，多余的外貌描述会干扰模型
- **发型要单独指定**：如果参考照是短发现代人，必须明确写 "long windswept black hair in ancient Chinese warrior topknot"
- **去眼镜**：写 "NO glasses"
- **风化效果**：用 "weathered, dust-stained, sun-bleached, torn hems" 而不是直接说 "dirty"

### 示例 prompt (合成场景帧)

```
Recreate the first image exactly — same composition, same desert ruins
background, same weathered white robes, same sword, same golden hour
lighting. Replace the face with the person from the second photo: same
facial structure, same eyes, same nose, same jawline, but NO glasses,
and with long windswept black hair partially tied in a loose ancient
Chinese warrior topknot. No text, no watermarks.
```

---

## 7. 视频 Prompt 经验

### 结构公式

```
[风格前缀] + [人物动作] + [镜头运动] + [音频提示(如开了generate_audio)]
```

### 风格前缀模板 (东邪西毒风)

```
1990s Hong Kong wuxia film directed by Wong Kar-wai,
shot on Eastmancolor film stock, anamorphic widescreen 2.35:1,
warm desaturated color palette of burnt sienna dusty gold and faded ochre,
heavy visible film grain and dust scratches,
golden hour desert lighting with atmospheric haze,
no text no subtitles no watermarks.
```

### 音频提示写法

当 `generate_audio=True` 时，在 prompt 末尾加音频描述：

- `"A melancholic erhu melody plays faintly"`
- `"Deep war drums begin, low and ominous"`
- `"Absolute silence except wind"`
- `"A weary male voice begins a quiet monologue in Chinese"`

### 打戏效果

**实测结论：Seedance 1.5 Pro 的打戏效果不佳**，复杂的多人交互动作（缠斗、兵器碰撞）容易出现：
- 人物肢体变形
- 动作不连贯
- 两人位置关系混乱

**建议**：打戏类镜头用较短时长(5-8s)，描述单一动作而非复杂编排，或等 Seedance 2.0 API 开放。

---

## 8. ffmpeg 拼接

### 直接拼接 (同编码参数)

```bash
# 生成文件列表
for f in S01.mp4 S02.mp4 ...; do echo "file '$f'" >> list.txt; done

# stream copy (快, 但各段编码参数需一致)
ffmpeg -y -f concat -safe 0 -i list.txt -c copy final.mp4
```

### 重编码拼接 (解决跳帧)

各段编码参数不一致时会跳帧/花屏，需重编码：

```bash
ffmpeg -y -f concat -safe 0 -i list.txt \
  -c:v libx264 -c:a aac -movflags +faststart \
  final.mp4
```

**实测经验**：Seedance 生成的各段 mp4 编码参数可能略有差异，`-c copy` 拼接后会有轻微跳帧。如果对质量有要求，建议用重编码模式。

---

## 9. 踩坑清单

| 坑 | 原因 | 解决 |
|----|------|------|
| `ak&sk authentication is currently not supported` | 内容生成 API 不支持 AK/SK | 改用 API Key: `Ark(api_key="...")` |
| `ModelNotOpen` | 账号未开通该模型 | 去方舟控制台模型广场开通 |
| 提交后长时间无响应 | 首帧图太大(>1MB), base64 上传慢 | 压缩图片到 1MB 以内 |
| 拼接后跳帧 | 各段编码参数不一致, `-c copy` 无法处理 | 改用 `-c:v libx264 -c:a aac` 重编码 |
| 打戏画面混乱 | 1.5 Pro 对复杂多人动作理解有限 | 简化动作描述, 缩短时长, 或等 2.0 |
| 人物一致性差 | 续拍链中间段可能偏移 | 确保首帧图质量高, prompt 中重复描述关键特征 |
| nano-banana 换脸时五官不像 | prompt 中写了多余的外貌描述 | 只说 "replace face with person from photo", 不描述五官 |
| 换脸后变成短发现代人 | 模型跟随参考照的发型 | 明确指定古装发型, 写 "NO glasses" |
| Seedance 2.0 | 暂不支持 API, 仅控制台体验 | 等官方开放, 关注文档更新 |

---

## 10. 完整工作流 Checklist

```
[ ] 1. 准备素材: 人物三视图 + 场景图 + 真人面部照
[ ] 2. nano-banana 合成: 人物融入场景 (风化/沧桑化)
[ ] 3. nano-banana 换脸: 真人面部 + 古装发型 + 去眼镜
[ ] 4. 确认首帧图效果
[ ] 5. 编写 SHOTS 列表 (prompt + 参数)
[ ] 6. 确认 API Key 有效 + 模型已开通
[ ] 7. 运行: python seedance_video.py --chain --batch-size 1
[ ] 8. 检查各段视频质量
[ ] 9. ffmpeg 重编码拼接: ffmpeg -y -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac final.mp4
[ ] 10. 后期: 调色/配乐/字幕 (DaVinci / 剪映)
```

---

## 11. 文件结构

```
jimeng-api/
├── seedance_video.py      # 主脚本 (Ark API)
├── jimeng_video.py         # 旧版脚本 (Visual API, 即梦3.0 Pro)
├── storyboard/             # 分镜图素材
├── output/
│   ├── S01.mp4 ~ S10.mp4  # 各段视频
│   ├── S01_last_frame.png  # 末帧 (续拍用)
│   ├── S01_video_url.txt   # 视频下载地址
│   └── final_film.mp4      # 拼接后完整影片
└── venv/                   # Python 虚拟环境
```

---

## 12. 关键命令速查

```bash
# 安装依赖
pip install 'volcengine-python-sdk[ark]'

# 生成全部 (续拍链)
python seedance_video.py --chain --batch-size 1

# 只生成某几段
python seedance_video.py --chain --batch-size 1 S01 S02 S03

# 草稿快速预览 (480p)
python seedance_video.py --chain --batch-size 1 --draft

# 手动重编码拼接 (解决跳帧)
ffmpeg -y -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac -movflags +faststart final.mp4
```
