# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 rather than 5 of 5 because search uses keyword matching, so some
natural phrasings may miss a relevant listing. One miss is tolerable, but the
usual matching query should still complete the full flow.

> **Tightened after baseline:** For the matching scenario used in this
> evaluation, the agent completes all three tool calls and returns a fit card
> in 5 of 5 tries.
>
> **Why tightened:** The fixed query passed all five baseline tries, so the
> original 4-of-5 target was conservative for this scenario. This does not
> establish reliability across other phrasings.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because an empty result should always take the same deterministic
branch; no model wording is needed to decide whether to stop. Every run should
avoid calling the next tool and give the user a useful change to try.

---

## 3. The selected item reaches the next tool

In 5 of 5 successful tries, the `suggest_outfit` trace input identifies the
same listing as `session["selected_item"]`: its `title`, `price`, and `platform`
match.

**Why this target:**
I chose 5 of 5 because passing the selected listing to the next tool is a direct
state handoff, not model-generated behavior. A mismatch means the agent may
suggest an outfit for the wrong item.


---

## 4. The fit card preserves item facts

For one fixed selected listing, all 5 uncached fit cards correctly mention the
item title, price, and platform; the wording may differ between tries.

**Why this target:**
I chose 5 of 5 because those facts are fixed in the listing and supplied to the
model, even though its phrasing can vary. I care about accurate captions, not
identical wording.


---

## 5. Search respects the price ceiling

Given a query with an explicit maximum price and at least one matching listing,
every result in `session["search_results"]` costs no more than that limit — 5
of 5 tries.

**Why this target:**
I chose 5 of 5 because filtering numeric prices against an explicit ceiling is
deterministic and does not depend on model wording. Returning an over-budget item
breaks a clear user constraint.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
