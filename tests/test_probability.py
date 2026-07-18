"""Tests for the hypergeometric probability engine."""
from collections import Counter

from ygo_advisor import probability as prob


def test_at_least_one_basic():
    # 3 copies in 40, drawing 5 -> known Yu-Gi-Oh consistency figure ~33.76%
    p = prob.at_least_one(40, 3, 5)
    assert abs(p - 0.3376) < 0.001


def test_at_least_one_edges():
    assert prob.at_least_one(40, 0, 5) == 0.0
    assert prob.at_least_one(40, 40, 5) == 1.0
    assert prob.at_least_one(40, 3, 0) == 0.0


def test_hyper_pmf_sums_to_one():
    N, K, n = 40, 9, 5
    total = sum(prob.hyper_pmf(N, K, n, k) for k in range(0, min(K, n) + 1))
    assert abs(total - 1.0) < 1e-9


def test_at_least_one_matches_pmf():
    N, K, n = 40, 9, 5
    via_pmf = 1 - prob.hyper_pmf(N, K, n, 0)
    assert abs(prob.at_least_one(N, K, n) - via_pmf) < 1e-9


def test_all_groups_two_disjoint():
    # 9 welcome-access + 16 monsters in a 40-card deck, hand 5.
    exact = prob.all_groups_at_least(40, [(9, 1), (16, 1)], 5)
    assert 0.60 < exact < 0.75  # ~0.68


def test_all_groups_matches_monte_carlo():
    # Build a synthetic deck: ids 1..9 = group A, 10..25 = group B, rest filler.
    deck = list(range(1, 10)) + list(range(10, 26)) + list(range(100, 115))
    assert len(deck) == 40
    exact = prob.all_groups_at_least(40, [(9, 1), (16, 1)], 5)

    def pred(hand: Counter) -> bool:
        a = any(hand.get(i, 0) for i in range(1, 10))
        b = any(hand.get(i, 0) for i in range(10, 26))
        return a and b

    mc = prob.monte_carlo(deck, 5, pred, trials=200_000, seed=1)
    assert abs(exact - mc) < 0.006


def test_going_second_beats_going_first():
    # More cards seen -> higher chance to open a given group.
    assert prob.at_least_one(40, 8, 6) > prob.at_least_one(40, 8, 5)
