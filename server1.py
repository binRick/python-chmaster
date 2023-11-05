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
            move = self.sf.get_best_move()
            print(f'best move: {move}')
            resp = {
              'move': move,
            }
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
