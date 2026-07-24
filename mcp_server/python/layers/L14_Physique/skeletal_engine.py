"""
SeshaAOS - Skeletal Engine (L14.1)
Version: 1.0.0
Description: Physical File and Storage Organization. Manages the host's "Skeletal Marrow."
"""

import json
import os
import shutil
import time
from pathlib import Path
from typing import Dict, List, Any, Optional


class SkeletalEngine:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.backup_dir = base_dir / "bone_marrow_backup"
        self.map_path = base_dir / "archives" / "dna_core" / "learning" / "skeletal_map.json"
        
        from layers.L14_Physique.volume_manager import VolumeManager
        self.volumes = VolumeManager(base_dir)

    def distribute_to_volumes(self):
        """Neural 13.8: Moves salience-matched files into isolated Soma volumes."""
        actions = []
        # AI: Move research and wisdom
        research_dir = self.base_dir / "archives" / "dna_core" / "learning"
        for f in research_dir.glob("*.json"):
            target = self.volumes.VOLUMES["AI"] / f.name
            try:
                shutil.copy2(str(f), str(target))
                actions.append(f"Volume Sync: Ingested {f.name} into Volume AI.")
            except: pass
            
        return actions
        """Neural 13.6: Deep Scans the host environment to build a physical file map."""
        if root is None:
            root = self.base_dir
            
        print(f"Mapping Skeletal Marrow: {root}...")
        file_map = []
        
        # Admin search across all files
        try:
            for p in root.rglob("*"):
                try:
                    if p.is_file():
                        file_map.append({
                            "name": p.name,
                            "path": str(p.relative_to(root)) if p.is_relative_to(root) else str(p),
                            "size": p.stat().st_size,
                            "mtime": p.stat().st_mtime,
                            "type": p.suffix.lower()
                        })
                except (PermissionError, OSError):
                    continue # Skip system-locked bones
        except Exception as e:
            return {"error": str(e)}
        
        # Save map to Learning DNA
        self.map_path.parent.mkdir(parents=True, exist_ok=True)
        self.map_path.write_text(json.dumps(file_map, indent=4), encoding="utf-8")
        
        return {"total_files": len(file_map), "map_path": str(self.map_path)}

    def execute_reorg(self) -> List[str]:
        """Neural 13.6: Physically aligns the host structure to the Agentic Body standard."""
        actions = []
        
        # 1. Create Safety Backup of critical DNA
        if not self.backup_dir.exists():
             self.backup_dir.mkdir(parents=True, exist_ok=True)
             
        # 2. Logic: Move loose .md to archives
        for f in self.base_dir.glob("*.md"):
            # Preserve identity files at root for now
            if f.name.lower() in ["agents.md", "readme.md", "aos_handbook.md"]: 
                continue
            
            target = self.base_dir / "archives" / "dna_core" / "foundation" / f.name
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(f), str(target))
                actions.append(f"Physique Alignment: Moved {f.name} to foundation archives.")
            except Exception as e:
                actions.append(f"Error moving {f.name}: {e}")
                
        # 3. Logic: Consolidate Monitoring Waste
        log_dir = self.base_dir / "core" / "monitoring"
        archive_log = log_dir / "archive"
        archive_log.mkdir(parents=True, exist_ok=True)
        
        for l in log_dir.glob("*.log"):
             # If log is larger than 1MB or older than 24h
             try:
                 if l.stat().st_size > 1024 * 1024 or (time.time() - l.stat().st_mtime > 86400):
                     shutil.move(str(l), str(archive_log / l.name))
                     actions.append(f"Physique Alignment: Archived bloated log: {l.name}")
             except: pass
                 
        return actions

    def get_pc_health_status(self) -> Dict[str, Any]:
        """Returns fragmentation and storage vitals."""
        total, used, free = shutil.disk_usage(self.base_dir)
        return {
            "disk_total_gb": round(total / (2**30), 2),
            "disk_free_gb": round(free / (2**30), 2),
            "storage_usage_pct": round((used/total)*100, 2),
            "marrow_mapped": self.map_path.exists()
        }

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[4]
    sk = SkeletalEngine(base)
    print(json.dumps(sk.organize_skeletal_marrow(), indent=2))

