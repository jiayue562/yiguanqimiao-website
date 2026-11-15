#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三向知识库同步脚本 (v6)
方向: WorkBuddy(OpcCla) → Obsidian → IMA
"""
import os, sys, json, time, shutil, urllib.request, urllib.error
from datetime import datetime, timezone

BASE = os.path.expanduser("~")
CONFIG_PATH = os.path.join(BASE, ".config", "qclaw", "sync.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"[-] Config not found: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def load_ima_creds():
    cid_file = os.path.join(BASE, ".config", "ima", "client_id")
    key_file = os.path.join(BASE, ".config", "ima", "api_key")
    if not os.path.exists(cid_file) or not os.path.exists(key_file):
        print("[-] IMA credentials not found")
        sys.exit(1)
    with open(cid_file, "r", encoding="utf-8-sig") as f:
        cid = f.read().strip()
    with open(key_file, "r", encoding="utf-8-sig") as f:
        key = f.read().strip()
    return cid, key

def ima_api(path, body, client_id, api_key, retries=5):
    url = f"https://ima.qq.com/{path}"
    for attempt in range(retries):
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={
            "ima-openapi-clientid": client_id,
            "ima-openapi-apikey": api_key,
            "Content-Type": "application/json"
        }, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if result.get("code") != 0:
                    msg = result.get("msg", "unknown")
                    targets = ["\u4e0a\u9650", "rate", "too many"]
                    if any(t in msg.lower() for t in targets):
                        if "\u660e\u5929" in msg:
                            print(f"  [DAILY QUOTA] \u4eca\u5929\u5df2\u7a77\u5c3d\uff0c\u8bf7\u660e\u5929\u518d\u8bd5")
                            return None
                        wait = 60 * (2 ** attempt)
                        print(f"  [RATE LIMITED] attempt {attempt+1}/{retries}, wait {wait}s...")
                        time.sleep(wait); continue
                    print(f"  [WARN] IMA API error: {msg}")
                    return None
                return result.get("data")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                wait = 60 * (2 ** attempt)
                print(f"  [403] attempt {attempt+1}/{retries}, wait {wait}s...")
                time.sleep(wait); continue
            print(f"  [ERROR] IMA API ({path[:30]}): {e}"); return None
        except Exception as e:
            print(f"  [ERROR] IMA API ({path[:30]}): {e}"); return None
    print(f"  [FAIL] IMA API ({path[:30]}): all retries exhausted")
    return None

def sync_wb_to_obsidian(cfg, dry_run):
    """WorkBuddy \u2192 Obsidian"""
    src = cfg["workbuddy_kb"]
    dst = os.path.join(cfg["obsidian_vault"], "00-WorkBuddy-Sync")
    print(f"\n=== WorkBuddy -> Obsidian ===")
    print(f"  Source: {src}")
    print(f"  Target: {dst}")
    if not os.path.exists(src):
        print(f"  [-] Source not found: {src}"); return
    if not os.path.exists(cfg["obsidian_vault"]):
        print(f"  [-] Obsidian vault not found: {cfg['obsidian_vault']}"); return
    count, skipped = 0, 0
    for root, dirs, files in os.walk(src):
        for file in files:
            if not file.endswith(".md"): continue
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, src)
            dst_file = os.path.join(dst, rel_path)
            if os.path.exists(dst_file):
                if os.path.getmtime(src_file) <= os.path.getmtime(dst_file) + 1:
                    skipped += 1; continue
            if dry_run:
                print(f"  [DRY] {rel_path}"); count += 1; continue
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file); count += 1
    print(f"  Result: {count} copied, {skipped} skipped\n")

def sync_obsidian_to_ima(cfg, client_id, api_key, dry_run, max_files=0):
    vault = cfg["obsidian_vault"]
    kb_name = cfg["ima"]["knowledge_base_name"]
    folder_id = cfg["ima"]["target_folder_id"]
    print(f"\n=== Obsidian -> IMA ===")
    print(f"  Vault: {vault}"); print(f"  KB: {kb_name}"); print(f"  Folder: {folder_id}")
    if not os.path.exists(vault):
        print(f"  [-] Vault not found: {vault}"); return

    # Get KB ID
    search = ima_api("openapi/wiki/v1/search_knowledge_base",
                     {"query": kb_name, "cursor": "", "limit": 10},
                     client_id, api_key)
    if not search or not search.get("info_list"):
        print(f"  [-] KB not found: {kb_name}"); return
    kb_id = search["info_list"][0]["kb_id"]
    print(f"  KB ID: {kb_id}")

    # Get existing MD files on IMA
    existing = {}
    cursor = ""
    while True:
        result = ima_api("openapi/wiki/v1/get_knowledge_list",
                        {"knowledge_base_id": kb_id, "cursor": cursor, "limit": 50},
                        client_id, api_key)
        if not result: break
        for item in result.get("item_list", []):
            if item.get("media_type") == 7:
                existing[item["title"]] = item
        if result.get("is_end", True): break
        cursor = result.get("next_cursor", "")
    print(f"  Existing MD files on IMA: {len(existing)}")

    # Dynamically discover directories (skip non-content dirs)
    skip_dirs = {"00-WorkBuddy-Sync", "09-技能库", "99-归档"}
    include_set = set()
    for d in os.listdir(vault):
        dpath = os.path.join(vault, d)
        if os.path.isdir(dpath) and not d.startswith(".") and d not in skip_dirs:
            include_set.add(d)

    md_files = []
    for root, dirs, files in os.walk(vault):
        rel_root = os.path.relpath(root, vault)
        parts = rel_root.split(os.sep)
        top_dir = parts[0] if parts else ""
        if top_dir not in include_set: continue
        for file in files:
            if file.endswith(".md") and not file.startswith("."):
                md_files.append(os.path.join(root, file))

    print(f"  Files to check: {len(md_files)}")
    if max_files > 0:
        md_files = md_files[:max_files]

    success, failed, skipped = 0, 0, 0
    total = len(md_files)
    last_pct = -1

    for idx, file_path in enumerate(md_files):
        pct = (idx + 1) * 100 // total if total > 0 else 100
        if pct // 5 > last_pct // 5:
            print(f"  Progress: {pct}% ({idx+1}/{total})"); last_pct = pct

        file_name = os.path.basename(file_path)
        if file_name in existing:
            obs_time = os.path.getmtime(file_path)
            ima_time = existing[file_name].get("modify_time", 0) / 1000
            if obs_time <= ima_time + 1: skipped += 1; continue

        if dry_run: success += 1; continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"    [SKIP] Read failed: {e}"); failed += 1; continue
        if not content.strip(): skipped += 1; continue

        # Step 1: Create media
        content_bytes = content.encode("utf-8")
        media = ima_api("openapi/wiki/v1/create_media", {
            "file_name": file_name, "file_size": len(content_bytes),
            "content_type": "text/markdown", "knowledge_base_id": kb_id, "file_ext": "md"
        }, client_id, api_key)
        if not media: failed += 1; continue

        cred = media["cos_credential"]

        # Step 2: Upload to COS via cos-upload.cjs (Tencent COS signing)
        cos_script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "..", "ima-skill", "knowledge-base", "scripts", "cos-upload.cjs")
        cos_script = os.path.normpath(cos_script)
        import subprocess
        r = subprocess.run([
            "node", cos_script,
            "--file", file_path,
            "--secret-id", cred.get("secret_id", ""),
            "--secret-key", cred.get("secret_key", ""),
            "--token", cred.get("token", ""),
            "--bucket", cred.get("bucket_name", ""),
            "--region", cred.get("region", ""),
            "--cos-key", cred.get("cos_key", ""),
            "--content-type", "text/markdown",
            "--start-time", str(cred.get("start_time", int(time.time()))),
            "--expired-time", str(cred.get("expired_time", int(time.time()) + 3600)),
        ], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            print(f"    [FAIL] COS upload: {r.stderr.strip() or r.stdout.strip()}"); failed += 1; continue

        # Step 3: Add knowledge
        add_result = ima_api("openapi/wiki/v1/add_knowledge", {
            "media_type": 7, "media_id": media["media_id"], "title": file_name,
            "knowledge_base_id": kb_id, "folder_id": folder_id,
            "file_info": {"cos_key": cred["cos_key"], "file_size": os.path.getsize(file_path), "file_name": file_name}
        }, client_id, api_key)
        if add_result: success += 1
        else: failed += 1
        time.sleep(1.5)

    print(f"  Result: {success} success, {skipped} skipped, {failed} failed\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Three-way knowledge sync")
    parser.add_argument("--direction", "-d", choices=["wb-to-obs", "obs-to-ima", "all"], default="all")
    parser.add_argument("--dry-run", "-n", action="store_true")
    parser.add_argument("--max-files", "-m", type=int, default=0, help="max files to sync (0=all)")
    args = parser.parse_args()
    cfg = load_config()
    cid, key = load_ima_creds()
    print("=" * 50)
    print(" Three-way Knowledge Sync")
    print(f" Direction: {args.direction}")
    if args.dry_run: print(" [DRY RUN] - no changes will be made")
    print("=" * 50)
    if args.direction in ("wb-to-obs", "all"): sync_wb_to_obsidian(cfg, args.dry_run)
    if args.direction in ("obs-to-ima", "all"):
        sync_obsidian_to_ima(cfg, cid, key, args.dry_run, args.max_files)
    print("Done!")

if __name__ == "__main__":
    main()
