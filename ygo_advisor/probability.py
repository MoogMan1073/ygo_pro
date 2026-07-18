"""Opening-hand probability tools.

Exact functions use the **hypergeometric** distribution — the right model
for drawing a hand *without replacement* from a finite deck. When a
condition is too awkward to express as disjoint groups (OR-conditions,
"any two of these five", etc.) fall back to :func:`monte_carlo`.

Master Duel note: going first you see 5 cards (no draw on turn 1); going
second you see 6 (you draw for turn). Pass ``hand_size=5`` or ``6``.
"""
from __future__ import annotations

import random
from collections import Counter
from itertools import product
from math import comb
from typing import Callable, Iterable, Sequence


def hyper_pmf(N: int, K: int, n: int, k: int) -> float:
    """P(exactly k successes): deck N, K successes, hand n."""
    if k < 0 or k > K or k > n or (n - k) > (N - K):
        return 0.0
    return comb(K, k) * comb(N - K, n - k) / comb(N, n)


def hyper_at_least(N: int, K: int, n: int, k: int = 1) -> float:
    """P(at least k successes)."""
    if k <= 0:
        return 1.0
    return sum(hyper_pmf(N, K, n, i) for i in range(k, min(K, n) + 1))


def at_least_one(N: int, K: int, n: int) -> float:
    """P(>=1 success) — the common 'do I open any copy?' query."""
    if K <= 0 or n <= 0:
        return 0.0
    if n >= N:
        return 1.0 if K > 0 else 0.0
    return 1.0 - comb(N - K, n) / comb(N, n)


def all_groups_at_least(N: int, groups: Sequence[tuple[int, int]], n: int) -> float:
    """P a hand of ``n`` from deck ``N`` meets a minimum for EACH group.

    ``groups`` is a list of ``(group_size, min_required)``. Groups must be
    **disjoint** (a card counted in one group is not counted in another);
    everything else in the deck is the implicit "other" bucket. Use this
    for AND-conditions such as "open >=1 Welcome-access AND >=1 Labrynth
    monster".
    """
    total_g = sum(s for s, _ in groups)
    remainder = N - total_g
    if remainder < 0:
        raise ValueError("group sizes exceed deck size")
    denom = comb(N, n)
    ranges = [range(m, min(s, n) + 1) for s, m in groups]
    numer = 0
    for combo in product(*ranges):
        used = sum(combo)
        rest = n - used
        if rest < 0 or rest > remainder:
            continue
        term = comb(remainder, rest)
        for (s, _), k in zip(groups, combo):
            term *= comb(s, k)
        numer += term
    return numer / denom


def monte_carlo(
    deck_ids: Iterable[int],
    hand_size: int,
    predicate: Callable[[Counter], bool],
    trials: int = 200_000,
    seed: int = 0,
) -> float:
    """Estimate P(predicate) by sampling hands.

    ``predicate`` receives a ``Counter`` mapping card-id -> copies in the
    drawn hand and returns True on a "good" hand. Use for OR / complex
    combos that :func:`all_groups_at_least` can't express directly.
    """
    rng = random.Random(seed)
    deck = list(deck_ids)
    if hand_size > len(deck):
        raise ValueError("hand larger than deck")
    hits = 0
    for _ in range(trials):
        hand = Counter(rng.sample(deck, hand_size))
        if predicate(hand):
            hits += 1
    return hits / trials


def pct(p: float) -> str:
    """Format a probability as a friendly percentage string."""
    return f"{p * 100:.1f}%"
