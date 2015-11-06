# -*- coding: utf-8 -*-
import socket
import json
from contextlib import closing, nested

"""
終了するときは Ctrl-Break
"""


"""
{
    "action": "setRespondTo",
    "param": {
        "host": "127.0.0.1",
        "port": 5000
    }
}

{
    "action": "touch",
    "param": {
        "x": 100,
        "y": 200
    },
}
"""


send_address = None # host, port


def create_udp_server(host, port, queue, handler={}):
    BUFSIZE = 4096
    send_sock = closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    recv_sock = closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

    def set_respond_to(host, port):
        global send_address
        send_address = (host, port)
        return "succeeded"

    receiver_handler = {
            "setRespondTo": set_respond_to
            }

    handler.update(receiver_handler)

    with nested(send_sock, recv_sock) as (sender, receiver):
        sender.settimeout(1.0)
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.bind((host, port))
        while True:
            try:
                data = json.loads(receiver.recv(BUFSIZE).decode('utf-8'))
                action = data['action']
                if action in handler:
                    message = handler[action](**data['param'])
                    status = "200"
                else:
                    status = "404"
                    message = "handler_not_found"
            except Exception as e:
                status = "400",
                message = unicode(e)

            print("receive: " + repr(data))
            print("status : " + repr(status))
            print("message: " + repr(message))

            if send_address:
                sender.sendto(
                        json.dumps({"status": status, "message": message}).encode('utf-8'),
                        send_address)


if __name__ == '__main__':
    create_udp_server('127.0.0.1', 4000, None)

