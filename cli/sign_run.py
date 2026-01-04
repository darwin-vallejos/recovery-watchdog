#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from recovery.crypto import sign_data
from recovery.integrity import get_run_hash, verify_hash_chain


def main():
    parser = argparse.ArgumentParser(description="Sign a coherence-engine run")
    parser.add_argument("--run", required=True, help="Path to experiment_result.json")
    parser.add_argument("--key", required=True, help="Private key PEM file")
    parser.add_argument("--output", required=True, help="Output signed JSON file")
    args = parser.parse_args()

    # Load run JSON (BOM-safe)
    with open(args.run, "r", encoding="utf-8-sig") as f:
        run_data = json.load(f)

    if "step_logs" not in run_data:
        raise RuntimeError("Run file missing 'step_logs'")

    ok, err = verify_hash_chain(run_data["step_logs"])
    if not ok:
        raise RuntimeError(f"Hash chain verification failed: {err}")

    print(f"✓ Hash chain verified ({len(run_data['step_logs'])} steps)")

    run_hash = get_run_hash(run_data["step_logs"])
    print(f"✓ Run hash: {run_hash}")

    private_key = Path(args.key).read_bytes()
    signature = sign_data(run_hash.encode("utf-8"), private_key)

    run_data["run_hash"] = run_hash
    run_data["run_signature"] = signature
    run_data["signer_key"] = Path(args.key).stem

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(run_data, f, indent=2)

    print(f"✓ Signed run saved to: {args.output}")


if __name__ == "__main__":
    main()
