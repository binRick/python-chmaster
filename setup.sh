#!/usr/bin/env bash
set -eou pipefail
if [[ ! -d .v ]]; then
	python3 -m venv .v
	source .v/bin/activate
	pip install -r requirements.txt
else
	source .v/bin/activate
fi

if ! command -v stockfish &>/dev/null; then
	brew install stockfish
fi



