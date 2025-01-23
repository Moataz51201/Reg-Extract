# Reg-Extract

A Python-based tool for exploring and analyzing the Windows registry. The tool supports both live system registry exploration and offline hive analysis, providing detailed insights into registry keys, values, and structure.

---

## Features

- **Interactive Live Registry Exploration**: 
  - Explore the live Windows registry interactively by selecting hives and navigating through subkeys.
  - View registry values with their data and types.

- **Offline Registry Hive Analysis**:
  - Load and parse offline registry hive files.
  - Extract and traverse the full registry structure of the hive.
  - Save extracted data in a structured JSON format.

- **Flexible Output**:
  - Specify an output file name for saving offline hive analysis results (default: `registry_output.json`).

## Prerequisites

- Python 3.6+
- Required libraries:
  - `argparse`: Built-in Python module for parsing command-line arguments.
  - `winreg`: Built-in module for accessing live Windows registry (Windows only).
  - `python-registry`: For processing offline registry hives. Install via:
    pip install python-registry

# Usage
General Syntax
python registry_explorer.py [OPTIONS]

# Options
-live: Explore the live Windows registry interactively.
-load <HIVE_PATH>: Load an offline registry hive file for analysis.
-output <OUTPUT_FILE>: Specify the output file name for offline hive analysis (default: registry_output.json).

# Explore the Live Registry
python registry_explorer.py -live

# Analyze an Offline Hive File 
python registry_explorer.py -load C:\Path\To\Offline\Hive -output custom_output.json

# Limitations
Permissions: Accessing certain registry keys or values may require administrative privileges.
Platform: The live registry exploration feature only works on Windows systems.
