import os
import re
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".pdf", ".pptx", ".ppt", ".docx", ".doc",
    ".xlsx", ".xls", ".csv", ".ipynb",
    ".html", ".htm", ".xml", ".json", ".yaml", ".yml",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff",
    ".mp3", ".wav", ".m4a",
    ".zip",
    ".md", ".txt", ".rst"
}

def convert_file(path: str) -> str:
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(path)
    return _clean(result.text_content)

def _clean(text: str) -> str:
    # Remove consecutive blank lines (collapse to one)
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip trailing whitespace per line
    lines = [l.rstrip() for l in text.split('\n')]
    # Remove lines that are only whitespace
    lines = [l for l in lines if l.strip() != '' or l == '']
    return '\n'.join(lines).strip()

SKIP_DIRS = {'node_modules', '__pycache__', 'venv', 'env', 'dist', 'build', '.tokencrush_output'}
SKIP_FILES = {'.tokencrush_cache.json'}

def find_convertible_files(directory: str) -> list[str]:
    files = []
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in SKIP_DIRS]
        for f in filenames:
            if f in SKIP_FILES or f.startswith('.tokencrush'):
                continue
            ext = Path(f).suffix.lower()
            if ext in SUPPORTED_EXTENSIONS:
                files.append(os.path.join(root, f))
    return files
