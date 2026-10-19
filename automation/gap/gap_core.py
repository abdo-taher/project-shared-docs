"""The capitalix.api-gap.v1 request logic lives in exactly one place: tools/capitalix_gap_core.py.

The consumer CLI and this automation both use it, so validation, sanitization and the fingerprint
cannot drift between them. This module only loads it under the name the automation modules import.
"""

import importlib.util
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
# In the repository the single copy is tools/capitalix_gap_core.py; inside the sandbox the tooling is staged
# (gap_sandbox.stage_tools) with that file next to this one.
_PATH = next(p for p in (_HERE.parent.parent / "tools" / "capitalix_gap_core.py", _HERE / "capitalix_gap_core.py")
             if p.is_file())
_spec = importlib.util.spec_from_file_location("capitalix_gap_core", _PATH)
_module = importlib.util.module_from_spec(_spec)
sys.modules["capitalix_gap_core"] = _module
_spec.loader.exec_module(_module)
globals().update({k: v for k, v in vars(_module).items() if not (k.startswith("__") and k.endswith("__"))})
