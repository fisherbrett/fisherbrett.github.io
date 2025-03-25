#!/bin/bash

# Loop through all markdown files in _posts
for file in _posts/*.md; do
  # Skip already processed files (those that start with a date)
  if [[ $(basename "$file") =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
    echo "Skipping already processed file: $file"
    continue
  fi
  
  # Extract the date from the frontmatter
  date=$(grep -m 1 "date:" "$file" | sed -E 's/date: *[\x27"]?([0-9]{4}-[0-9]{2}-[0-9]{2}).*[\x27"]?/\1/')
  
  if [[ -z "$date" ]]; then
    echo "Could not extract date from $file"
    continue
  fi
  
  # Create new filename
  new_file="_posts/$date-$(basename "$file")"
  echo "Processing $file -> $new_file"
  
  # Update frontmatter - remove description and tags, add layout: post
  sed -i '' '1,/^---$/!b;/^description:/d;/^tags:/d;/^date:/a\
layout: post' "$file"
  
  # Rename the file
  mv "$file" "$new_file"
  echo "Updated and renamed: $new_file"
done 