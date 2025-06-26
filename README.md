# 🎵 Sample Sorter - Сортировщик аудиосэмплов

**AENDY STUDIO**

Мощное приложение для автоматической сортировки аудиосэмплов, VST плагинов, проектов и других файлов с удобным графическим интерфейсом.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://www.python.org/)

## 📋 Возможности

- 🎯 **Автоматическая классификация** сэмплов по названию файла
- 📁 **Структурированная библиотека** с подкатегориями
- 🔍 **Рекурсивный поиск** в подпапках
- 💾 **База данных** для отслеживания всех операций
- 📊 **Статистика** и история операций
- 🎨 **Современный GUI** с прогресс-баром
- 🔄 **Восстановление** смешанных файлов
- 🎵 **Поддержка** аудио, VST, проектов, пресетов, MIDI, документов

## 🗂️ Структура библиотеки

Программа создает следующую структуру папок:

```
D:/Universal Library/
├── DRUMS/
│   ├── Kick/
│   ├── Snare/
│   ├── Hi-Hat/
│   ├── Crash/
│   ├── Ride/
│   ├── Perc/
│   ├── Clap/
│   └── Rim/
├── BASS/
│   ├── Sub/
│   ├── Reese/
│   ├── Acid/
│   ├── Pluck/
│   └── Wobble/
├── LEADS/
│   ├── Pluck/
│   ├── Saw/
│   ├── Square/
│   ├── Arp/
│   └── Sequence/
├── PADS/
│   ├── Ambient/
│   ├── Warm/
│   ├── Dark/
│   ├── Bright/
│   └── Strings/
├── FX/
│   ├── Riser/
│   ├── Impact/
│   ├── Sweep/
│   ├── Reverse/
│   ├── Noise/
│   └── Glitch/
├── VOCALS/
│   ├── Chops/
│   ├── Phrases/
│   ├── Adlibs/
│   ├── Hooks/
│   └── Acapella/
├── LOOPS/
│   ├── Melodic/
│   ├── Drum/
│   ├── Bass/
│   ├── Ambient/
│   └── Percussion/
├── VST_PLUGINS/
│   ├── Synths/
│   ├── Effects/
│   ├── Instruments/
│   └── Utilities/
├── PROJECTS/
│   ├── FL_Studio/
│   ├── Ableton/
│   ├── Logic/
│   ├── Cubase/
│   ├── Reaper/
│   └── Other/
├── PRESETS/
├── MIDI/
├── DOCUMENTS/
├── DUPLICATES/
├── UNCATEGORIZED/
└── DATABASE/
    ├── library.db
    └── sort_log.txt
```

## 🚀 Установка и запуск

### Требования
- Python 3.7+
- tkinter (обычно входит в Python)

### Быстрая установка

#### Windows
```bash
# Скачайте и распакуйте архив
# Запустите start.bat или выполните:
python run.py
```

#### Linux/macOS
```bash
# Сделайте скрипт исполняемым
chmod +x start.sh

# Запустите
./start.sh

# Или напрямую:
python3 run.py
```

### Установка через pip
```bash
pip install sample-sorter
sample-sorter
```

## �� Как использовать

### Основная программа (Sample Sorter)
1. **Запустите программу** - откроется главное окно
2. **Выберите исходную папку** - папка с сэмплами для сортировки
3. **Выберите папку библиотеки** - куда будут перемещены отсортированные файлы
4. **Настройте параметры**:
   - ✅ Рекурсивный поиск - искать в подпапках
   - ✅ Создать резервную копию - создать копию перед перемещением
   - Мин. размер (KB) - минимальный размер файла для обработки
5. **Нажмите "Запустить сортировку"**
6. **Следите за прогрессом** в логе операций

### Восстановление и сортировка (Restore & Sort)
1. **Запустите Restore & Sort**
2. **Выберите папку с смешанными файлами**
3. **Выберите папку библиотеки**
4. **Нажмите "Анализ файлов"** для предварительного анализа
5. **Нажмите "Сортировать"** для восстановления и сортировки

## 🎯 Классификация файлов

### Аудиосэмплы
Программа определяет категорию по ключевым словам в названии файла:

#### DRUMS (Ударные)
- **Kick**: kick, bd, bassdrum, 808, bass drum
- **Snare**: snare, sd, clap, snr
- **Hi-Hat**: hihat, hh, hat, ch, oh, hi-hat, hi hat
- **Crash**: crash, cymbal, cym
- **Perc**: perc, percussion, shaker, tambourine, tamb, shak
- **Rim**: rim, rimshot, cross, rim shot

#### BASS (Бас)
- **Sub**: sub, subbass, 808, sub bass
- **Reese**: reese, dnb, neuro, neurofunk
- **Acid**: acid, tb303, 303, acid bass
- **Pluck**: pluck, bass pluck, plucked
- **Wobble**: wobble, dubstep, wub, wobble bass

#### LEADS (Лиды)
- **Pluck**: pluck, lead pluck, plucked lead
- **Saw**: saw, sawtooth, saw wave
- **Square**: square, pulse, square wave
- **Arp**: arp, arpeggio, arpeggiated, arpegiator
- **Sequence**: seq, sequence, pattern, sequenced

#### PADS (Пэды)
- **Ambient**: ambient, atmosphere, atmos, atmospheric
- **Warm**: warm, soft, warmth
- **Dark**: dark, deep, darkness
- **Bright**: bright, shiny, brightness
- **Strings**: strings, str, orchestral, string

#### FX (Эффекты)
- **Riser**: riser, rise, buildup, build up
- **Impact**: impact, hit, stab, impact hit
- **Sweep**: sweep, swoosh, sweep fx
- **Reverse**: reverse, rev, reversed
- **Noise**: noise, white, pink, noise fx
- **Glitch**: glitch, stutter, chop, glitch fx

#### VOCALS (Вокал)
- **Chops**: chop, vocal chop, slice, vocal slice
- **Phrases**: phrase, vocal phrase, vocal line
- **Adlibs**: adlib, yeah, hey, ad lib
- **Hooks**: hook, vocal hook, chorus, vocal chorus
- **Acapella**: acapella, vocal only, dry vocal, a capella

### Другие типы файлов
- **VST плагины**: .dll, .vst, .vst3, .component, .bundle
- **Проекты**: .flp, .als, .logicx, .cpr, .rpp, .ptx, .ptf, .sesx, .ses
- **Пресеты**: .fxp, .fxb, .vstpreset, .preset, .fst, .nmsv, .nmsn
- **MIDI**: .mid, .midi, .rmi
- **Документы**: .pdf, .txt, .doc, .docx, .rtf, .html, .htm

## 📊 Поддерживаемые форматы

### Аудио
- **Lossless**: .wav, .flac, .aiff
- **Lossy**: .mp3, .ogg, .m4a, .wma, .aac

### VST плагины
- **Windows**: .dll, .vst, .vst3
- **macOS**: .component, .bundle

### Проекты DAW
- **FL Studio**: .flp
- **Ableton Live**: .als
- **Logic Pro**: .logicx
- **Cubase**: .cpr
- **Reaper**: .rpp
- **Pro Tools**: .ptx, .ptf
- **Adobe Audition**: .sesx, .ses

## 🔧 Настройка

Вы можете изменить настройки в файле `config.py`:
- Путь к библиотеке по умолчанию
- Структуру папок
- Ключевые слова для классификации
- Поддерживаемые форматы файлов

## 📈 Статистика

Программа ведет подробную статистику:
- Общее количество обработанных файлов
- Размер библиотеки
- Количество файлов по категориям
- История последних операций

## ⚠️ Важные замечания

1. **Резервное копирование** - рекомендуется создать резервную копию перед сортировкой
2. **Дубликаты** - файлы с одинаковыми именами автоматически переименовываются
3. **Безопасность** - программа не удаляет файлы, только перемещает их
4. **База данных** - все операции записываются в SQLite базу данных

## 🐛 Устранение неполадок

### Ошибка импорта модулей
Убедитесь, что все файлы находятся в одной папке:
- `gui_sorter.py`
- `restore_and_sort.py`
- `config.py`
- `sort_library.py`
- `database_manager.py`

### Ошибка доступа к файлам
- Проверьте права доступа к папкам
- Убедитесь, что файлы не используются другими программами

### Медленная работа
- Уменьшите количество файлов для обработки
- Отключите рекурсивный поиск для больших папок

## 🤝 Вклад в проект

Мы приветствуем вклады в развитие проекта! Если у вас есть идеи по улучшению:

1. Создайте fork репозитория
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📞 Поддержка

Если у вас возникли проблемы или есть предложения по улучшению:

- Создайте issue в репозитории проекта
- Опишите проблему подробно
- Приложите скриншоты если необходимо

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

---

**Sample Sorter** - сделайте вашу библиотеку сэмплов организованной! 🎵

**Разработано AENDY STUDIO** © 2025    
