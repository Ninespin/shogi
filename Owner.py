from enum import Enum


class Owner(Enum):
    GOTE = 0
    SENTE = 1


def get_owner_direction_mult(owner: Owner) -> int:
    return -1 if owner is Owner.SENTE else 1
