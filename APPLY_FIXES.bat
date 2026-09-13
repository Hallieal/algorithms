@echo off
py apply_site_fixes.py
if errorlevel 1 python apply_site_fixes.py
pause
