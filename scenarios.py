"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # Criterion 1: the catalog uses "sneakers", not "trainers".
        "name": "trainer synonym retrieves sneaker listings",
        "query": "trainers",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # Criterion 2: singular "trouser" expands to both catalog terms.
        "name": "singular trouser synonym retrieves results",
        "query": "trouser",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # Criterion 3: exact hits suppress the synonym fallback.
        "name": "exact pants matches are not broadened",
        "query": "pants",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Criterion 4: fallback results stay under the inclusive price ceiling.
        "name": "trainer fallback respects price ceiling",
        "query": "trainers under $20",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Criterion 5: a size miss stops before model-backed tools.
        "name": "trainer fallback handles no matching size",
        "query": "trainers size M",
        "wardrobe": "example",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
