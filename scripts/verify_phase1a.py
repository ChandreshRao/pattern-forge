"""Phase 1a/1b acceptance: auth progress + guest submit via backend → Judge0."""
from __future__ import annotations

import json
import os
import uuid
import urllib.error
import urllib.request

BASE = os.environ.get("PF_API_BASE", "http://127.0.0.1:8000")

GUEST = str(uuid.uuid4())
EMAIL = f"verify_{uuid.uuid4().hex[:8]}@example.com"
PASSWORD = "testpass123"

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


def req(method: str, path: str, body: dict | None = None, token: str | None = None):
    data = None if body is None else json.dumps(body).encode()
    headers = {}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        raise AssertionError(f"{method} {path} → {e.code}: {detail}") from e


def main() -> None:
    health = req("GET", "/health")
    assert health["status"] == "ok", health

    # Register + login
    auth = req("POST", "/auth/register", {"email": EMAIL, "password": PASSWORD})
    token = auth["access_token"]
    assert auth["user"]["email"] == EMAIL
    me = req("GET", "/auth/me", token=token)
    assert me["email"] == EMAIL
    print("auth register/me OK", EMAIL)

    progress = req("GET", "/progress", token=token)
    assert "q01_two_sum" in progress["unlocked_quest_ids"], progress
    print("initial unlocks", progress["unlocked_quest_ids"])

    run = req(
        "POST",
        "/submit",
        {
            "quest_id": "q01_two_sum",
            "language": "python",
            "source": SOLUTIONS["q01_two_sum"]["python"],
            "mode": "run",
        },
        token=token,
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
                "quest_id": qid,
                "language": "python",
                "source": SOLUTIONS[qid]["python"],
                "mode": "submit",
            },
            token=token,
        )
        assert res["passed"], (qid, res)
        assert res["reflection"] is not None, qid
        assert res["reflection"]["xp_awarded"] == 100, res["reflection"]
        assert res["progress"] is not None
        print(
            f"submit {qid} python: PASS · pattern={res['reflection']['pattern_reveal_name']} · xp={res['reflection']['xp_awarded']} · unlocked={res['progress']['unlocked_quest_ids']}"
        )

    js = req(
        "POST",
        "/submit",
        {
            "quest_id": "q01_two_sum",
            "language": "javascript",
            "source": SOLUTIONS["q01_two_sum"]["javascript"],
            "mode": "submit",
        },
        token=token,
    )
    assert js["passed"], js
    assert js["reflection"]["xp_awarded"] == 0
    print("submit q01 javascript: PASS · xp_awarded=0 (re-solve)")

    again = req("GET", "/progress", token=token)
    assert again["xp"] == 300, again
    assert set(again["completed_quest_ids"]) == {
        "q01_two_sum",
        "q02_contains_duplicate",
        "q03_valid_anagram",
    }
    print("progress reload: xp=300, all 3 completed")

    # Guest ephemeral submit still works (no auth)
    guest = req(
        "POST",
        "/submit",
        {
            "guest_id": GUEST,
            "quest_id": "q01_two_sum",
            "language": "python",
            "source": SOLUTIONS["q01_two_sum"]["python"],
            "mode": "submit",
        },
    )
    assert guest["passed"] and guest["progress"]["ephemeral"] is True
    print("guest submit ephemeral OK")
    print("ACCEPTANCE OK")


if __name__ == "__main__":
    main()
