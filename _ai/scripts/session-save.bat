@echo off
chcp 65001 >nul
echo ===== Codex Session Memory Saver =====
if not "%1"=="" set NOTE=%1
if not "%2"=="" set LEARN=%2
powershell -ExecutionPolicy Bypass -Command "& 'C:\Users\Administrator\知识库\_ai\scripts\session-save.ps1' -TaskNote '%NOTE%' -KeyLearnings '%LEARN%'"
pause
