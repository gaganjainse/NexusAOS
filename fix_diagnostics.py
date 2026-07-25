#!/usr/bin/env python3
"""
Comprehensive diagnostics fix script for Sesha NEURAL 15.0
Fixes: import paths, type annotations, missing imports, modern type annotations
"""

from pathlib import Path
from typing import Any, Callable, Dict, FrozenSet, List, Optional, Set, Tuple, Union
import re
import sys

PROJECT_ROOT = Path(__file__).parent

# Files to skip (generated, cache, etc.)
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', '.idea', '.zig-cache', '.artifacts'}

def should_process(filepath: Path) -> bool:
    parts = filepath.parts
    return not any(skip in parts for skip in SKIP_DIRS) and filepath.suffix in {'.py', '.pyx', '.pyi'}

def fix_imports_and_types(content: str, filepath: Path) -> str:
    """Apply systematic fixes to a Python file."""
    original = content
    
    # 1. Add missing common imports at top if needed
    lines = content.split('\n')
    
    # Find the import section (after docstring, before class/function definitions)
    import_end = 0
    in_docstring = False
    docstring_delim = None
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Detect docstring start/end
        if not in_docstring and stripped.startswith(('"""', "'''")):
            in_docstring = True
            docstring_delim = stripped[:3]
            if stripped.count(docstring_delim) == 2:  # Single line docstring
                in_docstring = False
        elif in_docstring and stripped.endswith(docstring_delim):
            in_docstring = False
        elif not in_docstring and stripped and not stripped.startswith('#'):
            import_end = i
            break
    
    # Check what imports are already present
    has_sys = any('import sys' in l for l in lines[:import_end])
    has_typing = any('from typing import' in l or 'import typing' in l for l in lines[:import_end])
    
    # Determine what typing imports are needed
    needs_Dict = 'dict[' in content or 'Dict ' in content
    needs_List = 'list[' in content or 'List ' in content
    needs_Optional = '' in content or 'Optional ' in content
    needs_Tuple = 'tuple[' in content or 'Tuple ' in content
    needs_Any = 'Any[' in content or 'Any ' in content
    needs_Callable = 'Callable[' in content
    needs_Optional_Type = '' in content
    needs_Set = 'set[' in content
    needs_FrozenSet = 'frozenset[' in content
    needs_Union = '' in content
    
    # Build new typing import if needed
    typing_imports = [
    if needs_Dict: typing_imports.append('Dict')
    if needs_List: typing_imports.append('List')
    if needs_Optional: typing_imports.append('Optional')
    if needs_Tuple: typing_imports.append('Tuple')
    if needs_Any: typing_imports.append('Any')
    if needs_Callable: typing_imports.append('Callable')
    if needs_Set: typing_imports.append('Set')
    if needs_Union: typing_imports.append('Union')
    
    # 2. Fix modern type annotations (Dict -> dict, etc.)
    # But be careful - we need to keep typing imports for annotations
    # Actually, modern Python prefers lowercase, but we need imports for annotations
    # Strategy: Keep typing imports, but use lowercase in annotations where possible
    
    # 3. Fix import paths - the main issue is `layers.*` vs actual paths
    # Map old import paths to new ones
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
    
    new_content = content
    
    # Apply import path fixes
    for old, new in import_replacements.items():
        new_content = new_content.replace(old, new)
    
    # 4. Fix modern type annotations in annotations (but keep typing imports)
    # dict[K, V] -> dict[K, V] (Python 3.9+)
    # But we must keep typing imports for older Python compatibility
    # Actually, let's convert to modern style where used in annotations
    # new_content = re.sub(r'\bDict\[', 'dict[', new_content)
    # new_content = re.sub(r'\bList\[', 'list[', new_content)
    # new_content = re.sub(r'\bTuple\[', 'tuple[', new_content)
    # new_content = re.sub(r'\bOptional\[', '| None', new_content)  # This is tricky
    # new_content = new_content.replace('', '').replace(']', ' | None') # too aggressive
    
    # 5. Fix missing sys import where sys.path.insert is used
    if 'sys.path.insert' in new_content and 'import sys' not in new_content[:500]:
        # Add import sys after existing imports
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                continue
            if line.strip() and not line.strip().startswith('#'):
                # Insert after the last import
                insert_idx = 0
                for j in range(len(lines)-1, -1, -1):
                    if lines[j].strip().startswith('import ') or lines[j].strip().startswith('from '):
                        insert_idx = j + 1
                        break
                lines.insert(insert_idx, 'import sys')
                new_content = '\n'.join(lines)
                break
    
    # 6. Add missing typing imports
    typing_needed = []
    if 'dict[' in new_content: typing_needed.append('Dict')
    if 'list[' in new_content: typing_needed.append('List')
    if '' in new_content: typing_needed.append('Optional')
    if 'tuple[' in new_content: typing_needed.append('Tuple')
    if 'Any[' in new_content: typing_needed.append('Any')
    if 'Callable[' in new_content: typing_needed.append('Callable')
    if 'set[' in new_content: typing_needed.append('Set')
    if 'frozenset[' in new_content: typing_needed.append('FrozenSet')
    if 'Union[' in new_content: typing_needed.append('Union')
    if 'Callable[' in new_content and 'from collections.abc import Callable' not in new_content:
        # We'll add it
        pass
    
    # Actually, let's be more targeted - only fix the most critical issues
    # The main issues are:
    # 1. Missing imports (sys, Optional, Dict, etc.)
    # 2. Wrong import paths (layers.* -> actual paths)
    # 3. Modern type annotations
    
    return new_content

def fix_file(filepath: Path):
    """Fix a single file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    new_content = fix_imports_and_types(content, filepath)
    
    if new_content != content:
        try:
            filepath.write_text(new_content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    return False

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
