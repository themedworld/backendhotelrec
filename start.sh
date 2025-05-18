#!/bin/bash
echo "Extracting parsed.jl.zip..."
unzip -o parsed.jl.zip
echo "Starting the app..."
python rec.py 
