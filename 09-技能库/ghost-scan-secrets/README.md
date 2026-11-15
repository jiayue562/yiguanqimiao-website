# Ghost Secrets Scanner

AI-powered secrets and credentials scanner for codebases. Uses [poltergeist](https://github.com/ghostsecurity/poltergeist) for fast pattern matching with AI analysis to filter false positives.

## Usage

```
/ghost-scan-secrets [path-to-scan]
```

Examples:
```
/ghost-scan-secrets .                    # Scan current directory
/ghost-scan-secrets ./src                # Scan specific directory
/ghost-scan-secrets /path/to/repo        # Scan absolute path
```

## How It Works

1. **Initialize**: Downloads/verifies poltergeist binary
2. **Scan**: Runs poltergeist to detect secret candidates
3. **Analyze**: AI agents evaluate each candidate for:
   - Real secret vs placeholder/example
   - Hardcoded vs environment-loaded
   - Production code vs test code
   - Evidence of exposure
4. **Report**: Generates findings and summary report

## Prerequisites

The skill requires the `poltergeist` binary. It will be installed automatically via one of two methods:

### Option 1: GitHub Releases (default)

If the [poltergeist repository](https://github.com/ghostsecurity/poltergeist) is reachable, the binary is downloaded automatically from GitHub releases.

### Option 2: Local Fallback

If GitHub is unavailable (network issues, air-gapped environment), place release artifacts in the fallback directory:

| Platform | Fallback Directory |
|----------|-------------------|
| Linux/macOS | `~/.ghost/releases/latest/` |
| Windows | `%USERPROFILE%\.ghost\releases\latest\` |

Required files (for your platform):
```
~/.ghost/releases/latest/
├── poltergeist_linux_amd64.tar.gz
├── poltergeist_linux_arm64.tar.gz
├── poltergeist_darwin_amd64.tar.gz
├── poltergeist_darwin_arm64.tar.gz
└── poltergeist_windows_amd64.zip
```

You only need the file for your platform.

## Supported Platforms

- Linux (amd64, arm64)
- macOS (amd64, arm64)
- Windows (amd64) - via Git Bash, WSL, or MSYS2

## Output

Findings are written to `~/.ghost/repos/<repo_id>/scans/<short_sha>/secrets/`:
```
~/.ghost/repos/myrepo-a1b2c3d4/scans/abc1234/secrets/
├── scan-output.json      # Raw poltergeist output
├── candidates.json       # Parsed candidates
├── findings/             # Confirmed security risks
│   └── <finding-id>.md
└── report.md             # Summary report
```

## Secret Types Detected

Poltergeist includes 100+ built-in rules for common secrets:
- API keys (AWS, GCP, Azure, Anthropic, OpenAI, etc.)
- Database credentials (PostgreSQL, MySQL, MongoDB)
- Private keys and certificates
- OAuth tokens and JWTs
- Service-specific tokens (Stripe, Twilio, SendGrid, etc.)

See [poltergeist rules documentation](https://github.com/ghostsecurity/poltergeist/blob/main/docs/rules.md) for the full list.

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ghost-scan-secrets/agents/analyze/analyzer]] — Analyzer Agent
- [[09-技能库/ghost-scan-secrets/agents/analyze/template-finding]] — Secret Finding: <title>
- [[09-技能库/ghost-scan-secrets/agents/summarize/template-report]] — Secrets Scan Report
- [[09-技能库/resources_analyzer]] — Analyzer Agent
- [[09-技能库/resources_template-finding]] — Secret Finding: <title>
- [[09-技能库/resources_template-report]] — Secrets Scan Report
- [[ψ技能体系/10-kernel/龙心OS/capability-evolver/README]] — 🧬 Evolver
- [[ψ技能体系/30-tools/api-gateway/references/google-merchant/README]] — Google Merchant Routing Reference
- [[ψ技能体系/30-tools/cli-anything-hub/SKILL]] — CLI-Hub Meta-Skill

<!-- AI-LINKS-END -->
