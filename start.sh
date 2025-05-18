#!/bin/bash

# Télécharge parsed.jl si absent
if [ ! -f parsed.jl ]; then
  echo "Téléchargement de parsed.jl depuis Google Drive..."
  gdown https://drive.google.com/uc?id=1ajxkOOkbF06HCIRR67bPxGKRgFoTTMsD -O parsed.jl
fi

# Lance le serveur Flask
exec gunicorn app:rec --bind 0.0.0.0:$PORT
