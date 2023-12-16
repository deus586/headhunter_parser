from abc import ABC, abstractmethod


class Parser(ABC):

    @abstractmethod
    def parser(self, comp_name):
        pass
