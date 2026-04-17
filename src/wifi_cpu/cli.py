from __future__ import annotations

import argparse
from pathlib import Path

from .audit import audit_quantum_build, load_spec, render_report
from .simulator import SimulatedCPU


DEFAULT_PROGRAM = """\
# Demo program: move a value through memory and an output port.
LOAD R1 7
LOAD R2 9
ADD R1 R2 R3
STORE R3 BUFFER
READ BUFFER R4
SEND R4 UPLINK
RECV UPLINK R5
EMIT R5
HALT
"""


def build_wifi_program(number: str) -> str:
    return f"CALL_WIFI {number}\nHALT\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wifi-cpu",
        description="Run or audit simulated CPU programs for logic, data flow, and build validation.",
    )
    parser.add_argument(
        "number",
        nargs="?",
        help="Phone number to call with the Wi-Fi demo path",
    )
    parser.add_argument(
        "--program-file",
        type=Path,
        help="Path to a custom CPU program file",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the built-in logic and data-flow demo program",
    )
    parser.add_argument(
        "--audit-file",
        type=Path,
        help="Path to a quantum-build audit spec in JSON format",
    )
    args = parser.parse_args()

    if args.audit_file:
        report = audit_quantum_build(load_spec(args.audit_file))
        print(render_report(report))
        if not report.passed:
            raise SystemExit(1)
        return

    cpu = SimulatedCPU()

    if args.program_file:
        cpu.load_program(args.program_file.read_text(encoding="utf-8"))
    elif args.demo or not args.number:
        cpu.load_program(DEFAULT_PROGRAM)
    else:
        cpu.load_program(build_wifi_program(args.number))

    result = cpu.run_with_state()
    for line in result.trace:
        print(line)

    print(f"REGISTERS: {result.state.registers}")
    print(f"MEMORY: {result.state.memory}")
    print(f"PORTS: {result.state.ports}")
    print(f"OUTPUT: {result.state.output}")
