#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from stockfish import Stockfish, StockfishException
import time, json, sys, os
from MoveDecoder import ChessDotComDecoder

hostName = "localhost"
serverPort = 4912

LOG_DIR = '.logs'

if not os.path.isdir(LOG_DIR):
	os.mkdir(LOG_DIR)

class MyServer(BaseHTTPRequestHandler):
    sf = Stockfish()
    elo = 1500
    moves_qty = 5
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        ts = int(time.time()*1000)
        print("posted")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        try:
          data = json.loads(self.data_string)
          #print(data)
          if len(data) > 0 and 'data' in data[0].keys() and 'game' in data[0]['data'] and 'moves' in data[0]['data']['game']:
            log_dir = f'{LOG_DIR}/{ts}'
            print(log_dir)
            if not os.path.isdir(log_dir):
              os.mkdir(log_dir)
            req_log = f'{log_dir}/req.json'
            res_log = f'{log_dir}/res.json'
            with open(req_log,'w') as f:
              f.write(json.dumps(data))
            moves = data[0]['data']['game']['moves']
            decoded_moves = ChessDotComDecoder(moves)
            player = data[0]['data']['game']['players'][0]['uid']
            opponent = data[0]['data']['game']['players'][1]['uid']
            seq = data[0]['data']['game']['seq']

            print(f'{player} / {opponent} :: #{seq} :: Moves: {moves} :: {decoded_moves}')
            self.sf.set_position(decoded_moves)
            self.sf.set_elo_rating(self.elo)
            move = self.sf.get_best_move()
            print(f'best move: {move}')
            ev = self.sf.get_evaluation()
            moves = self.sf.get_top_moves(self.moves_qty)
            wdl = self.sf.get_wdl_stats()
            params = self.sf.get_parameters()
            ver = self.sf.get_stockfish_major_version()
            resp = {
              'move': move,
              'evaluation': ev,
              'elo': self.elo,
              'moves': moves,
              'wdl': wdl,
              'params': params,
              'ver': ver,
            }
            '''response: {"move": "d2d4", "evaluation": {"type": "cp", "value": -60}, "elo": 1500, "moves": [{"Move": "c2c4", "Centipawn": -49, "Mate": null}, {"Move": "d2d3", "Centipawn": -76, "Mate": null}, {"Move": "e2e4", "Centipawn": -78, "Mate": null}, {"Move": "f1g2", "Centipawn": -79, "Mate": null}, {"Move": "b1c3", "Centipawn": -85, "Mate": null}], "wdl": [0, 865, 135], "params": {"Debug Log File": "", "Contempt": 0, "Min Split Depth": 0, "Ponder": "false", "MultiPV": 1, "Skill Level": 20, "Move Overhead": 10, "Minimum Thinking Time": 20, "Slow Mover": 100, "UCI_Chess960": "false", "UCI_LimitStrength": "true", "UCI_Elo": 1500, "Threads": 1, "Hash": 16}, "ver": 16}'''
            print(resp)
            with open(res_log,'w') as f:
              f.write(json.dumps(resp))
            self.wfile.write(bytes(json.dumps(resp),"utf-8"))
        except:
          return

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        print("test123")
        print(self.path, self.headers, self.command)
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
