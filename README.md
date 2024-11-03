# Weather&Movie Telegram Bot

Weather&Movie — это multy-tool Telegram бот, который предоставляет пользователям информацию о погоде в любом городе на сегодня или три дня вперед, рекомендует фильмы на основе выбранных типа и жанра, помогает найти описание фильма по его названию, напоминает о чем угодно в выбранное пользователем время, а также советует меню на ужин. Бот написан на Python версии 3.11.10 с использованием библиотеки aiogram 3.13 и использует SQLAlchemy для работы с базой данных SQLite в асинхронном режиме. Alembic применяется для управления миграциями базы данных, а Poetry — для управления зависимостями проекта.

## Установка

1. **Клонируйте репозиторий:**

   ```
   git clone https://github.com/yourusername/weather-movie-bot.git
   cd weather-movie_bot
   ```
2. **Установите Poetry (если он еще не установлен):**

```
Следуйте [официальной документации Poetry](https://python-poetry.org/docs/#installation) для установки.
```
3. **Установите зависимости проекта:**
```
poetry install
```
4. **Создайте файл конфигурации:**

Создайте файл `.env` в корневом каталоге проекта и добавьте следующие переменные окружения:
```
BOT__TOKEN=your bot token
BOT__ADMIN_ID=your admin id

WEATHER__URL=http://api.weatherapi.com/v1/forecast.json
WEATHER__TOKEN=your weatherapi token

MOVIE__URL=https://api.kinopoisk.dev/v1.4/movie/
MOVIE__TOKEN=your movieapi token

DB__URL=your sqlite db url
DB__ECHO=False

STORAGE__BASE=your redis url for main storage
STORAGE__THROTTLING=your redis url for throttling storage
```

5. **Настройте базу данных:**

Выполните миграции для создания структуры базы данных:
```
alembic init -t async alembic
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

## Запуск
Чтобы запустить бота, выполните следующую команду в корне проекта:
```
python main.py
```
## Использование
После запуска бота вы можете отправить команду /start, чтобы получить приветственное сообщение.

**В главном меню бота можно найти следующие команды:**
- Погода - для выбора варианта погоды: сегодня или на 3 дня вперед
- Фильмы - для выбора варианта поиска кино: случайный фильм или поиск фильма по названию
- Что на ужин - для подборки случайного меню
- Инструменты - для выбора из нескольких вариантов: напоминание, список дел или настрйки рассылок

## Поддержка
Если у вас возникли вопросы или проблемы с ботом, пожалуйста, создайте issue в репозитории или [свяжитесь](https://t.me/dare_ka) с разработчиком.
