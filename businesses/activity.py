from abc import ABC, abstractmethod


class Activity(ABC):
    def __init__(self, current_period: int = 0):
        self.current_period = current_period

        self.profit_history = []
        self.valuation_history = []

        self._current_valuation = None
        self._current_profit = None

    def profit(self) -> float:
        """
        Obtain profit of current period of this activity

        Returns:
            The profit (or loss) from this activity
        """
        if self._current_profit is None:
            raise ValueError("You must call step before having a profit.")

        return self._current_profit

    def valuation(self) -> float:
        """
        Obtains the value of this asset in the current period.

        Returns:
            The total valuation (or liability) of this activity.
        """
        return self._current_valuation

    @abstractmethod
    def _step(self, *args, **kwargs) -> tuple[float, float]:
        """
        Advance one period in time

        Args:
            *args:
            **kwargs:

        Returns:

        """
        pass

    def step(self, *args, **kwargs):
        # Take the step with the backend
        self._current_profit, self._current_valuation = self._step(*args, **kwargs)

        self.valuation_history.append(self._current_valuation)
        self.profit_history.append(self._current_profit)

        self.current_period += 1

    def reset(self):
        self.valuation_history = []
        self.profit_history = []

        self.current_period = 0

    def __repr__(self):
        return f"{self.__class__.__name__}:{self._current_valuation}"
