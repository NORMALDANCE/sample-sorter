import os
import shutil
import re
from config import Config
from database_manager import DatabaseManager

class MediaLibrarySorter:
    def __init__(self, source, library, recursive=True, min_size=1):
        self.source = source
        self.library = library
        self.recursive = recursive
        self.min_size = min_size  # Минимальный размер файла в КБ
        self.db = DatabaseManager()
        self.processed_files = 0
        self.total_files = 0

    def sort_files(self, progress_callback=None):
        """Основной метод сортировки файлов"""
        try:
            # Подсчет общего количества файлов
            self.total_files = self.count_files()
            
            # Создание структуры библиотеки если не существует
            Config.create_library_structure(self.library)
            
            # Сканирование и сортировка файлов
            if self.recursive:
                for root, _, files in os.walk(self.source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.process_file(file_path, progress_callback)
            else:
                for file in os.listdir(self.source):
                    file_path = os.path.join(self.source, file)
                    if os.path.isfile(file_path):
                        self.process_file(file_path, progress_callback)
            
            return True
        except Exception as e:
            print(f"Ошибка сортировки: {e}")
            return False

    def count_files(self):
        """Подсчет общего количества файлов для обработки"""
        count = 0
        if self.recursive:
            for root, _, files in os.walk(self.source):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.is_valid_file(file_path):
                        count += 1
        else:
            for file in os.listdir(self.source):
                file_path = os.path.join(self.source, file)
                if os.path.isfile(file_path) and self.is_valid_file(file_path):
                    count += 1
        return count

    def process_file(self, file_path, progress_callback=None):
        """Обработка одного файла"""
        if not self.is_valid_file(file_path):
            return
        
        try:
            filename = os.path.basename(file_path)
            category, subcategory = self.determine_category(filename)
            
            if category:
                self.move_file(file_path, category, subcategory)
                self.processed_files += 1
                
                if progress_callback:
                    progress = (self.processed_files / self.total_files) * 100
                    progress_callback(progress, f"Обработан: {filename}")
            
        except Exception as e:
            print(f"Ошибка обработки файла {file_path}: {e}")

    def is_valid_file(self, file_path):
        """Проверка валидности файла"""
        if not os.path.isfile(file_path):
            return False
        
        # Проверка размера файла
        if os.path.getsize(file_path) < self.min_size * 1024:
            return False
        
        # Проверка расширения - поддерживаем все типы файлов
        ext = os.path.splitext(file_path)[1].lower()
        all_extensions = (
            Config.AUDIO_EXTENSIONS | 
            Config.VST_EXTENSIONS | 
            Config.PROJECT_EXTENSIONS | 
            Config.PRESET_EXTENSIONS | 
            Config.MIDI_EXTENSIONS | 
            Config.DOCUMENT_EXTENSIONS
        )
        return ext in all_extensions

    def determine_category(self, filename):
        """Определение категории и подкатегории файла"""
        filename_lower = filename.lower()
        ext = os.path.splitext(filename)[1].lower()
        
        # Сначала определяем по расширению
        extension_category = Config.get_category_by_extension(ext)
        
        # Если это аудиофайл, пытаемся определить подкатегорию по ключевым словам
        if extension_category == "AUDIO":
            # Проверяем каждую категорию
            for category, settings in Config.LIBRARY_STRUCTURE.items():
                if category in ["DUPLICATES", "UNCATEGORIZED", "VST_PLUGINS", "PROJECTS", "PRESETS", "MIDI", "DOCUMENTS"]:
                    continue
                    
                subfolders = settings.get("subfolders", [])
                for subfolder in subfolders:
                    keywords = Config.CATEGORY_KEYWORDS.get(category, {}).get(subfolder.lower(), [])
                    
                    # Проверяем ключевые слова
                    for keyword in keywords:
                        if keyword in filename_lower:
                            return category, subfolder
            
            # Если не найдена категория, проверяем общие ключевые слова
            for category, settings in Config.CATEGORY_KEYWORDS.items():
                if category in ["DUPLICATES", "UNCATEGORIZED", "VST_PLUGINS", "PROJECTS", "PRESETS", "MIDI", "DOCUMENTS"]:
                    continue
                    
                for subcategory, keywords in settings.items():
                    for keyword in keywords:
                        if keyword in filename_lower:
                            return category, subcategory
            
            # Если ничего не найдено, помещаем в UNCATEGORIZED
            return "UNCATEGORIZED", ""
        
        # Для VST плагинов определяем подкатегорию
        elif extension_category == "VST_PLUGINS":
            for subcategory, keywords in Config.CATEGORY_KEYWORDS.get("VST_PLUGINS", {}).items():
                for keyword in keywords:
                    if keyword in filename_lower:
                        return "VST_PLUGINS", subcategory.title()
            return "VST_PLUGINS", "Other"
        
        # Для проектов определяем подкатегорию
        elif extension_category == "PROJECTS":
            for subcategory, keywords in Config.CATEGORY_KEYWORDS.get("PROJECTS", {}).items():
                for keyword in keywords:
                    if keyword in filename_lower:
                        return "PROJECTS", subcategory.replace("_", " ").title()
            return "PROJECTS", "Other"
        
        # Для остальных типов файлов
        elif extension_category in ["PRESETS", "MIDI", "DOCUMENTS"]:
            return extension_category, ""
        
        # Если ничего не найдено, помещаем в UNCATEGORIZED
        return "UNCATEGORIZED", ""

    def move_file(self, file_path, category, subcategory=""):
        """Перемещение файла в соответствующую папку"""
        try:
            filename = os.path.basename(file_path)
            
            # Определяем путь назначения
            if subcategory:
                dst_folder = os.path.join(self.library, category, subcategory)
            else:
                dst_folder = os.path.join(self.library, category)
            
            # Создаем папку если не существует
            os.makedirs(dst_folder, exist_ok=True)
            
            # Путь назначения
            dst_path = os.path.join(dst_folder, filename)
            
            # Обработка дубликатов
            counter = 1
            original_dst_path = dst_path
            while os.path.exists(dst_path):
                name, ext = os.path.splitext(filename)
                dst_path = os.path.join(dst_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            # Перемещаем файл
            shutil.move(file_path, dst_path)
            
            # Логируем в базу данных
            self.db.log_file(filename, file_path, dst_path, f"{category}/{subcategory}" if subcategory else category)
            
            print(f"Перемещен: {filename} -> {category}/{subcategory}")
            
        except Exception as e:
            print(f"Ошибка перемещения файла {file_path}: {e}")
            # В случае ошибки перемещаем в папку дубликатов
            self.move_to_duplicates(file_path)

    def move_to_duplicates(self, file_path):
        """Перемещение файла в папку дубликатов"""
        try:
            filename = os.path.basename(file_path)
            duplicates_folder = os.path.join(self.library, "DUPLICATES")
            os.makedirs(duplicates_folder, exist_ok=True)
            
            dst_path = os.path.join(duplicates_folder, filename)
            
            # Обработка дубликатов в папке дубликатов
            counter = 1
            while os.path.exists(dst_path):
                name, ext = os.path.splitext(filename)
                dst_path = os.path.join(duplicates_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            shutil.move(file_path, dst_path)
            self.db.log_file(filename, file_path, dst_path, "DUPLICATES")
            
        except Exception as e:
            print(f"Ошибка перемещения в дубликаты: {e}")

    def get_statistics(self):
        """Получение статистики сортировки"""
        return {
            "processed": self.processed_files,
            "total": self.total_files,
            "success_rate": (self.processed_files / self.total_files * 100) if self.total_files > 0 else 0
        }