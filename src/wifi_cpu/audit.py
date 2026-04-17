from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from .simulator import SimulationResult, SimulatedCPU


@dataclass
class AuditExpectation:
    halted: bool = True
    output: List[int] | None = None
    registers: Dict[str, int] = field(default_factory=dict)
    memory: Dict[str, int] = field(default_factory=dict)
    ports: Dict[str, int] = field(default_factory=dict)
    trace_contains: List[str] = field(default_factory=list)


@dataclass
class QuantumBuildSpec:
    name: str
    target: str
    simulator: str
    program: str
    expectations: AuditExpectation


@dataclass
class AuditReport:
    spec: QuantumBuildSpec
    passed: bool
    findings: List[str]
    result: SimulationResult


def load_spec(path: str | Path) -> QuantumBuildSpec:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    expectations = raw.get("expectations", {})
    return QuantumBuildSpec(
        name=raw["name"],
        target=raw.get("target", "quantum-build"),
        simulator=raw.get("simulator", "wifi_cpu"),
        program=_normalize_program(raw["program"]),
        expectations=AuditExpectation(
            halted=expectations.get("halted", True),
            output=expectations.get("output"),
            registers=expectations.get("registers", {}),
            memory=expectations.get("memory", {}),
            ports=expectations.get("ports", {}),
            trace_contains=expectations.get("trace_contains", []),
        ),
    )


def audit_quantum_build(spec: QuantumBuildSpec) -> AuditReport:
    if spec.simulator != "wifi_cpu":
        raise ValueError(f"Unsupported simulator for root audit package: {spec.simulator}")

    cpu = SimulatedCPU()
    cpu.load_program(spec.program)
    result = cpu.run_with_state()

    findings: List[str] = []
    expectations = spec.expectations

    if result.state.halted != expectations.halted:
        findings.append(
            f"Expected halted={expectations.halted}, observed halted={result.state.halted}"
        )

    if expectations.output is not None and result.state.output != expectations.output:
        findings.append(
            f"Expected output {expectations.output}, observed {result.state.output}"
        )

    findings.extend(
        _compare_mapping("register", expectations.registers, result.state.registers)
    )
    findings.extend(_compare_mapping("memory", expectations.memory, result.state.memory))
    findings.extend(_compare_mapping("port", expectations.ports, result.state.ports))

    for fragment in expectations.trace_contains:
        if not any(fragment in line for line in result.trace):
            findings.append(f"Missing trace fragment: {fragment}")

    return AuditReport(
        spec=spec,
        passed=not findings,
        findings=findings,
        result=result,
    )


def render_report(report: AuditReport) -> str:
    status = "PASS" if report.passed else "FAIL"
    lines = [
        f"AUDIT {status}: {report.spec.name}",
        f"Target: {report.spec.target}",
        f"Simulator: {report.spec.simulator}",
    ]
    if report.findings:
        lines.append("Findings:")
        lines.extend(f"- {finding}" for finding in report.findings)
    else:
        lines.append("Findings:")
        lines.append("- No audit findings")

    lines.append("Observed output:")
    lines.append(f"- output={report.result.state.output}")
    lines.append(f"- registers={report.result.state.registers}")
    lines.append(f"- memory={report.result.state.memory}")
    lines.append(f"- ports={report.result.state.ports}")
    return "\n".join(lines)


def _compare_mapping(
    label: str, expected: Dict[str, int], observed: Dict[str, int]
) -> List[str]:
    findings: List[str] = []
    for key, expected_value in expected.items():
        observed_value = observed.get(key)
        if observed_value != expected_value:
            findings.append(
                f"Expected {label} {key}={expected_value}, observed {observed_value}"
            )
    return findings


def _normalize_program(program: str | List[str]) -> str:
    if isinstance(program, list):
        return "\n".join(program) + "\n"
    return program
