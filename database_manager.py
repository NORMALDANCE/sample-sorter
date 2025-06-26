import sqlite3
import os
from config import Config

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Используем путь из конфигурации
            db_dir = os.path.dirname(Config.DATABASE_PATH)
            os.makedirs(db_dir, exist_ok=True)
            db_path = Config.DATABASE_PATH
        
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sorted_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                source_path TEXT NOT NULL,
                destination_path TEXT NOT NULL,
                category TEXT NOT NULL,
                file_size INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создаем индекс для быстрого поиска
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_category ON sorted_files(category)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON sorted_files(timestamp)
        ''')
        
        self.conn.commit()

    def log_file(self, filename, src, dst, category):
        """Логирование перемещенного файла"""
        try:
            file_size = os.path.getsize(dst) if os.path.exists(dst) else 0
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO sorted_files (filename, source_path, destination_path, category, file_size)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, src, dst, category, file_size))
            self.conn.commit()
            
        except Exception as e:
            print(f"Ошибка логирования файла {filename}: {e}")

    def get_statistics(self):
        """Получение статистики"""
        cursor = self.conn.cursor()
        
        # Общее количество файлов
        cursor.execute("SELECT COUNT(*) FROM sorted_files")
        total_files = cursor.fetchone()[0]
        
        # Статистика по категориям
        cursor.execute("""
            SELECT category, COUNT(*) as count, SUM(file_size) as total_size 
            FROM sorted_files 
            GROUP BY category 
            ORDER BY count DESC
        """)
        categories = cursor.fetchall()
        
        # Общий размер
        cursor.execute("SELECT SUM(file_size) FROM sorted_files")
        total_size = cursor.fetchone()[0] or 0
        
        return {
            "total_files": total_files,
            "total_size": total_size,
            "categories": categories
        }

    def get_recent_files(self, limit=10):
        """Получение последних обработанных файлов"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT filename, category, timestamp 
            FROM sorted_files 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()

    def search_files(self, query):
        """Поиск файлов по имени"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT filename, category, destination_path, timestamp 
            FROM sorted_files 
            WHERE filename LIKE ? 
            ORDER BY timestamp DESC
        """, (f"%{query}%",))
        return cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.conn:
            self.conn.close()