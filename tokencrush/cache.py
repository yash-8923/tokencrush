import json
import os
import hashlib
from pathlib import Path

CACHE_FILE = ".tokencrush_cache.json"
OUTPUT_DIR = ".tokencrush_output"

def _get_file_hash(path: str) -> str:
    stat = os.stat(path)
    return hashlib.md5(f"{path}:{stat.st_size}:{stat.st_mtime}".encode()).hexdigest()

def load_cache(directory: str) -> dict:
    cache_path = os.path.join(directory, CACHE_FILE)
    if os.path.exists(cache_path):
        try:
            with open(cache_path) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(directory: str, cache: dict):
    cache_path = os.path.join(directory, CACHE_FILE)
    with open(cache_path, 'w') as f:
        json.dump(cache, f, indent=2)

def is_cached(path: str, cache: dict) -> bool:
    return cache.get(path, {}).get("hash") == _get_file_hash(path)

def cache_file(path: str, cache: dict, stats: dict):
    cache[path] = {
        "hash": _get_file_hash(path),
        **stats
    }

def save_markdown(directory: str, original_path: str, markdown: str):
    out_dir = os.path.join(directory, OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    rel = os.path.relpath(original_path, directory)
    out_path = os.path.join(out_dir, rel + ".md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    return out_path
