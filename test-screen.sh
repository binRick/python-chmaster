#!/usr/bin/env bash
set -eou pipefail
source .v/bin/activate
source .envrc

WINDOW_ID="$(GetWindowID 'Google Chrome' --list|grep Chess.com|head -n1|tr ' ' '\n'|grep ^id=|cut -d'=' -f2)"
IMG="window-$WINDOW_ID-$(date +%s).png"
[[ -f "$IMG" ]] && unlink "$IMG"
screencapture -x -l $WINDOW_ID $IMG
FEN="$(cd detector && ./tensorflow_chessbot.py --filepath ../$IMG)"

echo -e "FEN:   \"$FEN\""

#FEN="$(echo -e "$FEN"|grep 'Predicted FEN' -A 1 | tail -n1|cut -d ' ' -f1,2)"
FEN="$(echo -e "$FEN"|cut -d ' ' -f1)"
echo -e "FEN=$FEN"
MOVE="$(./fish.py "$FEN")"

echo -e "$WINDOW_ID -> $IMG -> $FEN -> $MOVE"
