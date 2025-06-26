import os
import tkinter as tk
from tkinter import filedialog

class SampleOrganizer:
    """Простой организатор аудиосэмплов"""
    
    # Поддерживаемые расширения аудиофайлов
    SUPPORTED_AUDIO_EXTS = [".wav", ".mp3", ".flac"]
    
    # Ключевые слова для классификации
    CATEGORY_KEYWORDS = {
        "DRUMS": {
            "kick": ["kick", "bd", "bassdrum", "808"],
            "snare": ["snare", "sd", "clap"],
            "hihat": ["hihat", "hh", "hat", "ch", "oh"],
            "crash": ["crash", "cymbal"],
            "perc": ["perc", "percussion", "shaker", "tambourine"],
            "rim": ["rim", "rimshot", "cross"]
        },
        "BASS": {
            "sub": ["sub", "subbass", "808"],
            "reese": ["reese", "dnb", "neuro"],
            "acid": ["acid", "tb303", "303"],
            "pluck": ["pluck", "bass pluck"],
            "wobble": ["wobble", "dubstep", "wub"]
        },
        "LEADS": {
            "pluck": ["pluck", "lead pluck"],
            "saw": ["saw", "sawtooth"],
            "square": ["square", "pulse"],
            "arp": ["arp", "arpeggio", "arpeggiated"],
            "sequence": ["seq", "sequence", "pattern"]
        },
        "PADS": {
            "ambient": ["ambient", "atmosphere", "atmos"],
            "warm": ["warm", "soft"],
            "dark": ["dark", "deep"],
            "bright": ["bright", "shiny"],
            "strings": ["strings", "str", "orchestral"]
        },
        "FX": {
            "riser": ["riser", "rise", "buildup"],
            "impact": ["impact", "hit", "stab"],
            "sweep": ["sweep", "swoosh"],
            "reverse": ["reverse", "rev"],
            "noise": ["noise", "white", "pink"],
            "glitch": ["glitch", "stutter", "chop"]
        },
        "VOCALS": {
            "chops": ["chop", "vocal chop", "slice"],
            "phrases": ["phrase", "vocal phrase"],
            "adlibs": ["adlib", "yeah", "hey"],
            "hooks": ["hook", "vocal hook", "chorus"],
            "acapella": ["acapella", "vocal only", "dry vocal"]
        }
    }
    
    @staticmethod
    def select_folder(title: str) -> str:
        """Открыть диалоговое окно для выбора папки"""
        root = tk.Tk()
        root.withdraw()  # Скрываем основное окно
        folder_path = filedialog.askdirectory(title=title)
        root.destroy()
        return folder_path
    
    @staticmethod
    def classify_sample(file_name: str) -> str:
        """Классифицировать файл по ключевым словам"""
        file_name = file_name.lower()
        
        for category, keywords in SampleOrganizer.CATEGORY_KEYWORDS.items():
            for subcategory, keyword_list in keywords.items():
                if any(keyword in file_name for keyword in keyword_list):
                    return category
        
        return "OTHER"
    
    @staticmethod
    def organize_samples(source_folder: str, target_folder: str):
        """Переместить аудиосэмплы из исходной папки в целевую"""
        if not os.path.exists(source_folder):
            print(f"[ERROR] Исходная папка не существует: {source_folder}")
            return
        
        os.makedirs(target_folder, exist_ok=True)
        
        # Получаем список файлов в исходной папке
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        
        moved_files = 0
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            
            # Проверяем, является ли файл поддерживаемым аудиофайлом
            if file_extension in SampleOrganizer.SUPPORTED_AUDIO_EXTS:
                category = SampleOrganizer.classify_sample(file)
                category_folder = os.path.join(target_folder, category)
                os.makedirs(category_folder, exist_ok=True)
                
                source_file_path = os.path.join(source_folder, file)
                target_file_path = os.path.join(category_folder, file)
                
                if os.path.exists(target_file_path):
                    print(f"[WARNING] Файл уже существует: {target_file_path}")
                else:
                    os.rename(source_file_path, target_file_path)
                    print(f"[INFO] Перемещен: {file} -> {category_folder}")
                    moved_files += 1
        
        print(f"[INFO] Перемещено файлов: {moved_files}")
        print("[INFO] Организация завершена!")

# Инициализация при запуске
if __name__ == "__main__":
    # Выбор исходной папки
    print("Выберите исходную папку с аудиосэмплами...")
    source_folder = SampleOrganizer.select_folder("Выберите исходную папку")
    if not source_folder:
        print("[ERROR] Исходная папка не выбрана.")
        exit()

    # Выбор папки назначения
    print("Выберите папку назначения...")
    target_folder = SampleOrganizer.select_folder("Выберите папку назначения")
    if not target_folder:
        print("[ERROR] Папка назначения не выбрана.")
        exit()

    # Организация файлов
    SampleOrganizer.organize_samples(source_folder, target_folder)