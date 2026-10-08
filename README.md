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
> The tools and planning loop are implemented, so that last command runs a
> complete search, outfit suggestion, and fit-card flow.
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

FitFindr takes a description of a secondhand clothing item, with an optional
size and maximum price, and searches local listings for matches. For the best
match, it suggests outfits using the user's wardrobe, or general styling advice
if the wardrobe is empty. It then creates a short, post-ready fit-card caption
with the item's details. If no listing matches, it stops and tells the user
which search constraints to change.

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
$ python app.py ask 'vintage graphic tee under $30'

     Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

     Outfit:   Here are two practical, wearable outfits built around your new Y2K butterfly baby tee and pieces from your wardrobe:

### Outfit 1: High-Contrast Y2K Streetwear
* **Bottoms:** Baggy straight-leg jeans (dark wash)
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**How it works:**
This outfit leans directly into the Y2K aesthetic of the baby tee by playing with proportions. Because the butterfly tee is fitted and cropped, it creates a great silhouette when paired with your high-waisted, baggy dark-wash jeans. Tying the look together with the chunky white sneakers balances the chunky denim while keeping the footwear light and casual, and the black crossbody bag matches the streetwear vibe without competing with the pink and purple butterfly graphic.

***

### Outfit 2: Casual Edge (with Layering)
* **Outerwear:** Vintage black denim jacket
* **Bottoms:** Wide-leg khaki trousers
* **Shoes:** Black combat boots
* **Accessories:** Brown leather belt, black crossbody bag

**How it works:**
This outfit mixes the cute, soft cottagecore elements of the baby tee with tougher, minimal pieces. Tucking the fitted baby tee into the wide-leg khaki trousers defines your waist, especially when cinched with the brown leather belt. Throwing on the slightly cropped vintage black denim jacket and grounding the look with black combat boots adds an effortless, edgy contrast to the pink and purple tones of the shirt.

     Fit card: Found the absolute dream Y2K Baby Tee — Butterfly Print scrolling depop for just $18.00. I’m living for the pink and purple graphic and can’t wait to style it with baggy dark-wash jeans and chunky sneakers for an easy weekend fit.

0 model calls this session, 2 served from cache

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', size='M', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]
```

```
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
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; item=load_listings()[0]; [print(create_fit_card('jeans and white sneakers', item)) for _ in range(3)]"
Scored these vintage Levi's 501 Jeans — Medium Wash on depop for just $38.00 and they fit like an absolute dream. Obsessed with the knee fading that only real time can make. Can't wait to wear them out with my favorite white sneakers and an oversized tee.
Scored these vintage Levi's 501 Jeans — Medium Wash on depop for just $38.00 and they fit like an absolute dream. Obsessed with the knee fading that only real time can make. Can't wait to wear them out with my favorite white sneakers and an oversized tee.
Scored these vintage Levi's 501 Jeans — Medium Wash on depop for just $38.00 and they fit like an absolute dream. Obsessed with the knee fading that only real time can make. Can't wait to wear them out with my favorite white sneakers and an oversized tee.
---


The fit-card outputs are identical because `CACHE_ENABLED` is `True` in `config.py`; `TEMPERATURE` is `0.9`.
## How I Used AI

**Moment 1**

- *What I asked for:* I asked GitHub Copilot to build `create_fit_card` so it would use the model, mention the item's details, and produce a post-ready caption.
- *What came back:* The tool generated a caption, but three calls with the same item and outfit returned identical text.
- *What I changed:* I checked `config.py`, found `CACHE_ENABLED` was `True` while `TEMPERATURE` was `0.9`, and recorded that the repeated answer came from caching rather than a zero-temperature model.

**Moment 2**

- *What I asked for:* I asked GitHub Copilot to implement `run_agent()` with the empty-search branch and to pass tool results through the session.
- *What came back:* It added regex parsing and the session-backed tool sequence. My first PowerShell test accidentally expanded `$30`, so the session showed no price limit.
- *What I changed:* I escaped the dollar sign in the test command and reran it. The session then showed `max_price: 30.0`, and a capture around `suggest_outfit` confirmed it received the exact object in `session["selected_item"]`.

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
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item reaches the next tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card preserves item facts | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search respects the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

**Criterion 1 — Full three-tool run, Try 1**

Source: [run log](results/run_2026-10-07_2114_before.md), produced by `agent.py::run_agent`, captured by `run_eval.py::run_once`.

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10
[1] search_listings (via MCP)
     in:  description='vintage graphic tee', size=None, max_price=30.0
     out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
     in:  new_item=(title='Y2K Baby Tee — Butterfly Print', price=18.0, platform='depop'), wardrobe_items=10
     out: Here are two practical, wearable outfits built around your Y2K butterfly baby tee and pieces from your wardrob…
[3] create_fit_card
     in:  outfit='Here are two practical, wearable outfits built around your Y2K butterfly baby tee and pieces from your…
     out: Found this Y2K Baby Tee — Butterfly Print on depop for just $18.00 and I'm obsessed with the pink and purple d…
Fit card:
Found this Y2K Baby Tee — Butterfly Print on depop for just $18.00 and I'm obsessed with the pink and purple details. I've been styling it with baggy dark-wash jeans and a zip hoodie for an easy streetwear look that balances out the tiny crop. Honestly a 10/10 score.
```

**Criterion 2 — Impossible query, Try 1**

Source: [run log](results/run_2026-10-07_2114_before.md), produced by `agent.py::run_agent`, captured by `run_eval.py::run_once`.

```text
- stopped early: yes — I couldn't find a listing matching those filters. Try changing the description, size, or maximum price.
- selected_item: (none)
- search_results: 0
[1] search_listings (via MCP)
     in:  description='designer ballgown', size='XXS', max_price=5.0
     out: [] (empty)
     →    no matches; stopping
```

**Criterion 3 — Selected item reaches `suggest_outfit`, Try 1**

Source: [run log](results/run_2026-10-07_2114_before.md), trace produced by `agent.py::run_agent` and `trace.py::step`.

```text
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[2] suggest_outfit
     in:  new_item=(title='Y2K Baby Tee — Butterfly Print', price=18.0, platform='depop'), wardrobe_items=10
     out: Here is a practical, everyday outfit using your new butterfly baby tee and items from your wardrobe:  ### Outf…
```

**Criterion 4 — Fit card facts, Try 1**

Source: [run log](results/run_2026-10-07_2114_before.md), card produced by `tools.py::create_fit_card` for `session["selected_item"]`.

```text
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
Fit card:
Still obsessing over how this Y2K Baby Tee — Butterfly Print turned out. Snagged it on depop for just $18.00 and threw it on with wide-leg khaki trousers and a black denim jacket. Honestly living my best early-2000s mall-rat life right now.
```

**Criterion 5 — Price ceiling, Try 1**

Source: run log records 7 results for `session["search_results"]`; exact MCP output produced by `mcp_server.py::search_listings` for the recorded `description='denim jacket'`, `max_price=50.0` inputs.

```text
search_results (title, price):
[
  ('Denim Jacket — Light Wash, Cropped', 42.0),
  ("Vintage Levi's 501 Jeans — Medium Wash", 38.0),
  ('90s Track Jacket — Navy/White Stripe', 45.0),
  ('High-Waisted Denim Shorts — Cutoff', 24.0),
  ('Shacket — Olive Canvas', 33.0),
  ('Straight Leg Black Jeans — Faded', 30.0),
  ('Denim Vest — Medium Wash, Studded', 27.0)
]
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
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All five runs returned a fit card after the search, outfit, and fit-card steps completed. |
| 2 | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | All five runs returned zero results, set the actionable error, and traced no `suggest_outfit` call. |
| 3 | Selected item reaches the next tool | 5 of 5 | MET (5/5) | In all five traces, the `suggest_outfit` input title, price, and platform matched `session["selected_item"]`. |
| 4 | Fit card preserves item facts | 5 of 5 | MET (5/5) | All five cards for the fixed listing mentioned its exact title, $18.00 price, and depop platform. |
| 5 | Search respects the price ceiling | 5 of 5 | MET (5/5) | Every result in all five sessions was at or below $50; the highest returned price was $45.00. |

**Diagnoses**

No criteria were missed, so there is no failing step or mechanism to diagnose. The targets were not broadly too low: criteria 2–5 required 5/5, and each met that bar. Criterion 1's 4/5 target was conservative for this fixed query, which passed 5/5; I tightened criterion 1 to 5/5 and reran it. This does not establish reliability across other phrasings because the scenario tested only one query.



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
[1] search_listings (via MCP)
     in:  description='vintage graphic tee', size=None, max_price=30.0
     out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit
     in:  new_item=(title='Y2K Baby Tee — Butterfly Print', price=18.0, platform='depop'), wardrobe_items=10
     out: Here are two practical, wearable outfits built around your new Y2K butterfly baby tee and pieces from your war…
[3] create_fit_card
     in:  outfit='Here are two practical, wearable outfits built around your new Y2K butterfly baby tee and pieces from …
     out: Found the absolute dream Y2K Baby Tee — Butterfly Print scrolling depop for just $18.00. I’m living for the pi…
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

I tightened criterion 1's target from 4 of 5 to 5 of 5 for the fixed matching scenario. The original criterion remains above with the revision documented in `criteria.md`; no code or scenario inputs changed.

**Which failure it was meant to fix:**

There was no runtime failure. This addresses the diagnosis that 4 of 5 was a conservative target after the fixed query passed 5 of 5 baseline tries.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item reaches the next tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card preserves item facts | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search respects the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Complete after run log:** [results/run_2026-10-07_2124_after.md](results/run_2026-10-07_2124_after.md)

**Criterion 1 sample output, Try 1**

Source: [after run log](results/run_2026-10-07_2124_after.md), produced by `agent.py::run_agent`, captured by `run_eval.py::run_once`.

```text
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10
[1] search_listings (via MCP)
     in:  description='vintage graphic tee', size=None, max_price=30.0
[2] suggest_outfit
     in:  new_item=(title='Y2K Baby Tee — Butterfly Print', price=18.0, platform='depop'), wardrobe_items=10
[3] create_fit_card
Fit card:
Found this Y2K Baby Tee — Butterfly Print on depop for only $18.00 and I’m so obsessed. I'm styling it with dark wash baggy jeans and chunky white sneakers to lean into that ultimate 2000s streetwear vibe.
```

**Did it help, and how do I know:**

The tightened criterion 1 target passed at 5/5, and criteria 2–5 also remained at 5/5. Since this was a target change only, agent behavior did not change; the result confirms the fixed scenario meets the stricter threshold, not that other query phrasings are reliable.

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
