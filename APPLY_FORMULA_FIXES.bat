@echo off
cd /d "%~dp0"
python apply_formula_fixes.py
if errorlevel 1 (
  echo.
  echo Could not patch all lecture files. Make sure this folder is the repository root.
  pause
  exit /b 1
)
echo.
echo Formula fixes applied successfully.
pause
