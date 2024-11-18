from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def handle(self, order):
        pass
