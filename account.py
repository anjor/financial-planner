from enum import Enum


class HoldingsType(Enum):
    CASH = ("cash", True)
    S_AND_S = ("stocks and shares", True)
    PROPERTY = ("property", False)
    OTHER = ("other", False)

    def __init__(self, label, is_liquid):
        self.label = label
        self.is_liquid = is_liquid


class Account:
    def __init__(self, name: str, holdings_type: HoldingsType, growth_rate: float):
        self.name = name
        self.holdings_type = holdings_type
        self.value = 0
        self.growth_rate = growth_rate

    @property
    def is_liquid(self):
        return self.holdings_type.is_liquid


    def set_value(self, value):
        self.value = value

    def set_growth_rate(self, growth_rate):
        self.growth_rate = growth_rate

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.holdings_type,
            "value": self.value,
            "growth": self.growth_rate,
        }
