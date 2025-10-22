#!/usr/bin/env python3
"""Fix special characters in markdown files for PDF generation"""

import sys
from pathlib import Path

def fix_special_chars(content):
    """Replace problematic special characters with standard ones"""
    replacements = {
        # Curly quotes
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        # Em dash and en dash
        '\u2014': '--',  # Em dash
        '\u2013': '-',   # En dash
        # Other special characters
        '\u2026': '...',  # Ellipsis
        '\u00a0': ' ',    # Non-breaking space
        '\u2022': '*',    # Bullet
        # Fix literal \n in text (not actual newlines)
        '\\n': ' ',       # Literal backslash-n becomes space
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    return content

def main():
    if len(sys.argv) != 3:
        print("Usage: python fix_special_chars.py input.md output.md")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    print(f"Reading: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Fixing special characters...")
    fixed_content = fix_special_chars(content)
    
    print(f"Writing: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("Done!")

if __name__ == '__main__':
    main()

