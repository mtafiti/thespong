from datetime import timedelta

from thespian.actors import *


class Counter(ActorTypeDispatcher):
    def __init__(self):
        self.count = 0

    def receiveMsg_str(self, message, sender):
        if (message == "incr"):
            self.count += 1
        if (message == "get"):
            sender.send(self.count)


class CounterClient(ActorTypeDispatcher):
    def __init__(self):
        if not self.counter:
            self.counter = self.createActor(Counter)

        self.send(self.counter, "incr")
        self.send(self.counter, "incr")
        self.send(self.counter, "get")

    def receiveMsg_int(self, count):  # not ideal for all int, but works here
        print(f"returned count from counter: {count}")


if __name__ == "__main__":
    import sys

    asys = ActorSystem('counterExample')
    app = asys.createActor('counter.CounterClient',
                           sourceHash=sys.argv[1],
                           globalName='CounterExample:%s' % sys.argv[1])
    r = asys.ask(app, sys.stdin.read().strip(), timedelta(seconds=1))
    while r:
        print(r)
        r = asys.listen(timedelta(seconds=5.0))
    sys.exit(0)
