# markdown-to-epub

A clean, cross-platform Python tool to convert Markdown manuscripts into properly formatted EPUB 3.3 ebooks.

## Features

✅ **EPUB 3.3 Standard** - Modern, compliant ebook format  
✅ **Full Markdown Support** - Bold, italic, links, images, code blocks, blockquotes  
✅ **Cross-Platform** - Works on Windows, Mac, Linux  
✅ **No External Dependencies** - Built-in ZIP packaging (no 7-Zip needed)  
✅ **Flexible Configuration** - CLI args or config file  
✅ **Cover Images** - Automatic cover page generation  
✅ **Custom CSS** - Themeable styling  
✅ **Auto TOC** - Generates table of contents from chapters  

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

**Try the example first!**

```bash
# Test with the included example
python markdown_to_epub.py --config example/book.yaml

# Then try with your own manuscript
python markdown_to_epub.py --title "My Novel" --author "Your Name"

# Custom paths
python markdown_to_epub.py \
  --title "My Novel" \
  --author "Your Name" \
  --input-dir chapters/ \
  --output my-novel.epub \
  --cover cover.png

# Using config file
python markdown_to_epub.py --config book.yaml
```

## Project Structure

Your manuscript folder should contain:

```
manuscript/
├── chapter-01.md
├── chapter-02.md
├── chapter-03.md
└── ...
```

Chapter files should start with a heading:

```markdown
# Chapter 1: The Beginning

Your content here...
```

## Configuration File (Optional)

Create `book.yaml`:

```yaml
title: "My Novel"
author: "Your Name"
language: "en"
description: "A compelling story about..."

input_dir: "manuscript"
output: "my-novel.epub"
cover: "cover.png"

metadata:
  publisher: "Your Publisher"
  published_date: "2025-01-01"
  isbn: "978-0-000000-00-0"
  series: "Series Name"
  series_number: 1
```

## Markdown Support

- **Bold**: `**text**` or `__text__`
- **Italic**: `*text*` or `_text_`
- **Links**: `[text](url)`
- **Images**: `![alt](path)`
- **Headers**: `# H1` through `###### H6`
- **Blockquotes**: `> text`
- **Lists**: `- item` or `1. item`
- **Code blocks**: ` ```language ... ``` `
- **Horizontal rules**: `---` or `***`

## License

MIT License - Use for any purpose, commercial or personal.

## Credits

Created to solve a common problem: converting well-structured Markdown manuscripts into properly formatted EPUBs without fighting with complex tools.

**Made with ❤️ for writers who love Markdown**
