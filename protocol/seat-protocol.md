# Seat protocol v1

A line protocol that seats an external Texas 42 player ("the guest") in a host
harness. Design goals, in order: **no build dependency in either direction**,
**stateless requests** (any decision can be asked cold, including mid-hand),
and **every reply is a rules-conformance cross-check** for free.

Reference implementations:

- Server (guest side): `rob_bridge`
  ([texas-42, `rob/crates/verify/src/bin/rob_bridge.rs`](https://github.com/jasonyandell/texas-42/blob/main/rob/crates/verify/src/bin/rob_bridge.rs))
- Client (host side): mk5 `arena/rob_play.py` (private repo; the wire format
  below is normative, the implementations are the executable spec)

## Transport

The guest runs as a subprocess. One request per line on stdin, one reply per
line on stdout, plain ASCII integers separated by single spaces, `\n`
terminated, flush after every line. The guest is stateless across lines; hosts
may run a pool of guest processes and route requests to any of them.

## Shared conventions (must hold on both sides)

- **Domino encoding** — triangular: tile (a,b) with a ≥ b has id
  `a·(a+1)/2 + b`. So (0,0)=0, (1,0)=1, (1,1)=2, …, (6,6)=27.
- **Seats** — 0..3 in play order; **team = seat mod 2**.
- **Declaration id** (`decl_id`) — the shared declaration index; pip trump
  declarations use the pip value (0..6). (v1 traffic to date has exercised pip
  trumps only.)
- The guest sees **no bid value and no game score** — v1 seats are bid- and
  score-blind. A future version may extend the request; the version must bump.

## Request (host → guest)

One line of integers:

    player decl_id bidder h0 h1 h2 h3 h4 h5 h6 n_plays [actor domino]*n_plays

- `player` — the seat to move (0..3).
- `decl_id` — the declaration in force.
- `bidder` — the seat that holds the contract (trick 1 leader).
- `h0..h6` — `player`'s **original 7-tile hand** (domino ids), before any plays.
- `n_plays` — number of plays so far in the hand (0..27).
- Then `n_plays` pairs of `actor domino` — the full public play history in
  order.

Everything the guest needs is derivable from this line: current trick, whose
turn (must equal `player`), remaining tiles, revealed voids, team points.

## Reply (guest → host)

One line of four integers:

    domino leader p0 p1

- `domino` — the tile id the guest plays. Must be in `player`'s hand, unplayed,
  and legal under the rules.
- `leader` — the guest's independently derived current trick leader.
- `p0 p1` — the guest's independently derived team points (team 0, team 1),
  counting captured count tiles plus tricks per the straight-42 hand economy.

`leader`, `p0`, `p1` are **redundant on purpose**: the host asserts them
against its own engine on every decision. Any mismatch is a rules divergence
between two independent implementations and must abort the match loudly — it is
never a warning. (First campaign: ~180k+ decisions, zero divergences.)

## Errors

A guest that cannot answer must exit nonzero (host treats an empty reply as
guest death). There are no in-band error codes in v1.

## Versioning

This document is v1. Any change to the line grammar, the encoding, or the
blindness guarantees requires a v2 document; hosts and guests must not
silently extend v1.
