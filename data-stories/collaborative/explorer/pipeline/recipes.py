"""T018: Recipe-axis projection (savory↔sweet, complexity).

Per research R-8: anchor-based axis projection in MiniLM embedding space.
Each recipe gets a coordinate on each axis plus a recipe_confidence score.
"""

from __future__ import annotations

import numpy as np


# -----------------------------
# Anchor sentence sets (versioned)
# -----------------------------

ANCHORS_VERSION = 1

SAVORY_ANCHORS = [
    "Roast chicken with rosemary and garlic",
    "Beef stew with carrots and potatoes",
    "Spaghetti carbonara with bacon and parmesan",
    "Caesar salad with anchovies and croutons",
    "Mushroom risotto with parmesan",
    "Grilled salmon with lemon and dill",
    "Tomato basil soup with grilled cheese",
    "Roasted vegetable curry with coconut milk",
    "Pulled pork sandwich with coleslaw",
    "Chicken pot pie with peas and carrots",
    "Mac and cheese with sharp cheddar",
    "Beef tacos with onions and cilantro",
    "Pad thai with shrimp and peanuts",
    "Lasagna with ground beef and ricotta",
    "Garlic shrimp pasta with parsley",
]

SWEET_ANCHORS = [
    "Chocolate chip cookies",
    "Vanilla buttercream cupcakes",
    "Strawberry shortcake with whipped cream",
    "Apple pie with cinnamon",
    "Brownies with walnuts",
    "Lemon meringue pie",
    "Banana bread with chocolate chips",
    "Caramel apples with sprinkles",
    "Pumpkin pie with whipped cream",
    "Chocolate fudge brownies",
    "Sugar cookies with frosting",
    "Cinnamon rolls with cream cheese glaze",
    "Tiramisu with mascarpone",
    "Cheesecake with strawberry sauce",
    "Ice cream sundae with hot fudge",
]

SIMPLE_ANCHORS = [
    "Just three ingredients: bread, butter, jam.",
    "Boil water, add salt, drop the pasta in for ten minutes.",
    "Slice bananas, top with peanut butter.",
    "Toast bread, spread avocado, sprinkle salt.",
    "Whisk eggs and pour into a hot pan.",
    "Mix yogurt with honey and granola.",
    "Slice cheese onto crackers.",
    "Heat soup from a can.",
    "Microwave a baked potato for eight minutes.",
    "Layer cheese and tomato on bread, grill.",
    "Cut up fruit and toss with lemon juice.",
    "Boil eggs for seven minutes, peel.",
]

COMPLEX_ANCHORS = [
    "Marinate the lamb shanks overnight in red wine, garlic, and herbs, then sear and braise for four hours.",
    "Prepare the puff pastry by laminating butter through six folds with chilling between each.",
    "Make the bechamel base, cook the spinach filling, layer with handmade pasta sheets, top with mornay sauce, bake.",
    "Brine the turkey for 24 hours, stuff with aromatics, roast slowly while basting every 30 minutes.",
    "Reduce the demi-glace from beef bones and aromatics over six hours.",
    "Knead the dough, ferment for twelve hours, shape, proof, and bake in a preheated dutch oven.",
    "Assemble the croquembouche by piping individual choux puffs, filling with pastry cream, then binding with caramel.",
    "Smoke the brisket low and slow for fourteen hours with a careful temperature stall.",
    "Roll, wrap, and twist twenty-four homemade dumplings with a pleated edge.",
    "Stack a mille-feuille of caramelized phyllo, custard, and seasonal berries.",
]

RECIPE_ANCHORS = [
    "Ingredients: 2 cups flour, 1 cup sugar, 2 eggs, 1 cup milk. Mix dry ingredients then wet.",
    "Step 1: Preheat oven to 350. Step 2: Mix the batter. Step 3: Bake for 25 minutes.",
    "This is my grandmother's recipe for chicken soup with carrots, celery, and homemade noodles.",
    "Heat olive oil in a pan, add onions, cook until translucent, add garlic and tomatoes.",
    "Combine flour, baking soda, and salt. In a separate bowl whisk butter and sugar.",
    "Boil potatoes, mash with butter and milk, season with salt and pepper.",
    "Marinate the chicken in yogurt and spices overnight, then grill.",
    "Saute the mushrooms in butter, add cream, finish with parmesan.",
    "Layer noodles, sauce, and cheese; bake until bubbling.",
    "Whisk the eggs with sugar, add flour, fold in chocolate chips, drop spoonfuls onto a baking sheet.",
]


# -----------------------------
# Public API
# -----------------------------


def compute_axis_unit_vector(
    embed_fn,
    positive_anchors: list[str],
    negative_anchors: list[str],
) -> np.ndarray:
    """Build the unit vector pointing from negative→positive anchor centroids.

    `embed_fn(texts) -> np.ndarray` shape (n, d).
    """
    pos = embed_fn(positive_anchors).astype(np.float32)
    neg = embed_fn(negative_anchors).astype(np.float32)
    axis = pos.mean(axis=0) - neg.mean(axis=0)
    norm = float(np.linalg.norm(axis))
    if norm < 1e-9:
        # degenerate; return zero vector (will produce zero scores)
        return np.zeros_like(axis)
    return (axis / norm).astype(np.float32)


def project_to_axis(vectors: np.ndarray, axis_unit: np.ndarray) -> np.ndarray:
    """Project rows of `vectors` onto `axis_unit`, clipping to [-1, 1]."""
    if vectors.shape[0] == 0:
        return np.zeros(0, dtype=np.float32)
    raw = (vectors.astype(np.float32) @ axis_unit.astype(np.float32))
    # raw values are in [-1, 1] already (cosine-like) since both inputs are normalized
    return np.clip(raw, -1.0, 1.0)


def recipe_confidence(
    vectors: np.ndarray,
    recipe_anchor_centroid: np.ndarray,
) -> np.ndarray:
    """Cosine similarity to the recipe-anchor centroid, mapped to [0, 1]."""
    if vectors.shape[0] == 0:
        return np.zeros(0, dtype=np.float32)
    centroid = recipe_anchor_centroid.astype(np.float32)
    cn = float(np.linalg.norm(centroid))
    if cn < 1e-9:
        return np.full(vectors.shape[0], 0.5, dtype=np.float32)
    centroid = centroid / cn
    cos = (vectors.astype(np.float32) @ centroid).astype(np.float32)
    # cos already in [-1, 1] for normalized vectors; map to [0, 1]
    return np.clip((cos + 1.0) / 2.0, 0.0, 1.0)


def compute_recipe_axes(
    embeddings: np.ndarray,
    embed_fn,
) -> dict[str, np.ndarray]:
    """One-shot computation of (savory_sweet, complexity, recipe_confidence)."""
    sweet_axis = compute_axis_unit_vector(embed_fn, SWEET_ANCHORS, SAVORY_ANCHORS)
    complex_axis = compute_axis_unit_vector(embed_fn, COMPLEX_ANCHORS, SIMPLE_ANCHORS)
    recipe_centroid = embed_fn(RECIPE_ANCHORS).astype(np.float32).mean(axis=0)
    return {
        "savory_sweet": project_to_axis(embeddings, sweet_axis),
        "complexity": project_to_axis(embeddings, complex_axis),
        "recipe_confidence": recipe_confidence(embeddings, recipe_centroid),
    }


def axis_definitions() -> dict[str, dict]:
    """Return the JSON-friendly axis definitions for the bundle."""
    return {
        "savory_sweet": {
            "positive_anchors": SWEET_ANCHORS,
            "negative_anchors": SAVORY_ANCHORS,
            "version": ANCHORS_VERSION,
        },
        "complexity": {
            "positive_anchors": COMPLEX_ANCHORS,
            "negative_anchors": SIMPLE_ANCHORS,
            "version": ANCHORS_VERSION,
        },
    }
