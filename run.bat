@echo off
chcp 65001 > nul
echo.
echo ======================================================
echo  Запускаем скрипт для сбора информации о системе...
echo ======================================================
echo.

python specs.py

echo.
echo ======================================================
echo  Готово! Информация сохранена в файле specs.txt
echo ======================================================
echo.
pause