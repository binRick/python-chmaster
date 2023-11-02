#!/usr/bin/env python3
from stockfish import Stockfish, StockfishException
import sys

fen = sys.argv[1]
#fen = "7r/1pr1kppb/2n1p2p/2NpP2P/5PP1/1P6/P6K/R1R2B2 w - - 1 27"
#fen = "NBKQB1R/PPPPPPPP/5N2/8/4p3/8/pppp1ppp/rnbkqbnr w"

stockfish = Stockfish()
stockfish.set_fen_position(fen)

m = stockfish.get_best_move()

print(m)

