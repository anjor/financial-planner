from enum import Enum


class HoldingsType(Enum):
    CASH = "cash"
    S_AND_S = "stocks and shares"
    PROPERTY = "property"


class Account:
    def __init__(self, name: str, holdings_type: HoldingsType, growth_rate: float):
        self.name = name
        self.holdings_type = holdings_type
        self.value = 0
        self.growth_rate = growth_rate

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
