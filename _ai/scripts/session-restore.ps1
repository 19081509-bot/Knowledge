# Session Context Restore
$ctxPath = "C:\Users\Administrator\知识库\_ai\session-context.md"
if (-not (Test-Path $ctxPath)) {
    Write-Host "⚠️ session-context.md 未找到！"
    exit 1
}
$content = Get-Content $ctxPath -Raw -Encoding UTF8
Write-Host ""
Write-Host "====== 🧠 SESSION CONTEXT RESTORE ======"
Write-Host ""
if ($content -match '最后更新: (.+)') { Write-Host "📅 最后更新: $($matches[1])" }
if ($content -match '\*\*任务\*\*: (.+)') { Write-Host "📋 当前任务: $($matches[1])" }
Write-Host ""
Write-Host "📝 上次会话笔记:"
$nl = [Environment]::NewLine
$parts = $content -split "## 本次会话笔记"
if ($parts.Count -gt 1) {
    $end = $parts[1] -split "## " 
    Write-Host $end[0].Trim()
} else { Write-Host "  （无笔记记录）" }
Write-Host ""
Write-Host "📂 关键知识点:"
$parts = $content -split "## 关键知识点"
if ($parts.Count -gt 1) {
    $end = $parts[1] -split "## " 
    Write-Host $end[0].Trim()
} else { Write-Host "  （无知识点记录）" }
Write-Host ""
Write-Host "📌 待办事项:"
$parts = $content -split "## 待办"
if ($parts.Count -gt 1) {
    $end = $parts[1] -split "---" 
    Write-Host $end[0].Trim()
} else { Write-Host "  （无待办事项）" }
Write-Host ""
Write-Host "====== 文件路径 ======"
Write-Host $ctxPath
Write-Host "====== RECOVERY COMPLETE ======"
