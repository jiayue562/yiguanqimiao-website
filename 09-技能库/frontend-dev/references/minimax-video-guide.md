# Video Generation Guide

## CLI usage

```bash
# Basic
python scripts/minimax_video.py "A cat playing piano in a cozy room" -o cat.mp4

# With camera control
python scripts/minimax_video.py "Ocean waves crashing on rocks [Truck left]" -o waves.mp4

# 10 seconds, 1080P
python scripts/minimax_video.py "City skyline at sunset [Push in]" -o city.mp4 --duration 10 --resolution 1080P

# Disable prompt auto-optimization
python scripts/minimax_video.py "Exact prompt I want used" -o out.mp4 --no-optimize
```

## Programmatic usage

```python
from minimax_video import generate, create_task, poll_task, download_video

# Full pipeline (blocking)
generate("A cat playing piano", "cat.mp4", model="MiniMax-Hailuo-2.3", duration=6)

# Step by step
task_id = create_task("A cat playing piano")
file_id = poll_task(task_id, interval=10, max_wait=600)
download_video(file_id, "cat.mp4")
```

## Models

| Model | Resolution | Duration | Notes |
|-------|-----------|----------|-------|
| `MiniMax-Hailuo-2.3` | 768P, 1080P | 6s, 10s (768P only) | Latest, recommended |
| `MiniMax-Hailuo-02` | 768P, 1080P | 6s, 10s (768P only) | Previous gen |
| `T2V-01-Director` | 720P | 6s | Camera control optimized |
| `T2V-01` | 720P | 6s | Base model |

## Camera commands

Insert `[Command]` in prompt text to control camera movement:

| Command | Effect |
|---------|--------|
| `[Truck left]` | Camera moves left |
| `[Truck right]` | Camera moves right |
| `[Push in]` | Camera moves toward subject |
| `[Pull out]` | Camera moves away from subject |
| `[Pan left]` | Camera rotates left (fixed position) |
| `[Pan right]` | Camera rotates right (fixed position) |
| `[Tilt up]` | Camera tilts upward |
| `[Tilt down]` | Camera tilts downward |
| `[Pedestal up]` | Camera rises vertically |
| `[Pedestal down]` | Camera lowers vertically |
| `[Zoom in]` | Lens zooms in |
| `[Zoom out]` | Lens zooms out |
| `[Static shot]` | No camera movement |
| `[Tracking shot]` | Camera follows subject |
| `[Shake]` | Handheld shake effect |

Example: `"A runner sprints through a forest trail [Tracking shot]"`

## Pipeline

The script handles the full async flow:

1. **Create task** — `POST /v1/video_generation` → returns `task_id`
2. **Poll status** — `GET /v1/query/video_generation?task_id=xxx` → poll until `Success`
   - Status values: `Preparing` → `Queueing` → `Processing` → `Success` / `Fail`
3. **Download** — `GET /v1/files/retrieve?file_id=xxx` → get `download_url` (valid 1 hour) → save file

Typical generation time: 1–5 minutes depending on duration and resolution.

## Limits

- Prompt: max 2,000 characters
- 1080P: only supports 6s duration
- 10s duration: only available at 768P with Hailuo-2.3/02
- Download URL expires after 1 hour

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/frontend-dev/references/asset-prompt-guide]] — Prompt Engineering Guide
- [[09-技能库/frontend-dev/references/minimax-cli-reference]] — Provider Reference — MiniMax
- [[09-技能库/frontend-dev/references/minimax-image-guide]] — Image Generation Guide
- [[09-技能库/frontend-dev/references/minimax-music-guide]] — Music Generation Guide
- [[09-技能库/frontend-dev/references/minimax-tts-guide]] — TTS Guide
- [[ψ技能体系/30-tools/api-gateway/references/fal-ai/README]] — fal.ai Routing Reference
- [[ψ技能体系/30-tools/browser-use/references/cdp-python]] — Raw CDP & Python Session Reference

<!-- AI-LINKS-END -->
