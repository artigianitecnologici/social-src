#!/usr/bin/env python3

import asyncio
import websockets

# Funzione per la gestione dei messaggi ricevuti
def handle_message(myasr):
    print("Received message:", myasr)
    # Inserisci qui la logica per gestire i messaggi ricevuti, ad esempio salvare su file o elaborare ulteriormente

async def listen(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            myasr = await websocket.recv()
            handle_message(myasr)

# Avvia il listener websocket
asyncio.run(listen('ws://192.168.1.100:2700'))
