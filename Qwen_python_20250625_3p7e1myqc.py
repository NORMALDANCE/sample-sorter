import os
import tkinter as tk
from tkinter import filedialog, messagebox

class SampleSorterApp(tk.Tk):
    """Графический интерфейс для сортировки аудиосэмплов"""
    
    # Константы
    TITLE = "Universal Library Сортировщик"
    DEFAULT_SOURCE_PATH = "D:/Universal Library_old"
    SUPPORTED_EXTS = [".wav", ".mp3", ".flac"]
    
    # Ключевые слова для классификации
    CATEGORY_KEYWORDS = {
        "DRUMS": ["kick", "snare", "hihat", "crash", "perc", "rim"],
        "BASS": ["sub", "reese", "acid", "pluck", "wobble"],
        "LEADS": ["lead", "saw", "square", "arp", "sequence"],
        "PADS": ["ambient", "warm", "dark", "bright", "strings"],
        "FX": ["riser", "impact", "sweep", "reverse", "noise", "glitch"],
        "VOCALS": ["vocal", "chop", "phrase", "adlib", "hook", "acapella"]
    }
    
    def __init__(self):
        super().__init__()
        self.title(self.TITLE)
        self.geometry("400x300")
        
        # Переменные
        self.source_path = tk.StringVar(value=self.DEFAULT_SOURCE_PATH)
        self.target_path = "D:/Universal Library"  # Постоянная папка назначения
        
        # Основной контейнер
        container = tk.Frame(self)
        container.pack(padx=20, pady=20)
        
        # Исходная папка
        source_frame = tk.LabelFrame(container, text="Исходная папка:")
        source_frame.pack(pady=10)
        
        self.source_entry = tk.Entry(source_frame, textvariable=self.source_path, width=50)
        self.source_entry.pack(pady=5)
        
        select_btn = tk.Button(
            source_frame, 
            text="Выбрать папку", 
            command=self.select_source_folder
        )
        select_btn.pack(pady=5)
        
        # Дополнительные кнопки
        btn_frame = tk.Frame(container)
        btn_frame.pack(pady=10)
        
        clear_btn = tk.Button(
            btn_frame, 
            text="Очистить путь", 
            command=self.clear_path
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        sort_btn = tk.Button(
            btn_frame, 
            text="Начать сортировку", 
            command=self.start_sorting
        )
        sort_btn.pack(side=tk.LEFT, padx=5)
        
        # Статус
        self.status_label = tk.Label(container, text=" ", font=("Arial", 12))
        self.status_label.pack()
        
    def select_source_folder(self):
        """Выбрать исходную папку"""
        path = filedialog.askdirectory(title="Выберите исходную папку")
        if path:
            self.source_path.set(path)
    
    def clear_path(self):
        """Очистить поле исходной папки"""
        self.source_path.set("")
    
    def classify_sample(self, file_name: str) -> str:
        """Определить категорию файла"""
        file_name = file_name.lower()
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in file_name for keyword in keywords):
                return category
        
        return "OTHER"
    
    def start_sorting(self):
        """Запустить процесс сортировки"""
        source_folder = self.source_path.get()
        
        if not os.path.exists(source_folder):
            messagebox.showerror("Ошибка", "Исходная папка не существует!")
            return
        
        self.status_label.config(text="Сортировка в процессе...", fg="yellow")
        
        # Создаем структуру папок в целевой директории
        for category in set(self.CATEGORY_KEYWORDS.keys()):
            os.makedirs(os.path.join(self.target_path, category), exist_ok=True)
        
        # Обработка файлов
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        moved_files = 0
        
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            
            if file_ext in self.SUPPORTED_EXTS:
                category = self.classify_sample(file)
                target_dir = os.path.join(self.target_path, category)
                
                source_file = os.path.join(source_folder, file)
                target_file = os.path.join(target_dir, file)
                
                try:
                    os.rename(source_file, target_file)
                    moved_files += 1
                except FileExistsError:
                    pass  # Файл уже существует, игнорируем
        
        self.status_label.config(text=f"Перемещено файлов: {moved_files}", fg="green")
        messagebox.showinfo("Готово", f"Сортировка завершена! Перемещено {moved_files} файлов.")

# Запуск приложения
if __name__ == "__main__":
    app = SampleSorterApp()
    app.mainloop()