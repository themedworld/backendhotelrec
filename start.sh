#!/bin/bash
echo "Creating data directory..."
mkdir -p data

echo "Extracting parsed.jl.zip to data/..."
unzip -o parsed.jl.zip -d data

echo "Starting the backend..."
python rec.py
