# Utilise une image Python
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Flask
EXPOSE 8080

# Lancer l'application
CMD ["python", "app.py"]
