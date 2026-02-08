#!/bin/bash
cd "$(dirname "$0")/.."
if [[ $(git status --porcelain) ]]; then
    git add -A
    git commit -m "Auto-save $(date '+%Y-%m-%d %H:%M')"
fi
