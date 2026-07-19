/** Known-good solutions — mirrored from scripts/verify_phase1a.py */
export const SOLUTIONS = {
  q01_two_sum: {
    python: `
from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}
    for i, n in enumerate(nums):
        need = target - n
        if need in seen:
            return [seen[need], i]
        seen[n] = i
    return []
`.trim(),
    javascript: `
function twoSum(nums, target) {
  const seen = {};
  for (let i = 0; i < nums.length; i++) {
    const need = target - nums[i];
    if (need in seen) return [seen[need], i];
    seen[nums[i]] = i;
  }
  return [];
}
`.trim(),
  },
  q02_contains_duplicate: {
    python: `
from typing import List

def contains_duplicate(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))
`.trim(),
  },
} as const
