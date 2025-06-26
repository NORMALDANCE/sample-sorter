#!/bin/bash

echo "========================================"
echo "    Sample Sorter - AENDY STUDIO"
echo "========================================"
echo ""
echo "Выберите программу для запуска:"
echo ""
echo "1. Sample Sorter (Основная программа)"
echo "2. Restore & Sort (Восстановление и сортировка)"
echo "3. Выход"
echo ""
read -p "Введите номер (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Запуск Sample Sorter..."
        python3 run.py
        ;;
    2)
        echo ""
        echo "Запуск Restore & Sort..."
        python3 run_restore.py
        ;;
    3)
        echo "Выход..."
        exit 0
        ;;
    *)
        echo "Неверный выбор!"
        exit 1
        ;;
esac 