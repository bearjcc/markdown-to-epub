# Examples

## Basic Novel

```bash
# Create manuscript folder
mkdir manuscript
cd manuscript

# Create chapter files
echo "# Chapter 1: The Beginning\n\nOnce upon a time..." > chapter-01.md
echo "# Chapter 2: The Journey\n\nThe adventure continues..." > chapter-02.md
echo "# Chapter 3: The End\n\nAnd they lived happily ever after." > chapter-03.md

cd ..

# Generate EPUB
python markdown_to_epub.py \
  --title "My First Novel" \
  --author "Your Name" \
  --output my-novel.epub
```

## With Cover Image

```bash
# Same as above, but add:
--cover cover.png
```

## Using Config File

Create `book.yaml`:

```yaml
title: "The Great Adventure"
author: "Jane Doe"
language: "en"
input_dir: "manuscript"
output: "great-adventure.epub"
cover: "images/cover.png"
```

Then run:

```bash
python markdown_to_epub.py --config book.yaml
```

## Chapter Naming

The tool looks for files matching these patterns:

- `chapter-01.md`, `chapter-02.md`, etc.
- `chap-01.md`, `chap-02.md`, etc.

Numbers must be zero-padded (01, 02, not 1, 2).

## Markdown Features

### Headers

```markdown
# Chapter 1: Title
## Section Heading
### Subsection
```

### Emphasis

```markdown
**Bold text**
*Italic text*
***Bold and italic***
```

### Blockquotes

```markdown
> This is a quote.
> It can span multiple lines.
```

### Lists

```markdown
- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2
```

### Code

````markdown
Inline `code` here.

```python
def hello():
    print("Hello, World!")
```
````

### Links

```markdown
[Link text](https://example.com)
```

### Images

```markdown
![Alt text](images/diagram.png)
```

(Images will be embedded in the EPUB)

### Horizontal Rules

```markdown
---
***
```

## Advanced: Non-Fiction Book

For technical books with code examples:

```yaml
title: "Python Programming Guide"
author: "Tech Writer"
language: "en"
input_dir: "chapters"
output: "python-guide.epub"

metadata:
  publisher: "Tech Press"
  genre: "Programming"
  keywords:
    - Python
    - Programming
    - Tutorial
```

## Testing Your EPUB

After generating, test with:

1. **Calibre** (free ebook manager)
2. **Apple Books** (Mac/iOS)
3. **Adobe Digital Editions** (Windows/Mac)
4. **EPUBCheck** (validation tool):
   ```bash
   java -jar epubcheck.jar your-book.epub
   ```

## Troubleshooting

### "No chapter files found"

- Check that files are named `chapter-01.md`, `chapter-02.md`, etc.
- Verify `input_dir` path is correct

### Chapters out of order

- Ensure chapter numbers are zero-padded: `01`, `02`, not `1`, `2`

### Missing images

- Check image paths in markdown match actual file locations
- Images should be relative to the manuscript folder

### Styling issues

- EPUB readers may override some CSS
- Test in multiple readers
- Keep styling simple for best compatibility

