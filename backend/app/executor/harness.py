from __future__ import annotations

import json
from typing import Any


def _json_literal(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_python_harness(source: str, function_name: str, tests: list[dict[str, Any]]) -> str:
    tests_json = _json_literal(tests)
    return f"""{source}

# --- PatternForge harness ---
import json as _json

_TESTS = _json.loads({tests_json!r})
_RESULTS = []

def _pf_equal(a, b):
    if isinstance(a, list) and isinstance(b, list) and a and b and isinstance(a[0], list):
        return sorted(tuple(sorted(g)) for g in a) == sorted(tuple(sorted(g)) for g in b)
    return a == b

for _case in _TESTS:
    _cid = _case["id"]
    _inp = _case["input"]
    _exp = _case["expected"]
    try:
        _actual = {function_name}(**_inp)
        _ok = _pf_equal(_actual, _exp)
        _RESULTS.append({{
            "id": _cid,
            "passed": _ok,
            "expected": _exp,
            "actual": _actual,
            "error": None,
        }})
    except Exception as _e:
        _RESULTS.append({{
            "id": _cid,
            "passed": False,
            "expected": _exp,
            "actual": None,
            "error": f"{{type(_e).__name__}}: {{_e}}",
        }})

print("PF_RESULTS:" + _json.dumps(_RESULTS, default=str))
"""


def build_js_harness(source: str, function_name: str, tests: list[dict[str, Any]]) -> str:
    tests_json = _json_literal(tests)
    return f"""{source}

// --- PatternForge harness ---
const _TESTS = {tests_json};
const _RESULTS = [];

function _deepEqual(a, b) {{
  if (Array.isArray(a) && Array.isArray(b) && a.length && b.length && Array.isArray(a[0])) {{
    const norm = (groups) => JSON.stringify(groups.map((g) => g.slice().sort()).sort((x, y) => JSON.stringify(x).localeCompare(JSON.stringify(y))));
    return norm(a) === norm(b);
  }}
  return JSON.stringify(a) === JSON.stringify(b);
}}

for (const _case of _TESTS) {{
  const _cid = _case.id;
  const _inp = _case.input;
  const _exp = _case.expected;
  try {{
    const _args = Object.values(_inp);
    const _actual = {function_name}(..._args);
    const _ok = _deepEqual(_actual, _exp);
    _RESULTS.push({{
      id: _cid,
      passed: _ok,
      expected: _exp,
      actual: _actual,
      error: null,
    }});
  }} catch (_e) {{
    _RESULTS.push({{
      id: _cid,
      passed: false,
      expected: _exp,
      actual: null,
      error: String(_e && _e.stack ? _e.stack : _e),
    }});
  }}
}}

console.log("PF_RESULTS:" + JSON.stringify(_RESULTS));
"""


def build_ts_harness(source: str, function_name: str, tests: list[dict[str, Any]]) -> str:
    # Judge0 TypeScript 3.7: avoid Object.values and typed catch bindings.
    tests_json = _json_literal(tests)
    return f"""{source}

// --- PatternForge harness ---
const _TESTS: any[] = {tests_json};
const _RESULTS: any[] = [];

function _deepEqual(a: any, b: any): boolean {{
  if (Array.isArray(a) && Array.isArray(b) && a.length && b.length && Array.isArray(a[0])) {{
    const norm = (groups: any[]) => JSON.stringify(groups.map((g: any[]) => g.slice().sort()).sort((x: any, y: any) => JSON.stringify(x).localeCompare(JSON.stringify(y))));
    return norm(a) === norm(b);
  }}
  return JSON.stringify(a) === JSON.stringify(b);
}}

function _argValues(inp: any): any[] {{
  const out: any[] = [];
  for (const k in inp) {{
    if (Object.prototype.hasOwnProperty.call(inp, k)) {{
      out.push(inp[k]);
    }}
  }}
  return out;
}}

for (let _i = 0; _i < _TESTS.length; _i++) {{
  const _case = _TESTS[_i];
  const _cid = _case.id;
  const _inp = _case.input;
  const _exp = _case.expected;
  try {{
    const _args = _argValues(_inp);
    const _fn: any = {function_name};
    const _actual = _fn.apply(null, _args);
    const _ok = _deepEqual(_actual, _exp);
    _RESULTS.push({{
      id: _cid,
      passed: _ok,
      expected: _exp,
      actual: _actual,
      error: null,
    }});
  }} catch (_e) {{
    _RESULTS.push({{
      id: _cid,
      passed: false,
      expected: _exp,
      actual: null,
      error: String(_e),
    }});
  }}
}}

console.log("PF_RESULTS:" + JSON.stringify(_RESULTS));
"""


def build_harness(source: str, language: str, function_name: str, tests: list[dict[str, Any]]) -> str:
    if language == "python":
        return build_python_harness(source, function_name, tests)
    if language == "javascript":
        return build_js_harness(source, function_name, tests)
    if language == "typescript":
        return build_ts_harness(source, function_name, tests)
    raise ValueError(f"Unsupported language: {language}")
