"""XP awards keyed by canon.difficulty_rank."""

XP_BY_DIFFICULTY: dict[str, int] = {
    "explorer": 100,
    "investigator": 150,
    "detective": 200,
}


def xp_for_rank(difficulty_rank: str) -> int:
    return XP_BY_DIFFICULTY.get(difficulty_rank, 100)
