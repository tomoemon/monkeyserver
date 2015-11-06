# -*- coding: utf-8 -*-
import socket
import time
import json
from contextlib import closing, nested


def main():
    BUFSIZE = 4096
    send_sock = closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    recv_sock = closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    receive_host = "127.0.0.1"
    receive_port = 4001
    send_host = "127.0.0.1"
    send_port = 4000
    with nested(send_sock, recv_sock) as (sender, receiver):
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.settimeout(1.0)
        receiver.bind((receive_host, receive_port))
        sender.sendto(json.dumps(
            {
                "action": "setRespondTo",
                "param": {"host": receive_host, "port": receive_port}
                }).encode('utf-8'),
            (send_host, send_port))
        try:
            data = json.loads(receiver.recv(BUFSIZE).decode('utf-8'))
            print(data)
        except socket.error as e:
            # time out
            print(e)


if __name__ == '__main__':
    main()
