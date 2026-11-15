# Getting Started

## 1. Set API key

```bash
export MINIMAX_API_KEY="<paste-your-key-here>"
```

## 2. Install dependencies

```bash
pip install requests

# FFmpeg (optional, for audio post-processing)
# macOS:
brew install ffmpeg
# Ubuntu:
sudo apt install ffmpeg
```

## 3. Quick test

```bash
python scripts/minimax_tts.py "Hello world" -o test.mp3
```

If successful, you'll see `OK: xxxxx bytes -> test.mp3`.

## Next steps

- **Voice selection**: See [minimax-voice-catalog.md](minimax-voice-catalog.md)
- **TTS workflows**: See [minimax-tts-guide.md](minimax-tts-guide.md)
- **Troubleshooting**: See [troubleshooting.md](troubleshooting.md)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/Word 文档生成/references/troubleshooting]] — Troubleshooting Guide — Symptom-Driven
- [[09-技能库/baidu-search/references/apikey-fetch]] — Baidu API Key Setup Guide (OpenClaw)
- [[09-技能库/frontend-dev/references/minimax-cli-reference]] — Provider Reference — MiniMax
- [[09-技能库/frontend-dev/references/minimax-tts-guide]] — TTS Guide
- [[09-技能库/frontend-dev/references/minimax-voice-catalog]] — MiniMax Voice Catalog
- [[09-技能库/frontend-dev/references/troubleshooting]] — Troubleshooting

<!-- AI-LINKS-END -->
