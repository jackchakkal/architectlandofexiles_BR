@echo off
title Traducao PT-BR - Architect: Land of Exiles (remover)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" -Uninstall
if errorlevel 1 pause
