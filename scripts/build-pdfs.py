#!/usr/bin/env python3
"""
Convert assignment HTML files to PDF using Playwright headless browser.

Usage:
    python build-pdfs.py [--assignments-dir assignments/]

Requires: pip install playwright && playwright install chromium
"""

import argparse
import asyncio
import sys
from pathlib import Path


async def html_to_pdf(html_path, pdf_path):
    """Convert an HTML file to PDF via headless Chromium."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file://{html_path.resolve()}")
        await page.pdf(
            path=str(pdf_path),
            format="Letter",
            margin={"top": "1in", "bottom": "1in", "left": "0.75in", "right": "0.75in"},
            print_background=True,
        )
        await browser.close()


def main():
    parser = argparse.ArgumentParser(description="Convert assignment HTML to PDF")
    parser.add_argument(
        "--assignments-dir",
        default="assignments/",
        help="Directory containing assignment subdirectories",
    )
    args = parser.parse_args()

    assignments_dir = Path(args.assignments_dir)
    if not assignments_dir.exists():
        print(f"ERROR: Directory not found: {assignments_dir}")
        return 1

    html_files = list(assignments_dir.glob("*/index.html"))
    if not html_files:
        print(f"No HTML files found in {assignments_dir}/*/index.html")
        return 0

    converted = 0
    for html_path in sorted(html_files):
        assignment_dir = html_path.parent
        # Name PDF after the directory
        pdf_name = f"{assignment_dir.name}.pdf"
        pdf_path = assignment_dir / pdf_name

        print(f"PDF: {html_path} → {pdf_path}")
        try:
            asyncio.run(html_to_pdf(html_path, pdf_path))
            converted += 1
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\nConverted {converted}/{len(html_files)} files to PDF")
    return 0


if __name__ == "__main__":
    sys.exit(main())
