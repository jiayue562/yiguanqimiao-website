# ElevenLabs Routing Reference

**App name:** `elevenlabs`
**Base URL proxied:** `api.elevenlabs.io`

## API Path Pattern

```
/elevenlabs/v1/{resource}
```

## Common Endpoints

### Text-to-Speech

#### Convert Text to Speech
```bash
POST /elevenlabs/v1/text-to-speech/{voice_id}
```

#### Stream Text to Speech
```bash
POST /elevenlabs/v1/text-to-speech/{voice_id}/stream
```

### Voices

#### List Voices
```bash
GET /elevenlabs/v1/voices
```

#### Get Voice
```bash
GET /elevenlabs/v1/voices/{voice_id}
```

#### Create Voice Clone
```bash
POST /elevenlabs/v1/voices/add
```

#### Delete Voice
```bash
DELETE /elevenlabs/v1/voices/{voice_id}
```

### Models

#### List Models
```bash
GET /elevenlabs/v1/models
```

### User

#### Get User Info
```bash
GET /elevenlabs/v1/user
```

#### Get Subscription Info
```bash
GET /elevenlabs/v1/user/subscription
```

### History

#### List History
```bash
GET /elevenlabs/v1/history?page_size=100
```

#### Get Audio from History
```bash
GET /elevenlabs/v1/history/{history_item_id}/audio
```

### Sound Effects

#### Generate Sound Effect
```bash
POST /elevenlabs/v1/sound-generation
```

### Audio Isolation

#### Remove Background Noise
```bash
POST /elevenlabs/v1/audio-isolation
```

### Speech-to-Text

#### Transcribe Audio
```bash
POST /elevenlabs/v1/speech-to-text
```

### Speech-to-Speech

#### Convert Voice
```bash
POST /elevenlabs/v1/speech-to-speech/{voice_id}
```

## Notes

- Text-to-Speech returns audio/mpeg data
- Sound Effects returns audio/mpeg data
- Cursor-based pagination with `page_size` and `start_after_history_item_id`
- Response headers include `x-character-count` for usage tracking
- Models available: `eleven_multilingual_v2`, `eleven_turbo_v2_5`

## Resources

- [ElevenLabs API Documentation](https://elevenlabs.io/docs/api-reference)

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/30-tools/api-gateway/references/baserow/README]] — Baserow Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/calendly/README]] — Calendly Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/chargebee/README]] — Chargebee Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clickfunnels/README]] — ClickFunnels Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/clicksend/README]] — ClickSend Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/coda/README]] — Coda Routing Reference
- [[ψ技能体系/30-tools/api-gateway/references/fal-ai/README]] — fal.ai Routing Reference

<!-- AI-LINKS-END -->
