import abc

class LLMInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        pass

    @abc.abstractmethod
    def query(self, context="", query=""):
        raise NotImplementedError


    
