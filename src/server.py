# -*- coding: utf-8 -*-
import socket
import simplejson as json

"""
終了するときは Ctrl-Break
"""


"""
{
    "action": "touch",
    "params": {
        "x": 100,
        "y": 200
    },
}
"""


def create_udp_server(host, port, queue):
    BUFSIZE = 4096
    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recv_sock.bind((host, port))
        while True:
            try:
                data = json.loads(recv_sock.recv(BUFSIZE).decode('utf-8'))
                print("receive: " + repr(data))
                queue.put(data)
            except Exception, e:
                print(e)
    finally:
        recv_sock.close()


if __name__ == '__main__':
    create_udp_server('127.0.0.1', 4000, None)

