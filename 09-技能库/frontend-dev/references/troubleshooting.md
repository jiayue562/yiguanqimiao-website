# Troubleshooting

## Quick reference

| Error | Cause | Fix |
|-------|-------|-----|
| `MINIMAX_API_KEY is not set` | Key not set | `export MINIMAX_API_KEY="key"` |
| `401 Unauthorized` | Invalid/expired key | Check key validity |
| `429 Too Many Requests` | Rate limit | Add delays between requests |
| `TimeoutError` | Network or long text | Use async TTS for long text, check network |
| `invalid params, method t2a-v2 not have model` | Wrong model name | Use `speech-2.8-hd` (hyphens, not underscores) |
| `brotli: decoder process called...` | Encoding issue | Already fixed in utils.py (Accept-Encoding header) |

## Environment

### API key not set

```bash
export MINIMAX_API_KEY="<paste-your-key-here>"

# Verify
echo $MINIMAX_API_KEY
```

### FFmpeg not found

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Verify
ffmpeg -version
```

### Missing Python packages

```bash
pip install requests
```

## API errors

### Authentication (401)

- Verify API key is correct and not expired
- Check for extra spaces in key value

### Rate limiting (429)

Add delays between requests:
```python
import time
for text in texts:
    result = tts(text)
    time.sleep(1)
```

### Invalid model name

Valid names (use hyphens, must include -hd or -turbo):
- `speech-2.8-hd` (recommended)
- `speech-2.8-turbo`
- `speech-2.6-hd`
- `speech-2.6-turbo`

Wrong: `speech_01`, `speech_2.6`, `speech-01`

## Audio issues

### Poor quality

Re-generate with higher settings:
```bash
python scripts/minimax_tts.py "text" -o out.mp3 --sample-rate 32000 --model speech-2.8-hd
```

### Invalid emotion

Valid emotions:
- All models: happy, sad, angry, fearful, disgusted, surprised, calm
- speech-2.6 only: + fluent, whisper
- speech-2.8: auto-matched (leave empty, recommended)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/PPT 演示文稿/references/pitfalls]] — QA Process & Common Pitfalls
- [[09-技能库/baidu-search/references/apikey-fetch]] — Baidu API Key Setup Guide (OpenClaw)
- [[09-技能库/frontend-dev/references/env-setup]] — Getting Started
- [[09-技能库/frontend-dev/references/minimax-cli-reference]] — Provider Reference — MiniMax
- [[09-技能库/frontend-dev/references/minimax-tts-guide]] — TTS Guide
- [[09-技能库/impeccable/references/harden]] — harden
- [[09-技能库/impeccable/references/ux-writing]] — UX Writing
- [[09-技能库/resources_TROUBLESHOOTING]] — Troubleshooting Guide
- [[09-技能库/web-search-plus/TROUBLESHOOTING]] — Troubleshooting Guide
- [[ψ技能体系/30-tools/api-gateway/references/fal-ai/README]] — fal.ai Routing Reference

<!-- AI-LINKS-END -->
