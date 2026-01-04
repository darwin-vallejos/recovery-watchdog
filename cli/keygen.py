import argparse
from pathlib import Path
from recovery.crypto import generate_keypair

def main():
    parser = argparse.ArgumentParser(description="Generate signing keypair")
    parser.add_argument("--output", required=True, help="Key name (no extension)")
    args = parser.parse_args()

    base = Path(args.output)
    priv = base.with_suffix(".private.pem")
    pub = base.with_suffix(".public.pem")

    if priv.exists() or pub.exists():
        print("Keys already exist.")
        return

    private_pem, public_pem = generate_keypair()

    priv.parent.mkdir(parents=True, exist_ok=True)
    priv.write_bytes(private_pem)
    priv.chmod(0o600)
    pub.write_bytes(public_pem)

    print("Keys generated:")
    print(priv)
    print(pub)

if __name__ == "__main__":
    main()
