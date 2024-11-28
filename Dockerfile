FROM python:3.9-slim

# Installer les dépendances système, y compris cron
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unixodbc-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Installer le ODBC Driver 18 for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier l'application dans le container
COPY . /app
WORKDIR /app

# Ajouter le fichier crontab
COPY crontab /etc/cron.d/my-cron-job

# Donner les permissions correctes au fichier crontab
RUN chmod 0644 /etc/cron.d/my-cron-job

# Enregistrer le cron job
RUN crontab /etc/cron.d/my-cron-job

# Activer cron dans le conteneur
CMD ["cron", "-f"]


# To Check the cron log file : docker exec -it mon-pipeline-container tail -f /var/log/cron.log
