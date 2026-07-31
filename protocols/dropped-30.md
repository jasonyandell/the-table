# Match protocol: dropped-30

A fair head-to-head for 42 players that do not bid. In 42, when you're forced
to bid, the bid was "dropped on you" — this protocol drops every hand.

## Rules

1. **No auction.** Every hand is a forced 30 bid. The forced bidder is the
   first seat after the dealer; dealer rotates every hand.
2. **Declaration** = the best pip trump of the forced bidder's hand, chosen by
   a fixed deterministic heuristic (no minimum trump count). The contract is
   therefore a pure function of the deal.
3. **Mirrored pairs.** Because the contract is deal-deterministic, every deal
   is played exactly twice with the teams swapped. Deal seeds must be
   team-assignment-independent so the two copies are the same hand. Deal luck
   cancels exactly.
4. **Scoring: 1 mark per hand, binary.** The bidding team makes (≥ 30 of the
   42) or is set (defenders reach 13+). Making 29 is exactly as much a loss as
   making 0. Games race to 7 marks.
5. Both sides play the **same protocol at every seat** — offense and defense
   both measured; with mirrored pairs, defense is the complement of the
   opponent's offense on the same deals.

## Analysis

Pair hands on (deal, hand index) across the two mirrored halves. Concordant
pairs (both made, or neither) were decided by the deal; **discordant pairs are
the entire skill signal**. Report: discordant counts each way, McNemar z,
paired make-rate difference with discordant-only variance, per-declaration
split, plus raw points as a secondary read. Tooling:
[`../analysis/paired_analysis.py`](../analysis/paired_analysis.py).

## Honesty notes

- This ranks *play*, not 42: bidding is the heart of the real game and is
  deliberately deleted so non-bidding players are commensurable.
- The deal distribution is uniform-random hands under forced 30 with pip
  trumps — a different population than auction-selected contracts.
- Small runs have signs, not sizes: a 24-game probe preceding the founding
  match had the wrong sign. Use mirrored pairs at scale (the founding match:
  1,152 games, 6,028 pairs — [evidence](../evidence/2026-07-30-dropped30.md)).
