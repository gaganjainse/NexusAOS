#!/usr/bin/env python3
"""
Fix the syntax errors introduced by the Optional replacement.
Pattern: `Type | None = None` should become `Type | None = None`
"""

import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

PROJECT_ROOT = Path(__file__).parent

def fix_optional_syntax(content: str) -> str:
    """Fix Optional[Type | None = None -> Type | None = None syntax errors."""
    
    # Pattern 1: `Type | None = None` in type annotations (function parameters, variable annotations)
    # This matches patterns like `param: int | None = None` or `param: str | None = None`
    content = re.sub(
        r'(\w+:\s+\w+)\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 2: `Type | None = None` in variable annotations
    # Matches patterns like `var: list[str] | None = None` or `var: Dict | None = None`
    content = re.sub(
        r'(\w+:\s+[\w\[\],\s|]+)\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 3: More specific - `Type | None = None` where Type is a known type
    content = re.sub(
        r':\s*(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*=\s*None',
        r': \1 | None = None',
        content
    )
    
    # Pattern 4: Variable annotations with complex types
    content = re.sub(
        r'(\w+:\s*[^\]]+)\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 5: Fix annotations like `frameId: str | None = None`
    content = re.sub(
        r'(\w+:\s*\w+)\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 6: Fix annotations like `var: list[str] | None = None`
    content = re.sub(
        r'(\w+:\s*list\[\w+\])\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 7: Fix annotations like `var: Dict | None = None`
    content = re.sub(
        r'(\w+:\s*dict\[\w+,\s*\w+\])\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 8: Fix annotations like `var: Dict | None = None` (without generics)
    content = re.sub(
        r'(\w+:\s*(?:Dict|List|Tuple|Set|Optional|Union|Callable|Any))\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    # Pattern 9: More generic - type annotation ending with ] followed by = None
    # This handles cases like `variable: Type | None = None`
    content = re.sub(
        r'(\w+:\s*[A-Za-z_][A-Za-z0-9_]*\s*(?:\[[^\]]*\])?)\]\s*=\s*None',
        r'\1 | None = None',
        content
    )
    
    return content

def fix_file(filepath: Path) -> bool:
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    original = content
    content = fix_optional_syntax(content)
    
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
        # Skip certain directories
        if any(skip in filepath.parts for skip in {'.git', '__pycache__', '.pytest_cache', '.idea', '.zig-cache', '.artifacts'}):
            continue
            
        if fix_file(filepath):
            fixed_count += 1
            print(f"Fixed: {filepath.relative_to(PROJECT_ROOT)}")
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()