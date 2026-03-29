#!/usr/bin/env python3
"""
Build course pages from markdown sources.

Converts markdown files to styled HTML pages with:
- Dartmouth-themed styling (matching llm-course)
- Navigation bar with links to all spoke pages
- Dark/light theme toggle
- Tables, lists, code blocks, links

Adapted from ContextLab/llm-course build-pages.py.

Usage:
    python build-pages.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def strip_frontmatter(text):
    """Remove YAML frontmatter from markdown files."""
    if text.startswith("---"):
        end_match = re.search(r"\n---\s*\n", text[3:])
        if end_match:
            text = text[3 + end_match.end():]
    return text


def markdown_to_html(md_text):
    """Convert markdown text to HTML (simplified processor)."""
    md_text = strip_frontmatter(md_text)
    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    in_ol = False
    in_code = False
    in_table = False

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = stripped[3:].strip()
                cls = f' class="language-{lang}"' if lang else ""
                html_lines.append(f"<pre><code{cls}>")
                in_code = True
            continue

        if in_code:
            html_lines.append(
                line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            continue

        # Empty line
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_table:
                html_lines.append("</tbody></table>")
                in_table = False
            html_lines.append("")
            continue

        # Headers
        header_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if header_match:
            level = len(header_match.group(1))
            text = inline_format(header_match.group(2))
            slug = re.sub(r"[^\w\s-]", "", text.lower())
            slug = re.sub(r"[\s]+", "-", slug).strip("-")
            html_lines.append(f'<h{level} id="{slug}">{text}</h{level}>')
            continue

        # Table separator (skip)
        if re.match(r"^\|[\s\-:|]+\|$", stripped):
            continue

        # Table row
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            if not in_table:
                html_lines.append('<table><thead><tr>')
                for cell in cells:
                    html_lines.append(f"<th>{inline_format(cell)}</th>")
                html_lines.append("</tr></thead><tbody>")
                in_table = True
            else:
                html_lines.append("<tr>")
                for cell in cells:
                    html_lines.append(f"<td>{inline_format(cell)}</td>")
                html_lines.append("</tr>")
            continue

        # Unordered list
        list_match = re.match(r"^[\-\*]\s+(.+)$", stripped)
        if list_match:
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{inline_format(list_match.group(1))}</li>")
            continue

        # Ordered list
        ol_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ol_match:
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            html_lines.append(f"<li>{inline_format(ol_match.group(1))}</li>")
            continue

        # Horizontal rule
        if re.match(r"^---+$", stripped):
            html_lines.append("<hr>")
            continue

        # Paragraph
        html_lines.append(f"<p>{inline_format(stripped)}</p>")

    # Close any open tags
    if in_list:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")
    if in_code:
        html_lines.append("</code></pre>")
    if in_table:
        html_lines.append("</tbody></table>")

    return "\n".join(html_lines)


def inline_format(text):
    """Apply inline markdown formatting."""
    # Images
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def get_page_template(title, content, active_page=""):
    """Wrap content in full HTML page with nav and styling."""
    nav_items = [
        ("../index.html", "Home", "home"),
        ("slides.html", "Slides", "slides"),
        ("assignments.html", "Assignments", "assignments"),
        ("stories.html", "Data Stories", "stories"),
        ("syllabus.html", "Syllabus", "syllabus"),
    ]

    nav_html = ""
    for href, label, page_id in nav_items:
        active = ' class="active"' if page_id == active_page else ""
        nav_html += f'            <a href="{href}"{active}>{label}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Storytelling with Data</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="../css/base-styles.css">
    <link rel="stylesheet" href="../css/site-styles.css">
    <style>
        .page-content {{
            max-width: 900px;
            margin: 100px auto var(--spacing-2xl);
            padding: 0 var(--spacing-xl);
        }}
        .page-content h1 {{
            font-size: 2rem;
            margin-bottom: var(--spacing-lg);
            background: var(--gradient-accent);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .page-content h2 {{ margin-top: var(--spacing-xl); margin-bottom: var(--spacing-md); }}
        .page-content h3 {{ margin-top: var(--spacing-lg); margin-bottom: var(--spacing-sm); }}
        .page-content p {{ margin-bottom: var(--spacing-md); line-height: 1.7; color: var(--text-secondary); }}
        .page-content a {{ color: var(--primary-color); text-decoration: none; }}
        .page-content a:hover {{ text-decoration: underline; }}
        .page-content ul, .page-content ol {{ margin-bottom: var(--spacing-md); padding-left: var(--spacing-xl); }}
        .page-content li {{ margin-bottom: var(--spacing-xs); line-height: 1.6; color: var(--text-secondary); }}
        .page-content table {{ width: 100%; border-collapse: collapse; margin-bottom: var(--spacing-lg); }}
        .page-content th, .page-content td {{
            padding: var(--spacing-sm) var(--spacing-md);
            border: 1px solid var(--border-color);
            text-align: left;
        }}
        .page-content th {{ background: var(--surface-color); font-weight: 600; }}
        .page-content pre {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: var(--spacing-md);
            overflow-x: auto;
            margin-bottom: var(--spacing-md);
        }}
        .page-content code {{ font-family: 'Fira Code', monospace; font-size: 0.9em; }}
        .page-content hr {{ border: none; border-top: 1px solid var(--border-color); margin: var(--spacing-xl) 0; }}
        .download-btn {{
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-sm);
            padding: var(--spacing-sm) var(--spacing-md);
            background: var(--primary-color);
            color: white;
            border-radius: var(--radius-md);
            text-decoration: none;
            font-size: 0.875rem;
            transition: background var(--transition-fast);
        }}
        .download-btn:hover {{ background: var(--primary-dark); text-decoration: none; }}
    </style>
</head>
<body>
    <nav class="course-nav">
        <a class="logo" href="../index.html">SWD</a>
        <div class="nav-links">
{nav_html}            <button class="theme-toggle" id="themeToggle">☀️</button>
        </div>
    </nav>

    <main class="page-content">
{content}
    </main>

    <script>
        const themeToggle = document.getElementById('themeToggle');
        const saved = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', saved);
        themeToggle.textContent = saved === 'dark' ? '☀️' : '🌙';
        themeToggle.addEventListener('click', function() {{
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            this.textContent = next === 'dark' ? '☀️' : '🌙';
        }});
    </script>
</body>
</html>"""


def build_assignment_pages():
    """Build HTML pages for each assignment from markdown source."""
    assignments_dir = REPO_ROOT / "assignments"
    pages_dir = REPO_ROOT / "pages"

    for assignment_dir in sorted(assignments_dir.iterdir()):
        if not assignment_dir.is_dir():
            continue

        # Find markdown file
        md_files = list(assignment_dir.glob("*.md"))
        if not md_files:
            continue

        md_file = md_files[0]
        md_text = md_file.read_text(encoding="utf-8")
        content_html = markdown_to_html(md_text)

        title = assignment_dir.name.replace("-", " ").title()
        page_html = get_page_template(title, content_html, active_page="assignments")

        # Write to assignment dir as index.html
        out_file = assignment_dir / "index.html"
        out_file.write_text(page_html, encoding="utf-8")
        print(f"  Built: {out_file}")


def build_syllabus_page():
    """Build the syllabus spoke page."""
    # Check for markdown syllabus, otherwise create placeholder
    syllabus_md = REPO_ROOT / "admin" / "syllabus.md"
    pages_dir = REPO_ROOT / "pages"

    if syllabus_md.exists():
        md_text = syllabus_md.read_text(encoding="utf-8")
        content_html = markdown_to_html(md_text)
    else:
        content_html = """
        <h1>Syllabus</h1>
        <p>The course syllabus is available as a
        <a href="../admin/PSYC_81_syllabus.pdf">PDF download</a>.</p>
"""

    page_html = get_page_template("Syllabus", content_html, active_page="syllabus")
    out_file = pages_dir / "syllabus.html"
    out_file.write_text(page_html, encoding="utf-8")
    print(f"  Built: {out_file}")


def build_slides_index():
    """Build the slides index spoke page."""
    slides_dir = REPO_ROOT / "slides"
    pages_dir = REPO_ROOT / "pages"

    # Find all compiled slide HTML files
    slide_htmls = sorted(slides_dir.glob("*.html"))

    content = "<h1>Lecture Slides</h1>\n"
    content += "<p>All lecture presentations for Storytelling with Data.</p>\n"
    content += '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: var(--spacing-lg); margin-top: var(--spacing-xl);">\n'

    for html_file in slide_htmls:
        name = html_file.stem.replace("-", " ").replace("_", " ").title()
        content += f"""    <a href="../slides/{html_file.name}" style="
        display: block; padding: var(--spacing-lg); background: var(--surface-color);
        border: 1px solid var(--border-color); border-radius: var(--radius-lg);
        text-decoration: none; transition: transform var(--transition-fast), box-shadow var(--transition-fast);"
        onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='var(--shadow-lg)'"
        onmouseout="this.style.transform=''; this.style.boxShadow=''">
        <h3 style="color: var(--text-primary); margin-bottom: var(--spacing-xs);">{name}</h3>
        <p style="color: var(--text-muted); font-size: 0.875rem;"><i class="fas fa-presentation-screen"></i> View slides</p>
    </a>\n"""

    content += "</div>\n"

    page_html = get_page_template("Slides", content, active_page="slides")
    out_file = pages_dir / "slides.html"
    out_file.write_text(page_html, encoding="utf-8")
    print(f"  Built: {out_file}")


def build_assignments_index():
    """Build the assignments index spoke page."""
    assignments_dir = REPO_ROOT / "assignments"
    pages_dir = REPO_ROOT / "pages"

    content = "<h1>Assignments</h1>\n"
    content += "<p>Course assignments for Storytelling with Data.</p>\n"
    content += '<div style="margin-top: var(--spacing-xl);">\n'

    for assignment_dir in sorted(assignments_dir.iterdir()):
        if not assignment_dir.is_dir():
            continue

        name = assignment_dir.name.replace("-", " ").replace("_", " ").title()
        has_html = (assignment_dir / "index.html").exists()
        has_pdf = list(assignment_dir.glob("*.pdf"))

        content += f"""    <div style="padding: var(--spacing-lg); background: var(--surface-color);
        border: 1px solid var(--border-color); border-radius: var(--radius-lg);
        margin-bottom: var(--spacing-md);">
        <h3 style="color: var(--text-primary); margin-bottom: var(--spacing-sm);">{name}</h3>
        <div style="display: flex; gap: var(--spacing-md);">
"""
        if has_html:
            content += f'            <a href="../assignments/{assignment_dir.name}/index.html" class="download-btn"><i class="fas fa-eye"></i> View</a>\n'
        if has_pdf:
            pdf_name = has_pdf[0].name
            content += f'            <a href="../assignments/{assignment_dir.name}/{pdf_name}" class="download-btn"><i class="fas fa-download"></i> PDF</a>\n'

        content += "        </div>\n    </div>\n"

    content += "</div>\n"

    page_html = get_page_template("Assignments", content, active_page="assignments")
    out_file = pages_dir / "assignments.html"
    out_file.write_text(page_html, encoding="utf-8")
    print(f"  Built: {out_file}")


def main():
    # Ensure output directories exist (pages/ is gitignored)
    (REPO_ROOT / "pages").mkdir(parents=True, exist_ok=True)
    print("Building course pages...")
    print("\nAssignment pages:")
    build_assignment_pages()
    print("\nSyllabus page:")
    build_syllabus_page()
    print("\nSlides index:")
    build_slides_index()
    print("\nAssignments index:")
    build_assignments_index()
    print("\nDone!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
