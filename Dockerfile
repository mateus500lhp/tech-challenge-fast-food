FROM python:3.12.3-slim

WORKDIR /app

# Copiar somente o arquivo requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos
COPY . /app/

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]