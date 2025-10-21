#!/usr/bin/env python3
"""
Markdown to EPUB 3.3 Converter

Converts Markdown manuscripts into properly formatted EPUB 3.3 ebooks.
"""

import argparse
import os
import re
import shutil
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import markdown
    import yaml
    from PIL import Image
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    exit(1)


class MarkdownToEpub:
    """Convert Markdown manuscripts to EPUB 3.3"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.temp_dir = Path("_epub_temp")
        self.book_id = str(uuid.uuid4())
        self.chapters: List[Dict] = []
        
    def build(self):
        """Main build process"""
        print(f"Building EPUB: {self.config['title']}")
        print(f"Author: {self.config['author']}")
        print()
        
        # Create temp directory structure
        self._create_structure()
        
        # Process chapters
        self._process_chapters()
        
        # Copy assets
        self._copy_assets()
        
        # Generate EPUB files
        self._generate_mimetype()
        self._generate_container_xml()
        self._generate_content_opf()
        self._generate_nav_xhtml()
        self._generate_css()
        
        # Package EPUB
        self._package_epub()
        
        # Cleanup
        self._cleanup()
        
        print(f"\n✓ SUCCESS: {self.config['output']}")
        print(f"  Chapters: {len(self.chapters)}")
        print(f"  Size: {os.path.getsize(self.config['output']) / 1024:.1f} KB")
        
    def _create_structure(self):
        """Create EPUB directory structure"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        
        dirs = [
            self.temp_dir,
            self.temp_dir / "META-INF",
            self.temp_dir / "OEBPS",
            self.temp_dir / "OEBPS" / "Text",
            self.temp_dir / "OEBPS" / "Styles",
            self.temp_dir / "OEBPS" / "Images",
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def _process_chapters(self):
        """Convert Markdown chapters to XHTML"""
        input_dir = Path(self.config['input_dir'])
        
        # Find chapter files
        chapter_files = sorted(
            input_dir.glob("chapter-*.md"),
            key=lambda x: int(re.search(r'chapter-(\d+)', x.name).group(1))
        )
        
        if not chapter_files:
            chapter_files = sorted(
                input_dir.glob("chap-*.md"),
                key=lambda x: int(re.search(r'chap-(\d+)', x.name).group(1))
            )
        
        if not chapter_files:
            raise ValueError(f"No chapter files found in {input_dir}")
        
        print(f"Found {len(chapter_files)} chapters")
        
        # Convert each chapter
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'smarty'])
        
        for idx, chapter_file in enumerate(chapter_files, 1):
            print(f"  Converting: {chapter_file.name}")
            
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract chapter title from first heading
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            chapter_title = title_match.group(1) if title_match else f"Chapter {idx}"
            
            # Convert markdown to HTML
            html_content = md.convert(content)
            md.reset()
            
            # Generate XHTML file
            xhtml_filename = f"chapter-{idx:02d}.xhtml"
            xhtml_path = self.temp_dir / "OEBPS" / "Text" / xhtml_filename
            
            xhtml = self._generate_xhtml(chapter_title, html_content)
            
            with open(xhtml_path, 'w', encoding='utf-8') as f:
                f.write(xhtml)
            
            self.chapters.append({
                'id': f'chap{idx:02d}',
                'href': f'Text/{xhtml_filename}',
                'title': chapter_title,
                'filename': xhtml_filename
            })
    
    def _generate_xhtml(self, title: str, body: str) -> str:
        """Generate XHTML file"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{self.config['language']}" lang="{self.config['language']}">
<head>
    <meta charset="UTF-8"/>
    <title>{self._escape_xml(title)}</title>
    <link rel="stylesheet" type="text/css" href="../Styles/stylesheet.css"/>
</head>
<body>
{body}
</body>
</html>'''
    
    def _copy_assets(self):
        """Copy cover and other images"""
        cover_path = self.config.get('cover')
        if cover_path and Path(cover_path).exists():
            print(f"  Adding cover: {cover_path}")
            cover_ext = Path(cover_path).suffix
            dest = self.temp_dir / "OEBPS" / "Images" / f"cover{cover_ext}"
            shutil.copy(cover_path, dest)
            
            # Generate cover XHTML
            cover_xhtml = self._generate_cover_xhtml(f"Images/cover{cover_ext}")
            cover_path_xhtml = self.temp_dir / "OEBPS" / "Text" / "cover.xhtml"
            with open(cover_path_xhtml, 'w', encoding='utf-8') as f:
                f.write(cover_xhtml)
    
    def _generate_cover_xhtml(self, image_href: str) -> str:
        """Generate cover page XHTML"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <meta charset="UTF-8"/>
    <title>Cover</title>
    <link rel="stylesheet" type="text/css" href="../Styles/stylesheet.css"/>
</head>
<body class="cover">
    <div class="cover-image">
        <img src="../{image_href}" alt="Cover" />
    </div>
</body>
</html>'''
    
    def _generate_mimetype(self):
        """Generate mimetype file (must be first and uncompressed)"""
        with open(self.temp_dir / "mimetype", 'w', encoding='ascii', newline='') as f:
            f.write('application/epub+zip')
    
    def _generate_container_xml(self):
        """Generate META-INF/container.xml"""
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
        
        with open(self.temp_dir / "META-INF" / "container.xml", 'w', encoding='utf-8') as f:
            f.write(xml)
    
    def _generate_content_opf(self):
        """Generate OEBPS/content.opf (EPUB 3.3)"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Manifest items
        manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
        manifest.append('<item id="css" href="Styles/stylesheet.css" media-type="text/css"/>')
        
        # Cover
        if self.config.get('cover') and Path(self.config['cover']).exists():
            cover_ext = Path(self.config['cover']).suffix.lstrip('.')
            media_type = f'image/{cover_ext}' if cover_ext != 'jpg' else 'image/jpeg'
            manifest.append(f'<item id="cover-image" href="Images/cover.{cover_ext}" media-type="{media_type}" properties="cover-image"/>')
            manifest.append('<item id="cover" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>')
        
        # Chapters
        for chap in self.chapters:
            manifest.append(f'<item id="{chap["id"]}" href="{chap["href"]}" media-type="application/xhtml+xml"/>')
        
        # Spine
        spine = []
        if self.config.get('cover'):
            spine.append('<itemref idref="cover"/>')
        for chap in self.chapters:
            spine.append(f'<itemref idref="{chap["id"]}"/>')
        
        opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" xml:lang="{self.config['language']}" unique-identifier="book-id">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:identifier id="book-id">urn:uuid:{self.book_id}</dc:identifier>
        <dc:title>{self._escape_xml(self.config['title'])}</dc:title>
        <dc:creator>{self._escape_xml(self.config['author'])}</dc:creator>
        <dc:language>{self.config['language']}</dc:language>
        <dc:date>{today}</dc:date>
        <meta property="dcterms:modified">{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}Z</meta>
    </metadata>
    <manifest>
        {chr(10).join(f'        {item}' for item in manifest)}
    </manifest>
    <spine>
        {chr(10).join(f'        {item}' for item in spine)}
    </spine>
</package>'''
        
        with open(self.temp_dir / "OEBPS" / "content.opf", 'w', encoding='utf-8') as f:
            f.write(opf)
    
    def _generate_nav_xhtml(self):
        """Generate OEBPS/nav.xhtml (EPUB 3 TOC)"""
        toc_items = []
        for chap in self.chapters:
            toc_items.append(f'            <li><a href="{chap["href"]}">{self._escape_xml(chap["title"])}</a></li>')
        
        nav = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{self.config['language']}" lang="{self.config['language']}">
<head>
    <meta charset="UTF-8"/>
    <title>Table of Contents</title>
    <link rel="stylesheet" type="text/css" href="Styles/stylesheet.css"/>
</head>
<body>
    <nav epub:type="toc" id="toc">
        <h1>Table of Contents</h1>
        <ol>
{chr(10).join(toc_items)}
        </ol>
    </nav>
</body>
</html>'''
        
        with open(self.temp_dir / "OEBPS" / "nav.xhtml", 'w', encoding='utf-8') as f:
            f.write(nav)
    
    def _generate_css(self):
        """Generate default CSS"""
        css = '''/* EPUB 3.3 Stylesheet */

body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 0;
    padding: 1em;
}

h1, h2, h3, h4, h5, h6 {
    font-family: Georgia, "Times New Roman", serif;
    font-weight: bold;
    margin: 1.5em 0 0.5em;
    line-height: 1.2;
}

h1 { font-size: 2em; text-align: center; }
h2 { font-size: 1.5em; }
h3 { font-size: 1.3em; }

p {
    margin: 0 0 1em;
    text-indent: 0;
}

blockquote {
    margin: 1em 2em;
    padding-left: 1em;
    border-left: 3px solid #ccc;
    font-style: italic;
}

blockquote.epigraph {
    border: none;
    text-align: center;
    font-style: italic;
    margin: 2em auto;
    max-width: 80%;
}

code {
    font-family: "Courier New", Courier, monospace;
    background-color: #f4f4f4;
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

pre {
    background-color: #f4f4f4;
    padding: 1em;
    overflow-x: auto;
    border-radius: 5px;
}

pre code {
    background: none;
    padding: 0;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 2em 0;
}

.cover {
    text-align: center;
    margin: 0;
    padding: 0;
}

.cover-image img {
    max-width: 100%;
    height: auto;
}

/* Table of Contents */
nav#toc h1 {
    text-align: center;
}

nav#toc ol {
    list-style-type: none;
    padding-left: 0;
}

nav#toc li {
    margin: 0.5em 0;
}

nav#toc a {
    text-decoration: none;
    color: #333;
}

nav#toc a:hover {
    text-decoration: underline;
}
'''
        
        with open(self.temp_dir / "OEBPS" / "Styles" / "stylesheet.css", 'w', encoding='utf-8') as f:
            f.write(css)
    
    def _package_epub(self):
        """Package EPUB as ZIP"""
        output_path = Path(self.config['output'])
        if output_path.exists():
            output_path.unlink()
        
        print(f"\nPackaging EPUB...")
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as epub:
            # mimetype MUST be first and uncompressed
            epub.write(
                self.temp_dir / "mimetype",
                "mimetype",
                compress_type=zipfile.ZIP_STORED
            )
            
            # Add all other files
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    if file == 'mimetype':
                        continue
                    
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(self.temp_dir)
                    epub.write(file_path, arcname, compress_type=zipfile.ZIP_DEFLATED)
    
    def _cleanup(self):
        """Remove temporary directory"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    @staticmethod
    def _escape_xml(text: str) -> str:
        """Escape XML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))


def load_config(args) -> Dict:
    """Load configuration from args or config file"""
    config = {}
    
    # Load from config file if provided
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    
    # Override with CLI args
    if args.title:
        config['title'] = args.title
    if args.author:
        config['author'] = args.author
    if args.language:
        config['language'] = args.language
    if args.input_dir:
        config['input_dir'] = args.input_dir
    if args.output:
        config['output'] = args.output
    if args.cover:
        config['cover'] = args.cover
    
    # Defaults
    config.setdefault('title', 'Untitled')
    config.setdefault('author', 'Unknown Author')
    config.setdefault('language', 'en')
    config.setdefault('input_dir', 'manuscript')
    config.setdefault('output', 'book.epub')
    
    # Validate
    if not Path(config['input_dir']).exists():
        raise ValueError(f"Input directory not found: {config['input_dir']}")
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown manuscripts to EPUB 3.3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --title "My Novel" --author "Your Name"
  %(prog)s --config book.yaml
  %(prog)s --input-dir chapters/ --output my-book.epub --cover cover.png
        '''
    )
    
    parser.add_argument('--config', help='YAML configuration file')
    parser.add_argument('--title', help='Book title')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--language', default='en', help='Language code (default: en)')
    parser.add_argument('--input-dir', help='Input directory containing chapter-*.md files')
    parser.add_argument('--output', help='Output EPUB file')
    parser.add_argument('--cover', help='Cover image (PNG/JPG)')
    
    args = parser.parse_args()
    
    try:
        config = load_config(args)
        converter = MarkdownToEpub(config)
        converter.build()
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)


if __name__ == '__main__':
    main()

