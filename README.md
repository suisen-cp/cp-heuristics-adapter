# cp-heuristics-adapter

[![ubuntu-latest](https://github.com/suisen-cp/cp-heuristics-adapter/actions/workflows/ubuntu-latest.yml/badge.svg)](https://github.com/suisen-cp/cp-heuristics-adapter/actions/workflows/ubuntu-latest.yml)
[![macos-latest](https://github.com/suisen-cp/cp-heuristics-adapter/actions/workflows/macos-latest.yml/badge.svg)](https://github.com/suisen-cp/cp-heuristics-adapter/actions/workflows/macos-latest.yml)
[![windows-latest](https://github.com/suisen-cp/cp-heuristics-adapter/actions/workflows/windows-latest.yml/badge.svg)](https://github.com/suisen-cp/cp-heuristics-adapter/actions/workflows/windows-latest.yml)

A tool aimed at automating various operations of AtCoder Heuristics Contest (AHC).

## Environment

- OS
  - [x] Linux
  - [x] macOS
  - [x] Windows
- Python
  - [x] 3.11
  - [x] 3.12

## Install

```bash
cd /path/to/install
git clone git@github.com:suisen-cp/cp-heuristics-adapter.git
cd /path/to/install/cp-heuristics-adapter
pip install .
```

## Uninstall

```bash
pip uninstall cp-heuristics-adapter
```

## Usage

The structure of an AHC project using this tool:

```text
.
├── .cp-heuristics-adapter  # Configuration directory
│   ├── cpp_config.toml    # C++ configuration file
│   └── py_config.toml     # Python configuration file
├── your_solver.cpp         # C++ solver
├── your_solver.py          # Python solver
├── in                      # Input files
│   ├── 0000.txt
│   ├── 0001.txt
│   └── 0002.txt
├── out                     # Output files
│   ├── 0000.txt
│   ├── 0001.txt
│   └── 0002.txt
└── scores                  # Score files
    ├── scores_20240617-000049.summary.txt
    ├── scores_20240617-000049.txt
    ├── scores_20240617-000223.summary.txt
    └── scores_20240617-000223.txt
```

### Available languages

- [x] C++
- [x] Python

### `cp-heuristics-adapter init`

Initialize a new project.

```text
usage: cp-heuristics-adapter init [-h] [-p PATH] [--overwrite]

Initialize a new project

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to project directory
  --overwrite           Overwrite existing files
```

### `cp-heuristics-adapter clean`

Clean up the project.

```text
usage: cp-heuristics-adapter clean [-h] [-p PATH]

Clean the project

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to project directory
```

### `cp-heuristics-adapter run`

Run your solver.

- In addition to your solver, **you need to add code to output the score in one line. The output destination is given as the first (0-indexed) command-line argument**.
  - In C++, you can use `argv[1]` to get the output destination. Here is [an example C++ code](templates/example_solver.cpp).
  - In Python, you can use `sys.argv[1]` to get the output destination. Here is an [example Python code](templates/example_solver.py).
- You can specify the build mode (`debug` or `release`).
  - For example, in C++, you can enable `-g -fsanitize=address` only in `debug` mode and `-O2` only in `release` mode.
  - The settings for each build mode are to be written in the configuration files in the `.cp-heuristics-adapter` directory.

```text
usage: cp-heuristics-adapter run [-h] [-b {debug,release}] [-t TIME_LIMIT] [-s {plain,log}] source number

Run the program

positional arguments:
  source                Path to source file.
  number                Number of cases to run.

options:
  -h, --help            show this help message and exit
  -b {debug,release}, --build-mode {debug,release}
                        Build mode. Default is 'debug'.
  -t TIME_LIMIT, --time-limit TIME_LIMIT
                        Time limit for execution. Default is 2.0 seconds.
  -s {plain,log}, --score-type {plain,log}
                        Type of score. If a standings is calculated by the relative score, it is recommended to use 'log' type.
                        Default is 'plain'.
```
