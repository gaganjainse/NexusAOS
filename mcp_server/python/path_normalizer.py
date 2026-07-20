import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:/Users/gagan/Downloads/ClinicLedger-main/nexus_corporate_os")
ARCHIVE_DIR = BASE_DIR / "archives"

def normalize_paths():
    print("NexusOS Global Path Normalization Initializing...")

    # 1. Map all filenames to their relative paths from BASE_DIR
    file_map = {}
    for root, _, files in os.walk(str(ARCHIVE_DIR)):
        for file in files:
            if file.endswith(".md"):
                rel_path = Path(root).relative_to(BASE_DIR) / file
                file_map[file] = rel_path.as_posix()

    # 2. Iterate and fix links
    fixed_count = 0
    for root, _, files in os.walk(str(ARCHIVE_DIR)):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                def replace_link(match):
                    text = match.group(1)
                    link = match.group(2)

                    if link.startswith("#") or link.startswith("http"):
                        return match.group(0)

                    target_filename = link.split("/")[-1]
                    if target_filename in file_map:
                        # Calculate correct relative path
                        target_rel_from_base = Path(file_map[target_filename])
                        source_rel_from_base = file_path.relative_to(BASE_DIR)

                        # Use os.path.relpath to get correct ../ count
                        new_rel_link = os.path.relpath(
                            BASE_DIR / target_rel_from_base,
                            file_path.parent
                        ).replace("\\", "/")

                        return f"[{text}]({new_rel_link})"

                    return match.group(0)

                new_content = re.sub(r"\[(.*?)\]\((.*?)\)", replace_link, content)

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    fixed_count += 1

    print(f"Normalization Complete: {fixed_count} files corrected.")

if __name__ == "__main__":
    normalize_paths()
