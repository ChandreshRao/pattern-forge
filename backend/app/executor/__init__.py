from app.executor.judge0 import Judge0Executor

_executor: Judge0Executor | None = None


def get_executor() -> Judge0Executor:
    global _executor
    if _executor is None:
        _executor = Judge0Executor()
    return _executor
