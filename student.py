"""Example client."""
import asyncio
import getpass
import json
import os

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets

# mine imports
from search import *
from common import *
from tree_search import *
import time

#ant_level = 1



async def agent_loop(server_address="localhost:8000", agent_name="103199"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))


        # goal = Coordinates(5,2) # always the same goal

        solution = []

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                st = time.time()

                # print("--------------inicio do loop--------------------")
                key = ""

                map = Map(state.get("grid"))
                cursor = state.get("cursor")
                sel = state.get("selected")

                # print(map.grid)
                # for x in map.grid:
                #     print(x)
                #     print("\n")
                # print(solution)

                if solution == []:
                    domain = RushHour(map)
                    p = SearchProblem(domain, domain.map)
                    t = SearchTree(p, 'greedy')
                    full_search_solution = t.search()
                    solution = full_search_solution[1:]

                # print(solution)

                # if state.get("level") == 2:
                    # print("-----lvl2-------")

                # print(solution[0])
                # print(map.grid_size)
                key, done = do_action(map, solution[0], cursor, sel)

                

                if done == 1:
                    solution.pop(0)

                # print("key:", key)

                ft = time.time()
                # print(ft-st)

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return



# auxiliary functions


def do_action(map, action, cursor, sel):
    piece = action[0]
    act = action[1]
    done = 0
    if not same_coords(map, piece, cursor) and sel == '':
        return move_cursor_to_car(map, piece, cursor), done
    if not same_coords(map, piece, cursor) and sel != '':
        return ' ', done
    if same_coords(map, piece, cursor) and sel != piece:
        return ' ', done
    if same_coords(map, piece, cursor) and sel == piece:
        done = 1
        return act, done


def same_coords(map, piece: str, cursor):
    piece_x = map.piece_coordinates(piece)[1].x
    cursor_x = cursor[0]
    piece_y = map.piece_coordinates(piece)[1].y
    cursor_y = cursor[1]
    return piece_x == cursor_x and piece_y == cursor_y


def move_cursor_to_car(map, piece: str, cursor):
    key = ""
    x_diff = cursor[0]-map.piece_coordinates(piece)[1].x
    if (x_diff > 0):
        key = "a"
    elif (x_diff < 0):
        key = "d"
    else:
        y_diff = cursor[1]-map.piece_coordinates(piece)[1].y
        if (y_diff > 0):
            key = "w"
        elif (y_diff < 0):
            key = "s"
    return key


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
