# Используем готовый образ с Chrome от Selenium
FROM selenium/standalone-chrome:latest

USER root

# Установите Python
RUN sudo apt-get update && \
    sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && sudo rm -rf /var/lib/apt/lists/*

# Создайте рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Установите Python зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

EXPOSE 8501 

# Запуск Streamlit
ENTRYPOINT ["streamlit", "run", "main.py","--server.headless=true", "--server.port=8501", "--server.address=0.0.0.0"]
