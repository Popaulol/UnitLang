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
        if isinstance(value, int) or value.is_integer():
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
                ".": "ˑ",
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


@dataclass(frozen=True)
class UnitType:
    value: float
    unit: Unit = Unit()

    def __add__(self, other: UnitType | float | int) -> UnitType:
        if isinstance(other, float) or isinstance(other, int):
            return UnitType(self.value + other, self.unit)
        return UnitType(self.value + other.value, self.unit + other.unit)

    def __sub__(self, other: UnitType) -> UnitType:
        return UnitType(self.value - other.value, self.unit - other.unit)

    def __mul__(self, other: UnitType | float | int) -> UnitType:
        if isinstance(other, float) or isinstance(other, int):
            return UnitType(self.value * other, self.unit)
        return UnitType(self.value * other.value, self.unit * other.unit)

    def __rmul__(self, other: UnitType | float | int) -> UnitType:
        return self.__mul__(other)

    def __truediv__(self, other: UnitType) -> UnitType:
        return UnitType(self.value / other.value, self.unit / other.unit)

    def __pow__(self, power: float) -> UnitType:
        return UnitType(self.value ** power, self.unit ** power)  # type: ignore

    def __neg__(self) -> UnitType:
        return UnitType(-self.value, self.unit)

    def __str__(self) -> str:
        return f"{round(self.value, ROUNDING)} {str(self.unit)}"

    def __repr__(self) -> str:
        return f"{round(self.value, ROUNDING)} {str(self.unit)}"


alias_map = {
    Unit(s=1): "s",
    Unit(kg=1): "kg",
    Unit(m=1): "m",
    Unit(A=1): "A",
    Unit(mol=1): "mol",
    Unit(cd=1): "cd",
    Unit(K=1): "K",
    Unit(s=-1): "Hz",
    Unit(kg=1, m=1, s=-2): "N",
    Unit(m=-1, kg=1, s=-2): "Pa",
    Unit(kg=1, m=2, s=-2): "J",
    Unit(kg=1, m=2, s=-3): "W",
    Unit(s=1, A=1): "C",
    Unit(m=2, kg=1, s=-3, A=-1): "V",
    Unit(m=-2, kg=-1, s=4, A=2): "F",
    Unit(m=2, kg=1, s=-3, A=-2): "Ω",
    Unit(m=-2, kg=-1, s=3, A=2): "S",
    Unit(m=2, kg=1, s=-2, A=-1): "Wb",
    Unit(kg=1, s=-2, A=-1): "T",
    Unit(m=2, kg=1, s=-2, A=-2): "H",
    Unit(m=-2, cd=1): "lx",
    Unit(m=2, s=-2): "Sv",
    Unit(s=-1, mol=1): "kat",
    Unit(m=1, s=-1): "m/s",
    Unit(m=1, s=-2): "m/s²",
    Unit(kg=1, m=-3): "kg/m³",
}

for unit, symbol in alias_map.items():
    globals()[symbol] = UnitType(1, unit)  # type: ignore

if __name__ == "__main__":
    import code
    from math import *

    tau = 2 * pi
    g = 9.81

    code.interact(local=locals())  # type: ignore
