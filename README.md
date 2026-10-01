# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches listings by description keywords, with optional size and inclusive maximum-price filters. Size matching is case-insensitive: split slash-delimited sizes into whole components and match exactly, ignoring parenthetical fit notes; for example, `M` matches `S/M`, but `L` does not match `XL`.
- **Inputs:** `description` (`str`), `size` (`str | None`), `max_price` (`float | None`).
- **Returns:** A list of matching listing dicts, each with `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`, sorted best match first and limited to `config.SEARCH_RESULT_LIMIT`.
- **When it has nothing:** An empty list (`[]`) if no listings match.

### `suggest_outfit`

- **What it does:** Suggests one or two outfits using the item being considered and the user's wardrobe.
- **Inputs:** `new_item` (`dict`), `wardrobe` (`dict` with an `items` list).
- **Returns:** A non-empty string containing outfit suggestions.
- **When it has nothing:** With an empty wardrobe, returns general styling advice for the item rather than an empty string or an error.

### `create_fit_card`

- **What it does:** Writes a short, post-ready caption about the thrifted item and its suggested outfit.
- **Inputs:** `outfit` (`str`), `new_item` (`dict`).
- **Returns:** A two-to-four sentence caption mentioning the item, its price, its platform, and its vibe.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a descriptive message instead of raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put an actionable message in `session["error"]` and stop. Otherwise, take the first result and go to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regular expressions extract an optional `size` and maximum price; the remaining query text becomes the search description.

**What moves through the session:** `parsed` feeds `search_results`. If that list is empty, `error` is set and the run stops. Otherwise the first result is stored as `selected_item`, passed with `wardrobe` to `suggest_outfit`, and then that stored suggestion and item go to `create_fit_card`; both outputs are stored in the session.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', size='M', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; ..."
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two practical, everyday outfits built around your new vintage Levi's 501 jeans:

### Outfit 1: Casual Streetwear Layer
* **The Look:** Effortless, comfortable, and plays on vintage proportions.
* **Top:** White ribbed tank top tucked into the Levi's 501 jeans. The fitted, minimal basic balances the straight-leg cut of the denim.
* **Outerwear:** Oversized grey crewneck sweatshirt layered over the tank. Because the sweatshirt drops below the hip, letting it slouch loosely over the mid-rise 501s gives you that easy, relaxed streetwear aesthetic.
* **Shoes:** Chunky white sneakers to tie into the white tank and anchor the chunky proportions of the outfit.
* **Accessories:** Black crossbody bag for everyday functionality.

### Outfit 2: Edgy Double-Denim
* **The Look:** A nod to classic Americana with a modern, grungy edge.
* **Top:** White ribbed tank top as the base layer.
* **Outerwear:** Vintage black denim jacket worn over the tank. The slightly cropped fit of the jacket creates a great waistline contrast against the medium wash of the Levi's 501s.
* **Shoes:** Black combat boots. Let the hems of the 501s rest right at the top of the mid-ankle boots to show off the lace-up detail.
* **Accessories:** Brown leather belt threaded through the jeans to add a subtle earth-tone contrast, paired with the black crossbody bag.

```
$ python -c "from tools import create_fit_card; ..."

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; item=load_listings()[0]; [print(create_fit_card('jeans and white sneakers', item)) for _ in range(3)]"
Scored these vintage Levi's 501 Jeans — Medium Wash on depop for just $38.00 and they fit like an absolute dream. Obsessed with the knee fading that only real time can make. Can't wait to wear them out with my favorite white sneakers and an oversized tee.
Scored these vintage Levi's 501 Jeans — Medium Wash on depop for just $38.00 and they fit like an absolute dream. Obsessed with the knee fading that only real time can make. Can't wait to wear them out with my favorite white sneakers and an oversized tee.
Scored these vintage Levi's 501 Jeans — Medium Wash on depop for just $38.00 and they fit like an absolute dream. Obsessed with the knee fading that only real time can make. Can't wait to wear them out with my favorite white sneakers and an oversized tee.
---


The fit-card outputs are identical because `CACHE_ENABLED` is `True` in `config.py`; `TEMPERATURE` is `0.9`.
## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
