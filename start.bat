@echo off
echo ========================================
echo    Sample Sorter - AENDY STUDIO
echo ========================================
echo.
echo Выберите программу для запуска:
echo.
echo 1. Sample Sorter (Основная программа)
echo 2. Restore & Sort (Восстановление и сортировка)
echo 3. Выход
echo.
set /p choice="Введите номер (1-3): "

if "%choice%"=="1" (
    echo.
    echo Запуск Sample Sorter...
    python run.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo Запуск Restore & Sort...
    python run_restore.py
    pause
) else if "%choice%"=="3" (
    echo Выход...
    exit
) else (
    echo Неверный выбор!
    pause
    goto :eof
) 