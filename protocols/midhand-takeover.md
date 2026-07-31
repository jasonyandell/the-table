# Match protocol: midhand-takeover

A localization instrument: *where* in the hand does one player's edge over
another live? Instead of playing whole hands, both contenders pick up the same
game already in progress.

## Rules

1. Deal and contract exactly as [dropped-30](dropped-30.md) (forced 30, pip
   trump by fixed heuristic, deterministic from the deal).
2. A **fast deterministic heuristic plays all four seats** through the first
   T−1 tricks ("takeover at trick T"). The prefix player must be deterministic
   (pure argmax, no sampling) so the position is a pure function of the deal.
3. The position is frozen. It is then played out **twice from the
   byte-identical state**: contender A's team holding the contract with
   contender B's team defending, then A's team defending the identical
   position with B holding it.
4. Score each playout make/set as in dropped-30. The paired unit is the
   position; compare offense-vs-offense (and by complement,
   defense-vs-defense) on identical positions.

## The knob

Takeover trick T is the instrument's dial. Sweep it: wherever the paired
result is a dead heat, the contenders are equals from there on; the earliest T
where parity breaks brackets the region where the edge is generated. Run the
full-hand protocol alongside as the T=1 endpoint.

## Analysis

Discordant pairs and McNemar as in dropped-30, per takeover trick, plus
points-per-hand as the finer secondary read.

## Honesty notes

- Positions descend from the *heuristic's* play, not from either contender's
  own opening style. The instrument measures skill from common positions;
  compounding along self-steered early trajectories is a separate quantity the
  full-hand protocol includes and this one deliberately excludes.
- The heuristic should be competent enough that positions are representative;
  degenerate prefixes make every playout concordant and the instrument goes
  blind (founding run: a small distilled value net, no oracle).
- Founding use: [2026-07-30 midhand](../evidence/2026-07-30-midhand.md) —
  dead heat at tricks 3/4/5 localized a full-hand 6.5σ deficit entirely to
  the opening tricks.
