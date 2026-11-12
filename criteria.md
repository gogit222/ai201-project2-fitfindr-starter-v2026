# Acceptance criteria — FitFindr synonym fallback

These five criteria evaluate the synonym-aware search extension. The earlier
baseline criteria and their results remain documented in `README.md`; these are
the active targets for the extension.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

The search operates over a fixed local catalog, so each target is exact and
repeatable. All five criteria include new fallback behavior rather than only
retesting the existing agent flow.

---

## 1. British shoe wording retrieves sneaker listings

**Target:** 5 of 5 runs.

For `trainers`, `session["search_results"]` contains exactly `lst_019` followed
by `lst_035`.

**Why this target:**
I chose 5 of 5 because this is deterministic local search; 4 of 5 would hide a
missed alias, and a stricter rate than 5 of 5 is impossible. A miss means users
who say `trainers` cannot find either sneaker listing.

---

## 2. Singular trouser wording retrieves both catalog terms

**Target:** 5 of 5 runs.

For `trouser`, `session["search_results"]` contains exactly `lst_005`, `lst_011`,
`lst_021`, and `lst_025`, in that order.

**Why this target:**
I chose 5 of 5 because the fixed catalog and synonym map have deterministic
results; 4 of 5 would tolerate a broken vocabulary group, while more than 5 of
5 cannot be required. Missing any ID loses a real matching listing, and an
extra ID pollutes the results.

---

## 3. Exact matches do not trigger fallback expansion

**Target:** 5 of 5 runs.

For `pants`, results remain exactly `lst_005` and `lst_011`; trouser-only
listings `lst_021` and `lst_025` are not added.

**Why this target:**
I chose 5 of 5 because exact-token ranking is deterministic; 4 of 5 would allow
the fallback to broaden a successful query one time in five. That can push an
exact match out of the limited result list and change which item gets styled;
5 of 5 is the strictest meaningful target across five runs.

---

## 4. Price ceiling remains strict during fallback

**Target:** 5 of 5 runs.

For `trainers under $20`, `session["search_results"]` contains only `lst_035`,
priced at $20.00, and no result exceeds the inclusive ceiling.

**Why this target:**
I chose 5 of 5 because price filtering and fallback both run over fixed local
data; 4 of 5 would accept an over-budget result in one run. That breaks an
explicit spending limit, while a stricter rate than 5 of 5 is impossible.

---

## 5. Size-filtered empty fallback stops cleanly

**Target:** 5 of 5 runs.

For `trainers size M`, `session["search_results"]` is empty,
`session["error"]` names a filter to change, and both
`session["outfit_suggestion"]` and `session["fit_card"]` remain `None`.

**Why this target:**
I chose 5 of 5 because the catalog has only US 8 and US 9 sneakers, so size M
must deterministically produce no results; 4 of 5 would allow a wrong-size shoe
through. Stopping before model calls avoids spending tokens styling an invalid
item, and a stricter rate than 5 of 5 is impossible.

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
