# -*- coding: utf-8 -*-
import os, sys
from os import path
from optparse import OptionParser
from datetime import datetime


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


def main():
    init_path()
    parser = OptionParser(usage="usage: %prog [options] SCENARIO [[[arg1] arg2] ...]")
    parser.add_option("-c", "--count", action="store", default=1,
            type="int", dest="count", metavar="COUNT", help="run script COUNT times")
    options, args = parser.parse_args()

    if len(args) < 1:
        parser.error("must specify SCENARIO")
        return 1

    target = args[0]
    repeat = options.count
    quest_method = None
    try:
        sys.path.append(path.dirname(path.abspath(target)))
        env = {}
        execfile(target, env)
        quest_method = env['run']
    except KeyError, e:
        if str(e) == "'run'":
            sys.stderr.write("'run' function must be defined in scenario file:\n\t%s" % target)
            return 1
    except IOError, e:
        if "File not found" in str(e):
            sys.stderr.write("scenario file not found: %s\n" % target)
        else:
            raise e
        return 1

    for i in range(repeat):
        print("start quest %s at %s" % (target, datetime.now()))
        if quest_method(args[1:]) == False:
            print("failed quest %s at %s" % (target, datetime.now()))
        else:
            print("succeeded quest %s at %s" % (target, datetime.now()))


if __name__ == '__main__':
    sys.exit(main() or 0)

