from abc import ABC
from abc import abstractmethod


class BaseTopicInterpreter(ABC):

    @abstractmethod
    def interpret(
        self,
        keywords: list[str],
    ) -> str:
        pass