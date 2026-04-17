from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")


setup(
    name="wifi-cpu",
    version="0.2.0",
    description="Audit-friendly simulated CPU toolkit for logic, data-flow, and quantum-build checks",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Joshua Fitzgerald",
    author_email="fitzyracing1@gmail.com",
    url="https://github.com/fitzyracing1/mars-suit-communication-ai-cpu-sim",
    license="MIT",
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    entry_points={"console_scripts": ["wifi-cpu=wifi_cpu.cli:main"]},
    extras_require={
        "test": ["pytest>=8.2"],
        "build": ["build>=1.2"],
    },
    project_urls={
        "Homepage": "https://fitzyracing1.github.io/mars-suit-communication-ai-cpu-sim/",
        "Repository": "https://github.com/fitzyracing1/mars-suit-communication-ai-cpu-sim",
        "Issues": "https://github.com/fitzyracing1/mars-suit-communication-ai-cpu-sim/issues",
    },
    keywords=["simulator", "cpu", "audit", "quantum-build", "testing"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
