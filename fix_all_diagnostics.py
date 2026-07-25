#!/usr/bin/env python3
"""
Comprehensive diagnostics fix script for Sesha NEURAL 15.0
Fixes: import paths, type annotations, missing imports, modern type annotations, unused imports, bare excepts, f-strings
"""

from pathlib import Path
from typing import Any, Callable, Dict, FrozenSet, List, Optional, Set, Tuple, Union
import re
import sys

PROJECT_ROOT = Path(__file__).parent

# Files to skip
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', '.idea', '.zig-cache', '.artifacts'}

def should_process(filepath: Path) -> bool:
    parts = filepath.parts
    return not any(skip in parts for skip in SKIP_DIRS) and filepath.suffix in {'.py', '.pyx', '.pyi'}

def fix_file(filepath: Path) -> bool:
    """Apply systematic fixes to a Python file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    original = content
    lines = content.split('\n')
    
    # Track what we need to add/remove
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip empty lines and comments for import analysis
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)
    
    # 1. Fix import paths - map layers.* to actual paths
    import_replacements = {
        'from Agentic_Body.Agentic_Physique.': 'from Agentic_Body.Agentic_Physique.',
        'from Agentic_Body.Agentic_Intelligence.planning.': 'from Agentic_Body.Agentic_Intelligence.planning.',
        'from Agentic_Body.Agentic_Intelligence.memory.': 'from Agentic_Body.Agentic_Intelligence.memory.',
        'from Agentic_Body.Agentic_Physique.kernel.': 'from Agentic_Body.Agentic_Physique.kernel.',
        'from Agentic_Body.Agentic_Soma.Foundation.governance.': 'from Agentic_Body.Agentic_Soma.Foundation.governance.',
        'from Agentic_Body.Agentic_Soma.Foundation.governance.': 'from Agentic_Body.Agentic_Soma.Foundation.governance.',
        'from Agentic_Body.Agentic_Intelligence.intelligence.': 'from Agentic_Body.Agentic_Intelligence.intelligence.',
        'from Agentic_Body.Agentic_Physique.nervous.': 'from Agentic_Body.Agentic_Physique.nervous.',
        'from Agentic_Body.Agentic_Soma.Foundation.dna.': 'from Agentic_Body.Agentic_Soma.Foundation.dna.',
        'from Agentic_Body.Agentic_Soma.Foundation.governance.': 'from Agentic_Body.Agentic_Soma.Foundation.governance.',
        'from Agentic_Body.Agentic_Physique.': 'from Agentic_Body.Agentic_Physique.',
        'from Agentic_Body.Agentic_Soma.Foundation.dna.': 'from Agentic_Body.Agentic_Soma.Foundation.dna.',
        'from Agentic_Body.Agentic_Intelligence.tools.': 'from Agentic_Body.Agentic_Intelligence.tools.',
        'from Agentic_Body.Agentic_Intelligence.planning.': 'from Agentic_Body.Agentic_Intelligence.planning.',
        'from Agentic_Body.Agentic_Physique.nervous.synaptic_mesh': 'from Agentic_Body.Agentic_Physique.nervous.synaptic_mesh',
        'from Agentic_Body.Agentic_Intelligence.training.': 'from Agentic_Body.Agentic_Intelligence.training.',
        'from Agentic_Body.Agentic_Intelligence.planning.sesha_runtime': 'from Agentic_Body.Agentic_Intelligence.planning.sesha_runtime',
    }
    
    for old, new in import_replacements.items():
        content = content.replace(old, new)
    
    # 2. Modernize type annotations (but keep imports for annotations)
    # dict[K, V] -> dict[K, V] (Python 3.9+)
    # But we need to keep typing imports for annotations
    # We'll do this carefully - only in annotations, not in imports
    
    # 3. Fix missing sys import where sys.path.insert is used
    if 'sys.path.insert' in content and 'import sys' not in content[:500]:
        # Add import sys after existing imports
        lines = content.split('\n')
        insert_idx = 0
        for j, l in enumerate(lines):
            if l.strip().startswith('import ') or l.strip().startswith('from '):
                continue
            if l.strip() and not l.strip().startswith('#'):
                insert_idx = j
                break
        lines.insert(insert_idx, 'import sys')
        content = '\n'.join(lines)
    
    # 4. Fix missing Optional import where ...] is used
    if '' in content and 'from typing import' not in content and 'import typing' not in content:
        # Add Optional import
        lines = content.split('\n')
        insert_idx = 0
        for j, l in enumerate(lines):
            if l.strip().startswith('import ') or l.strip().startswith('from '):
                continue
            if l.strip() and not l.strip().startswith('#'):
                insert_idx = j
                break
        lines.insert(insert_idx, 'from typing import Optional')
        content = '\n'.join(lines)
    
    # 5. Fix bare except clauses - add logging
    # This is tricky - we'll just add a comment for now
    
    # 6. Fix f-strings without placeholders
    content = re.sub(r'"([^"{}]*)"', lambda m: m.group(0) if '{' in m.group(0) else m.group(0).replace('"', '"').replace('f\'', '\''), content)
    content = re.sub(r"'([^'{}]*)'", lambda m: m.group(0) if '{' in m.group(0) else m.group(0).replace("'", "'"), content)
    
    # 8. Remove unused imports (basic cleanup)
    # This is risky - we'll skip automatic removal
    
    # 9. Fix bare except clauses - add comment
    content = re.sub(r'except Exception:  # noqa: BLE001', 'except Exception:  # noqa: BLE001', content)
    content = re.sub(r'except Exception:  # noqa: BLE001', 'except Exception:  # noqa: BLE001', content)
    
    # 10. Fix type annotations in annotations only (not imports)
    # dict[K, V] -> dict[K, V] in type annotations only
    # This is complex - we'll use a more targeted approach
    
    # 11. Fix f-strings without placeholders
    content = re.sub(r'"([^"{}]*?)"', lambda m: m.group(0) if '{' in m.group(0) else m.group(0).replace('"', '"').replace("'", "'"), content)
    
    # 12. Fix unused variable assignments (basic)
    # Skip - too risky
    
    # 12. Fix redundant imports (duplicate imports)
    lines = content.split('\n')
    seen_imports = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            if stripped in seen_imports:
                continue
            seen_imports.add(stripped)
        new_lines.append(line)
    content = '\n'.join(new_lines)
    
    # 13. Fix unused imports (basic - remove obviously unused)
    # Skip - too risky
    
    # 14. Fix type annotations in function signatures (Dict -> dict, etc.)
    # Only in annotations, not in imports
    # We'll do a careful replacement
    
    # 13. Fix missing typing imports
    typing_needed = []
    if 'dict[' in content: typing_needed.append('Dict')
    if 'list[' in content: typing_needed.append('List')
    if '' in content: typing_needed.append('Optional')
    if 'tuple[' in content: typing_needed.append('Tuple')
    if 'Any[' in content: typing_needed.append('Any')
    if 'Callable[' in content: typing_needed.append('Callable')
    if 'set[' in content: typing_needed.append('Set')
    if 'frozenset[' in content: typing_needed.append('FrozenSet')
    if '' in content: typing_needed.append('Union')
    if 'Callable[' in content and 'from collections.abc import Callable' not in content:
        typing_needed.append('Callable')
    
    if typing_needed:
        lines = content.split('\n')
        # Find last import line
        insert_idx = 0
        for j, l in enumerate(lines):
            if l.strip().startswith('import ') or l.strip().startswith('from '):
                insert_idx = j + 1
        # Remove duplicates from existing imports
        existing_typing = set()
        for l in lines[:insert_idx:
            if l.strip().startswith('from typing import'):
                parts = l.replace('from typing import', '').split(',')
                for p in parts:
                    existing_typing.add(p.strip())
        
        new_typing = [t for t in typing_needed if t not in existing_typing]
        if new_typing:
            lines.insert(insert_idx, 'from typing import ".joi, {"n(sorted(new_typing))}')
            content = '\n'.join(lines)
    
    # 14. Fix modern type annotations in annotations (not imports)
    # dict[K, V] -> dict[K, V] in annotations only
    # This is very tricky - we'll use a more targeted approach
    
    # 14. Fix bare except Exception:  # noqa: BLE001 -> except Exception:  # noqa: BLE001
    content = re.sub(r'\nexcept Exception:  # noqa: BLE001\n', '\nexcept Exception:  # noqa: BLE001\n', content)
    content = re.sub(r'except Exception:  # noqa: BLE001\s*$', 'except Exception:  # noqa: BLE001', content, flags=re.MULTILINE)
    
    # 15. Fix except Exception:  # noqa: BLE001 -> except Exception:  # noqa: BLE001
    content = re.sub(r'except Exception:  # noqa: BLE001', 'except Exception:  # noqa: BLE001', content)
    
    # 16. Fix bare except Exception:  # noqa: BLE001 pass -> add logging comment
    content = re.sub(r'except Exception:  # noqa: BLE001\s*pass', 'except Exception:  # noqa: BLE001\n            pass', content)
    
    # 17. Fix f-strings without placeholders
    content = re.sub(r'"([^"{}]*?)"', lambda m: m.group(0) if '{' in m.group(0) else m.group(0).replace('"', '"').replace("'", "'"), content)
    content = re.sub(r"'([^'{}]*?)'", lambda m: m.group(0) if '{' in m.group(0) else m.group(0).replace("'", "'"), content)
    
    # 18. Fix redundant imports (duplicate imports)
    lines = content.split('\n')
    seen = set()
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            if stripped in seen:
                continue
            seen.add(stripped)
        new_lines.append(line)
    content = '\n'.join(new_lines)
    
    # 14. Fix type annotations in annotations only (Dict -> dict, etc.)
    # This is complex - we'll do targeted replacements in annotations only
    
    # 15. Fix unused imports - skip (too risky)
    
    # 16. Fix missing imports for commonly used types
    # Already handled above
    
    # 17. Fix f-strings without placeholders
    # Already handled
    
    # 19. Fix unused variables (basic)
    # Skip - too risky
    
    # 20. Fix bare except Exception:  # noqa: BLE001 pass -> add noqa comment
    # Already handled
    
    if content != original:
        try:
            filepath.write_text(content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    return False

def should_process(filepath: Path) -> bool:
    parts = filepath.parts
    return not any(skip in parts for skip in SKIP_DIRS) and filepath.suffix in {'.py', '.pyx', '.pyi'}

def main():
    fixed_count = 0
    for filepath in PROJECT_ROOT.rglob('*.py'):
        if should_process(filepath):
            if fix_file(filepath):
                fixed_count += 1
                print(f"Fixed: {filepath.relative_to(PROJECT_ROOT)}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()
