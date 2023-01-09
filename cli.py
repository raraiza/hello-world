# Author: Roberto Araiza
# to run from the command line:
# > python3 cli.py
# make sure you have all dependencies installed: socketio, requests, websocket-client

import time
import socketio

HOST = "http://localhost:3000"
client = socketio.Client()
expected_events = -1
received_events = 0


@client.event
def search(data):
    global expected_events
    global received_events

    if ("error" in data):
        print("ERR: " + data["error"])
    else:
        print(f"({data['page']}/{data['resultCount']}) {data['name']} - [{data['films']}]")

    expected_events = data["resultCount"]
    received_events = data["page"]


def wait_for_all_events():
    while received_events != expected_events:
        time.sleep(1)


def main():
    client.connect(HOST)
    global expected_events
    global received_events

    while True:
        query = input("What character would you like to search for? ")

        if not query:
            break

        print("Searching for " + query + "...")

        expected_events = -1
        received_events = 0

        client.emit("search", {"query": query})
        wait_for_all_events()

    client.disconnect()


if __name__ == "__main__":
    main()
