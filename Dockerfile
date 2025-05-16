# Usa imagem leve com Python 3.11
FROM python:3.11-slim

# Instalações básicas para dependências (como ffmpeg se necessário)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH="${PYTHONPATH}:/bot"

# Define o diretório de trabalho
WORKDIR /bot

# Copia os arquivos do projeto para dentro do container
COPY . /bot

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Define variável de ambiente para garantir que UTF-8 funcione
ENV PYTHONUNBUFFERED=1

# Executa o bot
CMD ["python", "bot/main.py"]
