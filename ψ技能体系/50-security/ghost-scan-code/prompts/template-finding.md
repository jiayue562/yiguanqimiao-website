# Finding: <title>

## Metadata
- **ID**: <finding_id>
- **Project**: <project_id>
- **Project Type**: <project_type>
- **Agent**: <agent_name>
- **Vector**: <vector_name>
- **CWE**: <cwe_id>
- **Severity**: <high|medium|low>
- **Status**: unverified (always set this to unverified. the verifier will set this to verified or rejected)

## Location
- **File**: <relative/path/to/file>
- **Line**: <line_number>
- **Function**: <function_or_method_name>

## Description
<2-4 sentences describing the vulnerability>

## Vulnerable Code
```<language>
<the vulnerable code snippet, 5-15 lines>
```

## Remediation
<2-4 sentences with specific fix guidance>

## Fixed Code
```<language>
<the corrected code snippet>
```

## Validation Evidence
| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | <criterion text> | <evidence> |
| 2 | <criterion text> | <evidence> |

## Verification
- **Verdict**: <pending>
- **Reason**: <pending>
- **Verified By**: <pending>
- **Criteria Confirmed**: <pending>

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ghost-scan-code/prompts/template-finding]] — Finding: <title>
- [[09-技能库/ghost-scan-deps/agents/analyze/template-finding]] — SCA Finding: <vuln_id> in <package_name>
- [[09-技能库/ghost-scan-secrets/agents/analyze/template-finding]] — Secret Finding: <title>
- [[09-技能库/resources_template-finding]] — Secret Finding: <title>
- [[ψ技能体系/50-security/ghost-scan-deps/agents/analyze/template-finding]] — SCA Finding: <vuln_id> in <package_name>
- [[ψ技能体系/50-security/ghost-scan-secrets/agents/analyze/template-finding]] — Secret Finding: <title>

<!-- AI-LINKS-END -->
