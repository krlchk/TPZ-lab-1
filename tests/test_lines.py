import pytest

from lines_app import (
    Line,
    InputError,
    line_from_slope,
    line_from_point_normal,
    analyze_three_lines,
    MIN_VAL,
    MAX_VAL,
    EPS,
)


def assert_point_close(p, x, y, eps=EPS):
    px, py = p
    assert abs(px - x) <= eps
    assert abs(py - y) <= eps

def test_coincide_all_three():
    l1 = Line(1.0, -1.0, 1.0)
    l2 = Line(2.0, -2.0, 2.0)
    l3 = Line(-1.0, 1.0, -1.0)

    status, pts = analyze_three_lines(l1, l2, l3)
    assert status == "COINCIDE"
    assert pts == []


def test_none_all_parallel_distinct():
    l1 = Line(2.0, -1.0, 1.0)
    l2 = Line(2.0, -1.0, 2.0)
    l3 = Line(2.0, -1.0, -3.0)

    status, pts = analyze_three_lines(l1, l2, l3)
    assert status == "NONE"
    assert pts == []


def test_one_all_concurrent():
    l1 = line_from_slope(1, 1)
    l2 = line_from_point_normal(0, 1, 1, 0, idx=1)
    l3 = line_from_point_normal(0, 1, 0, 1, idx=2)

    status, pts = analyze_three_lines(l1, l2, l3)
    assert status == "ONE"
    assert len(pts) == 1
    assert_point_close(pts[0], 0.0, 1.0)


def test_two_one_parallel_pair():
    l1 = line_from_slope(0, 1)
    l2 = line_from_point_normal(0, 0, 1, 0, idx=1)
    l3 = line_from_point_normal(2, 0, 1, 0, idx=2)

    status, pts = analyze_three_lines(l1, l2, l3)
    assert status == "TWO"
    assert len(pts) == 2


def test_three_general_case():
    l1 = Line(1.0, -1.0, 0.0)
    l2 = Line(1.0, 1.0, 0.0)
    l3 = Line(0.0, 1.0, -1.0)

    status, pts = analyze_three_lines(l1, l2, l3)
    assert status == "THREE"
    assert len(pts) == 3

def test_slope_b_zero_raises():
    with pytest.raises(InputError):
        line_from_slope(1, 0)


def test_point_normal_zero_vector_raises():
    with pytest.raises(InputError):
        line_from_point_normal(0, 0, 0, 0, idx=1)


@pytest.mark.parametrize("value", [MIN_VAL - 1, MAX_VAL + 1])
def test_out_of_range_raises(value):
    with pytest.raises(InputError):
        line_from_slope(0, value if value != 0 else 1)


def test_range_edges_ok():
    line_from_slope(MIN_VAL, -1)
    line_from_slope(MAX_VAL, 1)