#!/usr/bin/env bash
set -eou pipefail
FEN="$(./random_fen.sh)"
MOVE="$(./fish.py "$FEN")"

echo -e "$FEN -> $MOVE"
