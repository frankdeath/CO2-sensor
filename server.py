#!/usr/bin/env python3

import asyncio
import websockets
import json
import datetime as dt

import sensor

CLIENTS = set()
SENSOR = sensor.Sensor()

async def handler(websocket, path):
    # Send the history when clients connect
    hist = SENSOR.getHist()
    hist["type"] = "history"
    message = json.dumps(hist)
    await websocket.send(message)

    # Add the client to the broadcast list
    CLIENTS.add(websocket)
    try:
        #!print("someone connected")
        await websocket.wait_closed()
    finally:
        CLIENTS.remove(websocket)
        #!print("someone disconnected")

async def broadcast(message):
    for websocket in CLIENTS.copy():
        try:
            await websocket.send(message)
        except websockets.ConnectionClosed:
            pass

async def broadcast_messages():
    while True:
        data = SENSOR.getDict()
        data["type"] = "data"
        data["users"] = len(CLIENTS)
        message = json.dumps(data)
        #!print("sending {}".format(message))
        await broadcast(message)
        await asyncio.sleep(2.0)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await broadcast_messages()  # runs forever

if __name__ == "__main__":
    asyncio.run(main())

