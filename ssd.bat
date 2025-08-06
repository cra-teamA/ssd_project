@echo off
set PYTHONPATH=%~dp0
python %~dp0\core\ssd_controller.py %1 %2 %3
