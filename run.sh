#!/bin/sh

# Author : Swapnil Shinde
# Copyright (c) AtmegaBuzz
# Script follows here:

echo "Adding Dependencies..."
pip install -r requirements.txt
echo "deps added..."

echo "running bot...."
python main.py
