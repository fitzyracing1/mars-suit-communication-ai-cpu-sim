from __future__ import annotations

import argparse
from pathlib import Path

from .simulator import SeriesGateCPU


DEMO_PROGRAM = """\
# 5th series / 2nd return / 3 logic / 4th gate / 1A1 option demo
LOAD R1 1
LOAD R2 0
LOAD R3 1
RETURN2 R1 R4
LOGIC3 R1 R2 R3 R5
GATE4 R1 R3 R4 R5 R6
OPTION1A1 R2 R6 R7
EMIT R7
HALT
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="series-gate-cpu",
        description="Run the second simulated CPU in the 5th series profile.",
    )
    parser.add_argument(
        "--program-file",
        type=Path,
        help="Path to a custom TECS2 program file",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the built-in TECS2 demo",
    )
    args = parser.parse_args()

    cpu = SeriesGateCPU()
    if args.program_file:
        cpu.load_program(args.program_file.read_text(encoding="utf-8"))
    else:
        cpu.load_program(DEMO_PROGRAM)

    result = cpu.run_with_state()
    for line in result.trace:
        print(line)
    print(f"REGISTERS: {result.state.registers}")
    print(f"OUTPUT: {result.state.output}")
