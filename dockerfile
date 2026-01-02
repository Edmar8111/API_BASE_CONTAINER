# -----------------------------
# Etapa 1: Imagem base segura e leve!
# -----------------------------
FROM python:3.12-slim AS base

# -----------------------------
# Definir variáveis de ambiente
# -----------------------------
# Evita que o Python grave arquivos .pyc (melhora performance de container)
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que o log seja exibido imediatamente no console
ENV PYTHONUNBUFFERED=1
# Define diretório padrão de trabalho
WORKDIR /app

# -----------------------------
# Atualiza o sistema e instala dependências essenciais
# -----------------------------
# - gcc e libpq-dev: necessários para algumas bibliotecas Flask (como psycopg2)
# - netcat-traditional: útil para checar disponibilidade de serviços externos
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Copia arquivos de dependências
# -----------------------------
COPY requirements.txt .

# -----------------------------
# Instala dependências do projeto
# -----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copia o código-fonte para o container
# -----------------------------
COPY . .

# -----------------------------
# Exposição da porta Flask
# -----------------------------
EXPOSE 5000

# -----------------------------
# Comando padrão de inicialização
# -----------------------------
# Usa o módulo 'flask run' com host público

# CMD ["flask", "run", "--host=0.0.0.0"]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

