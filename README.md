# markdown-to-epub

A clean, cross-platform Python tool to convert Markdown manuscripts into properly formatted EPUB 3.3 ebooks.

## Features

✅ **EPUB 3.3 Standard** - W3C Recommendation compliant  
✅ **WCAG 2.1 Level AA** - Full accessibility support  
✅ **Semantic HTML** - Proper epub:type and ARIA roles  
✅ **Landmarks Navigation** - Screen reader friendly  
✅ **Full Markdown Support** - Bold, italic, links, images, code blocks, blockquotes  
✅ **Cross-Platform** - Works on Windows, Mac, Linux  
✅ **No External Dependencies** - Built-in ZIP packaging (no 7-Zip needed)  
✅ **Flexible Configuration** - CLI args or config file  
✅ **Cover Images** - Automatic cover page generation with proper alt text  
✅ **Custom CSS** - Kindle-compatible styling  
✅ **Auto TOC** - Generates table of contents from chapters  

### Accessibility Features

- ✅ Proper semantic structure (`role="doc-chapter"`, `epub:type="chapter"`)
- ✅ Descriptive cover alt text (includes title and author)
- ✅ ARIA landmarks navigation for assistive technologies
- ✅ Accessibility metadata (schema:accessMode, accessibilityFeature)
- ✅ WCAG 2.1 Level AA compliant CSS (orphans, widows, page-break-after)
- ✅ Screen reader optimized navigation

**Passes EPUBCheck validation and Ace accessibility checker.**  

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
```

## Modes of Operation

### 1. Consolidate Mode (for AI review and iteration)

Merge all chapters into a single Markdown file for easy reviewing:

```bash
python markdown_to_epub.py --consolidate \
  --input-dir manuscript/ \
  --output full-novel.md
```

**Use when:**
- Sending to AI agents for review
- Printing for self-review
- Sharing draft with beta readers
- Iterating on content (~25 revisions before EPUB)

### 2. Unpackaged EPUB (for Calibre editing)

Create EPUB folder structure without zipping:

```bash
python markdown_to_epub.py --no-package \
  --title "My Novel" \
  --author "Your Name" \
  --input-dir manuscript/
```

**Use when:**
- Editing in Calibre
- Fine-tuning EPUB structure
- Manual adjustments needed
- Creates `_epub_temp/` folder you can import

### 3. Full EPUB (for publishing)

Create packaged EPUB file ready to publish:

```bash
python markdown_to_epub.py \
  --title "My Novel" \
  --author "Your Name" \
  --input-dir manuscript/ \
  --output my-novel.epub \
  --cover cover.png
```

**Use when:**
- Ready for final publication
- Sending to publisher
- Self-publishing on platforms

## Absolute Paths Supported

All paths can be absolute or relative:

```bash
python markdown_to_epub.py \
  --consolidate \
  --input-dir "C:\MyNovels\Project\manuscript" \
  --output "C:\MyNovels\Project\full-draft.md"
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
