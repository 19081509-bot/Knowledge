# Session Memory Saver
param(
    [string]$TaskNote = '',
    [string]$KeyLearnings = ''
)

$homeDir = $env:USERPROFILE
$ctxPath = "$homeDir\知识库\_ai\session-context.md"
$backupDir = "$homeDir\知识库\_ai\session-backups"

if (-not (Test-Path $backupDir)) {
    New-Item $backupDir -ItemType Directory -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

if (Test-Path $ctxPath) {
    $bf = Join-Path $backupDir ("session-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".md")
    Copy-Item $ctxPath $bf -ErrorAction SilentlyContinue
}

$lines = @()
$lines += "# Session Context - 对话上下文持久化"
$lines += ""
$lines += "> 最后更新: " + $timestamp
$lines += "> 当前模型: DeepSeek V4"
$lines += ""
$lines += "## 本次会话笔记"
if ($TaskNote) { $lines += $TaskNote } else { $lines += "(无笔记)" }
$lines += ""
$lines += "## 关键知识点"
if ($KeyLearnings) { $lines += $KeyLearnings } else { $lines += "(无新增知识点)" }
$lines += ""
$lines += "## 待办"
$lines += "- [ ] 继续当前任务"
$lines += ""
$lines += "---"
$lines += "保存: session-save.ps1 | 恢复: session-restore.ps1"

$final = $lines -join [Environment]::NewLine
Set-Content -Path $ctxPath -Value $final -Encoding UTF8
Write-Host ("Saved to: " + $ctxPath)
