from __future__ import annotations

import argparse

from .simulator import SimulatedCPU


def build_program(number: str) -> str:
    return f"CALL_WIFI {number}\nHALT\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wifi-cpu",
        description="Call one number over Wi-Fi using the simulated CPU program.",
    )
    parser.add_argument(
        "number",
        nargs="?",
        default="+15551234567",
        help="Phone number to call (default: +15551234567)",
    )
    args = parser.parse_args()

    cpu = SimulatedCPU()
    cpu.load_program(build_program(args.number))
    for line in cpu.run():
        print(line)


if __name__ == "__main__":
    main()
