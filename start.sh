#!/bin/bash

echo "Creating data directory..."
mkdir -p data

if [ -f data/parsed.jl.zip ]; then
    echo "Extracting parsed.jl.zip to data/..."
    unzip -o data/parsed.jl.zip -d data
else
    echo "❌ Erreur : fichier data/parsed.jl.zip introuvable !"
    exit 1
fi

echo "Starting the backend..."
python rec.py
