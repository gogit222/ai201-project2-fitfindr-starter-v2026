"""Standalone search, outfit-suggestion, and fit-card tools for FitFindr."""

import re

import config
from generate import generate
from utils.data_loader import load_listings


def _size_components(size: str) -> set[str]:
    without_notes = re.sub(r"\([^)]*\)", "", size).casefold()
    return {part.strip() for part in without_notes.split("/") if part.strip()}


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    """
    keywords = set(re.findall(r"[a-z0-9]+", description.casefold()))
    if not keywords:
        return []

    requested_sizes = _size_components(size) if size else None
    matches = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if requested_sizes and not requested_sizes.intersection(
            _size_components(listing.get("size", ""))
        ):
            continue

        searchable_text = " ".join(
            [
                str(listing.get("title") or ""),
                str(listing.get("description") or ""),
                str(listing.get("category") or ""),
                str(listing.get("brand") or ""),
                " ".join(listing.get("style_tags") or []),
                " ".join(listing.get("colors") or []),
            ]
        )
        score = len(keywords.intersection(
            re.findall(r"[a-z0-9]+", searchable_text.casefold())
        ))
        if score:
            matches.append((score, listing))

    matches.sort(key=lambda match: match[0], reverse=True)
    return [listing for _, listing in matches[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    """
    wardrobe_items = wardrobe.get("items") or []
    item_details = (
        f"Item: {new_item.get('title', 'Unknown item')}\n"
        f"Category: {new_item.get('category', 'unknown')}\n"
        f"Description: {new_item.get('description', '')}\n"
        f"Size: {new_item.get('size', 'unknown')}\n"
        f"Colors: {', '.join(new_item.get('colors') or [])}\n"
        f"Style tags: {', '.join(new_item.get('style_tags') or [])}"
    )
    system = (
        "You are a practical personal stylist. Suggest one or two wearable, "
        "specific outfits. When wardrobe pieces are provided, name only pieces "
        "the user owns and explain how they work with the new item."
    )

    if wardrobe_items:
        wardrobe_details = "\n".join(
            f"- {item.get('name', 'Unnamed item')} "
            f"(category: {item.get('category', 'unknown')}; "
            f"colors: {', '.join(item.get('colors') or [])}; "
            f"style: {', '.join(item.get('style_tags') or [])}; "
            f"notes: {item.get('notes') or 'none'})"
            for item in wardrobe_items
        )
        prompt = (
            f"Suggest one or two outfits for this thrifted item, using the "
            f"wardrobe pieces below. Be specific and practical.\n\n"
            f"{item_details}\n\nUser wardrobe:\n{wardrobe_details}"
        )
    else:
        prompt = (
            f"The user has no saved wardrobe yet. Give general, practical "
            f"styling advice and one or two outfit ideas for this item without "
            f"assuming they own particular pieces.\n\n{item_details}"
        )

    response = generate(prompt, system=system).strip()
    if response:
        return response
    return (
        f"For a versatile look, pair {new_item.get('title', 'this item')} "
        "with a simple base layer and comfortable shoes in a complementary color."
    )


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    """
    title = new_item.get("title", "Unknown item")
    price = new_item.get("price", "unknown price")
    platform = new_item.get("platform", "unknown platform")

    if not outfit.strip():
        return (
            f"{title} is listed for ${price:.2f} on {platform}. "
            "Add outfit suggestions to create a complete fit card."
            if isinstance(price, (int, float))
            else f"{title} is listed on {platform}. Add outfit suggestions to create a complete fit card."
        )

    item_details = (
        f"Title: {title}\n"
        f"Price: ${price:.2f}\n"
        f"Platform: {platform}\n"
        f"Description: {new_item.get('description', '')}\n"
        f"Category: {new_item.get('category', 'unknown')}\n"
        f"Colors: {', '.join(new_item.get('colors') or [])}"
        if isinstance(price, (int, float))
        else f"Title: {title}\nPrice: {price}\nPlatform: {platform}\n"
        f"Description: {new_item.get('description', '')}\n"
        f"Category: {new_item.get('category', 'unknown')}\n"
        f"Colors: {', '.join(new_item.get('colors') or [])}"
    )
    prompt = (
        "Write a post-ready thrift-find caption in two to four sentences. "
        "Make it sound like a real person's post, not a product listing. "
        "Mention the exact item title, price, and platform exactly once each, "
        "and make the vibe specific. Use the outfit suggestion naturally. "
        "Return only the caption.\n\n"
        f"{item_details}\n\nOutfit suggestion:\n{outfit.strip()}"
    )
    response = generate(
        prompt,
        system="You write concise, vivid social captions about secondhand style.",
    ).strip()
    if response:
        return response
    return f"Found {title} for ${price} on {platform}. The {outfit.strip()} styling gives it an easy, personal feel."
