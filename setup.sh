#!/bin/bash

#echo "Installing requirements..."
#pip install -r requirements.txt

if [ ! -e ~/.silencebreaker ]; then
    echo "Making ~/.silencebreaker directory..."
    mkdir ~/.silencebreaker
fi

echo "Copying init settings..."
cp data/settings_setup.json ~/.silencebreaker/settings.json

echo "Creating desktop launcher..."
program_dir=$(pwd)
echo "Program files at: $program_dir"
cd ~/Desktop
echo "python3 $program_dir/main.py" > silenceBreaker.sh
chmod +x ~/Desktop/silenceBreaker.sh

echo "Done."