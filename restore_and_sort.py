#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restore and Sort - Программа для восстановления и сортировки смешанных файлов
Запуск: python restore_and_sort.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.filedialog as filedialog
import os
import threading
import shutil
from datetime import datetime
from config import Config
from sort_library import MediaLibrarySorter
from database_manager import DatabaseManager

class RestoreAndSortGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restore & Sort - AENDY STUDIO")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Переменные
        self.mixed_folder = tk.StringVar(value="")
        self.library_path = tk.StringVar(value=Config.DEFAULT_LIBRARY_PATH)
        self.recursive = tk.BooleanVar(value=True)
        self.min_size = tk.IntVar(value=1)
        self.create_backup = tk.BooleanVar(value=True)
        self.auto_restore = tk.BooleanVar(value=True)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Инициализация базы данных
        self.db = DatabaseManager()
        
        self.root.mainloop()

    def create_widgets(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🔄 Restore & Sort - Восстановление и сортировка", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Секция папки с смешанными файлами
        mixed_frame = ttk.LabelFrame(main_frame, text="Папка с смешанными файлами", padding="10")
        mixed_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        mixed_frame.columnconfigure(1, weight=1)
        
        ttk.Label(mixed_frame, text="Папка с файлами:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(mixed_frame, textvariable=self.mixed_folder, width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(mixed_frame, text="Обзор", command=self.browse_mixed_folder).grid(row=0, column=2)
        
        # Секция путей
        path_frame = ttk.LabelFrame(main_frame, text="Пути", padding="10")
        path_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(1, weight=1)
        
        # Папка библиотеки
        ttk.Label(path_frame, text="Папка библиотеки:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(path_frame, textvariable=self.library_path, width=60).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(path_frame, text="Обзор", command=self.browse_library).grid(row=0, column=2)
        
        # Секция настроек
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Рекурсивный поиск", variable=self.recursive).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(settings_frame, text="Создать резервную копию", variable=self.create_backup).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        ttk.Checkbutton(settings_frame, text="Автоматическое восстановление", variable=self.auto_restore).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Минимальный размер
        ttk.Label(settings_frame, text="Мин. размер (KB):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(settings_frame, textvariable=self.min_size, width=10).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="🔍 Анализ файлов", 
                  command=self.analyze_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🔄 Сортировать", 
                  command=self.restore_and_sort).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📁 Создать структуру", 
                  command=self.create_structure).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📊 Статистика", 
                  command=self.show_statistics).pack(side=tk.LEFT)
        
        # Лог
        log_frame = ttk.LabelFrame(main_frame, text="Лог операций", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=100)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Прогресс бар
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Информация о разработчике в нижней части
        dev_label = ttk.Label(main_frame, text="AENDY STUDIO", 
                             font=("Arial", 10, "bold"), foreground="gray")
        dev_label.grid(row=7, column=0, columnspan=3, pady=(5, 0))

    def browse_mixed_folder(self):
        path = filedialog.askdirectory(title="Выберите папку с смешанными файлами")
        if path:
            self.mixed_folder.set(path)
            self.log_message(f"Выбрана папка с файлами: {path}")

    def browse_library(self):
        path = filedialog.askdirectory(title="Выберите папку библиотеки")
        if path:
            self.library_path.set(path)
            self.log_message(f"Выбрана папка библиотеки: {path}")

    def create_structure(self):
        """Создание структуры библиотеки"""
        try:
            Config.create_library_structure(self.library_path.get())
            self.log_message("✅ Структура библиотеки создана успешно")
            messagebox.showinfo("Успех", "Структура библиотеки создана!")
        except Exception as e:
            self.log_message(f"❌ Ошибка создания структуры: {e}")
            messagebox.showerror("Ошибка", f"Не удалось создать структуру: {e}")

    def analyze_files(self):
        """Анализ файлов в папке"""
        if not self.mixed_folder.get() or not os.path.exists(self.mixed_folder.get()):
            messagebox.showerror("Ошибка", "Выберите папку с файлами!")
            return
        
        thread = threading.Thread(target=self.analyze_files_thread)
        thread.daemon = True
        thread.start()
        self.progress.start()

    def analyze_files_thread(self):
        """Анализ файлов в отдельном потоке"""
        try:
            self.log_message("🔍 Начинаем анализ файлов...")
            
            file_stats = {
                'total': 0,
                'audio': 0,
                'vst': 0,
                'projects': 0,
                'presets': 0,
                'midi': 0,
                'documents': 0,
                'uncategorized': 0,
                'categories': {}
            }
            
            # Сканируем файлы
            for root, _, files in os.walk(self.mixed_folder.get()):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        file_stats['total'] += 1
                        
                        # Определяем тип файла
                        ext = os.path.splitext(file)[1].lower()
                        category = Config.get_category_by_extension(ext)
                        
                        if category == "AUDIO":
                            file_stats['audio'] += 1
                            # Определяем подкатегорию
                            subcategory = self.get_audio_subcategory(file)
                            if subcategory not in file_stats['categories']:
                                file_stats['categories'][subcategory] = 0
                            file_stats['categories'][subcategory] += 1
                        elif category == "VST_PLUGINS":
                            file_stats['vst'] += 1
                        elif category == "PROJECTS":
                            file_stats['projects'] += 1
                        elif category == "PRESETS":
                            file_stats['presets'] += 1
                        elif category == "MIDI":
                            file_stats['midi'] += 1
                        elif category == "DOCUMENTS":
                            file_stats['documents'] += 1
                        else:
                            file_stats['uncategorized'] += 1
            
            # Выводим статистику
            self.log_message(f"📊 Результаты анализа:")
            self.log_message(f"Всего файлов: {file_stats['total']}")
            self.log_message(f"Аудиофайлы: {file_stats['audio']}")
            self.log_message(f"VST плагины: {file_stats['vst']}")
            self.log_message(f"Проекты: {file_stats['projects']}")
            self.log_message(f"Пресеты: {file_stats['presets']}")
            self.log_message(f"MIDI: {file_stats['midi']}")
            self.log_message(f"Документы: {file_stats['documents']}")
            self.log_message(f"Неопределенные: {file_stats['uncategorized']}")
            
            if file_stats['categories']:
                self.log_message(f"\n🎵 Аудио по категориям:")
                for category, count in file_stats['categories'].items():
                    self.log_message(f"  {category}: {count}")
            
            self.root.after(0, lambda: messagebox.showinfo("Анализ завершен", 
                f"Найдено файлов: {file_stats['total']}\n"
                f"Аудио: {file_stats['audio']}\n"
                f"VST: {file_stats['vst']}\n"
                f"Проекты: {file_stats['projects']}"))
            
        except Exception as e:
            self.log_message(f"❌ Ошибка анализа: {e}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка анализа: {e}"))
        finally:
            self.root.after(0, self.progress.stop)

    def get_audio_subcategory(self, filename):
        """Определение подкатегории аудиофайла"""
        filename_lower = filename.lower()
        
        for category, settings in Config.CATEGORY_KEYWORDS.items():
            if category in ["DUPLICATES", "UNCATEGORIZED", "VST_PLUGINS", "PROJECTS", "PRESETS", "MIDI", "DOCUMENTS"]:
                continue
                
            for subcategory, keywords in settings.items():
                for keyword in keywords:
                    if keyword in filename_lower:
                        return f"{category}/{subcategory}"
        
        return "UNCATEGORIZED"

    def restore_and_sort(self):
        """Восстановление и сортировка файлов"""
        if not self.mixed_folder.get() or not os.path.exists(self.mixed_folder.get()):
            messagebox.showerror("Ошибка", "Выберите папку с файлами!")
            return
            
        if not os.path.exists(self.library_path.get()):
            messagebox.showerror("Ошибка", "Папка библиотеки не существует!")
            return
        
        thread = threading.Thread(target=self.restore_and_sort_thread)
        thread.daemon = True
        thread.start()
        self.progress.start()

    def restore_and_sort_thread(self):
        """Восстановление и сортировка в отдельном потоке"""
        try:
            self.log_message("🔄 Начинаем восстановление и сортировку...")
            
            # Создаем структуру библиотеки
            Config.create_library_structure(self.library_path.get())
            
            # Создаем резервную копию если нужно
            if self.create_backup.get():
                backup_path = os.path.join(self.library_path.get(), "BACKUP", datetime.now().strftime("%Y%m%d_%H%M%S"))
                os.makedirs(backup_path, exist_ok=True)
                self.log_message(f"📦 Создаем резервную копию в: {backup_path}")
            
            sorter = MediaLibrarySorter(
                source=self.mixed_folder.get(),
                library=self.library_path.get(),
                recursive=self.recursive.get(),
                min_size=self.min_size.get()
            )
            
            # Функция обратного вызова для прогресса
            def progress_callback(progress, message):
                self.root.after(0, lambda: self.log_message(f"{message} ({progress:.1f}%)"))
            
            # Запускаем сортировку
            success = sorter.sort_files(progress_callback)
            
            if success:
                stats = sorter.get_statistics()
                self.log_message(f"✅ Восстановление и сортировка завершены!")
                self.log_message(f"📊 Обработано файлов: {stats['processed']} из {stats['total']}")
                self.log_message(f"📈 Успешность: {stats['success_rate']:.1f}%")
                
                self.root.after(0, lambda: messagebox.showinfo("Готово", 
                    f"Восстановление и сортировка завершены!\n\n"
                    f"Обработано файлов: {stats['processed']} из {stats['total']}\n"
                    f"Успешность: {stats['success_rate']:.1f}%"))
            else:
                self.log_message("❌ Ошибка при восстановлении и сортировке")
                self.root.after(0, lambda: messagebox.showerror("Ошибка", "Произошла ошибка при восстановлении и сортировке"))
            
        except Exception as e:
            self.log_message(f"❌ Ошибка восстановления и сортировки: {e}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка восстановления и сортировки: {e}"))
        finally:
            self.root.after(0, self.progress.stop)

    def show_statistics(self):
        """Показать статистику"""
        try:
            stats = self.db.get_statistics()
            
            stats_text = f"📊 Статистика библиотеки:\n"
            stats_text += f"Всего файлов: {stats['total_files']}\n"
            
            # Конвертируем размер в читаемый формат
            total_size_mb = stats['total_size'] / (1024 * 1024)
            stats_text += f"Общий размер: {total_size_mb:.1f} MB\n\n"
            
            stats_text += "По категориям:\n"
            for category, count, size in stats['categories']:
                size_mb = size / (1024 * 1024) if size else 0
                stats_text += f"  {category}: {count} файлов ({size_mb:.1f} MB)\n"
            
            # Показываем последние файлы
            recent_files = self.db.get_recent_files(5)
            if recent_files:
                stats_text += f"\n🕒 Последние файлы:\n"
                for filename, category, timestamp in recent_files:
                    stats_text += f"  {filename} -> {category}\n"
            
            self.log_message(stats_text)
            
        except Exception as e:
            self.log_message(f"❌ Ошибка получения статистики: {e}")

    def log_message(self, message):
        """Добавление сообщения в лог"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

if __name__ == "__main__":
    app = RestoreAndSortGUI() 