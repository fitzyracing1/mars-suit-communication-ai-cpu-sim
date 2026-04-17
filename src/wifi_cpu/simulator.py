from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Instruction:
    op: str
    args: Tuple[str, ...]


class SimulatedCPU:
    """Minimal simulator that only performs one action: call a number over Wi-Fi."""

    def __init__(self) -> None:
        self.pc = 0
        self.halted = False
        self.program: List[Instruction] = []

    def load_program(self, program_text: str) -> None:
        self.program = []
        for raw_line in program_text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.replace(",", " ").split()
            op = parts[0].upper()
            args = tuple(parts[1:])
            self.program.append(Instruction(op, args))
        self.pc = 0
        self.halted = False

    def run(self) -> List[str]:
        trace: List[str] = []
        while not self.halted and self.pc < len(self.program):
            instr = self.program[self.pc]
            self.pc += 1
            self._execute(instr, trace)
        return trace

    def _execute(self, instr: Instruction, trace: List[str]) -> None:
        if instr.op == "CALL_WIFI":
            if len(instr.args) != 1:
                raise ValueError("CALL_WIFI requires exactly one argument: a phone number")
            number = instr.args[0]
            self._validate_number(number)
            trace.extend(self._simulate_wifi_call(number))
            return

        if instr.op == "HALT":
            self.halted = True
            trace.append("HALT: execution stopped")
            return

        raise ValueError(f"Unknown instruction: {instr.op}")

    @staticmethod
    def _validate_number(number: str) -> None:
        if not re.fullmatch(r"\+?\d+", number):
            raise ValueError(f"Invalid phone number: {number}")

    @staticmethod
    def _simulate_wifi_call(number: str) -> List[str]:
        return [
            "Wi-Fi call stack initialized",
            "VoWiFi session established",
            f"Dialing {number} over Wi-Fi",
            f"Call connected to {number}",
        ]
