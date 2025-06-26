import tkinter as tk
from tkinter import filedialog
import os

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)
        analyze_folder(folder_selected)

def analyze_folder(folder_path):
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Audios": [".mp3", ".wav"],
        "Videos": [".mp4", ".avi"],
        "Documents": [".pdf", ".docx", ".txt"],
        "Others": []
    }

    counts = {category: 0 for category in categories}

    for root_dir, _, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            matched = False
            for category, extensions in categories.items():
                if ext in extensions:
                    counts[category] += 1
                    matched = True
                    break
            if not matched:
                counts["Others"] += 1

    stats_label.config(
        text=f"Файлы: {sum(counts.values())}\n"
             f"Изображения: {counts['Images']}\n"
             f"Аудио: {counts['Audios']}\n"
             f"Видео: {counts['Videos']}\n"
             f"Документы: {counts['Documents']}\n"
             f"Другое: {counts['Others']}"
    )

# Основное окно
root = tk.Tk()
root.title("File Sorter")
root.geometry("600x400")

# Поле ввода пути
path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=10)

# Кнопка выбора папки
browse_button = tk.Button(root, text="Выбрать папку", command=browse_folder)
browse_button.pack(pady=5)

# Показ статистики
stats_label = tk.Label(root, text="Файлы: 0\nИзображения: 0\nАудио: 0\nВидео: 0\nДокументы: 0\nДругое: 0")
stats_label.pack(pady=20)

# Кнопка запуска сортировки
start_button = tk.Button(root, text="START", bg="orange", fg="white", width=15)
start_button.pack(pady=10)

# Запуск главного цикла
root.mainloop()