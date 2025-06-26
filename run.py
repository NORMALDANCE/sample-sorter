#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Sorter - Программа для сортировки аудиосэмплов
Запуск: python run.py
"""

import sys
import os

# Добавляем текущую папку в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui_sorter import SampleSorterGUI
    print("🎵 Запуск Sample Sorter...")
    app = SampleSorterGUI()
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что все файлы находятся в одной папке:")
    print("- gui_sorter.py")
    print("- config.py")
    print("- sort_library.py")
    print("- database_manager.py")
except Exception as e:
    print(f"❌ Ошибка запуска: {e}")
    input("Нажмите Enter для выхода...") 