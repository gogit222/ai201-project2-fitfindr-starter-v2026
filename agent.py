"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import trace as trace_module
from mcp_client import call_tool
from generate import ModelUnavailable
from tools import suggest_outfit, create_fit_card


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


_PRICE_PATTERN = re.compile(
    r"\b(?:under|below|less\s+than|up\s+to|max(?:imum)?(?:\s+price)?)"
    r"\s*\$?\s*(?P<price>\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)
_SIZE_PATTERN = re.compile(
    r"\bsize\s+((?:us\s*)?\d+(?:\.\d+)?|one\s+size|"
    r"[a-z]{1,3}\d+(?:\s+[a-z]{1,3}\d+)?|[a-z]+(?:\s*/\s*[a-z]+)?)\b",
    re.IGNORECASE,
)


def _parse_query(query: str) -> dict:
    remaining_query = query
    price_match = _PRICE_PATTERN.search(remaining_query)
    max_price = float(price_match.group("price")) if price_match else None
    if price_match:
        remaining_query = (
            remaining_query[:price_match.start()]
            + " "
            + remaining_query[price_match.end():]
        )

    size_match = _SIZE_PATTERN.search(remaining_query)
    size = size_match.group(1).strip() if size_match else None
    if size_match:
        remaining_query = (
            remaining_query[:size_match.start()]
            + " "
            + remaining_query[size_match.end():]
        )

    description = re.sub(r"\s+", " ", remaining_query).strip(" ,.-")
    return {
        "description": description,
        "size": size,
        "max_price": max_price,
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

     The query parser extracts an optional size and maximum price with regular
     expressions, then treats the remaining text as the description. Tool
     results are stored in the session before their values are passed onward.
     An empty search stores an actionable message and returns before the other
     tools are called.
    """
    session = new_session(query, wardrobe)

    session["parsed"] = _parse_query(session["query"])
    parsed = session["parsed"]

    session["search_results"] = call_tool("search_listings", {
        "description": parsed["description"],
        "size": parsed["size"],
        "max_price": parsed["max_price"],
    })
    trace_module.step(
        "search_listings (via MCP)",
        inputs=(
            f"description={parsed['description']!r}, "
            f"size={parsed['size']!r}, max_price={parsed['max_price']!r}"
        ),
        returned=session["search_results"],
        note="no matches; stopping" if not session["search_results"] else "",
    )
    if not session["search_results"]:
        session["error"] = (
            "I couldn't find a listing matching those filters. Try changing "
            "the description, size, or maximum price."
        )
        return session

    session["selected_item"] = session["search_results"][0]
    selected_item = session["selected_item"]
    outfit_inputs = (
        f"new_item=(title={selected_item.get('title')!r}, "
        f"price={selected_item.get('price')!r}, "
        f"platform={selected_item.get('platform')!r}), "
        f"wardrobe_items={len(session['wardrobe'].get('items') or [])}"
    )
    try:
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"], session["wardrobe"]
        )
    except ModelUnavailable as exc:
        session["error"] = (
            f"Outfit suggestion failed because the model was unavailable. {exc}"
        )
        trace_module.step(
            "suggest_outfit",
            inputs=outfit_inputs,
            returned=session["error"],
            note="stopping after model failure",
        )
        return session
    trace_module.step(
        "suggest_outfit",
        inputs=outfit_inputs,
        returned=session["outfit_suggestion"],
    )

    fit_card_inputs = (
        f"outfit={session['outfit_suggestion']!r}, "
        f"new_item={session['selected_item'].get('title')!r}"
    )
    try:
        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"], session["selected_item"]
        )
    except ModelUnavailable as exc:
        session["error"] = (
            f"Fit card creation failed because the model was unavailable. {exc}"
        )
        trace_module.step(
            "create_fit_card",
            inputs=fit_card_inputs,
            returned=session["error"],
            note="stopping after model failure",
        )
        return session
    trace_module.step(
        "create_fit_card",
        inputs=fit_card_inputs,
        returned=session["fit_card"],
    )
    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
