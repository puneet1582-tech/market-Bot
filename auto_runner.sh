#!/bin/bash

echo "Ultimate Brain started..."

while true
do
    date
    python run.py
    echo "Cycle complete. Sleeping 30 minutes..."
    sleep 1800
done
