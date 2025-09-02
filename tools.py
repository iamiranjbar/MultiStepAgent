import math
import signal
from dataclasses import dataclass
from typing import Dict, Callable, Any

@dataclass
class Tool:
    name: str
    fn: callable # fn(**kwargs) -> str

def _with_timeout(seconds, fn, **kw):
    def _handler(signum, frame): 
        raise TimeoutError("tool timeout")
    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(seconds)
    try: 
        return fn(**kw)
    finally: 
        signal.alarm(0)

def calculator(expr: str) -> str:
    # Replace ^ with ** for exponentiation (common user mistake)
    expr = expr.replace('^', '**')
    allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
    return str(eval(expr, {"__builtins__": {}}, allowed))

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Wrote {len(content)} chars to {path}"

TOOLS: Dict[str, Tool] = {
    "calculator": Tool("calculator", calculator),
    "read_file": Tool("read_file", read_file),
    "write_file": Tool("write_file", write_file),
}
