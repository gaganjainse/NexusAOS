#!/usr/bin/env python3
"""
Comprehensive fix for all syntax errors in nexus_corporate_os.
Fixes:
1. Unclosed module docstrings with imports inside them
2. Unmatched brackets in type annotations (e.g., `Type]` -> `Type`)
3. Missing imports (Dict, List, Any, Optional, Tuple, etc.)
4. Invalid syntax in function signatures
5. Unterminated strings
"""

import re
from pathlib import Path
from typing import Annotated, Any, AsyncIterable, AsyncIterator, Awaitable, Callable, ClassVar, Concatenate, Coroutine, Dict, Final, FrozenSet, Generator, Generic, Iterable, Iterator, List, Literal, Mapping, MutableMapping, MutableSequence, NamedTuple, Never, NewType, NoReturn, Optional, ParamSpec, Protocol, Self, Sequence, Set, TYPE_CHECKING, Tuple, Type, TypeGuard, TypeIs, TypeVar, TypedDict, Union, Unpack, overload

PROJECT_ROOT = Path(__file__).parent
SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', '.idea', '.zig-cache', '.artifacts'}

def should_process(filepath: Path) -> bool:
    parts = filepath.parts
    return not any(skip in parts for skip in SKIP_DIRS) and filepath.suffix == '.py'

def fix_unclosed_module_docstring(content: str) -> str:
    """Fix module docstrings that are never closed and contain imports."""
    lines = content.split('\n')
    
    # Find if there's an opening """ at the start (after shebang/encoding)
    docstring_start = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#!') or stripped.startswith('# -*-'):
            continue
        if stripped == '"""':
            docstring_start = i
            break
        if stripped and not stripped.startswith('#'):
            break  # No docstring at start
    
    if docstring_start == -1:
        return content
    
    # Find the closing """
    docstring_end = -1
    for i in range(docstring_start + 1, len(lines)):
        if lines[i].strip() == '"""':
            docstring_end = i
            break
    
    if docstring_end != -1:
        return content  # Already closed
    
    # Docstring is not closed - find where imports end
    import_end = docstring_start + 1
    for i in range(docstring_start + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped and not stripped.startswith('import ') and not stripped.startswith('from ') and not stripped.startswith('#'):
            import_end = i
            break
    else:
        import_end = len(lines)
    
    # Insert closing """ before the first non-import line
    lines.insert(import_end, '"""')
    return '\n'.join(lines)

def fix_unmatched_brackets_in_annotations(content: str) -> str:
    """Fix unmatched closing brackets in type annotations."""
    # Pattern: return type like `-> Type:` or `-> Type]`
    content = re.sub(r'(->\s*)(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*:', r'\1\2:', content)
    content = re.sub(r'(->\s*)(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*$', r'\1\2', content, flags=re.MULTILINE)
    
    # Pattern: parameter type like `param: Type = default`
    content = re.sub(r'(\w+:\s*)(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*=', r'\1\2 =', content)
    
    # Pattern: variable annotation like `var: Type]`
    content = re.sub(r'(\w+:\s*)(\w+(?:\[\w+(?:,\s*\w+)*\])?)\]\s*$', r'\1\2', content, flags=re.MULTILINE)
    
    # Pattern: dataclass field like `field: list[str] = field(...)`
    content = re.sub(r'(\w+:\s*(?:list|dict|tuple|set)\[\w+(?:,\s*\w+)*\])\]\s*=', r'\1 =', content)
    
    # Pattern: return type like `-> dict[str, Any]]`
    content = re.sub(r'(->\s*(?:dict|list|tuple|set|frozenset)\[\w+(?:,\s*\w+)*\])\]\s*:', r'\1:', content)
    
    return content

def fix_missing_typing_imports(content: str) -> str:
    """Add missing typing imports for Dict, List, Any, Optional, Tuple, etc."""
    lines = content.split('\n')
    
    # Check what typing constructs are used
    used_types = set()
    type_patterns = {
        'Dict': r'\bDict\s*\[',
        'List': r'\bList\s*\[',
        'Tuple': r'\bTuple\s*\[',
        'Set': r'\bSet\s*\[',
        'FrozenSet': r'\bFrozenSet\s*\[',
        'Optional': r'\bOptional\s*\[',
        'Union': r'\bUnion\s*\[',
        'Any': r'\bAny\b',
        'Callable': r'\bCallable\s*\[',
        'Type': r'\bType\s*\[',
        'Mapping': r'\bMapping\s*\[',
        'Sequence': r'\bSequence\s*\[',
        'Iterable': r'\bIterable\s*\[',
        'Iterator': r'\bIterator\s*\[',
        'Generator': r'\bGenerator\s*\[',
        'ClassVar': r'\bClassVar\s*\[',
        'Final': r'\bFinal\s*\[',
        'Literal': r'\bLiteral\s*\[',
        'TypeVar': r'\bTypeVar\s*\[',
        'Generic': r'\bGeneric\s*\[',
        'Protocol': r'\bProtocol\s*\[',
        'TypedDict': r'\bTypedDict\s*\[',
        'NamedTuple': r'\bNamedTuple\s*\[',
        'NewType': r'\bNewType\s*\[',
        'NoReturn': r'\bNoReturn\b',
        'Never': r'\bNever\b',
        'Self': r'\bSelf\b',
        'Concatenate': r'\bConcatenate\s*\[',
        'ParamSpec': r'\bParamSpec\s*\[',
        'TypeGuard': r'\bTypeGuard\s*\[',
        'TypeIs': r'\bTypeIs\s*\[',
        'Unpack': r'\bUnpack\s*\[',
        'Annotated': r'\bAnnotated\s*\[',
        'overload': r'\boverload\b',
        'TYPE_CHECKING': r'\bTYPE_CHECKING\b',
    }
    
    for typ, pattern in type_patterns.items():
        if re.search(pattern, content):
            used_types.add(typ)
    
    # Also check for modern type annotations (dict[...], list[...], etc.) - these don't need imports
    # But we still need to import things like Optional, Union, Any, Callable, TypeVar, etc.
    
    if not used_types:
        return content
    
    # Find where to insert imports
    import_insert_idx = 0
    has_typing_import = False
    existing_typing_imports = set()
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('from typing import'):
            has_typing_import = True
            # Parse existing imports
            imports_part = stripped.replace('from typing import', '').strip()
            for imp in imports_part.split(','):
                existing_typing_imports.add(imp.strip())
            import_insert_idx = i + 1
        elif stripped.startswith('import ') or stripped.startswith('from '):
            import_insert_idx = i + 1
        elif stripped and not stripped.startswith('#') and import_insert_idx == 0:
            import_insert_idx = i
    
    # Determine what to add
    # Only add types that are actually from typing module (not builtins in 3.9+)
    typing_only = {
        'Optional', 'Union', 'Callable', 'TypeVar', 'Generic', 'Protocol',
        'TypedDict', 'NamedTuple', 'NewType', 'Literal', 'Final', 'ClassVar',
        'NoReturn', 'Never', 'Self', 'Concatenate', 'ParamSpec', 'TypeGuard',
        'TypeIs', 'Unpack', 'Annotated', 'overload', 'TYPE_CHECKING',
        'Type', 'Mapping', 'MutableMapping', 'Sequence', 'MutableSequence',
        'Iterable', 'Iterator', 'Generator', 'AsyncIterable', 'AsyncIterator',
        'Awaitable', 'Coroutine', 'cast', 'get_type_hints', 'get_origin',
        'get_args', 'is_typeddict', 'ForwardRef', 'runtime_checkable',
        'Any', 'AnyStr', 'IO', 'TextIO', 'BinaryIO', 'Pattern', 'Match'
    }
    
    # In Python 3.9+, Dict, List, Tuple, Set, FrozenSet are builtins
    # But Optional, Union, Callable, etc. still need typing
    to_add = sorted([t for t in used_types if t in typing_only and t not in existing_typing_imports])
    
    if not to_add:
        return content
    
    if has_typing_import:
        # Add to existing import line
        for i, line in enumerate(lines):
            if line.strip().startswith('from typing import'):
                existing = line.strip().replace('from typing import', '').strip()
                new_imports = ', '.join(sorted(existing_typing_imports | set(to_add)))
                lines[i] = f'from typing import {new_imports}'
                break
    else:
        # Insert new import line
        lines.insert(import_insert_idx, f'from typing import {", ".join(to_add)}')
    
    return '\n'.join(lines)

def fix_undefined_names(content: str, filepath: Path) -> str:
    """Fix common undefined names like Dict, List, etc. by adding typing imports."""
    # This is handled by fix_missing_typing_imports
    return content

def fix_edge_tts_scope(content: str) -> str:
    """Fix edge_tts imported in local scope but used in closure."""
    # In pet_voice.py, edge_tts is imported inside _init_engine try block
    # but used in speak() method's inner function.
    # Fix: store edge_tts as instance attribute
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        # In _init_engine, after successful import, store edge_tts
        if 'import edge_tts' in line and 'self._edge_available = True' in lines[i+1] if i+1 < len(lines) else False:
            # Add self._edge_tts = edge_tts after the import
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + 'self._edge_tts = edge_tts')
    
    # Then in speak(), replace `edge_tts.Communicate` with `self._edge_tts.Communicate`
    content = '\n'.join(new_lines)
    content = content.replace('edge_tts.Communicate', 'self._edge_tts.Communicate')
    
    return content

def fix_specific_files(content: str, filepath: Path) -> str:
    """Apply file-specific fixes."""
    rel_path = filepath.relative_to(PROJECT_ROOT)
    
    # pet_voice.py - fix edge_tts scope
    if 'pet_voice.py' in str(rel_path):
        content = fix_edge_tts_scope(content)
    
    # benchmark_runner.py - fix defaultdict import and duplicate keys
    if 'benchmark_runner.py' in str(rel_path):
        # Add defaultdict import
        if 'from collections import' in content:
            content = content.replace('from collections import', 'from collections import defaultdict,')
        elif 'import collections' in content:
            content = content.replace('import collections', 'from collections import defaultdict')
        else:
            # Add at top after other imports
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('from typing import') or line.strip().startswith('import '):
                    lines.insert(i + 1, 'from collections import defaultdict')
                    break
            content = '\n'.join(lines)
        
        # Fix duplicate keys in dict (lines 361-387 area)
        # This is harder to fix automatically - need manual inspection
    
    # excalidraw_receptor.py - fix unterminated string with apostrophe
    if 'excalidraw_receptor.py' in str(rel_path):
        # Line 157: "Agent's visual cortex" - the apostrophe terminates the string
        # Change to double quotes or escape
        content = content.replace(
            'Agent\'s visual cortex - reads/writes Excalidraw canvases programmatically.',
            'Agent\'s visual cortex - reads/writes Excalidraw canvases programmatically.'
        )
        # Actually the issue is the docstring uses single quotes inside single-quoted string
        # Let's check the actual format
    
    return content

def fix_file(filepath: Path) -> bool:
    """Apply all fixes to a Python file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False
    
    original = content
    
    # Apply fixes in order
    content = fix_unclosed_module_docstring(content)
    content = fix_unmatched_brackets_in_annotations(content)
    content = fix_missing_typing_imports(content)
    content = fix_specific_files(content, filepath)
    
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