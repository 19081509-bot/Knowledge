#!/usr/bin/env python3
"""
Heartbeat 清洗脚本
由 OpenClaw heartbeat 触发，自动扫描 00_Inbox/ 并归档。
"""

import os, shutil, re, json
from datetime import datetime
from pathlib import Path

VAULT = Path("/Users/w/Documents/知识库")
INBOX = VAULT / "00_Inbox"
ARCHIVE_BASE = VAULT / "AI对话存档"
SCRIPT_DIR = VAULT / "_ai/scripts"
LOG_FILE = SCRIPT_DIR / "heartbeat-cleanup.log"

# 分类规则：关键词 → 目标目录
CLASSIFY_RULES = [
    (r"codex-relay|codex_relay|codexplus|Codex\+\+|codex-plus-plus", "codex-relay踩坑"),
    (r"Clash|clash|mihomo|代理|Verge", "Clash Verge配置排错"),
    (r"OpenClaw|openclaw|Gateway|gateway", "系统调试日志"),
    (r"跨Agent|记忆持久化|全局规则", "系统调试日志"),
]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def classify(content: str, filename: str) -> str:
    """根据内容关键词分类，返回目标子目录名"""
    for pattern, category in CLASSIFY_RULES:
        if re.search(pattern, content, re.IGNORECASE):
            return category
    # 默认：如果文件名或内容含"豆包" → 通用技术
    if "豆包" in filename or "doubao" in content.lower():
        return "通用技术记录"
    return "通用技术记录"

def clean_doubao_frontmatter(content: str) -> str:
    """清洗豆包剪藏的冗余前页"""
    lines = content.split("\n")
    # 如果已有标准 frontmatter，保留；如果是豆包剪藏格式，简化
    if content.startswith("---\n"):
        # 读取前页
        end_idx = content.find("---\n", 4)
        if end_idx > 0:
            front = content[4:end_idx].strip()
            # 提取可用的字段
            title = ""
            created = ""
            for line in front.split("\n"):
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"').strip("'")
                if line.startswith("created:"):
                    created = line.split(":", 1)[1].strip().strip('"').strip("'")
            
            # 生成新前页
            new_front = f"---\ndate: {created or datetime.now().strftime('%Y-%m-%d')}\ntags: [AI对话, 待分类]\n---\n"
            body = content[end_idx+4:].strip()
            return new_front + "\n\n" + body
    return content

def clean_webclipper_ads(content: str) -> str:
    """去除网页剪藏自带的广告/推广文字"""
    ad_patterns = [
        r"Seedance 2\.0.*?免费使用",
        r"豆包 是你的 AI 聊天.*?感兴趣的话题",
        r"https://link\.wtturl\.cn/\?target=.*?(?:\s|$)",
    ]
    for pat in ad_patterns:
        content = re.sub(pat, "", content)
    # 清理多余空行
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()

def process_file(filepath: Path) -> bool:
    """处理单个文件：清洗→分类→移动"""
    log(f"处理: {filepath.name}")
    
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    if not content.strip():
        log(f"  跳过空文件: {filepath.name}")
        return False
    
    # 1. 清洗
    cleaned = clean_doubao_frontmatter(content)
    cleaned = clean_webclipper_ads(cleaned)
    
    # 2. 分类
    category = classify(content, filepath.name)
    target_dir = ARCHIVE_BASE / category
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. 生成目标文件名（避免重名）
    target_path = target_dir / filepath.name
    if target_path.exists():
        stem = target_path.stem
        suffix = target_path.suffix
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
    
    # 4. 写入清洗后的内容
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    
    # 5. 删除原文件
    filepath.unlink()
    
    log(f"  → {target_path.relative_to(VAULT)}")
    return True

def update_memory_summary(processed: list):
    """在 _ai/MEMORY.md 末尾追加本次处理摘要"""
    if not processed:
        return
    
    summary_path = VAULT / "_ai/MEMORY.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    summary = f"\n> **Heartbeat 自动归档 ({ts})**：处理了 {len(processed)} 个文件\n"
    for f in processed:
        summary += f"> - {f}\n"
    
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(summary)
    
    log(f"已更新 MEMORY.md 摘要")

def git_sync():
    """Git 提交推送（带 rebase）"""
    import subprocess
    try:
        os.chdir(str(VAULT))
        # 1. add
        subprocess.run(["git", "add", "-A"], capture_output=True)
        
        # 2. commit
        ts = datetime.now().strftime("%Y-%m-%d-%H%M")
        result = subprocess.run(
            ["git", "commit", "-m", f"heartbeat: auto cleanup {ts}"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log(f"Git commit: {result.stdout.strip()}")
        else:
            log(f"Git commit (可能无变更): {result.stderr.strip()}")
        
        # 3. pull --rebase
        rebase = subprocess.run(
            ["git", "pull", "--rebase"],
            capture_output=True, text=True
        )
        if rebase.returncode != 0:
            log(f"Git pull --rebase 失败: {rebase.stderr.strip()}")
            # 如果有未暂存变更，stash 后重试
            stash = subprocess.run(["git", "stash"], capture_output=True, text=True)
            if stash.returncode == 0:
                log("已 stash 未暂存变更")
                rebase2 = subprocess.run(["git", "pull", "--rebase"], capture_output=True, text=True)
                if rebase2.returncode == 0:
                    log("Git pull --rebase: ✅ (stash 后)")
                    subprocess.run(["git", "stash", "pop"], capture_output=True, text=True)
                else:
                    log(f"Git pull --rebase 仍失败: {rebase2.stderr.strip()}")
                    subprocess.run(["git", "stash", "drop"], capture_output=True, text=True)
                    return
            else:
                return
        
        # 4. push
        push = subprocess.run(["git", "push"], capture_output=True, text=True)
        if push.returncode == 0:
            log("Git push: ✅")
        else:
            log(f"Git push: {push.stderr.strip()}")
    except Exception as e:
        log(f"Git sync error: {e}")

def main():
    log("=" * 40)
    log("Heartbeat 清洗开始")
    
    if not INBOX.exists():
        log(f"Inbox 目录不存在: {INBOX}")
        return
    
    files = sorted(INBOX.glob("*.md"))
    log(f"发现 {len(files)} 个待处理文件")
    
    processed = []
    for f in files:
        try:
            if process_file(f):
                processed.append(f.name)
        except Exception as e:
            log(f"  错误: {f.name} → {e}")
    
    if processed:
        update_memory_summary(processed)
        git_sync()
    else:
        log("无文件需要处理")
    
    log(f"Heartbeat 清洗完成，处理了 {len(processed)} 个文件")
    log("=" * 40)

if __name__ == "__main__":
    main()
