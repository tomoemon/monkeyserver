# -*- coding: utf-8 -*-
import os, sys
from os import path
import time
import types


if sys.getdefaultencoding() == 'ascii':
  reload(sys)
  sys.setdefaultencoding('utf-8')
  delattr(sys, 'setdefaultencoding')


def init_path():
    # monkeyrunner.bat から起動すると
    # monkeyrunner.bat が存在するディレクトリをカレントディレクトリにしてしまうため、
    # src ディレクトリからインポートできるようにする
    os.chdir(os.getenv('CURRENT_DIR'))
    sys.path.append(path.join(path.dirname(path.dirname(__file__)), "src"))
    sys.path.append(path.join(path.dirname(path.dirname(__file__)), "lib"))


def queueing(queue):
    import server
    server.create_udp_server("127.0.0.1", 4000, queue)


def main():
    init_path()

    from threading import Thread
    from Queue import Queue
    import command

    functions = dict([(i, getattr(command, i))
        for i in dir(command) if isinstance(getattr(command, i), types.FunctionType)])

    queue = Queue(32)
    t = Thread(target=queueing, args=(queue,))
    t.daemon = True
    t.start()

    print("start serving: " + "127.0.0.1:4000")

    while True:
        q = queue.get()
        size = queue.qsize()
        action = q['action']
        function = functions[action]
        params = q['params']
        print("queue count: " + str(size))
        print(q)
        function(**params)


if __name__ == '__main__':
    sys.exit(main() or 0)

