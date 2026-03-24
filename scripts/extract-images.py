#!/usr/bin/env python3
"""
Extract images from .key (Keynote) and .pptx (PowerPoint) files.

.key files are ZIP archives with images in Data/ directory.
.pptx files are ZIP archives with images in ppt/media/ directory.

Usage:
    python extract-images.py <input_file> [--output-dir slides/figs/]
"""

import argparse
import os
import re
import zipfile
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".tiff", ".bmp", ".pdf"}


def slugify(name):
    """Convert a filename to a descriptive slug."""
    name = Path(name).stem.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    return name.strip("-")


def extract_from_key(key_path, output_dir, prefix):
    """Extract images from a Keynote (.key) file (ZIP archive)."""
    extracted = []
    with zipfile.ZipFile(key_path, "r") as z:
        for entry in z.namelist():
            # Keynote stores images in Data/ directory
            if not entry.startswith("Data/"):
                continue
            ext = Path(entry).suffix.lower()
            if ext not in IMAGE_EXTENSIONS:
                continue
            basename = Path(entry).name
            out_name = f"{prefix}-{basename}"
            out_path = output_dir / out_name
            with z.open(entry) as src, open(out_path, "wb") as dst:
                dst.write(src.read())
            extracted.append(out_name)
    return extracted


def extract_from_pptx(pptx_path, output_dir, prefix):
    """Extract images from a PowerPoint (.pptx) file (ZIP archive)."""
    extracted = []
    with zipfile.ZipFile(pptx_path, "r") as z:
        for entry in z.namelist():
            # PowerPoint stores images in ppt/media/
            if not entry.startswith("ppt/media/"):
                continue
            ext = Path(entry).suffix.lower()
            if ext not in IMAGE_EXTENSIONS:
                continue
            basename = Path(entry).name
            out_name = f"{prefix}-{basename}"
            out_path = output_dir / out_name
            with z.open(entry) as src, open(out_path, "wb") as dst:
                dst.write(src.read())
            extracted.append(out_name)
    return extracted


def main():
    parser = argparse.ArgumentParser(
        description="Extract images from .key and .pptx files"
    )
    parser.add_argument("input_file", help="Path to .key or .pptx file")
    parser.add_argument(
        "--output-dir",
        default="slides/figs/",
        help="Output directory for extracted images (default: slides/figs/)",
    )
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        return 1

    prefix = slugify(input_path.stem)
    ext = input_path.suffix.lower()

    if ext == ".key":
        extracted = extract_from_key(input_path, output_dir, prefix)
    elif ext == ".pptx":
        extracted = extract_from_pptx(input_path, output_dir, prefix)
    else:
        print(f"ERROR: Unsupported format: {ext} (expected .key or .pptx)")
        return 1

    print(f"Extracted {len(extracted)} images from {input_path.name}:")
    for name in sorted(extracted):
        print(f"  → {output_dir / name}")

    return 0


if __name__ == "__main__":
    exit(main())
