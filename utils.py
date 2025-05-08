from datetime import date


def get_mid(seq: list[int | float]) -> float:
    return sum(seq) / len(seq) if seq else 0.0


def get_current_semester() -> int:
    today = date.today()
    if 9 <= today.month <= 12:
        return 1
    elif 1 <= today.month <= 5:
        return 2
    return -1
