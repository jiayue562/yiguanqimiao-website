# -*- coding: utf-8 -*-
import os, re, json
ROOT = r"D:\以观其妙书院知识库\以观其妙书院"
NAV = os.path.join(ROOT, "05-五行人格心理学", "00-入口")
NEW = ["00-总览图·一心三界五行九层.md","01-一心·体-入口.md","02-三界·相-入口.md",
       "03-五行·用-入口.md","04-九层·度-入口.md","05-象思维·法-入口.md","06-归位对账表.md",
       "07-应用出口·八大场景.md","08-系统元层·索引与配置.md","09-融合素材·心理学与哲学.md"]
allnames = set()
for dp, dn, fns in os.walk(ROOT):
    if "\\.git" in dp: continue
    for fn in fns:
        n, e = os.path.splitext(fn)
        allnames.add(n); allnames.add(n + e)
bad = {}; cnt = 0
for f in NEW:
    t = open(os.path.join(NAV, f), encoding="utf-8").read()
    cnt += len(re.findall(r"\[\[", t))
    for l in re.findall(r"\[\[([^\]]+)\]\]", t):
        tgt = l.split("|")[0].strip().replace("\\", "/").split("/")[-1]
        base = os.path.splitext(tgt)[0]
        if tgt not in allnames and base not in allnames:
            bad.setdefault(f, []).append(tgt)
c = open(os.path.join(NAV, "导航画布·五层架构.canvas"), encoding="utf-8").read()
cfile = [os.path.splitext(os.path.basename(x))[0] for x in re.findall(r'"(05-[^"]+)"', c)]
print("md wikilinks:", cnt, "| canvas file refs:", len(cfile))
print("unresolved:", json.dumps(bad, ensure_ascii=False))
print("canvas missing:", [x for x in cfile if x not in allnames])
total = md = 0
for dp, dn, fns in os.walk(os.path.join(ROOT, "05-五行人格心理学")):
    for fn in fns:
        total += 1; md += fn.endswith(".md")
print("05 files now:", total, "| md:", md)
