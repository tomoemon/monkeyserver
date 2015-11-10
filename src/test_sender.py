# -*- coding: utf-8 -*-
import socket
import time
import json


class Socket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.socket.close()
        return True

    def send(self, action ,params):
        self.socket.sendto(json.dumps(
            {
                "action": action,
                "params": params
            }), (self.host, self.port))


def main():
    send_host = "127.0.0.1"
    send_port = 4000
    with Socket(send_host, send_port) as sender:
        #for i in range(10):
        #    sender.send('touch', {'x': 500, 'y': 500})
        #return

        sender.send('touch_down', {'x': 500, 'y': 500})
        sender.send('touch_move', {
            'start': (500, 800),
            'end': (500, 300),
            'duration': 0.3,
            'step': 4
            })
        sender.send('touch_up', {'x': 500, 'y': 50})


if __name__ == '__main__':
    main()
