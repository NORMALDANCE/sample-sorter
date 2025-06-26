#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore and Sort - Программа для восстановления и сортировки смешанных файлов
Запуск: python run_restore.py
"""

import sys
import os

# Добавляем текущую папку в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from restore_and_sort import RestoreAndSortGUI
    print("🔄 Запуск Restore & Sort...")
    app = RestoreAndSortGUI()
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что все файлы находятся в одной папке:")
    print("- restore_and_sort.py")
    print("- config.py")
    print("- sort_library.py")
    print("- database_manager.py")
except Exception as e:
    print(f"❌ Ошибка запуска: {e}")
    input("Нажмите Enter для выхода...") 