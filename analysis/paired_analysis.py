"""Paired mirror analysis for the dropped-30 rob-vs-E[Q] evals.

Pairs hands on (game_idx, hand_idx) across the two halves (a_team 0/1).
Each pair is the same deal, same forced bidder seat, same declaration —
one copy with rob's team bidding, one with E[Q]'s. The discordant pairs
(one side made the contract, the other didn't, holding identical cards)
are the pure play-skill signal; McNemar's test sizes it.
"""
import csv
import math
import sys
from collections import defaultdict

paths = sys.argv[1:]
pairs = {}  # (path, game, hand) -> {a_team: row}
for path in paths:
    with open(path + "/per_hand.csv") as fh:
        for row in csv.DictReader(fh):
            key = (path, int(row["game_idx"]), int(row["hand_idx"]))
            pairs.setdefault(key, {})[int(row["a_team"])] = row

n_pairs = 0
rob_made = eq_made = 0
rob_only = eq_only = both = neither = 0
a_marks = b_marks = hands = 0
by_decl = defaultdict(lambda: [0, 0, 0])  # decl -> [rob_only, eq_only, pairs]

for key, halves in sorted(pairs.items()):
    if len(halves) != 2:
        continue
    r0, r1 = halves[0], halves[1]
    assert r0["seed"] == r1["seed"] and r0["decl_id"] == r1["decl_id"]
    # the copy where rob's team holds the bid: bidder_is_a == 1
    rob_copy = r0 if r0["bidder_is_a"] == "1" else r1
    eq_copy = r1 if rob_copy is r0 else r0
    assert rob_copy["bidder_is_a"] == "1" and eq_copy["bidder_is_a"] == "0"
    n_pairs += 1
    rm, em = rob_copy["made"] == "1", eq_copy["made"] == "1"
    rob_made += rm
    eq_made += em
    d = by_decl[r0["decl_id"]]
    d[2] += 1
    if rm and not em:
        rob_only += 1
        d[0] += 1
    elif em and not rm:
        eq_only += 1
        d[1] += 1
    elif rm:
        both += 1
    else:
        neither += 1

# unpaired-inclusive totals for the running tally cross-check
for key, halves in pairs.items():
    for row in halves.values():
        hands += 1
        won = (row["made"] == "1") == (row["bidder_is_a"] == "1")
        a_marks += won
        b_marks += not won

n = rob_only + eq_only
print(f"instances: {len(paths)}")
print(f"hands total {hands}: rob marks {a_marks} ({a_marks/hands:.1%}), eq {b_marks}")
print(f"mirrored pairs: {n_pairs}")
print(f"  rob made {rob_made} ({rob_made/n_pairs:.1%})   eq made {eq_made} ({eq_made/n_pairs:.1%})  of the SAME deals")
print(f"  both made {both}   neither {neither}   discordant {n}:")
print(f"    rob-only {rob_only}   eq-only {eq_only}")
if n:
    p = rob_only / n
    se = math.sqrt(p * (1 - p) / n)
    z = (rob_only - eq_only) / math.sqrt(n)
    print(f"  discordant share rob {p:.1%} [{p-1.96*se:.1%}, {p+1.96*se:.1%}]  (50% = even)")
    print(f"  McNemar z = {z:+.2f}  (|z|>1.96 = significant at 95%)")
    diff = (rob_made - eq_made) / n_pairs
    sed = math.sqrt(n) / n_pairs  # paired: variance from discordants only
    print(f"  make-rate edge rob-eq: {diff:+.2%} [{diff-1.96*sed:+.2%}, {diff+1.96*sed:+.2%}] per contract")
print("\nby declaration (rob-only vs eq-only discordants / pairs):")
for decl, (r, e, np_) in sorted(by_decl.items(), key=lambda kv: -kv[1][2]):
    print(f"  decl {decl}: rob {r:3d}  eq {e:3d}  pairs {np_}")
