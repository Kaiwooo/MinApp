FROM python:3.13-slim

# Рабочая директория
WORKDIR /app

# Системные зависимости (минимальные)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы проекта
COPY . /app

# Устанавливаем pip-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Экспорт переменной окружения (бот)
ENV BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]