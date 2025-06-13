# Overview
The Windows Registry Toolkit is a versatile Python-based utility for analyzing
and extracting data from the Windows Registry. Designed with both live system
interrogation and offline forensics in mind, this tool is ideal for cybersecurity
professionals, digital forensics analysts, red teamers, and system
administrators.
With built-in support for interactive exploration, sensitive hive dumping, and
offline hive parsing, the tool provides deep visibility into Windows system
configuration, user activity, credential storage, and much more.
Whether you're conducting incident response, malware analysis, or system
auditing, the Windows Registry Toolkit empowers you to automate and
streamline your registry investigation workflow.

# Key features
- Live Registry Exploration
● Interactively navigate the Windows Registry in real-time.
● Select from main registry hives (e.g., HKLM, HKCU, HKU, etc.).
● Recursively list subkeys and view registry values, including type information.
● Built-in support for back, exit, and direct value inspection via numbered input.

- Hive Dumping (Live Extraction)
● Automatically dump critical registry hives (SAM, SYSTEM, SECURITY, SOFTWARE,
.DEFAULT) from the live system.
● Uses Windows-native reg save command for consistent and secure extraction.
● Default save location is set to C:\Users\Public\, but easily customizable.

- Offline Hive Analysis
● Load and parse offline .hiv registry hive files (ideal for forensic investigations).
● Recursively traverse all keys, subkeys, and values—including binary blobs.
● Handles binary data with proper hex encoding for safe viewing and processing.
● Supports exporting the full structure and data into a clean, human-readable JSON
format.

# Usage
1. Live Registry Interactive Mode
python registry_tool.py -live
2. Dump Sensitive Registry Hives
python registry_tool.py -dump
Dumps:
● HKEY_LOCAL_MACHINE\SAM
● HKEY_LOCAL_MACHINE\SYSTEM
● HKEY_LOCAL_MACHINE\SECURITY
● HKEY_LOCAL_MACHINE\SOFTWARE
● HKEY_USERS\.DEFAULT
Output:
All dumped hives are saved in a dumped_hives/ folder as .hiv files.

3. Load and Parse Offline Hive File
python registry_tool.py -load <path_to_hive_file> [-output
<output_file.json>]
If -output is not specified, the output defaults to registry_output.json.

# Output Format
 JSON file contains the full recursive structure:
{
"CurrentControlSet": {
"Enum": {
"PCI": {
"VEN_8086&DEV_1234": {
"DeviceDesc": "Intel PCI Controller",
"LocationInformation": "PCI bus 0, device 2"
}
}
}
}
