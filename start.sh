#!/bin/sh
# cd bot
while true
do
    echo "pulling updated bot"
    git pull origin main
    echo "starting bot"
    python bot.py
    echo "bot stopped"
done