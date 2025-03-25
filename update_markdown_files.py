#!/usr/bin/env python3
import os
import re
from datetime import datetime
import shutil

# Directory containing the markdown files
posts_dir = "_posts"

# Process all markdown files in the directory
for filename in os.listdir(posts_dir):
    # Skip files that already have date prefix
    if re.match(r"^\d{4}-\d{2}-\d{2}", filename):
        print(f"Skipping already processed file: {filename}")
        continue

    # Skip non-markdown files
    if not (filename.endswith(".md") or filename.endswith(".markdown")):
        print(f"Skipping non-markdown file: {filename}")
        continue

    file_path = os.path.join(posts_dir, filename)

    # Read the file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Check if the file has frontmatter (between --- markers)
    frontmatter_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        print(f"No frontmatter found in {filename}, skipping...")
        continue

    frontmatter = frontmatter_match.group(1)

    # Extract the date from frontmatter
    date_match = re.search(r'date:\s*[\'"]?(\d{4}-\d{2}-\d{2})', frontmatter)
    if not date_match:
        print(f"No date found in {filename}, skipping...")
        continue

    date_str = date_match.group(1)

    # Create new filename with date prefix
    new_filename = f"{date_str}-{filename}"
    new_file_path = os.path.join(posts_dir, new_filename)

    # Update frontmatter: keep title and date, add layout, remove description and tags
    new_frontmatter_lines = []
    for line in frontmatter.split("\n"):
        # Keep title and date lines
        if line.strip().startswith("title:") or line.strip().startswith("date:"):
            new_frontmatter_lines.append(line)

    # Add layout property
    new_frontmatter_lines.append("layout: post")

    # Create new content
    new_frontmatter = "\n".join(new_frontmatter_lines)
    new_content = re.sub(
        r"^---\s*\n.*?\n---", f"---\n{new_frontmatter}\n---", content, flags=re.DOTALL
    )

    # Write updated content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)

    # Rename the file
    try:
        os.rename(file_path, new_file_path)
        print(f"Processed {filename} -> {new_filename}")
    except Exception as e:
        print(f"Error renaming {filename}: {e}")

print("All markdown files processed.")
