#!/usr/bin/env bash
set -eou pipefail
cat fens/boards.fen | python3 -c 'print(__import__("random").choice(__import__("sys").stdin.readlines()))'|head -n1
