#!/bin/bash

<<<<<<< HEAD
echo "Téléchargement de parsed.jl depuis Google Drive..."
gdown --id 1ajxkOOkbF06HCIRR67bPxGKRgFoTTMsD -O parsed.jl

echo "Lancement de l'application Flask avec Gunicorn (1 worker)..."
exec gunicorn rec:app \
  --bind 0.0.0.0:$PORT \
  --workers 1 \
  --threads 1 \
  --timeout 120

=======
# Télécharge parsed.jl si absent
if [ ! -f parsed.jl ]; then
  echo "Téléchargement de parsed.jl depuis Google Drive..."
  gdown https://drive.google.com/uc?id=1ajxkOOkbF06HCIRR67bPxGKRgFoTTMsD -O parsed.jl
fi

# Lance le serveur Flask
exec gunicorn app:app --bind 0.0.0.0:$PORT
>>>>>>> 14f6219 (Ajout du fichier parsed.jl.zip)
