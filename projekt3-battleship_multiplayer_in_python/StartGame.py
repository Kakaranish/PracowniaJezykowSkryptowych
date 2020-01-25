#!/usr/bin/env python3
import os
import argparse
from Game import *
from Utilities import *

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description='''
DESCRIPTION
The goal of the game is to sink all enemy player ships before he/she will destroy yours.
At the beginning of the game you need to wait for other player if you connected server as first.
When other player joins game, you have to place your ships in such way he/she won't be able to hit them.
Then game begins. It's your or your opponent turn. 
The game lasts until one's player ships are destroyed.

GAME NAVIGATION:
- BACKSPACE - ship rotation in ships placement phase
- arrows - ship/shot caret movement
- SPACE - ship placement or takin a shot
''')
parser.add_argument("-p", dest="port", metavar="port",
                    nargs=1, type=int, help="port on which server is running")
args = parser.parse_args()

server_port = DEFAULT_PORT
if args.port is not None:
    server_port = args.port[0]

game = Game(port=server_port)
game.start()
