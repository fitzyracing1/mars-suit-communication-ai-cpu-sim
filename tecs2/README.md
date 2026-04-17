# TECS2 Series Gate CPU

This is a second standalone simulated CPU package in the `tecs2` folder.

It is built around the design you asked for:

- 5th series profile
- 2nd return path
- 3 logic mode
- 4th gate mode
- 1A1 option mode

## Install

```bash
cd tecs2
python3 -m pip install -e .
```

Install test dependencies:

```bash
python3 -m pip install -e '.[test]'
```

## CLI

Run the built-in demo:

```bash
series-gate-cpu --demo
```

Run a custom program:

```bash
series-gate-cpu --program-file examples/series_path.cpu
```

## Instruction set

- `LOAD <register> <value>`
- `RETURN2 <source_register> <target_register>`
- `LOGIC3 <left_register> <mid_register> <right_register> <target_register>`
- `GATE4 <r1> <r2> <r3> <r4> <target_register>`
- `OPTION1A1 <primary_register> <fallback_register> <target_register>`
- `EMIT <register>`
- `HALT`
