from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class CPUProfile:
    series: str = "5th series"
    return_path: str = "2nd return"
    logic_mode: str = "3 logic"
    gate_mode: str = "4th gate"
    option_mode: str = "1A1 option"


@dataclass
class Instruction:
    op: str
    args: Tuple[str, ...]


@dataclass
class CPUState:
    pc: int = 0
    halted: bool = False
    registers: Dict[str, int] = field(default_factory=dict)
    output: List[int] = field(default_factory=list)


@dataclass
class SimulationResult:
    trace: List[str]
    state: CPUState
    profile: CPUProfile


class SeriesGateCPU:
    """A themed second CPU simulator for return, logic, gate, and option routing."""

    def __init__(self) -> None:
        self.profile = CPUProfile()
        self.program: List[Instruction] = []
        self.state = CPUState()

    def reset(self) -> None:
        self.state = CPUState()

    def load_program(self, program_text: str) -> None:
        self.program = []
        for raw_line in program_text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.replace(",", " ").split()
            self.program.append(Instruction(parts[0].upper(), tuple(parts[1:])))
        self.reset()

    def run_with_state(self) -> SimulationResult:
        trace = [
            f"Profile active: {self.profile.series}, {self.profile.return_path}, "
            f"{self.profile.logic_mode}, {self.profile.gate_mode}, {self.profile.option_mode}"
        ]
        while not self.state.halted and self.state.pc < len(self.program):
            instruction = self.program[self.state.pc]
            current_pc = self.state.pc
            self.state.pc += 1
            self._execute(instruction, trace, current_pc)
        return SimulationResult(trace=trace, state=self.state, profile=self.profile)

    def _execute(self, instruction: Instruction, trace: List[str], current_pc: int) -> None:
        op = instruction.op

        if op == "LOAD":
            self._require_args(op, instruction.args, 2)
            register, value = instruction.args
            parsed = int(value)
            self.state.registers[register] = parsed
            trace.append(f"PC {current_pc}: LOAD {register} <= {parsed}")
            return

        if op == "RETURN2":
            self._require_args(op, instruction.args, 2)
            source, target = instruction.args
            value = self._read_register(source)
            self.state.registers[target] = value
            trace.append(f"PC {current_pc}: RETURN2 {source} ({value}) -> {target}")
            return

        if op == "LOGIC3":
            self._require_args(op, instruction.args, 4)
            left, middle, right, target = instruction.args
            values = [self._read_register(left), self._read_register(middle), self._read_register(right)]
            result = 1 if sum(1 for value in values if value != 0) >= 2 else 0
            self.state.registers[target] = result
            trace.append(
                f"PC {current_pc}: LOGIC3 {left}/{middle}/{right} -> {target} ({result})"
            )
            return

        if op == "GATE4":
            self._require_args(op, instruction.args, 5)
            first, second, third, fourth, target = instruction.args
            inputs = [
                self._read_register(first),
                self._read_register(second),
                self._read_register(third),
                self._read_register(fourth),
            ]
            result = 1 if all(value != 0 for value in inputs) else 0
            self.state.registers[target] = result
            trace.append(
                f"PC {current_pc}: GATE4 {first}/{second}/{third}/{fourth} -> {target} ({result})"
            )
            return

        if op == "OPTION1A1":
            self._require_args(op, instruction.args, 3)
            primary, fallback, target = instruction.args
            primary_value = self._read_register(primary)
            fallback_value = self._read_register(fallback)
            result = primary_value if primary_value != 0 else fallback_value
            self.state.registers[target] = result
            trace.append(
                f"PC {current_pc}: OPTION1A1 {primary}/{fallback} -> {target} ({result})"
            )
            return

        if op == "EMIT":
            self._require_args(op, instruction.args, 1)
            register = instruction.args[0]
            value = self._read_register(register)
            self.state.output.append(value)
            trace.append(f"PC {current_pc}: EMIT {register} ({value})")
            return

        if op == "HALT":
            self.state.halted = True
            trace.append(f"PC {current_pc}: HALT")
            return

        raise ValueError(f"Unknown instruction: {op}")

    @staticmethod
    def _require_args(op: str, args: Tuple[str, ...], expected: int) -> None:
        if len(args) != expected:
            raise ValueError(f"{op} requires exactly {expected} arguments")

    def _read_register(self, register: str) -> int:
        if register not in self.state.registers:
            raise ValueError(f"Register {register} is not initialized")
        return self.state.registers[register]
