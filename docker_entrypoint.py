import os
import subprocess
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def main() -> None:
    if not os.path.exists(os.path.join(DATA_DIR, "orders.csv")):
        print("No seed data found - generating...")
        subprocess.run([sys.executable, "seed_data.py"], check=True)

    subprocess.run(
        ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-f", "definitions.py"],
        check=True,
    )


if __name__ == "__main__":
    main()
