#!/usr/bin/env bash
cd "$(dirname "$0")" || exit
python3 "src/main.py" "$@"
