from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict
import pandas as pd

@dataclass(frozen=True)
class Sorteio:
    data: date
    concurso: str
    principais: List[int]
    acumulou: bool
    jackpot_fmt: str
    locais: List[Dict[str, str | int]]
    ganhadores: int = 0

    concurso_base: int = field(init=False)
    sorteio_num: int = field(init=False)

    def __post_init__(self):
        d = self.data
        if isinstance(d, pd.Timestamp):
            d = d.date()
        elif isinstance(d, datetime):
            d = d.date()
        object.__setattr__(self, "data", d)

        object.__setattr__(self, "principais", sorted(self.principais))

        if "-" in self.concurso:
            base, num = self.concurso.split("-")
            object.__setattr__(self, "concurso_base", int(base))
            object.__setattr__(self, "sorteio_num", int(num))
        else:
            object.__setattr__(self, "concurso_base", int(self.concurso))
            object.__setattr__(self, "sorteio_num", 1)












