from __future__ import annotations

import pytest

from wifi_cpu import SimulatedCPU


def test_data_flow_program_moves_values_through_cpu_parts() -> None:
    program = """
    LOAD R1 12
    LOAD R2 30
    ADD R1 R2 R3
    STORE R3 CACHE
    READ CACHE R4
    SEND R4 RADIO
    RECV RADIO R5
    EMIT R5
    HALT
    """

    cpu = SimulatedCPU()
    cpu.load_program(program)
    result = cpu.run_with_state()

    assert result.state.registers["R3"] == 42
    assert result.state.memory["CACHE"] == 42
    assert result.state.ports["RADIO"] == 42
    assert result.state.output == [42]
    assert result.state.halted is True


def test_wifi_call_instruction_keeps_demo_path_available() -> None:
    cpu = SimulatedCPU()
    cpu.load_program("CALL_WIFI +15551234567\nHALT\n")

    result = cpu.run_with_state()

    assert any("Dialing +15551234567 over Wi-Fi" in line for line in result.trace)
    assert result.state.halted is True


def test_uninitialized_register_raises_clear_error() -> None:
    cpu = SimulatedCPU()
    cpu.load_program("EMIT R9\nHALT\n")

    with pytest.raises(ValueError, match="Register R9 is not initialized"):
        cpu.run_with_state()
