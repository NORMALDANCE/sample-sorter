import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.filedialog as filedialog
import os
import threading
from config import Config
from sort_library import MediaLibrarySorter
from database_manager import DatabaseManager

class SampleSorterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sample Sorter - AENDY STUDIO")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Настройка иконки
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Переменные
        self.source_path = tk.StringVar(value="D:/Downloads")
        self.library_path = tk.StringVar(value=Config.DEFAULT_LIBRARY_PATH)
        self.recursive = tk.BooleanVar(value=True)
        self.min_size = tk.IntVar(value=1)
        self.create_backup = tk.BooleanVar(value=True)
        
        # Создание интерфейса
        self.create_widgets()
        
        # Инициализация базы данных
        self.db = DatabaseManager()
        
        # Проверка и создание структуры библиотеки
        self.initialize_library()
        
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
        title_label = ttk.Label(main_frame, text="🎵 Sample Sorter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Секция путей
        path_frame = ttk.LabelFrame(main_frame, text="Пути", padding="10")
        path_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(1, weight=1)
        
        # Исходная папка
        ttk.Label(path_frame, text="Исходная папка:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(path_frame, textvariable=self.source_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(path_frame, text="Обзор", command=self.browse_source).grid(row=0, column=2)
        
        # Папка библиотеки
        ttk.Label(path_frame, text="Папка библиотеки:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        ttk.Entry(path_frame, textvariable=self.library_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(10, 0))
        ttk.Button(path_frame, text="Обзор", command=self.browse_library).grid(row=1, column=2, pady=(10, 0))
        
        # Секция настроек
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Чекбоксы
        ttk.Checkbutton(settings_frame, text="Рекурсивный поиск", variable=self.recursive).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(settings_frame, text="Создать резервную копию", variable=self.create_backup).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Минимальный размер
        ttk.Label(settings_frame, text="Мин. размер (KB):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        ttk.Entry(settings_frame, textvariable=self.min_size, width=10).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="🔄 Запустить сортировку", 
                  command=self.start_sorting).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📁 Создать структуру", 
                  command=self.create_structure).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📊 Показать статистику", 
                  command=self.show_statistics).pack(side=tk.LEFT)
        
        # Лог
        log_frame = ttk.LabelFrame(main_frame, text="Лог операций", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Прогресс бар
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Информация о разработчике в нижней части
        dev_label = ttk.Label(main_frame, text="AENDY STUDIO", 
                             font=("Arial", 10, "bold"), foreground="gray")
        dev_label.grid(row=6, column=0, columnspan=3, pady=(5, 0))

    def browse_source(self):
        path = filedialog.askdirectory(title="Выберите исходную папку")
        if path:
            self.source_path.set(path)
            self.log_message(f"Выбрана исходная папка: {path}")

    def browse_library(self):
        path = filedialog.askdirectory(title="Выберите папку библиотеки")
        if path:
            self.library_path.set(path)
            self.log_message(f"Выбрана папка библиотеки: {path}")

    def initialize_library(self):
        """Инициализация библиотеки"""
        try:
            if not os.path.exists(self.library_path.get()):
                self.create_structure()
            else:
                self.log_message("Библиотека уже существует")
        except Exception as e:
            self.log_message(f"Ошибка инициализации: {e}")

    def create_structure(self):
        """Создание структуры библиотеки"""
        try:
            Config.create_library_structure(self.library_path.get())
            self.log_message("✅ Структура библиотеки создана успешно")
            messagebox.showinfo("Успех", "Структура библиотеки создана!")
        except Exception as e:
            self.log_message(f"❌ Ошибка создания структуры: {e}")
            messagebox.showerror("Ошибка", f"Не удалось создать структуру: {e}")

    def start_sorting(self):
        """Запуск сортировки в отдельном потоке"""
        if not os.path.exists(self.source_path.get()):
            messagebox.showerror("Ошибка", "Исходная папка не существует!")
            return
            
        if not os.path.exists(self.library_path.get()):
            messagebox.showerror("Ошибка", "Папка библиотеки не существует!")
            return
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=self.sort_files_thread)
        thread.daemon = True
        thread.start()
        
        self.progress.start()

    def sort_files_thread(self):
        """Сортировка файлов в отдельном потоке"""
        try:
            self.log_message("🚀 Начинаем сортировку...")
            
            sorter = MediaLibrarySorter(
                source=self.source_path.get(),
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
                self.log_message(f"✅ Сортировка завершена!")
                self.log_message(f"📊 Обработано файлов: {stats['processed']} из {stats['total']}")
                self.log_message(f"📈 Успешность: {stats['success_rate']:.1f}%")
                
                self.root.after(0, lambda: messagebox.showinfo("Готово", 
                    f"Сортировка завершена успешно!\n\n"
                    f"Обработано файлов: {stats['processed']} из {stats['total']}\n"
                    f"Успешность: {stats['success_rate']:.1f}%"))
            else:
                self.log_message("❌ Ошибка при сортировке")
                self.root.after(0, lambda: messagebox.showerror("Ошибка", "Произошла ошибка при сортировке"))
            
        except Exception as e:
            self.log_message(f"❌ Ошибка сортировки: {e}")
            self.root.after(0, lambda: messagebox.showerror("Ошибка", f"Ошибка сортировки: {e}"))
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
    app = SampleSorterGUI() 