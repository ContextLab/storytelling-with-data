#!/usr/bin/env python3
"""
Generate the Data Stories gallery page from stories.yaml metadata.

Usage:
    python build-gallery.py [--data data/stories.yaml] [--output pages/stories.html]

Reads story metadata and generates an HTML gallery page with:
- Stories grouped by year, then by assignment type
- Embedded YouTube thumbnails with click-to-play
- Client-side search filtering (title, student, year, tags)
"""

import argparse
import re
import sys
from pathlib import Path

import yaml


TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Stories - Storytelling with Data</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="stylesheet" href="../css/base-styles.css">
    <link rel="stylesheet" href="../css/site-styles.css">
    <style>
        .gallery-search {
            max-width: 600px;
            margin: 0 auto var(--spacing-xl);
            position: relative;
        }
        .gallery-search input {
            width: 100%;
            padding: var(--spacing-md) var(--spacing-lg);
            padding-left: 3rem;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-full);
            color: var(--text-primary);
            font-size: 1rem;
            transition: border-color var(--transition-fast);
        }
        .gallery-search input:focus {
            outline: none;
            border-color: var(--primary-color);
        }
        .gallery-search .search-icon {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }
        .result-count {
            text-align: center;
            color: var(--text-secondary);
            margin-bottom: var(--spacing-lg);
        }
        .year-section { margin-bottom: var(--spacing-2xl); }
        .year-section h2 {
            font-size: 1.75rem;
            margin-bottom: var(--spacing-lg);
            color: var(--text-primary);
        }
        .assignment-group { margin-bottom: var(--spacing-xl); }
        .assignment-group h3 {
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: var(--spacing-md);
            text-transform: capitalize;
        }
        .story-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: var(--spacing-lg);
        }
        .story-card {
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            overflow: hidden;
            transition: transform var(--transition-fast), box-shadow var(--transition-fast);
        }
        .story-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        .story-card.hidden { display: none; }
        .story-card .thumb {
            position: relative;
            padding-bottom: 56.25%;
            background: var(--bg-secondary);
        }
        .story-card .thumb img {
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .story-card .thumb .play-btn {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60px;
            height: 60px;
            background: rgba(0,0,0,0.7);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background var(--transition-fast);
        }
        .story-card .thumb .play-btn:hover { background: var(--primary-color); }
        .story-card .thumb .play-btn i { color: white; font-size: 1.5rem; margin-left: 4px; }
        .story-card .info { padding: var(--spacing-md); }
        .story-card .info h4 { margin-bottom: var(--spacing-xs); color: var(--text-primary); }
        .story-card .info .meta { color: var(--text-secondary); font-size: 0.875rem; }
        .story-card .tags { padding: 0 var(--spacing-md) var(--spacing-md); display: flex; flex-wrap: wrap; gap: var(--spacing-xs); }
        .story-card .tags span {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            padding: 2px 8px;
            border-radius: var(--radius-full);
            font-size: 0.75rem;
        }
        .video-modal {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: var(--z-modal);
            align-items: center;
            justify-content: center;
        }
        .video-modal.active { display: flex; }
        .video-modal .modal-content {
            width: 90%;
            max-width: 900px;
            aspect-ratio: 16/9;
        }
        .video-modal .modal-content iframe {
            width: 100%;
            height: 100%;
            border: none;
            border-radius: var(--radius-lg);
        }
        .video-modal .close-btn {
            position: absolute;
            top: var(--spacing-lg);
            right: var(--spacing-lg);
            color: white;
            font-size: 2rem;
            cursor: pointer;
            background: none;
            border: none;
        }
        .unavailable {
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            font-style: italic;
        }
    </style>
</head>
<body>
"""

TEMPLATE_FOOT = """
    <!-- Video Modal -->
    <div class="video-modal" id="videoModal">
        <button class="close-btn" onclick="closeVideo()">&times;</button>
        <div class="modal-content">
            <iframe id="videoFrame" allowfullscreen></iframe>
        </div>
    </div>

    <script>
        // Search filtering
        const searchInput = document.getElementById('storySearch');
        const cards = document.querySelectorAll('.story-card');
        const countEl = document.getElementById('resultCount');

        searchInput.addEventListener('input', function() {
            const q = this.value.toLowerCase();
            let visible = 0;
            cards.forEach(card => {
                const text = card.dataset.search.toLowerCase();
                const match = !q || text.includes(q);
                card.classList.toggle('hidden', !match);
                if (match) visible++;
            });
            countEl.textContent = q ? `${visible} of ${cards.length} stories` : `${cards.length} stories`;
        });

        // Video playback
        function playVideo(youtubeId) {
            document.getElementById('videoFrame').src =
                `https://www.youtube-nocookie.com/embed/${youtubeId}?autoplay=1`;
            document.getElementById('videoModal').classList.add('active');
        }
        function closeVideo() {
            document.getElementById('videoFrame').src = '';
            document.getElementById('videoModal').classList.remove('active');
        }
        document.getElementById('videoModal').addEventListener('click', function(e) {
            if (e.target === this) closeVideo();
        });
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeVideo();
        });

        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            const saved = localStorage.getItem('theme') || 'dark';
            document.documentElement.setAttribute('data-theme', saved);
            themeToggle.textContent = saved === 'dark' ? '☀️' : '🌙';
            themeToggle.addEventListener('click', function() {
                const current = document.documentElement.getAttribute('data-theme');
                const next = current === 'dark' ? 'light' : 'dark';
                document.documentElement.setAttribute('data-theme', next);
                localStorage.setItem('theme', next);
                this.textContent = next === 'dark' ? '☀️' : '🌙';
            });
        }
    </script>
</body>
</html>
"""

ASSIGNMENT_LABELS = {
    "assignment-1": "Assignment 1: Personal Stories",
    "assignment-2": "Assignment 2: Data Story Remix",
    "assignment-3": "Assignment 3: Neat Demos",
    "assignment-4": "Assignment 4: Class Data Story",
    "part-ii": "Part II: Independent Data Stories",
}


def extract_youtube_id(url):
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"youtu\.be/([^?&]+)",
        r"youtube\.com/watch\?v=([^?&]+)",
        r"youtube\.com/embed/([^?&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def validate_stories(stories):
    """Validate story entries against schema. Returns list of warnings."""
    warnings = []
    required = ["title", "student", "year", "term", "assignment", "youtube_url"]
    valid_assignments = {"assignment-1", "assignment-2", "assignment-3", "assignment-4", "part-ii"}

    for i, story in enumerate(stories):
        for field in required:
            if field not in story or not story[field]:
                warnings.append(f"Story {i+1}: missing required field '{field}'")
        if story.get("assignment") not in valid_assignments:
            warnings.append(
                f"Story {i+1}: invalid assignment '{story.get('assignment')}'"
            )
        if story.get("youtube_url") and not extract_youtube_id(story["youtube_url"]):
            warnings.append(
                f"Story {i+1}: could not extract YouTube ID from '{story['youtube_url']}'"
            )
    return warnings


def generate_gallery_html(stories):
    """Generate the full gallery HTML page."""
    # Group by year (descending), then by assignment
    by_year = {}
    for story in stories:
        year = story.get("year", "Unknown")
        by_year.setdefault(year, []).append(story)

    html = TEMPLATE_HEAD
    html += """
    <nav class="course-nav">
        <a class="logo" href="../index.html">SWD</a>
        <div class="nav-links">
            <a href="../index.html">Home</a>
            <a href="slides.html">Slides</a>
            <a href="assignments.html">Assignments</a>
            <a href="stories.html" class="active">Data Stories</a>
            <a href="syllabus.html">Syllabus</a>
            <button class="theme-toggle" id="themeToggle">☀️</button>
        </div>
    </nav>

    <main style="max-width: 1200px; margin: 0 auto; padding: 100px var(--spacing-xl) var(--spacing-2xl);">
        <h1 style="text-align: center; font-size: 2.5rem; margin-bottom: var(--spacing-sm);
            background: var(--gradient-accent); -webkit-background-clip: text;
            background-clip: text; -webkit-text-fill-color: transparent;">
            Data Stories
        </h1>
        <p style="text-align: center; color: var(--text-secondary); margin-bottom: var(--spacing-xl);">
            Student data stories from Storytelling with Data (PSYC 81.09)
        </p>

        <div class="gallery-search">
            <i class="fas fa-search search-icon"></i>
            <input type="text" id="storySearch"
                   placeholder="Search by title, student, year, or topic...">
        </div>
        <p class="result-count" id="resultCount">""" + f"{len(stories)} stories" + """</p>
"""

    for year in sorted(by_year.keys(), reverse=True):
        year_stories = by_year[year]
        html += f'        <div class="year-section">\n'
        html += f"            <h2>{year}</h2>\n"

        # Group by assignment within year
        by_assignment = {}
        for s in year_stories:
            a = s.get("assignment", "other")
            by_assignment.setdefault(a, []).append(s)

        for assignment in ["assignment-1", "assignment-2", "assignment-3", "assignment-4", "part-ii"]:
            if assignment not in by_assignment:
                continue
            label = ASSIGNMENT_LABELS.get(assignment, assignment)
            html += f'            <div class="assignment-group">\n'
            html += f"                <h3>{label}</h3>\n"
            html += '                <div class="story-grid">\n'

            for story in by_assignment[assignment]:
                yt_id = extract_youtube_id(story.get("youtube_url", ""))
                title = story.get("title", "Untitled")
                student = story.get("student", "Unknown")
                tags = story.get("tags", [])
                search_text = f"{title} {student} {year} {story.get('term', '')} {' '.join(tags)}"

                html += f'                    <div class="story-card" data-search="{search_text}">\n'
                if yt_id:
                    thumb_url = f"https://img.youtube.com/vi/{yt_id}/mqdefault.jpg"
                    html += f'                        <div class="thumb">\n'
                    html += f'                            <img src="{thumb_url}" alt="{title}" loading="lazy">\n'
                    html += f'                            <div class="play-btn" onclick="playVideo(\'{yt_id}\')">\n'
                    html += f'                                <i class="fas fa-play"></i>\n'
                    html += f"                            </div>\n"
                    html += f"                        </div>\n"
                else:
                    html += f'                        <div class="thumb unavailable">\n'
                    html += f"                            <span>Video unavailable</span>\n"
                    html += f"                        </div>\n"

                html += f'                        <div class="info">\n'
                html += f"                            <h4>{title}</h4>\n"
                html += f'                            <p class="meta">{student} &middot; {story.get("term", str(year))}</p>\n'
                html += f"                        </div>\n"

                if tags:
                    html += f'                        <div class="tags">\n'
                    for tag in tags:
                        html += f"                            <span>{tag}</span>\n"
                    html += f"                        </div>\n"

                html += f"                    </div>\n"

            html += "                </div>\n"
            html += "            </div>\n"

        html += "        </div>\n"

    html += "    </main>\n"
    html += TEMPLATE_FOOT
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate data story gallery HTML")
    parser.add_argument("--data", default="data/stories.yaml", help="Path to stories YAML")
    parser.add_argument("--output", default="pages/stories.html", help="Output HTML path")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"ERROR: Data file not found: {data_path}")
        return 1

    with open(data_path) as f:
        stories = yaml.safe_load(f) or []

    warnings = validate_stories(stories)
    for w in warnings:
        print(f"WARNING: {w}")

    html = generate_gallery_html(stories)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Generated gallery with {len(stories)} stories → {output_path}")
    if warnings:
        print(f"  ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
