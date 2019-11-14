
import abc

class State(abc.ABC):

    @abc.abstractmethod
    def transition(self, prev):
        pass



class Start(State):

    def __init__(self):
        pass

    def transition(self, prev):
        pass


class InBus(State):

    def __init__(self):
        pass

    def transition(self, prev):
        pass

class OutBus(State):

    def __init__(self):
        pass

    def transition(self, prev):
        pass

class InTrain(State):

    def __init__(self):
        pass

    def transition(self, prev):
        pass

class OutTrain(State):

    def __init__(self):
        pass

    def transition(self, prev):
        pass


class End(State):

    def __init__(self):
        pass

    def transition(self, prev):
        pass
