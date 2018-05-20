import asyncio
import sys

import colorama

from ctrl.command.base import Commandable


colorama.init()


class CtrlError(ValueError):
    pass


class Ctrl(Commandable):

    def handle(self, *args):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.run(self.parse(*args)))
        finally:
            loop.close()


def main():
    try:
        sys.exit(Ctrl().handle(*sys.argv[1:]))
    except CtrlError as e:
        sys.stdout.write(
            "\n".join(reversed([str(x) for x in e] + ["\nCtrl Error!\n"])))
        sys.exit(1)


if __name__ == '__main__':
    main()
