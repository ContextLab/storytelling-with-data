"""Curated theme codebook for the 'How will you apply what you learned?' question.

Replaces the auto-generated HDBSCAN cluster names (which read as keyword
bags like "Try, New, Things") with a small set of human-named themes.
Each theme has 5-10 exemplar phrases. At build time, we embed every
response and assign it to the theme whose exemplar centroid has the
highest cosine similarity, provided that similarity exceeds a threshold.
Below threshold → 'Other'.

Themes derived from manual examination of ~200 responses sampled across
all 12 'how will you apply' columns. See the docstring for the
methodology.

Usage:
    from pipeline import curated_themes
    assignments = curated_themes.assign(
        texts=normalized_texts,
        embed_fn=nlp.embed,
    )
    # → list of (theme_id, similarity) per text
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Theme:
    id: str
    name: str           # human-readable label (1-4 words)
    description: str    # 1-sentence description
    exemplars: list[str]


# Confidence threshold below which a response is assigned 'other'.
# Calibrated empirically: at threshold=0.30 about 80-85% of responses get a
# theme. Tweak via env var EXPLORER_THEME_THRESHOLD if needed.
DEFAULT_THRESHOLD = 0.30


THEMES: list[Theme] = [
    Theme(
        id="kindness",
        name="Be kind & inclusive",
        description="Treat others kindly, be friendly, be inclusive.",
        exemplars=[
            "Be nice to everyone.",
            "I will always be kind to people around me.",
            "Be friendly and inclusive.",
            "Treat others with kindness and respect.",
            "I'll make sure I'm not being rude to anyone, and be nice to everyone.",
            "I will try to do those extra little acts of kindness as much as I can.",
            "Be more inclusive and welcoming to people I don't know.",
            "I will try to be kinder in my daily life.",
        ],
    ),
    Theme(
        id="avoid_substances",
        name="Avoid drugs/vapes/alcohol",
        description="Personal commitment to not use or to refuse substances.",
        exemplars=[
            "I will not do drugs.",
            "Never use a vape.",
            "I will not drink alcohol.",
            "I will say no to drugs.",
            "I won't try vaping.",
            "I will think about the effects of addiction.",
            "I will apply this by staying away from places or people that could cause me to develop an addiction.",
            "Don't do drugs because it changes your brain.",
            "Avoid substance use and make healthy choices.",
        ],
    ),
    Theme(
        id="reach_out",
        name="Reach out & connect",
        description="Reach out to others, talk to more people, build relationships.",
        exemplars=[
            "I will reach out to friends and family more.",
            "Talk to more people around me.",
            "I will start talking to more people.",
            "Reach out and connect with others.",
            "I will try to talk to more people, even if I don't know them well.",
            "Speaking to new people and being open.",
            "I will reach out to people in my community.",
            "Try to make conversation more frequently.",
        ],
    ),
    Theme(
        id="help_others",
        name="Help & support others",
        description="Help others, be there for people who need support.",
        exemplars=[
            "I will help others who are struggling.",
            "Be there for someone when they're struggling.",
            "I will support my friends through hard times.",
            "I will be there if anyone I know needs someone to talk to.",
            "Help my kids be better people for others.",
            "I will check on people when they might not be doing well.",
            "I will use my knowledge to help others in times of need.",
            "Be supportive of those around me.",
        ],
    ),
    Theme(
        id="self_care",
        name="Self-care & coping",
        description="Use coping strategies, breathing, calming techniques.",
        exemplars=[
            "I will use breathing techniques to calm down.",
            "When I'm anxious I'll take a deep breath.",
            "Use this breathing technique when I'm anxious.",
            "I'll find healthy ways to manage stress.",
            "Take time for myself to relax.",
            "When I'm getting frustrated I can use it to calm down.",
            "I'll take time to cultivate things that bring peace.",
            "Practice self-care during hard times.",
        ],
    ),
    Theme(
        id="positive_mindset",
        name="Stay positive",
        description="Keep a positive mindset, hunt the good stuff, optimism.",
        exemplars=[
            "Keep a positive mindset.",
            "I'll be positive.",
            "More positive thinking.",
            "Push myself and stay positive.",
            "Hunt the good stuff and stay positive.",
            "Positive thinking and positive talk is key.",
            "I will be a positive presence in others' lives.",
            "Keep positive thoughts.",
        ],
    ),
    Theme(
        id="awareness",
        name="Mindfulness & awareness",
        description="Be more aware, mindful, think before acting.",
        exemplars=[
            "Be more aware of others' responses.",
            "Think before doing.",
            "I will think about the effects before I act.",
            "Be mindful of my mind.",
            "By keeping awareness of what social media I use.",
            "Pay more attention to my surroundings.",
            "Try to think about my actions before I do them.",
            "I will be aware of the propaganda I am being exposed to.",
        ],
    ),
    Theme(
        id="ask_for_help",
        name="Ask for help",
        description="Don't be afraid to seek help or use available resources.",
        exemplars=[
            "Not be afraid to ask for help.",
            "I will ask people for help when I need it.",
            "Seek help if I need it.",
            "Take advantage of available resources.",
            "Reach out for support when I'm struggling.",
            "Use the resources I have access to.",
            "Don't be afraid to ask questions.",
        ],
    ),
    Theme(
        id="set_goals",
        name="Set goals & motivation",
        description="Set goals, create a plan, motivate myself.",
        exemplars=[
            "I will set goals for myself.",
            "I made a vision board.",
            "By setting goals.",
            "I will follow my own dreams and motivate myself.",
            "Create goals and stick to them.",
            "Make a board each year.",
            "Set measurable goals.",
            "Push myself to achieve my dreams.",
        ],
    ),
    Theme(
        id="listen_communicate",
        name="Listen & communicate",
        description="Listen carefully, communicate better, less judgment.",
        exemplars=[
            "Less judgment and listening carefully.",
            "Listen to others without judging.",
            "I will try to communicate more openly.",
            "Talk and communicate with more people.",
            "Listen to my friends when they need me.",
            "Try to understand where they're coming from.",
            "I will be a better listener.",
            "Communicate without arguing.",
        ],
    ),
    Theme(
        id="educate_share",
        name="Educate & share knowledge",
        description="Teach or warn others about what I learned.",
        exemplars=[
            "I can help educate others about the effects of vapes.",
            "Warn my friends about the dangers of vaping.",
            "Teach others what I learned.",
            "Share this information with people around me.",
            "Help advise people not to use drugs.",
            "Educate my kids about substance use.",
            "Tell others about the effects of addiction.",
        ],
    ),
    Theme(
        id="community",
        name="Community involvement",
        description="Volunteer, get involved in the community, give back.",
        exemplars=[
            "I will volunteer in my community.",
            "Be more involved in my community.",
            "Help out the community.",
            "I will support our neighbors.",
            "Get involved in clubs and activities.",
            "I will continue to help others in my community and volunteer more.",
            "Be a more active member of my community.",
        ],
    ),
    Theme(
        id="gratitude",
        name="Gratitude",
        description="Be grateful, appreciate what I have.",
        exemplars=[
            "Be grateful for what I have.",
            "Don't take anything for granted.",
            "Appreciate the people in my life.",
            "I'm grateful for my community.",
            "Seek joy and be grateful.",
            "Appreciate the small things.",
            "Notice and value my support people.",
        ],
    ),
    Theme(
        id="resilience",
        name="Resilience & perseverance",
        description="Don't give up, face challenges, build resilience.",
        exemplars=[
            "When I am faced with a challenge, I will not give up.",
            "I won't let a failure defeat me.",
            "Face my challenges with resilience.",
            "Push through hard times.",
            "Keep going even when it's hard.",
            "Don't give up on myself.",
            "Bounce back from setbacks.",
        ],
    ),
    Theme(
        id="confidence",
        name="Self-confidence",
        description="Build confidence, speak up for myself, trust myself.",
        exemplars=[
            "Be more confident when meeting new people.",
            "Speak up if I feel unsafe.",
            "Stand up for myself.",
            "Believe in myself.",
            "Be true to who I am.",
            "Have the confidence to say no.",
            "Trust my own judgment.",
        ],
    ),
    Theme(
        id="uncertain",
        name="Not sure / no answer",
        description="Respondent gave a non-answer (idk, n/a, no idea).",
        exemplars=[
            "I do not know.",
            "Not sure yet.",
            "I have no idea.",
            "Not sure how I will apply this.",
            "Don't know.",
            "n/a",
            "No comment.",
        ],
    ),
]


def assign(
    texts: list[str],
    embed_fn,
    threshold: float = DEFAULT_THRESHOLD,
) -> list[tuple[str, float]]:
    """For each text, return (theme_id, similarity) using cosine of the
    text embedding against each theme's mean exemplar embedding.

    Falls back to ('other', best_sim) when the best similarity is below
    `threshold`.
    """
    if not texts:
        return []
    # Compute theme centroids once.
    centroids = []
    for theme in THEMES:
        ex_emb = embed_fn(theme.exemplars).astype(np.float32)
        # Embeddings are L2-normalized by sentence-transformers
        centroid = ex_emb.mean(axis=0)
        n = float(np.linalg.norm(centroid))
        if n > 1e-9:
            centroid = centroid / n
        centroids.append(centroid)
    C = np.stack(centroids, axis=0)  # (T, d)

    # Embed all texts at once
    X = embed_fn(texts).astype(np.float32)  # (N, d), already L2-normalized

    # Cosine similarity = dot product (both normalized)
    sims = X @ C.T  # (N, T)
    out: list[tuple[str, float]] = []
    for i in range(sims.shape[0]):
        j = int(np.argmax(sims[i]))
        s = float(sims[i, j])
        if s >= threshold:
            out.append((THEMES[j].id, s))
        else:
            out.append(("other", s))
    return out


def theme_records() -> list[dict]:
    """Return JSON-friendly theme metadata for the bundle."""
    return [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "exemplars": t.exemplars,
        }
        for t in THEMES
    ] + [
        {
            "id": "other",
            "name": "Other / unclassified",
            "description": "Responses that did not match any curated theme above the confidence threshold.",
            "exemplars": [],
        }
    ]
