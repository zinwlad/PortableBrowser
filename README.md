# Portable Browser Bookmarks Manager

Удобный портативный менеджер закладок, построенный на PyQt5. Приложение позволяет управлять и организовывать закладки по категориям, предоставляя интуитивно понятный интерфейс для быстрого доступа к вашим любимым сайтам.

## Основные функции

- **Управление закладками:**
  - Добавление новых закладок в разные категории
  - Удаление закладок через контекстное меню
  - Открытие сайтов в текущем или новом окне браузера
  
- **Умный поиск:**
  - Мгновенный поиск по названиям закладок
  - Автоматическая фильтрация категорий при поиске
  - Быстрый доступ к поиску через Ctrl+F

- **Гибкий интерфейс:**
  - Сворачиваемые категории для экономии места
  - Система уведомлений об ошибках
  - Поддержка иконок для закладок
  - Сворачивание в системный трей

- **Настройка через конфигурацию:**
  - Настраиваемые размеры окна и кнопок
  - Возможность отключения сворачивания в трей
  - Гибкая настройка через config.json

## Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/your-username/portable-browser-bookmarks-manager.git
   cd portable-browser-bookmarks-manager
   ```

2. **Установите зависимости:**
   ```bash
   pip install PyQt5
   ```

## Использование

1. **Запуск приложения:**
   ```bash
   python main.py
   ```

2. **Горячие клавиши:**
   - `Ctrl+F` - фокус на поиске
   - `Esc` - свернуть окно в трей (если включено)

3. **Управление закладками:**
   - Левый клик - открыть сайт
   - Правый клик - контекстное меню с дополнительными действиями
   - Кнопка ▼/▶ - свернуть/развернуть категорию

## Структура проекта

- `main.py` - точка входа приложения, инициализация и обработка ошибок
- `bookmark_main_window.py` - основной класс окна и управление интерфейсом
- `sity_list.py` - хранение и управление закладками
- `config.json` - файл конфигурации с настройками приложения
- `browser.log` - лог-файл для отслеживания ошибок

## Конфигурация

Файл `config.json` позволяет настроить:
```json
{
    "window_width": 450,
    "window_height": 650,
    "min_width": 300,
    "min_height": 400,
    "max_width": 800,
    "max_height": 1200,
    "button_width": 150,
    "minimize_to_tray": true
}
```

## Логирование

Приложение ведет подробный лог в файле `browser.log`, который помогает отслеживать:
- Успешные операции с закладками
- Ошибки при открытии сайтов
- Проблемы с загрузкой иконок
- Другие важные события

## Требования

- Python 3.6+
- PyQt5
- Доступ к интернету для открытия закладок

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле LICENSE.
