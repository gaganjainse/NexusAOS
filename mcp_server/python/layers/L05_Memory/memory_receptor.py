"""
SeshaAOS - Memory Receptor (Hippocampus)
Version: 1.0.0
Description: Entity storage, recall, and linking (knowledge graph).
"""
import json
from pathlib import Path

_python_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_python_root) not in sys.path:
    sys.path.insert(0, str(_python_root))


class MemoryReceptor:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.memory_dir = base_dir / "core" / "monitoring" / "memory_graph"
        self.memory_dir.mkdir(exist_ok=True, parents=True)
        self.entities_file = self.memory_dir / "entities.json"
        self.links_file = self.memory_dir / "links.json"
        self._init_files()

    def _init_files(self):
        if not self.entities_file.exists():
            with open(self.entities_file, "w") as f:
                json.dump({}, f)
        if not self.links_file.exists():
            with open(self.links_file, "w") as f:
                json.dump([], f)

    def _load_entities(self) -> dict:
        try:
            with open(self.entities_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_entities(self, entities: dict):
        with open(self.entities_file, "w") as f:
            json.dump(entities, f, indent=2)

    def _load_links(self) -> list:
        try:
            with open(self.links_file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_links(self, links: list):
        with open(self.links_file, "w") as f:
            json.dump(links, f, indent=2)

    def store_entity(self, entity_id: str, properties: dict) -> dict:
        entities = self._load_entities()
        entities[entity_id] = {**properties, "created_at": str(Path.cwd())}
        self._save_entities(entities)
        return {"success": True, "entity_id": entity_id}

    def recall_entity(self, entity_id: str) -> dict:
        entities = self._load_entities()
        if entity_id in entities:
            return {"success": True, "entity": entities[entity_id]}
        return {"success": False, "error": "Entity not found"}

    def link_entities(self, from_id: str, to_id: str, relation: str) -> dict:
        links = self._load_links()
        links.append({
            "from": from_id,
            "to": to_id,
            "relation": relation
        })
        self._save_links(links)
        return {"success": True}

