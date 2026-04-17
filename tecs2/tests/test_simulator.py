from __future__ import annotations

import pytest

from series_gate_cpu import SeriesGateCPU


def test_series_profile_and_output_path() -> None:
    program = """
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

    cpu = SeriesGateCPU()
    cpu.load_program(program)
    result = cpu.run_with_state()

    assert result.profile.series == "5th series"
    assert result.profile.return_path == "2nd return"
    assert result.profile.logic_mode == "3 logic"
    assert result.profile.gate_mode == "4th gate"
    assert result.profile.option_mode == "1A1 option"
    assert result.state.registers["R7"] == 1
    assert result.state.output == [1]


def test_gate4_blocks_when_one_input_is_zero() -> None:
    cpu = SeriesGateCPU()
    cpu.load_program(
        "LOAD A 1\nLOAD B 1\nLOAD C 1\nLOAD D 0\nGATE4 A B C D OUT\nEMIT OUT\nHALT\n"
    )

    result = cpu.run_with_state()

    assert result.state.registers["OUT"] == 0
    assert result.state.output == [0]


def test_missing_register_raises_clear_error() -> None:
    cpu = SeriesGateCPU()
    cpu.load_program("RETURN2 R9 R1\nHALT\n")

    with pytest.raises(ValueError, match="Register R9 is not initialized"):
        cpu.run_with_state()
