from __future__ import annotations
from dataclasses import dataclass

ROUNDING = 2


@dataclass(frozen=True, kw_only=True)
class Unit:
    s: float = 0
    kg: float = 0
    m: float = 0
    A: float = 0
    mol: float = 0
    cd: float = 0
    K: float = 0

    @classmethod
    def from_string(cls, s: str, /) -> Unit:
        assert s in alias_map.values()
        for key, value in alias_map.items():
            if value == s:
                return key

        assert False

    @staticmethod
    def power_string(value: float) -> str:
        if value.is_integer():
            value = int(value)
        return "".join(
            {
                "-": "⁻",
                "0": "⁰",
                "1": "¹",
                "2": "²",
                "3": "³",
                "4": "⁴",
                "5": "⁵",
                "6": "⁶",
                "7": "⁷",
                "8": "⁸",
                "9": "⁹",
                ".": "ˑ"
            }[digit]
            for digit in str(round(value, ROUNDING))
        )

    def __str__(self) -> str:
        if self in alias_map:
            return alias_map[self]
        return " ".join(
            symbol if value == 1 else (symbol + self.power_string(value))
            for symbol, value in [
                ("s", self.s),
                ("kg", self.kg),
                ("m", self.m),
                ("A", self.A),
                ("mol", self.mol),
                ("cd", self.cd),
                ("K", self.K),
            ]
            if value != 0
        )

    def __mul__(self, other: Unit) -> Unit:
        assert isinstance(other, Unit)
        return Unit(
            s=self.s + other.s,
            kg=self.kg + other.kg,
            m=self.m + other.m,
            A=self.A + other.A,
            mol=self.mol + other.mol,
            cd=self.cd + other.cd,
            K=self.K + other.K,
        )

    def __truediv__(self, other: Unit) -> Unit:
        assert isinstance(other, Unit)
        return Unit(
            s=self.s - other.s,
            kg=self.kg - other.kg,
            m=self.m - other.m,
            A=self.A - other.A,
            mol=self.mol - other.mol,
            cd=self.cd - other.cd,
            K=self.K - other.K,
        )

    def __add__(self, other: Unit) -> Unit:
        assert isinstance(other, Unit)
        assert self == other
        return self

    def __sub__(self, other: Unit) -> Unit:
        assert isinstance(other, Unit)
        assert self == other
        return self

    def __pow__(self, power: float, modulo: None = None) -> Unit:
        assert modulo is None
        return Unit(
            s=self.s * power,
            kg=self.kg * power,
            m=self.m * power,
            A=self.A * power,
            mol=self.mol * power,
            cd=self.cd * power,
            K=self.K * power,
        )

    def __neg__(self) -> Unit:
        return self


alias_map = {
    Unit(s=-1): "Hz",
    Unit(kg=1, m=1, s=-2): "N",
    Unit(kg=1, m=2, s=-2): "J",
    Unit(kg=1, m=2, s=-3): "W",
    Unit(m=1, s=-1): "m/s",
    Unit(m=1, s=-2): "m/s²",
}


@dataclass(frozen=True)
class UnitType:
    value: float
    unit: Unit = Unit()

    def __add__(self, other: UnitType) -> UnitType:
        return UnitType(self.value + other.value, self.unit + other.unit)

    def __sub__(self, other: UnitType) -> UnitType:
        return UnitType(self.value - other.value, self.unit - other.unit)

    def __mul__(self, other: UnitType) -> UnitType:
        return UnitType(self.value * other.value, self.unit * other.unit)

    def __truediv__(self, other: UnitType) -> UnitType:
        return UnitType(self.value / other.value, self.unit / other.unit)

    def __pow__(self, power: float) -> UnitType:
        return UnitType(self.value ** power, self.unit ** power)

    def __neg__(self) -> UnitType:
        return UnitType(-self.value, self.unit)

    def __str__(self):
        return f"{round(self.value, ROUNDING)} {str(self.unit)}"
