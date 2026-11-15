# The Table

Where Texas 42 players from different projects sit down and play each other.

The family of 42 projects federates over protocols and artifacts, never over
shared code. Each player lives in its home repository with its own engine, its
own training stack, and its own standards of evidence. When two of them need to
meet, they meet **here**: the table owns the wire protocol that seats a player
in a foreign harness, the match protocols that make a comparison fair, the
analysis tooling that sizes a result honestly, and the evidence records of the
matches that have been played.

The table never implements a player and never implements game rules. It is
neutral ground by construction — the same reason a card table doesn't deal.

## The family

| project | role | where |
|---|---|---|
| [texas-42](https://github.com/jasonyandell/texas-42) | What is *true* — the mathematics (exact fibers, canonical support quotients, losslessness), proved before code is trusted; Lean formalization; **rob**, a certified exact imperfect-information solver | GitHub, public |
| [mk5-main](https://github.com/jasonyandell/mk5-main) | How strong players are *made* — **Walt** and **Zeb**, the players that never see another seat's hand (Zeb is on npm as `@jasonyandell/zeb`); Silas, a query language for positions; the standing ladder; and the finished oracle era, whose champion **E[Q] n=10** Walt beat in October 2026 | GitHub, public |
| [plunge](https://github.com/jasonyandell/plunge) | Where the game is *played* by humans — free mobile web 42, full family rules, honest AI ladder | GitHub, public · [play it](https://plunge.jasonyandell.workers.dev) |
| the table (this repo) | Where they *meet* — seat protocol, match protocols, analysis, evidence | GitHub, public |
| artifacts | Model weights, datasets and the ladder's records | [Hugging Face](https://huggingface.co/jasonyandell), public |

Everything in the family is free as in beer (CC0).

## What lives here

- [`protocol/seat-protocol.md`](protocol/seat-protocol.md) — the versioned line
  protocol that seats an external player in a harness: one decision per line,
  plain integers, no build dependency in either direction, and every reply
  doubles as a rules-conformance cross-check.
- [`protocols/`](protocols/) — match protocols: how to make a comparison fair
  before anyone shuffles. Currently [dropped-30](protocols/dropped-30.md)
  (auction deleted, mirrored pairs, marks per hand) and
  [midhand-takeover](protocols/midhand-takeover.md) (shared heuristic prefix,
  frozen position played out both ways — the localization instrument).
- [`analysis/`](analysis/) — [`paired_analysis.py`](analysis/paired_analysis.py):
  mirrored-pair pairing, discordant counts, McNemar, paired make-rate CIs.
- [`evidence/`](evidence/) — the match records, dated. Founding documents:
  [2026-07-30 dropped-30](evidence/2026-07-30-dropped30.md) (full hand: the
  champion defeats rob ≈6.5σ) and
  [2026-07-30 midhand](evidence/2026-07-30-midhand.md) (from rob's exact
  window: statistical dead heat — together they localize the entire deficit to
  the opening tricks rob plays with disposable scaffolding).

## Epistemic status of this repo

Evidence records here are **field measurements**: honest, mirrored, sized with
paired statistics — and still not proofs. Each home repository keeps its own
evidentiary standards (texas-42's claim tiers and receipts are the strictest;
nothing here ever counts as a receipt there). A number in `evidence/` is a fact
about a match, not a theorem about the game.

## Known seats

- **rob** (texas-42) — `rob_bridge` binary
  ([source](https://github.com/jasonyandell/texas-42/blob/main/rob/crates/verify/src/bin/rob_bridge.rs)),
  serves the seat protocol over stdin/stdout. The reference server.
- **E[Q] n=10 and the mk5 stable** — seated via mk5's arena adapters
  (`arena/rob_play.py` is the reference protocol client; the champion plays
  through its native harness).
- **plunge AIs** — prospective: plunge's engine is pure/deterministic and its
  AIs are observation-honest, so a protocol seat is a natural fit (play rob
  from your phone).
