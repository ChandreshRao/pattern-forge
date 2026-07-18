"""Phase 1a acceptance: submit solutions via backend → Judge0."""
from __future__ import annotations

import json
import uuid
import urllib.request

import os

BASE = os.environ.get("PF_API_BASE", "http://127.0.0.1:8000")

GUEST = str(uuid.uuid4())

SOLUTIONS = {
    "q01_two_sum": {
        "python": """
from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    return []
""",
        "javascript": """
function twoSum(nums, target) {
  const seen = {};
  for (let i = 0; i < nums.length; i++) {
    const need = target - nums[i];
    if (need in seen) return [seen[need], i];
    seen[nums[i]] = i;
  }
  return [];
}
""",
    },
    "q02_contains_duplicate": {
        "python": """
from typing import List

def contains_duplicate(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))
""",
    },
    "q03_valid_anagram": {
        "python": """
def valid_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if ch not in counts:
            return False
        counts[ch] -= 1
        if counts[ch] == 0:
            del counts[ch]
    return not counts
""",
    },
}


def req(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if body is not None else {},
    )
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    health = req("GET", "/health")
    assert health["status"] == "ok", health

    progress = req("GET", f"/progress/{GUEST}")
    assert "q01_two_sum" in progress["unlocked_quest_ids"], progress
    print("guest", GUEST)
    print("initial unlocks", progress["unlocked_quest_ids"])

    # Run mode: public tests only
    run = req(
        "POST",
        "/submit",
        {
            "guest_id": GUEST,
            "quest_id": "q01_two_sum",
            "language": "python",
            "source": SOLUTIONS["q01_two_sum"]["python"],
            "mode": "run",
        },
    )
    assert run["passed"], run
    assert len(run["results"]) == 2, run
    assert run["reflection"] is None
    print("run q01 python: PASS (2 public tests)")

    for qid in ("q01_two_sum", "q02_contains_duplicate", "q03_valid_anagram"):
        res = req(
            "POST",
            "/submit",
            {
                "guest_id": GUEST,
                "quest_id": qid,
                "language": "python",
                "source": SOLUTIONS[qid]["python"],
                "mode": "submit",
            },
        )
        assert res["passed"], (qid, res)
        assert res["reflection"] is not None, qid
        assert res["reflection"]["xp_awarded"] == 100, res["reflection"]
        assert res["progress"] is not None
        print(
            f"submit {qid} python: PASS · pattern={res['reflection']['pattern_reveal_name']} · xp={res['reflection']['xp_awarded']} · unlocked={res['progress']['unlocked_quest_ids']}"
        )

    # JS submit on quest 1 (already completed → 0 XP)
    js = req(
        "POST",
        "/submit",
        {
            "guest_id": GUEST,
            "quest_id": "q01_two_sum",
            "language": "javascript",
            "source": SOLUTIONS["q01_two_sum"]["javascript"],
            "mode": "submit",
        },
    )
    assert js["passed"], js
    assert js["reflection"]["xp_awarded"] == 0
    print("submit q01 javascript: PASS · xp_awarded=0 (re-solve)")

    # Progress survives fetch
    again = req("GET", f"/progress/{GUEST}")
    assert again["xp"] == 300, again
    assert set(again["completed_quest_ids"]) == {
        "q01_two_sum",
        "q02_contains_duplicate",
        "q03_valid_anagram",
    }
    print("progress reload: xp=300, all 3 completed")
    print("ACCEPTANCE OK")


if __name__ == "__main__":
    main()
