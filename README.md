# Mars Suit Communication AI CPU Sim

This project is packaged as an installable Python program named `wifi-cpu` and
also includes a minimal landing page plus sitemap metadata for GitHub Pages.

## What it does

It performs one action only: call one phone number over Wi-Fi.

## Install as a program

From the project root:

```bash
python3 -m pip install -e .
```

This installs a command-line program:

```bash
wifi-cpu
```

You can pass a number:

```bash
wifi-cpu +14155550123
```

Phone number format accepted:
- Digits only, such as `15551234567`
- Optional leading `+`, such as `+15551234567`

## Project structure

- `pyproject.toml`: package metadata and CLI entry point
- `src/wifi_cpu/simulator.py`: simulator core
- `src/wifi_cpu/cli.py`: command-line interface
- `cpu_simulator.py`: compatibility launcher
- `index.html`: GitHub Pages landing page
- `robots.txt` and `sitemap.xml`: crawler metadata
