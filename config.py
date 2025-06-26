import os
from typing import Set

class Config:
    """Конфигурация для работы с аудиосэмплами, VST и проектами"""
    
    # Основные пути
    DEFAULT_LIBRARY_PATH = "D:/Universal Library"
    DATABASE_PATH = os.path.join(DEFAULT_LIBRARY_PATH, "DATABASE", "library.db")
    LOG_FILE = os.path.join(DEFAULT_LIBRARY_PATH, "DATABASE", "sort_log.txt")
    
    # Структура библиотеки
    LIBRARY_STRUCTURE = {
        "DRUMS": {
            "subfolders": ["Kick", "Snare", "Hi-Hat", "Crash", "Ride", "Perc", "Clap", "Rim"],
        },
        "BASS": {
            "subfolders": ["Sub", "Reese", "Acid", "Pluck", "Wobble"],
        },
        "LEADS": {
            "subfolders": ["Pluck", "Saw", "Square", "Arp", "Sequence"],
        },
        "PADS": {
            "subfolders": ["Ambient", "Warm", "Dark", "Bright", "Strings"],
        },
        "FX": {
            "subfolders": ["Riser", "Impact", "Sweep", "Reverse", "Noise", "Glitch"],
        },
        "VOCALS": {
            "subfolders": ["Chops", "Phrases", "Adlibs", "Hooks", "Acapella"],
        },
        "LOOPS": {
            "subfolders": ["Melodic", "Drum", "Bass", "Ambient", "Percussion"],
        },
        "VST_PLUGINS": {
            "subfolders": ["Synths", "Effects", "Instruments", "Utilities"],
        },
        "PROJECTS": {
            "subfolders": ["FL_Studio", "Ableton", "Logic", "Cubase", "Reaper", "Other"],
        },
        "PRESETS": {
            "subfolders": ["Synth_Presets", "Effect_Presets", "Drum_Presets"],
        },
        "MIDI": {
            "subfolders": ["Melodies", "Basslines", "Drums", "Chords", "Arpeggios"],
        },
        "DOCUMENTS": {
            "subfolders": ["Manuals", "Tutorials", "Charts", "Notes"],
        },
        "DUPLICATES": {
            "subfolders": [],
        },
        "UNCATEGORIZED": {
            "subfolders": [],
        }
    }
    
    # Расширения файлов по категориям
    AUDIO_EXTENSIONS: Set[str] = {
        '.wav', '.mp3', '.flac', '.aiff', '.ogg', '.m4a', '.wma', '.aac'
    }
    
    VST_EXTENSIONS: Set[str] = {
        '.dll', '.vst', '.vst3', '.component', '.bundle'
    }
    
    PROJECT_EXTENSIONS: Set[str] = {
        '.flp', '.als', '.logicx', '.cpr', '.rpp', '.ptx', '.ptf', '.sesx', '.ses'
    }
    
    PRESET_EXTENSIONS: Set[str] = {
        '.fxp', '.fxb', '.vstpreset', '.preset', '.fst', '.nmsv', '.nmsn'
    }
    
    MIDI_EXTENSIONS: Set[str] = {
        '.mid', '.midi', '.rmi'
    }
    
    DOCUMENT_EXTENSIONS: Set[str] = {
        '.pdf', '.txt', '.doc', '.docx', '.rtf', '.html', '.htm'
    }
    
    # Ключевые слова для классификации
    CATEGORY_KEYWORDS = {
        "DRUMS": {
            "kick": ["kick", "bd", "bassdrum", "808", "bass drum"],
            "snare": ["snare", "sd", "clap", "snr"],
            "hihat": ["hihat", "hh", "hat", "ch", "oh", "hi-hat", "hi hat"],
            "crash": ["crash", "cymbal", "cym"],
            "perc": ["perc", "percussion", "shaker", "tambourine", "tamb", "shak"],
            "rim": ["rim", "rimshot", "cross", "rim shot"]
        },
        "BASS": {
            "sub": ["sub", "subbass", "808", "sub bass"],
            "reese": ["reese", "dnb", "neuro", "neurofunk"],
            "acid": ["acid", "tb303", "303", "acid bass"],
            "pluck": ["pluck", "bass pluck", "plucked"],
            "wobble": ["wobble", "dubstep", "wub", "wobble bass"]
        },
        "LEADS": {
            "pluck": ["pluck", "lead pluck", "plucked lead"],
            "saw": ["saw", "sawtooth", "saw wave"],
            "square": ["square", "pulse", "square wave"],
            "arp": ["arp", "arpeggio", "arpeggiated", "arpegiator"],
            "sequence": ["seq", "sequence", "pattern", "sequenced"]
        },
        "PADS": {
            "ambient": ["ambient", "atmosphere", "atmos", "atmospheric"],
            "warm": ["warm", "soft", "warmth"],
            "dark": ["dark", "deep", "darkness"],
            "bright": ["bright", "shiny", "brightness"],
            "strings": ["strings", "str", "orchestral", "string"]
        },
        "FX": {
            "riser": ["riser", "rise", "buildup", "build up"],
            "impact": ["impact", "hit", "stab", "impact hit"],
            "sweep": ["sweep", "swoosh", "sweep fx"],
            "reverse": ["reverse", "rev", "reversed"],
            "noise": ["noise", "white", "pink", "noise fx"],
            "glitch": ["glitch", "stutter", "chop", "glitch fx"]
        },
        "VOCALS": {
            "chops": ["chop", "vocal chop", "slice", "vocal slice"],
            "phrases": ["phrase", "vocal phrase", "vocal line"],
            "adlibs": ["adlib", "yeah", "hey", "ad lib"],
            "hooks": ["hook", "vocal hook", "chorus", "vocal chorus"],
            "acapella": ["acapella", "vocal only", "dry vocal", "a capella"]
        },
        "VST_PLUGINS": {
            "synths": ["synth", "synthesizer", "vst", "plugin", "instrument"],
            "effects": ["effect", "fx", "filter", "reverb", "delay"],
            "instruments": ["instrument", "piano", "guitar", "bass", "drums"],
            "utilities": ["utility", "meter", "analyzer", "tool"]
        },
        "PROJECTS": {
            "fl_studio": ["flp", "fl studio", "fruity loops"],
            "ableton": ["als", "ableton", "live"],
            "logic": ["logicx", "logic pro", "logic"],
            "cubase": ["cpr", "cubase"],
            "reaper": ["rpp", "reaper"],
            "other": ["project", "session", "song"]
        }
    }
    
    @staticmethod
    def get_category_by_extension(extension: str) -> str:
        """Определить категорию по расширению файла"""
        extension = extension.lower()
        
        if extension in Config.AUDIO_EXTENSIONS:
            return "AUDIO"
        elif extension in Config.VST_EXTENSIONS:
            return "VST_PLUGINS"
        elif extension in Config.PROJECT_EXTENSIONS:
            return "PROJECTS"
        elif extension in Config.PRESET_EXTENSIONS:
            return "PRESETS"
        elif extension in Config.MIDI_EXTENSIONS:
            return "MIDI"
        elif extension in Config.DOCUMENT_EXTENSIONS:
            return "DOCUMENTS"
        else:
            return "UNCATEGORIZED"
    
    @staticmethod
    def create_library_structure(base_path: str):
        """Создать структуру библиотеки"""
        try:
            for category, settings in Config.LIBRARY_STRUCTURE.items():
                category_path = os.path.join(base_path, category)
                os.makedirs(category_path, exist_ok=True)
                
                # Создаем подпапки
                for subfolder in settings.get("subfolders", []):
                    subfolder_path = os.path.join(category_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
            
            # Создаем папку DATABASE
            database_path = os.path.join(base_path, "DATABASE")
            os.makedirs(database_path, exist_ok=True)
            
            print(f"[INFO] Создана структура библиотеки в {base_path}")
            return True
        except Exception as e:
            print(f"[ERROR] Не удалось создать структуру библиотеки: {e}")
            return False
    
    @staticmethod
    def validate_paths():
        """Проверка существования необходимых путей"""
        paths_to_check = [
            Config.DEFAULT_LIBRARY_PATH,
            os.path.dirname(Config.DATABASE_PATH),
            os.path.dirname(Config.LOG_FILE)
        ]
        
        for path in paths_to_check:
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                    print(f"[INFO] Создана папка: {path}")
                except Exception as e:
                    print(f"[ERROR] Не удалось создать папку {path}: {e}")
                    return False
        
        return True

# Инициализация при импорте
if __name__ == "__main__":
    # Проверяем и создаем структуру
    Config.validate_paths()
    Config.create_library_structure(Config.DEFAULT_LIBRARY_PATH)
    print("Конфигурация инициализирована!")