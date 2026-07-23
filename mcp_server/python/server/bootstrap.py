"""NexusAOS server bootstrap helpers."""

import os
import sys
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))

BASE_DIR = _python_root.parent.parent

_PACKAGE_DIR = _python_root / "layers"
_CORE_PACKAGES = {
    "L00_Experience",
    "L01_Planning",
    "L02_Agent",
    "L03_Runtime",
    "L04_Composition",
    "L05_Memory",
    "L06_Tool",
    "L07_Integration",
    "L08_Governance",
    "L09_Observability",
    "L10_Intelligence",
    "L11_Data",
    "L12_Infrastructure",
    "L13_Hive",
    "L14_Physique",
}

_SUB_PACKAGES = {
    "compiler",
    "maintenance_core",
    "monitoring",
    "monitoring_active",
}


def setup(base_dir=None):
    base_path = Path(base_dir) if base_dir is not None else BASE_DIR
    ensure_core_packages(_PACKAGE_DIR)
    ensure_core_packages(_python_root, candidates=_SUB_PACKAGES, allow_missing=True)
    return base_path


def ensure_core_packages(root, candidates=None, allow_missing=False):
    root = Path(root)
    candidates = candidates or _CORE_PACKAGES
    for name in candidates:
        package_dir = root / name
        init_file = package_dir / "__init__.py"
        if not package_dir.is_dir():
            if allow_missing:
                continue
            raise RuntimeError(f"Missing package: {package_dir}")
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")
