# Specialization framework applied (AGENTS.md line 36-39): AB/AP balance + DNA blueprint + governance + provenance + Voice DNA. Source: dataset/ab_ap_balance/AB_AP_BALANCE_RULES.md + archives/dna_core/blueprints/COMPLETE_ARCHITECTURE.md.
"""
SkeletalRegistry — Skeletal / Structural System
Biological analog: Bones, cartilage, structural support, mineral storage

Responsibilities (1:1 biology mapping):
- Schema registry / DDL versioning
- Structural integrity validation
- Mineral storage (config defaults/calcium analog)
- Growth / schema migration
- Joint flexibility (API version tolerance)
"""

from __future__ import annotations

import sys
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))
BASE_DIR = _python_root.parent.parent

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

TOOL_BASE_DIR = BASE_DIR


@dataclass
class Bone:
    id: str
    name: str
    schema_version: str
    structure: Dict[str, Any]
    density: float = 80.0
    last_migration: Optional[str] = None
    created_at: float = field(default_factory=time.time)


@dataclass
class SkeletalState:
    bones: Dict[str, Bone] = field(default_factory=dict)
    marrow: Dict[str, Any] = field(default_factory=dict)  # config defaults
    calcium_reserves: float = 100.0
    growth_plates: List[str] = field(default_factory=list)


class SkeletalRegistry:
    """Structural schema registry — skeleton of the system."""

    def __init__(self, base_dir: Path = TOOL_BASE_DIR):
        self.base_dir = base_dir
        self.state = SkeletalState()

    def register_schema(self, name: str, schema: Dict[str, Any], version: str = "1.0.0") -> Dict:
        """Register a new schema (bone)."""
        bone_id = str(uuid.uuid4())
        self.state.bones[bone_id] = Bone(
            id=bone_id,
            name=name,
            schema_version=version,
            structure=schema,
        )

        return {
            "registered": True,
            "bone_id": bone_id,
            "name": name,
            "version": version,
        }

    def migrate_schema(self, bone_id: str, new_version: str, migrations: Dict[str, Any]) -> Dict:
        """Migrate schema to new version."""
        if bone_id not in self.state.bones:
            return {"migrated": False, "reason": "bone_not_found", "bone_id": bone_id}

        bone = self.state.bones[bone_id]
        bone.schema_version = new_version
        bone.structure = self._apply_migrations(bone.structure, migrations)
        bone.last_migration = new_version

        return {
            "migrated": True,
            "bone_id": bone_id,
            "new_version": new_version,
        }

    def validate_structure(self, bone_id: str, data: Dict[str, Any]) -> Dict:
        """Validate data against registered schema."""
        if bone_id not in self.state.bones:
            return {"valid": False, "reason": "bone_not_found"}

        bone = self.state.bones[bone_id]
        schema = bone.structure

        # Simple validation: check required fields
        required = schema.get("required", [])
        missing = [field for field in required if field not in data]

        if missing:
            return {
                "valid": False,
                "reason": "missing_fields",
                "missing": missing,
                "required": required,
            }

        return {"valid": True, "bone_id": bone_id, "version": bone.schema_version}

    def store_marrow(self, key: str, value: Any):
        """Store config/defaults in marrow."""
        self.state.marrow[key] = value

    def get_marrow(self, key: str, default: Any = None) -> Any:
        """Retrieve config/default from marrow."""
        return self.state.marrow.get(key, default)

    def reinforce(self, bone_id: str, reinforcement: float = 10.0) -> Dict:
        """Reinforce bone structure (increase density)."""
        if bone_id not in self.state.bones:
            return {"reinforced": False, "reason": "bone_not_found"}

        bone = self.state.bones[bone_id]
        bone.density = min(100.0, bone.density + reinforcement)

        return {
            "reinforced": True,
            "bone_id": bone_id,
            "new_density": bone.density,
        }

    def get_registry(self) -> Dict:
        """Get full schema registry."""
        return {
            bone_id: {
                "name": bone.name,
                "version": bone.schema_version,
                "density": bone.density,
                "last_migration": bone.last_migration,
            }
            for bone_id, bone in self.state.bones.items()
        }

    def _apply_migrations(self, structure: Dict[str, Any], migrations: Dict[str, Any]) -> Dict[str, Any]:
        updated = dict(structure)
        for key, value in migrations.items():
            updated[key] = value
        return updated
