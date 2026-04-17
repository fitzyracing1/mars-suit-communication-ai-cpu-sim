# Simulated CPU Quantum Build Audit Toolkit

This project is packaged as an installable Python program named `wifi-cpu`.
It now acts as an audit toolkit for simulated CPU builds, with a focus on logic
flow, data flow, and audit checks for claimed quantum-style builds.

Project site:
`https://fitzyracing1.github.io/mars-suit-communication-ai-cpu-sim/`

## What it does

It gives people a small simulated CPU they can install from pip and use to test:

- logic flow between instructions
- data flow through registers, memory, ports, and output
- custom programs loaded from text files
- audit specifications that verify a build against expected CPU behavior
- a Wi-Fi call demo path for the original concept

## Install as a program

From the project root:

```bash
python3 -m pip install -e .
```

This installs a command-line program:

```bash
wifi-cpu --demo
```

You can also install test dependencies:

```bash
python3 -m pip install -e '.[test]'
```

## Example usage

Run the built-in demo:

```bash
wifi-cpu --demo
```

Run the Wi-Fi call path:

```bash
wifi-cpu +14155550123
```

Run a custom program file:

```bash
wifi-cpu --program-file examples/data_flow.cpu
```

Run an audit spec:

```bash
wifi-cpu --audit-file examples/quantum_build_audit.json
```

Use it from Python:

```python
from wifi_cpu import SimulatedCPU

program = """
LOAD R1 5
LOAD R2 8
ADD R1 R2 R3
EMIT R3
HALT
"""

cpu = SimulatedCPU()
cpu.load_program(program)
result = cpu.run_with_state()
print(result.trace)
print(result.state.output)
```

## Instruction set

- `LOAD <register> <value>`
- `MOVE <source_register> <target_register>`
- `ADD <left_register> <right_register> <target_register>`
- `SUB <left_register> <right_register> <target_register>`
- `STORE <register> <memory_key>`
- `READ <memory_key> <register>`
- `SEND <register> <port_name>`
- `RECV <port_name> <register>`
- `EMIT <register>`
- `CALL_WIFI <number>`
- `HALT`

## Audit spec format

Audit files are JSON documents that declare a target build, a simulator, a
program, and the expected observed behavior.

```json
{
  "name": "Quantum Uplink Build",
  "target": "uplink-audit",
  "simulator": "wifi_cpu",
  "program": [
    "LOAD R1 5",
    "LOAD R2 8",
    "ADD R1 R2 R3",
    "EMIT R3",
    "HALT"
  ],
  "expectations": {
    "halted": true,
    "output": [13],
    "registers": {"R3": 13},
    "trace_contains": ["EMIT R3"]
  }
}
```

If an audit expectation does not match the simulated CPU result, the CLI exits
with a failing status and lists the findings.

## Testing

Run the tests:

```bash
pytest
```

Build distributable files:

```bash
python3 -m pip install '.[build]'
python3 -m build
```

The built wheel and source tarball will be created in `dist/`.

## Publishing

Build locally:

```bash
python3 -m build
```

Upload manually with Twine:

```bash
python3 -m pip install twine
python3 -m twine upload dist/*
```

Or use the GitHub Actions workflow in `.github/workflows/publish-pypi.yml`
with PyPI Trusted Publishing after configuring the project on PyPI.

## Project structure

- `pyproject.toml`: package metadata and CLI entry point
- `src/wifi_cpu/simulator.py`: simulator core
- `src/wifi_cpu/audit.py`: audit model and report generation
- `src/wifi_cpu/cli.py`: command-line interface
- `tests/test_simulator.py`: package tests
- `tests/test_audit.py`: audit tests
- `examples/data_flow.cpu`: sample custom program
- `examples/quantum_build_audit.json`: sample audit spec
- `cpu_simulator.py`: compatibility launcher
- `index.html`: GitHub Pages landing page
- `robots.txt` and `sitemap.xml`: crawler metadata
