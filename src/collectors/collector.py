from abc import ABC, abstractmethod

class Collector(ABC):
    """
    Abstract base class for collectors.
    Collectors are responsible for gathering data from various sources.
    """

    @abstractmethod
    def collect(self):
        """
        Collect data from the source.
        This method should be implemented by subclasses to define how data is collected.
        """
        pass
