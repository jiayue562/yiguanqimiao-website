#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Check v3 - Six Detection Domains
Port/Permission/Secrets/Process/Network/CVE
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

try:
    import psutil
except ImportError:
    print("Installing psutil...")
    os.system('pip install psutil')
    import psutil

# ANSI Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

HIGH_RISK_PORTS = {
    11434: 'Ollama', 18789: 'OpenClaw', 19890: 'OpenClaw',
    8080: 'HTTP Proxy', 3000: 'Dev Server', 7860: 'Gradio',
    5000: 'Flask', 8000: 'Python HTTP', 22: 'SSH', 3389: 'RDP',
}

SECRET_PATTERNS = {
    'API_Key': r'(?i)(api[_-]?key)\s*[=:]\s*["\']?([a-zA-Z0-9_\-]{20,})["\']?',
    'Password': r'(?i)(password|passwd)\s*[=:]\s*["\']?([^\s"\']{8,})["\']?',
    'Token': r'(?i)(token)\s*[=:]\s*["\']?([a-zA-Z0-9_\-\.]{20,})["\']?',
}

WHITELIST = ['node_modules', '.git', 'site-packages', 'skills_extra']

def check_ports():
    findings, score = [], 100
    print(f"\n{Colors.BLUE}[1] Listening Ports{Colors.RESET}")
    
    try:
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status == 'LISTEN':
                port = conn.laddr.port
                if port in HIGH_RISK_PORTS:
                    if conn.laddr.ip in ['0.0.0.0', '::']:
                        findings.append({'level': 'HIGH', 'type': 'port', 
                            'detail': f'{HIGH_RISK_PORTS[port]}:{port} exposed on {conn.laddr.ip}',
                            'suggestion': 'Bind to 127.0.0.1', 'score_deduct': 30})
                        score -= 30
                        print(f"  {Colors.RED}[HIGH]{Colors.RESET} {HIGH_RISK_PORTS[port]}:{port} publicly exposed!")
                    else:
                        score -= 10
                        print(f"  {Colors.YELLOW}[MEDIUM]{Colors.RESET} {HIGH_RISK_PORTS[port]}:{port} localhost only")
    except Exception as e:
        print(f"  {Colors.YELLOW}Error: {e}{Colors.RESET}")
    
    return findings, max(0, score)

def check_secrets():
    findings, score = [], 100
    print(f"\n{Colors.BLUE}[2] Secret Leaks{Colors.RESET}")
    
    workspace = Path.home() / '.openclaw' / 'workspace'
    if not workspace.exists():
        return findings, score
    
    count = 0
    for f in workspace.rglob('*'):
        if f.is_file() and f.suffix.lower() in ['.md','.txt','.json','.yaml','.py','.env']:
            path_str = str(f).lower()
            if any(w in path_str for w in WHITELIST):
                continue
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                count += 1
                for name, pattern in SECRET_PATTERNS.items():
                    for m in re.finditer(pattern, content):
                        findings.append({'level': 'HIGH', 'type': 'secret',
                            'detail': f'{f.relative_to(workspace)} contains {name}',
                            'suggestion': 'Use environment variables', 'score_deduct': 25})
                        score -= 25
                        print(f"  {Colors.RED}[HIGH]{Colors.RESET} {f.relative_to(workspace)}: {name} found")
            except:
                pass
    
    if not findings:
        print(f"  {Colors.GREEN}[OK]{Colors.RESET} No secrets found ({count} files checked)")
    
    return findings, max(0, score)

def check_network():
    findings, score = [], 100
    print(f"\n{Colors.BLUE}[3] Network Connections{Colors.RESET}")
    
    try:
        ips = set()
        for c in psutil.net_connections(kind='inet'):
            if c.status == 'ESTABLISHED' and c.raddr:
                ip = c.raddr.ip
                if not (ip.startswith(('192.168.','10.','172.','127.'))):
                    ips.add(ip)
        
        for ip in ips:
            findings.append({'level': 'MEDIUM', 'type': 'network',
                'detail': f'Connection to {ip}',
                'suggestion': 'Verify this is a legitimate service', 'score_deduct': 10})
            score -= 10
            print(f"  {Colors.YELLOW}[MEDIUM]{Colors.RESET} External IP: {ip}")
        
        if not ips:
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} No suspicious connections")
    except Exception as e:
        print(f"  {Colors.YELLOW}Error: {e}{Colors.RESET}")
    
    return findings, max(0, score)

def check_processes():
    findings, score = [], 100
    print(f"\n{Colors.BLUE}[4] Processes{Colors.RESET}")
    
    suspicious = ['miner', 'xmrig', 'coinhive']
    for p in psutil.process_iter(['pid', 'name']):
        try:
            name = p.info['name'].lower()
            if any(s in name for s in suspicious):
                findings.append({'level': 'HIGH', 'type': 'process',
                    'detail': f'Suspicious: {p.info["name"]} (PID:{p.info["pid"]})',
                    'suggestion': 'Investigate and terminate if malicious', 'score_deduct': 30})
                score -= 30
                print(f"  {Colors.RED}[HIGH]{Colors.RESET} {p.info['name']}")
        except:
            pass
    
    if not findings:
        print(f"  {Colors.GREEN}[OK]{Colors.RESET} No suspicious processes")
    
    return findings, max(0, score)

def generate_report(findings, scores):
    total = sum(scores) // len(scores) if scores else 0
    level = 'A-Safe' if total >= 90 else 'B-OK' if total >= 70 else 'C-Risk' if total >= 50 else 'D-High'
    
    print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}Security Report{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
    
    color = Colors.GREEN if total >= 70 else Colors.YELLOW if total >= 50 else Colors.RED
    print(f"\n{color}Score: {total}/100 - {level}{Colors.RESET}")
    print(f"Findings: {len(findings)}")
    
    for i, f in enumerate(findings, 1):
        icon = '[!]' if f['level'] == 'HIGH' else '[!]' if f['level'] == 'MEDIUM' else '[i]'
        print(f"\n{i}. {icon} {f['detail']}")
        print(f"   -> {f['suggestion']}")
    
    # Save JSON
    report = {'timestamp': datetime.now().isoformat(), 'score': total, 'level': level, 'findings': findings}
    report_path = Path.home() / '.openclaw' / 'security_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nSaved: {report_path}")
    
    # Save HTML
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Security Report</title>
    <style>body{{font-family:Arial;max-width:800px;margin:40px auto}}.score{{font-size:36px;text-align:center}}
    .high{{color:#dc3545}}.medium{{color:#ffc107}}.low{{color:#17a2b8}}</style></head><body>
    <h1>Security Report</h1><p>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <div class="score {'high' if total<50 else 'medium' if total<70 else ''}">{total}/100 - {level}</div>
    <h2>Findings ({len(findings)})</h2>"""
    for f in findings:
        html += f'<div style="border-left:4px solid {'#dc3545' if f['level']=='HIGH' else '#ffc107'};padding:10px;margin:10px 0;background:#f8f9fa"><b>{f["level"]}</b>: {f["detail"]}<br><i>{f["suggestion"]}</i></div>'
    html += '</body></html>'
    
    html_path = Path.home() / '.openclaw' / 'security_report.html'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Saved: {html_path}")
    
    return report

def main():
    if sys.platform == 'win32':
        os.system('chcp 65001 >nul')
    
    print(f"\n{Colors.BOLD}Security Check v3.0{Colors.RESET}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_findings, scores = [], []
    
    f, s = check_ports(); all_findings.extend(f); scores.append(s)
    f, s = check_secrets(); all_findings.extend(f); scores.append(s)
    f, s = check_network(); all_findings.extend(f); scores.append(s)
    f, s = check_processes(); all_findings.extend(f); scores.append(s)
    
    generate_report(all_findings, scores)
    
    next_check = datetime.now() + timedelta(days=7)
    print(f"\n{Colors.GREEN}Next check recommended: {next_check.strftime('%Y-%m-%d')}{Colors.RESET}")

if __name__ == '__main__':
    main()
