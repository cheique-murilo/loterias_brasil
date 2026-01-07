from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass(frozen=True)
class Sorteio:
    data: datetime
    concurso: str
    principais: List[int] = field(default_factory=list)
    complementares: List[int] = field(default_factory=list)
    acumulou: bool = False
    jackpot: int = 0
    jackpot_fmt: str = ""   # ← NOVO CAMPO
    paises_ganhadores: Optional[str] = ""
    num_vencedores_jackpot: int = 0

    def __post_init__(self):
        # Ordena os números principais
        if self.principais:
            object.__setattr__(self, "principais", sorted(self.principais))

        # Normaliza o concurso como string limpa
        if self.concurso:
            object.__setattr__(self, "concurso", str(self.concurso).strip())

