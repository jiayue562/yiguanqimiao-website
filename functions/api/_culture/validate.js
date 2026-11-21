/* _culture/validate.js — 输入校验：防注入、限长、词条 ID 白名单（统一注册表） */
import { ALLOWED_IDS } from "./registry.js";
const ALLOWED = new Set(ALLOWED_IDS);

export function validateInput(body) {
  if (!body || typeof body !== "object") return { ok: false, error: "bad_request" };
  if (body.schema !== "culture_check_v1") return { ok: false, error: "bad_schema" };
  const text = String(body.text || "").trim();
  if (text.length < 4) return { ok: false, error: "text_too_short" };
  if (text.length > 1500) return { ok: false, error: "text_too_long" };
  const exampleId = String(body.exampleId || "");
  if (!ALLOWED.has(exampleId)) return { ok: false, error: "bad_example" };
  // 去掉可能的提示注入控制字符
  const clean = text.replace(/[\u0000-\u001f\u007f]/g, " ").slice(0, 1500);
  return { ok: true, text: clean, exampleId };
}
