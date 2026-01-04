import hashlib
import json
from typing import Tuple


def compute_step_hash(step_data: dict, prev_hash: str) -> str:
    clean = {k: v for k, v in step_data.items() if k != "step_hash"}
    canonical = json.dumps(clean, sort_keys=True, separators=(",", ":"))
    payload = prev_hash.encode("utf-8") + canonical.encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_hash_chain(step_logs: list[dict]) -> Tuple[bool, str | None]:
    prev = "GENESIS"
    for i, step in enumerate(step_logs):
        expected = compute_step_hash(step, prev)
        if step.get("step_hash") != expected:
            return False, f"Hash mismatch at step {i}"
        prev = expected
    return True, None


def get_run_hash(step_logs: list[dict]) -> str:
    if not step_logs:
        return ""
    return step_logs[-1]["step_hash"]
