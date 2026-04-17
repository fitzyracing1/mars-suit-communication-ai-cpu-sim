from __future__ import annotations

from pathlib import Path

from wifi_cpu.audit import audit_quantum_build, load_spec


def test_quantum_build_audit_passes_for_matching_spec() -> None:
    spec_path = Path(__file__).resolve().parents[1] / "examples" / "quantum_build_audit.json"
    report = audit_quantum_build(load_spec(spec_path))

    assert report.passed is True
    assert report.findings == []
    assert report.result.state.output == [13]


def test_quantum_build_audit_reports_mismatched_output() -> None:
    spec_path = Path(__file__).resolve().parents[1] / "examples" / "quantum_build_audit.json"
    spec = load_spec(spec_path)
    spec.expectations.output = [99]

    report = audit_quantum_build(spec)

    assert report.passed is False
    assert any("Expected output [99], observed [13]" in finding for finding in report.findings)
