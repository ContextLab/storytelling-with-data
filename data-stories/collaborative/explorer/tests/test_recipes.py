"""T027 + T068: recipes.py — calibration test for the savory↔sweet axis (SC-008)."""

from __future__ import annotations

import numpy as np

from pipeline import nlp, recipes


KNOWN_SWEET = [
    "Chocolate fudge brownie sundae with whipped cream and a cherry",
    "Apple pie with cinnamon and a flaky crust",
    "Strawberry jam jelly donut",
    "Lemon meringue pie with toasted topping",
    "Vanilla cupcake with buttercream frosting and rainbow sprinkles",
    "Banana split with three flavors of ice cream",
    "Chocolate chip cookie dough",
    "Caramel apple with crushed peanuts",
    "Birthday cake with chocolate ganache",
    "Maple syrup pancakes with butter",
]

KNOWN_SAVORY = [
    "Roast chicken with garlic mashed potatoes and gravy",
    "Beef stew with carrots and onions in red wine",
    "Cheeseburger with bacon, lettuce, and tomato",
    "Spicy chili con carne with kidney beans",
    "Stir-fried noodles with shrimp and vegetables",
    "Lamb curry with basmati rice",
    "Grilled salmon with asparagus",
    "Mushroom risotto with parmesan",
    "Caesar salad with anchovies and croutons",
    "Fried chicken with mashed potatoes and gravy",
]


def test_savory_sweet_axis_calibration():
    """SC-008: ≥18/20 of known sweet/savory items land on the correct side."""
    all_items = KNOWN_SWEET + KNOWN_SAVORY
    expected = [True] * len(KNOWN_SWEET) + [False] * len(KNOWN_SAVORY)  # True = sweet side

    embeddings = nlp.embed(all_items).astype(np.float32)
    axes = recipes.compute_recipe_axes(embeddings, nlp.embed)

    correct = 0
    for i, expected_sweet in enumerate(expected):
        score = axes["savory_sweet"][i]
        is_sweet = score > 0
        if is_sweet == expected_sweet:
            correct += 1

    assert correct >= 18, (
        f"expected ≥18/20 calibration; got {correct}/{len(all_items)}. "
        f"Scores: {axes['savory_sweet'].tolist()}"
    )


def test_recipe_confidence_in_unit_interval():
    embeddings = nlp.embed(["chocolate cake with raspberries"]).astype(np.float32)
    axes = recipes.compute_recipe_axes(embeddings, nlp.embed)
    assert 0.0 <= axes["recipe_confidence"][0] <= 1.0
