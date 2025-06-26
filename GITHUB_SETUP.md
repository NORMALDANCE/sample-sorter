# 🚀 Инструкции по загрузке на GitHub

## Шаги для публикации проекта на GitHub

### 1. Создание репозитория на GitHub

1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите кнопку "New" или "+" → "New repository"
3. Заполните форму:
   - **Repository name**: `sample-sorter`
   - **Description**: `Powerful audio sample sorting application with GUI by AENDY STUDIO`
   - **Visibility**: Public (или Private по вашему выбору)
   - **Initialize with**: НЕ ставьте галочки (у нас уже есть файлы)
4. Нажмите "Create repository"

### 2. Подключение локального репозитория к GitHub

```bash
# Добавьте удаленный репозиторий (замените YOUR_USERNAME на ваше имя пользователя)
git remote add origin https://github.com/YOUR_USERNAME/sample-sorter.git

# Переименуйте основную ветку в main (современный стандарт)
git branch -M main

# Отправьте код на GitHub
git push -u origin main
```

### 3. Настройка GitHub Pages (опционально)

Если хотите создать веб-страницу для проекта:

1. Перейдите в Settings → Pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: / (root)
5. Нажмите Save

### 4. Создание Release

1. Перейдите в Releases
2. Нажмите "Create a new release"
3. Заполните:
   - **Tag version**: `v1.0.0`
   - **Release title**: `Sample Sorter v1.0.0`
   - **Description**: Описание релиза
4. Нажмите "Publish release"

### 5. Настройка тегов и меток

Добавьте теги для лучшей организации:

- `python`
- `audio`
- `gui`
- `sample-sorter`
- `music-production`
- `vst`
- `daw`

### 6. Настройка профиля README

Создайте файл `README.md` в профиле для отображения проекта:

```markdown
# 👋 Привет, я AENDY STUDIO

## 🎵 Sample Sorter

Мощное приложение для автоматической сортировки аудиосэмплов с GUI.

[![Sample Sorter](https://img.shields.io/badge/Sample_Sorter-v1.0.0-blue.svg)](https://github.com/YOUR_USERNAME/sample-sorter)

### Возможности:
- 🎯 Автоматическая классификация сэмплов
- 📁 Структурированная библиотека
- 🔄 Восстановление смешанных файлов
- 💾 База данных для отслеживания

[Подробнее →](https://github.com/YOUR_USERNAME/sample-sorter)
```

## Полезные команды Git

```bash
# Проверить статус
git status

# Посмотреть историю коммитов
git log --oneline

# Создать новую ветку
git checkout -b feature/new-feature

# Переключиться на ветку
git checkout main

# Объединить ветки
git merge feature/new-feature

# Отправить изменения
git push origin main

# Получить изменения
git pull origin main
```

## Рекомендации

1. **Регулярно обновляйте код** - делайте коммиты при каждом значимом изменении
2. **Используйте понятные сообщения коммитов** - описывайте что именно изменилось
3. **Создавайте Issues** - для отслеживания багов и предложений
4. **Используйте Pull Requests** - для обсуждения изменений
5. **Добавьте скриншоты** - в README для лучшего понимания программы

## Контакты

- **GitHub**: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- **Email**: contact@aendystudio.com
- **Website**: https://aendystudio.com

---

**Удачи с публикацией проекта! 🎵** 