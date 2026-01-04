import argparse, json
from pathlib import Path
from recovery.crypto import verify_signature
from recovery.integrity import verify_hash_chain, get_run_hash

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()

    run = json.load(open(args.run))

    ok, err = verify_hash_chain(run["step_logs"])
    if not ok:
        raise RuntimeError(err)

    computed = get_run_hash(run["step_logs"])
    if computed != run["run_hash"]:
        raise RuntimeError("Run hash mismatch")

    pub = Path(args.key).read_bytes()
    if not verify_signature(run["run_hash"].encode(), run["run_signature"], pub):
        raise RuntimeError("Bad signature")

    print("Verification OK")

if __name__ == "__main__":
    main()
