## Features

- Listens dynamically to Houdini Digital Asset (HDA) cook events inside Unreal Engine.
- Extracts critical output details including index, type, name, and proxy status.
- **Batch Validator Tool:** Features a custom floating PySide UI panel to check assets for physics collision data and LOD counts instantly, raising warning notifications for failing meshes.

## Usage

Import and run the floating interface tool:

```python
import batch_validator

# Launch the visual UI dashboard window panel inside Unreal Engine
batch_validator.launch_validator_tool()
```
