#!/bin/bash

echo "Téléchargement de parsed.jl depuis Google Drive..."
gdown --id 1ajxkOOkbF06HCIRR67bPxGKRgFoTTMsD -O parsed.jl

echo "Lancement de l'application Flask avec Gunicorn (1 worker)..."
exec gunicorn rec:app \
  --bind 0.0.0.0:$PORT \
  --workers 1 \
  --threads 1 \
  --timeout 120

