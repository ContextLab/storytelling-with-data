#!/usr/bin/env python3
"""Generate index.html from slides/README.md (the course outline).

Usage:
    python scripts/build-index.py              # reads slides/README.md, writes index.html
    python scripts/build-index.py outline.md   # custom input
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "slides" / "README.md"
DEFAULT_OUTPUT = REPO_ROOT / "index.html"


def parse_outline(text: str):
    """Parse the weekly schedule markdown into structured data."""
    weeks = []
    part2_content = ""
    current_week = None
    current_day = None
    current_subsection = None  # 'resources', 'recordings', 'submissions', None
    in_part2 = False
    part2_lines = []

    for line in text.splitlines():
        # Detect Part II section (# Part II at end of file)
        if re.match(r"^# Part II\s*$", line):
            in_part2 = True
            continue
        if in_part2:
            part2_lines.append(line)
            continue

        # Week header: ## Week N: Title (dates)
        m = re.match(r"^## Week (\d+):\s*(.+?)(?:\s*\((.+?)\))?\s*$", line)
        if m:
            current_week = {
                "number": int(m.group(1)),
                "title": m.group(2).strip(),
                "dates": m.group(3).strip() if m.group(3) else "",
                "days": [],
                "resources": [],
                "recordings": [],
                "submissions": [],
            }
            weeks.append(current_week)
            current_day = None
            current_subsection = None
            continue

        if current_week is None:
            continue

        # Day header: ### DayName Date — Title
        m = re.match(r"^### (.+?)$", line)
        if m:
            current_subsection = None
            day_text = m.group(1).strip()
            current_day = {"heading": day_text, "items": []}
            current_week["days"].append(current_day)
            continue

        # Subsection headers
        if re.match(r"^####\s+Resources?\s*$", line, re.IGNORECASE):
            current_subsection = "resources"
            current_day = None
            continue
        if re.match(r"^####\s+Lecture recordings?\s*$", line, re.IGNORECASE):
            current_subsection = "recordings"
            current_day = None
            continue
        if re.match(r"^####\s+Student submissions?\s*$", line, re.IGNORECASE):
            current_subsection = "submissions"
            current_day = None
            continue

        # List items
        m_item = re.match(r"^(\s*)-\s+(.+)$", line)
        if m_item:
            content = m_item.group(2)
            indent = len(m_item.group(1))
            if current_subsection == "resources":
                current_week["resources"].append((indent, content))
            elif current_subsection == "recordings":
                current_week["recordings"].append((indent, content))
            elif current_subsection == "submissions":
                current_week["submissions"].append((indent, content))
            elif current_day is not None:
                current_day["items"].append(content)
            continue

    part2_content = "\n".join(part2_lines)
    return weeks, part2_content


def md_to_html(text: str) -> str:
    """Convert simple markdown inline formatting to HTML."""
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Links: [text](url) — make slide links relative to slides/
    def link_replace(m):
        label, url = m.group(1), m.group(2)
        if not url.startswith("http") and not url.startswith("../") and not url.startswith("#"):
            url = f"slides/{url}"
        return f'<a href="{url}">{label}</a>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replace, text)
    return text


def render_list_items(items, css_class=""):
    """Render a list of (indent, content) or plain strings as nested HTML."""
    if not items:
        return ""
    html = f'<ul class="{css_class}">\n' if css_class else "<ul>\n"
    for item in items:
        if isinstance(item, tuple):
            indent, content = item
            html += f"  <li>{md_to_html(content)}</li>\n"
        else:
            html += f"  <li>{md_to_html(item)}</li>\n"
    html += "</ul>\n"
    return html


def render_week(week):
    """Render a single week section."""
    num = week["number"]
    title = week["title"]
    dates = week["dates"]
    is_noclass = "No Class" in title or "No class" in title

    # Week header
    html = f'''
    <div class="week-section" id="week{num}">
      <div class="week-header" onclick="toggleWeek(this)">
        <div class="week-header-info">
          <span class="week-number">Week {num}</span>
          <span class="week-dates">{dates}</span>
          <span class="week-theme">{title}</span>
        </div>
        <i class="fas fa-chevron-down expand-icon"></i>
      </div>
      <div class="week-content">
'''

    if is_noclass and not week["days"]:
        html += '        <p class="no-class-notice"><em>No class this week</em></p>\n'
    else:
        for day in week["days"]:
            heading = day["heading"]
            # Detect no-class days
            no_class = any("No class" in it or "no class" in it for it in day["items"])
            cancelled_class = "cancelled" if no_class else ""

            html += f'        <div class="day-row {cancelled_class}">\n'
            html += f'          <div class="day-heading">{md_to_html(heading)}</div>\n'
            if day["items"]:
                html += '          <div class="day-details">\n'
                html += render_list_items(day["items"])
                html += '          </div>\n'
            html += '        </div>\n'

    # Resources accordion
    if week["resources"]:
        html += '        <details class="week-details">\n'
        html += '          <summary><i class="fas fa-book"></i> Resources</summary>\n'
        html += render_list_items(week["resources"])
        html += '        </details>\n'

    # Recordings accordion
    if week["recordings"]:
        html += '        <details class="week-details">\n'
        html += '          <summary><i class="fas fa-play-circle"></i> Lecture Recordings</summary>\n'
        html += render_list_items(week["recordings"])
        html += '        </details>\n'

    # Student submissions
    if week["submissions"]:
        html += '        <details class="week-details">\n'
        html += '          <summary><i class="fas fa-film"></i> Student Submissions</summary>\n'
        html += render_list_items(week["submissions"])
        html += '        </details>\n'

    html += '      </div>\n    </div>\n'
    return html


def render_part2(md_text):
    """Render the Part II description section."""
    if not md_text.strip():
        return ""
    # Simple markdown to HTML conversion for the Part II block
    html = '<div class="part2-description">\n'
    in_list = False
    for line in md_text.splitlines():
        line = line.strip()
        if not line:
            if in_list:
                html += "</ol>\n"
                in_list = False
            continue
        if line.startswith("## "):
            if in_list:
                html += "</ol>\n"
                in_list = False
            html += f"<h3>{md_to_html(line[3:])}</h3>\n"
        elif re.match(r"^\d+\.\s", line):
            if not in_list:
                html += "<ol>\n"
                in_list = True
            content = re.sub(r"^\d+\.\s+", "", line)
            html += f"  <li>{md_to_html(content)}</li>\n"
        elif line.startswith("- "):
            html += f"<li>{md_to_html(line[2:])}</li>\n"
        else:
            html += f"<p>{md_to_html(line)}</p>\n"
    if in_list:
        html += "</ol>\n"
    html += "</div>\n"
    return html


def generate_html(weeks, part2_content):
    """Generate the full index.html."""
    # Week pills
    pills = []
    for w in weeks:
        pills.append(f'<a href="#week{w["number"]}" class="week-pill">W{w["number"]}</a>')
    pills.append('<a href="#part2" class="week-pill">Part II</a>')
    pills_html = "\n            ".join(pills)

    # Week sections
    weeks_html = "\n".join(render_week(w) for w in weeks)

    # Part II section
    part2_html = render_part2(part2_content)

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Storytelling with Data - PSYC 81.09</title>
    <meta name="description" content="Course materials for PSYC 81.09: Storytelling with Data - Dartmouth College">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="./css/base-styles.css">
    <link rel="stylesheet" href="./css/site-styles.css">

    <style>
        /* Week pills bar */
        .week-pills {{
            background: var(--surface-color);
            border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem;
            position: sticky;
            top: 60px;
            z-index: 100;
        }}
        .week-pills-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        .week-pill {{
            background: var(--bg-color);
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: var(--radius-full);
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            border: 1px solid var(--border-color);
            transition: all var(--transition-base);
            text-decoration: none;
        }}
        .week-pill:hover {{
            border-color: var(--primary-color);
            color: var(--primary-color);
        }}

        /* Week sections */
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}

        .week-section {{
            margin-bottom: 1rem;
            scroll-margin-top: 140px;
        }}
        .week-header {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1rem 1.5rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .week-header:hover {{
            border-color: var(--primary-color);
            background: var(--surface-hover);
        }}
        .week-header.expanded {{
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            border-bottom-color: transparent;
        }}
        .week-header-info {{
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .week-number {{
            display: inline-block;
            background: var(--gradient-primary);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        .week-dates {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        .week-theme {{
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1.1rem;
        }}
        .expand-icon {{
            color: var(--text-muted);
            transition: transform 0.3s ease;
            flex-shrink: 0;
        }}
        .week-header.expanded .expand-icon {{
            transform: rotate(180deg);
        }}

        .week-content {{
            display: none;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 var(--radius-lg) var(--radius-lg);
            padding: 1.5rem;
        }}
        .week-content.expanded {{
            display: block;
        }}

        /* Day rows */
        .day-row {{
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--border-color);
        }}
        .day-row:last-of-type {{
            border-bottom: none;
        }}
        .day-row.cancelled {{
            opacity: 0.6;
        }}
        .day-heading {{
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }}
        .day-details ul {{
            margin: 0.25rem 0 0 1.25rem;
            padding: 0;
            color: var(--text-secondary);
            line-height: 1.7;
        }}
        .day-details li {{
            margin-bottom: 0.15rem;
        }}
        .day-details a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        .day-details a:hover {{
            text-decoration: underline;
        }}
        .no-class-notice {{
            color: var(--text-muted);
            padding: 1rem 0;
        }}

        /* Week details (resources, recordings) */
        .week-details {{
            margin-top: 1rem;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
        }}
        .week-details summary {{
            padding: 0.75rem 1rem;
            cursor: pointer;
            color: var(--text-secondary);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .week-details summary:hover {{
            color: var(--primary-color);
        }}
        .week-details[open] summary {{
            border-bottom: 1px solid var(--border-color);
        }}
        .week-details ul {{
            margin: 0.5rem 1rem 1rem 2rem;
            padding: 0;
            color: var(--text-secondary);
            line-height: 1.8;
        }}
        .week-details a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        .week-details a:hover {{
            text-decoration: underline;
        }}

        /* Part II description */
        .part2-description {{
            color: var(--text-secondary);
            line-height: 1.7;
        }}
        .part2-description h3 {{
            color: var(--text-primary);
            margin-top: 1.5rem;
        }}
        .part2-description a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        .part2-description a:hover {{
            text-decoration: underline;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .week-pills-container {{ gap: 0.25rem; }}
            .week-pill {{ font-size: 0.75rem; padding: 0.375rem 0.75rem; }}
            .week-header-info {{ gap: 0.5rem; }}
            .week-theme {{ font-size: 1rem; }}
        }}
    </style>
</head>
<body>
    <nav class="course-nav">
        <a class="logo" href="index.html">SWD</a>
        <button class="hamburger" id="hamburger" aria-label="Toggle menu">
            <i class="fas fa-bars"></i>
        </button>
        <div class="nav-links" id="navLinks">
            <a href="index.html" class="active">Home</a>
            <a href="pages/slides.html">Slides</a>
            <a href="pages/assignments.html">Assignments</a>
            <a href="pages/stories.html">Data Stories</a>
            <a href="pages/syllabus.html">Syllabus</a>
            <button class="theme-toggle" id="themeToggle">&#9728;&#65039;</button>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero" style="margin-top: 70px; padding: 3rem 2rem 2rem; text-align: center;
        background: linear-gradient(180deg, var(--surface-color) 0%, var(--bg-color) 100%);">
        <h1 style="font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; margin-bottom: 1rem;
            background: var(--gradient-accent); -webkit-background-clip: text;
            background-clip: text; -webkit-text-fill-color: transparent;
            animation: fadeInUp 0.8s ease;">
            Storytelling with Data
        </h1>
        <p style="font-size: clamp(1rem, 2vw, 1.25rem); color: var(--text-secondary);
            max-width: 700px; margin: 0 auto 1.5rem; animation: fadeInUp 0.8s ease 0.2s both;">
            Learn to tell compelling stories using data science tools and techniques.
            Explore, analyze, and communicate insights through the art of data storytelling.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;
            animation: fadeInUp 0.8s ease 0.3s both;">
            <span style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary);">
                <i class="fas fa-graduation-cap"></i> PSYC 81.09
            </span>
            <span style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary);">
                <i class="fas fa-university"></i> Dartmouth College
            </span>
            <span style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary);">
                <i class="fas fa-code"></i> Python &amp; Jupyter
            </span>
            <span style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary);">
                <i class="fas fa-book-open"></i> Open Course
            </span>
        </div>
    </section>

    <!-- Week Pills -->
    <div class="week-pills">
        <div class="week-pills-container">
            {pills_html}
        </div>
    </div>

    <div class="container">

{weeks_html}

        <!-- Part II Description -->
        <h2 id="part2" style="color: var(--text-primary); font-size: 1.75rem; margin: 2rem 0 1rem;
            padding-bottom: 0.5rem; border-bottom: 2px solid var(--primary-color);
            scroll-margin-top: 140px;">
            Part II
        </h2>
{part2_html}

        <!-- Getting Help -->
        <div class="week-section" id="help" style="margin-top: 2rem;">
            <div class="week-header" onclick="toggleWeek(this)">
                <div class="week-header-info">
                    <span class="week-number" style="background: var(--gradient-secondary);">Resources</span>
                    <span class="week-theme">Getting Help</span>
                </div>
                <i class="fas fa-chevron-down expand-icon"></i>
            </div>
            <div class="week-content">
                <h3>Getting Help</h3>
                <ul>
                    <li><a href="https://chat.dartmouth.edu">Dartmouth AI Chat</a> and <a href="https://chat.openai.com/">ChatGPT</a> &mdash; AI tools for code, ideas, and more</li>
                    <li><a href="https://stackoverflow.com/">Stack Overflow</a> &mdash; Q&amp;A for technical topics</li>
                    <li><a href="https://github.com/ContextLab/CDL-tutorials">CDL Tutorials</a> &mdash; lab tutorials on a variety of topics</li>
                    <li><a href="https://stories-about-data.slack.com">Slack</a> &mdash; course chatroom for Dartmouth students</li>
                </ul>
                <h3>Datasets</h3>
                <ul>
                    <li><a href="https://www.kaggle.com/datasets">Kaggle</a></li>
                    <li><a href="https://github.com/fivethirtyeight/data">FiveThirtyEight</a></li>
                    <li><a href="https://github.com/caesar0301/awesome-public-datasets">Awesome Public Datasets</a></li>
                    <li><a href="https://data.worldbank.org/">World Bank Open Data</a></li>
                    <li><a href="https://apps.who.int/gho/data/node.home">World Health Organization</a></li>
                    <li><a href="https://registry.opendata.aws/">Registry of Open Data on AWS</a></li>
                </ul>
            </div>
        </div>

    </div>

    <!-- Footer -->
    <footer style="text-align: center; padding: 2rem; color: var(--text-muted);
        border-top: 1px solid var(--border-color); margin-top: 2rem; font-size: 0.875rem;">
        <p>
            <a href="https://github.com/ContextLab/storytelling-with-data" style="color: var(--text-secondary);">
                <i class="fab fa-github"></i> GitHub
            </a>
            &nbsp;&middot;&nbsp;
            <a href="https://pbs.dartmouth.edu/" style="color: var(--text-secondary);">Dartmouth PBS</a>
            &nbsp;&middot;&nbsp;
            <a href="https://www.contextlab.io/" style="color: var(--text-secondary);">Contextual Dynamics Lab</a>
        </p>
        <p style="margin-top: 0.5rem;">
            <a href="https://doi.org/10.5281/zenodo.5182775" style="color: var(--text-muted);">
                <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5182775.svg" alt="DOI" style="vertical-align: middle;">
            </a>
        </p>
    </footer>

    <script>
        // Week expand/collapse
        function toggleWeek(header) {{
            const content = header.nextElementSibling;
            header.classList.toggle('expanded');
            content.classList.toggle('expanded');
        }}

        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        const saved = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', saved);
        themeToggle.textContent = saved === 'dark' ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
        themeToggle.addEventListener('click', function() {{
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            this.textContent = next === 'dark' ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
        }});

        // Hamburger menu
        document.getElementById('hamburger').addEventListener('click', function() {{
            document.getElementById('navLinks').classList.toggle('open');
        }});

        // Scroll nav shadow
        window.addEventListener('scroll', function() {{
            const nav = document.querySelector('.course-nav');
            nav.classList.toggle('scrolled', window.scrollY > 10);
        }});
    </script>
</body>
</html>
'''


def main():
    input_file = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_file = DEFAULT_OUTPUT

    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)

    text = input_file.read_text(encoding="utf-8")
    weeks, part2_content = parse_outline(text)

    print(f"Parsed {len(weeks)} weeks from {input_file.name}")

    html = generate_html(weeks, part2_content)
    output_file.write_text(html, encoding="utf-8")
    print(f"Generated {output_file} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
