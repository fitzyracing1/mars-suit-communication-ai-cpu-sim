from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Instruction:
    op: str
    args: Tuple[str, ...]


@dataclass
class CPUState:
    pc: int = 0
    halted: bool = False
    registers: Dict[str, int] = field(default_factory=dict)
    memory: Dict[str, int] = field(default_factory=dict)
    ports: Dict[str, int] = field(default_factory=dict)
    output: List[int] = field(default_factory=list)


@dataclass
class SimulationResult:
    trace: List[str]
    state: CPUState


class SimulatedCPU:
    """Small test-oriented CPU simulator for logic and data-flow experiments."""

    def __init__(self) -> None:
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
            op = parts[0].upper()
            args = tuple(parts[1:])
            self.program.append(Instruction(op, args))
        self.reset()

    def run(self) -> List[str]:
        return self.run_with_state().trace

    def run_with_state(self) -> SimulationResult:
        trace: List[str] = []
        while not self.state.halted and self.state.pc < len(self.program):
            instr = self.program[self.state.pc]
            current_pc = self.state.pc
            self.state.pc += 1
            self._execute(instr, trace, current_pc)
        return SimulationResult(trace=trace, state=self.state)

    def _execute(self, instr: Instruction, trace: List[str], current_pc: int) -> None:
        op = instr.op

        if op == "LOAD":
            self._require_args(op, instr.args, 2)
            register, value = instr.args
            parsed = self._parse_value(value)
            self.state.registers[register] = parsed
            trace.append(f"PC {current_pc}: LOAD {register} <= {parsed}")
            return

        if op == "MOVE":
            self._require_args(op, instr.args, 2)
            source, target = instr.args
            value = self._read_register(source)
            self.state.registers[target] = value
            trace.append(f"PC {current_pc}: MOVE {source} ({value}) -> {target}")
            return

        if op == "ADD":
            self._require_args(op, instr.args, 3)
            left, right, target = instr.args
            result = self._read_register(left) + self._read_register(right)
            self.state.registers[target] = result
            trace.append(f"PC {current_pc}: ADD {left} + {right} -> {target} ({result})")
            return

        if op == "SUB":
            self._require_args(op, instr.args, 3)
            left, right, target = instr.args
            result = self._read_register(left) - self._read_register(right)
            self.state.registers[target] = result
            trace.append(f"PC {current_pc}: SUB {left} - {right} -> {target} ({result})")
            return

        if op == "STORE":
            self._require_args(op, instr.args, 2)
            register, address = instr.args
            value = self._read_register(register)
            self.state.memory[address] = value
            trace.append(f"PC {current_pc}: STORE {register} ({value}) -> MEM[{address}]")
            return

        if op == "READ":
            self._require_args(op, instr.args, 2)
            address, register = instr.args
            value = self.state.memory.get(address, 0)
            self.state.registers[register] = value
            trace.append(f"PC {current_pc}: READ MEM[{address}] ({value}) -> {register}")
            return

        if op == "SEND":
            self._require_args(op, instr.args, 2)
            register, port = instr.args
            value = self._read_register(register)
            self.state.ports[port] = value
            trace.append(f"PC {current_pc}: SEND {register} ({value}) -> PORT[{port}]")
            return

        if op == "RECV":
            self._require_args(op, instr.args, 2)
            port, register = instr.args
            value = self.state.ports.get(port, 0)
            self.state.registers[register] = value
            trace.append(f"PC {current_pc}: RECV PORT[{port}] ({value}) -> {register}")
            return

        if op == "EMIT":
            self._require_args(op, instr.args, 1)
            register = instr.args[0]
            value = self._read_register(register)
            self.state.output.append(value)
            trace.append(f"PC {current_pc}: EMIT {register} ({value})")
            return

        if op == "CALL_WIFI":
            self._require_args(op, instr.args, 1)
            number = instr.args[0]
            trace.extend(self._simulate_wifi_call(current_pc, number))
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

    @staticmethod
    def _parse_value(raw: str) -> int:
        return int(raw)

    def _read_register(self, register: str) -> int:
        if register not in self.state.registers:
            raise ValueError(f"Register {register} is not initialized")
        return self.state.registers[register]

    def _simulate_wifi_call(self, current_pc: int, number: str) -> List[str]:
        if not number or any(ch not in "+0123456789" for ch in number):
            raise ValueError(f"Invalid phone number: {number}")
        return [
            f"PC {current_pc}: Wi-Fi call stack initialized",
            f"PC {current_pc}: VoWiFi session established",
            f"PC {current_pc}: Dialing {number} over Wi-Fi",
            f"PC {current_pc}: Call connected to {number}",
        ]
