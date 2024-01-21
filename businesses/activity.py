from abc import ABC, abstractmethod


class Activity(ABC):
    def __init__(self, current_period: int):
        self.current_period = current_period

        self.profit_history = []
        self.valuation_history = []

    @abstractmethod
    def profit(self) -> float:
        """
        Obtain profit of current period of this activity

        Returns:
            The profit (or loss) from this activity
        """
        pass

    @abstractmethod
    def valuation(self) -> float:
        """
        Obtains the value of this asset in the current period.

        Returns:
            The total valuation (or liability) of this activity.
        """
        pass

    @abstractmethod
    def _step(self, *args, **kwargs):
        """
        Move one month forward in time
        Args:
            *args:
            **kwargs:

        Returns:

        """
        pass

    def step(self, *args, **kwargs):
        # Take the step with the
        self._step(*args, **kwargs)

        self.valuation_history.append(self.valuation())
        self.profit_history.append(self.profit())

    def reset(self):
        self.valuation_history = []
        self.profit_history = []

        self.current_period = 0
