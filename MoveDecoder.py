#!/usr/bin/env python3

letters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 ! ?'.split(' ')

def decode_chess_dot_com_moves(moves):
  chess_moves = []
  for move in moves:
    p1 = letters.index(move[0])
    p2 = letters.index(move[1])
    r1 = p1 % 8
    r2 = p2 % 8
    q1 = int(p1 / 8)
    q2 = int(p2 / 8)
    movePosition_START_X = letters[r1]
    movePosition_START_Y = q1 + 1
    movePosition_END_X = letters[r2]
    movePosition_END_Y = q2 + 1
    pos = f'{movePosition_START_X}{movePosition_START_Y}{movePosition_END_X}{movePosition_END_Y}'
    chess_moves.append(pos)

  return chess_moves
  
def decode_chess_dot_com_moves_string(s):
  moves = []
  move = ''
  for i, c in enumerate(s):
    is_even = (i % 2) == 0
    if is_even:
      move = c
    else:
      move = f'{move}{c}'
      moves.append(move)
  return moves

def ChessDotComDecoder(moves):
  return decode_chess_dot_com_moves(decode_chess_dot_com_moves_string(moves))

if __name__ == '__main__':
  ss = [
    'owZRmu1Tjr2Ugv0SksSKpxRJltTLvK6SwELE',
  ]
  for s in ss:
    chess_moves = ChessDotComDecoder(s)
    print(f'[{s}] :: {chess_moves}')
