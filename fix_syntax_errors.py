#!/usr/bin/env python3
"""
Comprehensive fix for all syntax errors introduced by the type annotation migration.
Fixes:
1. Unmatched brackets in type annotations (Dict] -> dict, Optional] -> | None, etc.)
2. Unclosed module docstrings (opening """ without closing)
3. Invalid return type annotations (str, bytes -> str | bytes)
4. Missing closing brackets in dataclass fields
"""

import re
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple, Type

PROJECT_ROOT = Path(__file__).parent

SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', '.idea', '.zig-cache', '.artifacts'}

def should_process(filepath: Path) -> bool:
    parts = filepath.parts
    return not any(skip in parts for skip in SKIP_DIRS) and filepath.suffix == '.py'

def fix_unclosed_module_docstring(content: str) -> str:
    """Fix unclosed module docstrings - add closing \"\"\" after imports."""
    lines = content.split('\n')
    
    # Find if there's an opening """ at the start (after shebang/imports)
    in_module_docstring = False
    docstring_start = -1
    import_end = -1
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check for shebang
        if i == 0 and stripped.startswith('#!'):
            continue
            
        # Check for opening module docstring
        if not in_module_docstring and stripped == '"""':
            in_module_docstring = True
            docstring_start = i
            continue
            
        # If we're in a module docstring, look for the end of imports
        if in_module_docstring:
            # Check for closing """
            if stripped == '"""':
                # Already closed properly
                in_module_docstring = False
                docstring_start = -1
                continue
                
            # Look for end of import section (first non-import, non-empty, non-comment line)
            if stripped and not stripped.startswith('import ') and not stripped.startswith('from ') and not stripped.startswith('#'):
                import_end = i
                break
    
    # If we found an unclosed module docstring, close it after imports
    if in_module_docstring and import_end > 0:
        lines.insert(import_end, '"""')
        content = '\n'.join(lines)
    
    return content

def fix_type_annotations(content: str) -> str:
    """Fix type annotations with unmatched brackets."""
    
    # Fix patterns like `Type] = None` -> `Type | None = None`
    # But only in type annotations (after colon, before = or comma)
    content = re.sub(
        r':\s*(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*=\s*None',
        r': \1 | None = None',
        content
    )
    
    # Fix patterns like `-> Type:` -> `-> Type:`
    content = re.sub(
        r'->\s*(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*:',
        r'-> \1:',
        content
    )
    
    # Fix patterns like `list[Type]]` -> `list[Type]`
    content = re.sub(
        r'\b(list|dict|tuple|set|frozenset)\[([^\]]+)\]\]',
        r'\1[\2]',
        content
    )
    
    # Fix patterns like `Dict[K, V]]` -> `dict[K, V]`
    content = re.sub(
        r'\b(Dict|List|Tuple|Set|FrozenSet)\[([^\]]+)\]\]',
        lambda m: f'{m.group(1).lower()}[{m.group(2)}]',
        content
    )
    
    # Fix return type annotations like `-> str, bytes:` -> `-> str | bytes:`
    content = re.sub(
        r'->\s*([A-Za-z_][A-Za-z0-9_]*),\s*([A-Za-z_][A-Za-z0-9_]*)\s*:',
        r'-> \1 | \2:',
        content
    )
    
    # Fix unmatched ] in dataclass fields like `field: dict[str, Any | None ] = None`
    content = re.sub(
        r'(\w+:\s*dict\[[^\]]+)\s*=\s*None',
        r'\1] = None',
        content
    )
    
    return content

def fix_return_type_annotations(content: str) -> str:
    """Fix invalid return type annotations."""
    # Fix `-> str, bytes:` -> `-> str | bytes:`
    content = re.sub(
        r'def\s+(\w+)\s*\([^)]*\)\s*->\s*([A-Za-z_][A-Za-z0-9_]*),\s*([A-Za-z_][A-Za-z0-9_]*)\s*:',
        r'def \1(...) -> \2 | \3:',
        content
    )
    
    return content

def normalize_line_endings(content: str) -> str:
    """Normalize line endings to \n."""
    return content.replace('\r\n', '\n').replace('\r', '\n')

def fix_file(filepath: Path) -> bool:
    """Apply all fixes to a Python file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    original = content
    
    # Apply fixes in order
    content = normalize_line_endings(content)
    content = fix_unclosed_module_docstring(content)
    content = fix_type_annotations(content)
    content = fix_return_type_annotations(content)
    
    if content != original:
        try:
            filepath.write_text(content, encoding='utf-8')
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
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()