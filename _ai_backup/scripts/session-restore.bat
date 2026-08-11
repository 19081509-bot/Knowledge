@echo off
chcp 65001 >nul
echo ===== Codex Session Context Restore =====
powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\Administrator\知识库\_ai\scripts\session-restore.ps1'"
pause
