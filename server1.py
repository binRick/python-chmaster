#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from stockfish import Stockfish, StockfishException
import time, json, sys
from MoveDecoder import ChessDotComDecoder

hostName = "localhost"
serverPort = 4912

class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        print("posted")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        try:
          data = json.loads(self.data_string)
          #print(data)
          if len(data) > 0 and 'data' in data[0].keys() and 'game' in data[0]['data'] and 'moves' in data[0]['data']['game']:
            moves = data[0]['data']['game']['moves']
            decoded_moves = ChessDotComDecoder(moves)
            print(f'MOVES: {moves} :: {decoded_moves}')
            sf = Stockfish()
            sf.set_position(decoded_moves)
            move = sf.get_best_move()
            print(f'best move: {move}')
            resp = {
              'move': move,
            }
            print(resp)
            self.wfile.write(bytes(json.dumps(resp)),"utf-8")
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
