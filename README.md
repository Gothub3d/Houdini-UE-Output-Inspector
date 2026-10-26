# Houdini UE Output Inspector

A Python script for Unreal Engine that hooks into the Houdini Engine Public API, listens for HDA cook events, and exports generated output data to a CSV for pipeline auditing.

## Features

- Listens dynamically to Houdini Digital Asset (HDA) cook events inside Unreal Engine.
- Extracts critical output details including index, type, name, and proxy status.
- Automates reporting by exporting clean, production-ready CSV files for pipeline auditing.

## Usage

Import the module and run the export function:

```python
import test_hda

# Run with default path
test_hda.export_hda_report()
```
