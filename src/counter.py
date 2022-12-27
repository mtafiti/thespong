from dataclasses import dataclass
from thespian.actors import *

@dataclass(frozen=True)
class CounterMessages(object):
    incr: str
    get: str

class Counter(ActorTypeDispatcher):
    def __init__(self):
        self.count = 0

    def receiveMsg_incr(self): #todo: check if this is correct
        self.count += 1

    def receiveMsg_get(self):
        return self.count

class CounterClient(ActorTypeDispatcher):
    def __init__(self):
        if not self.counter:
            self.counter = self.createActor(Counter)

        self.send(self.counter, CounterMessages.incr)
        self.send(self.counter, CounterMessages.incr)
        self.send(self.counter, CounterMessages.get, self)

    def receiveMsg_count(self, count):
        println(f"returned count from counter: {count}")