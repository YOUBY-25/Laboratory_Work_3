"""
Laboratory Work No. 3
Computational Geometry

Tests for:
1. Point and Segment data structures
2. Segment intersection detection
3. Bentley-Ottmann algorithm
4. Vertical segments
5. Endpoint intersections
6. Naive algorithm comparison
"""

from geometry import Point, Segment, segments_intersect, intersection_point
from task1_bentley_ottmann import BentleyOttmann


def get_points(result):
    """Convert an intersection result to a list.

    The Bentley-Ottmann implementation returns a set of Point objects.
    This helper makes the tests independent of the result container type.
    """
    return list(result)


def test_crossing_segments():
    """Test two crossing segments."""
    s1 = Segment(Point(1, 1), Point(5, 5), 1)
    s2 = Segment(Point(2, 4), Point(4, 2), 2)

    assert segments_intersect(s1, s2)

    point = intersection_point(s1, s2)

    assert point is not None
    assert abs(point.x - 3.0) < 1e-6
    assert abs(point.y - 3.0) < 1e-6

    print("PASS: Crossing segments")


def test_non_intersecting_segments():
    """Test two segments that do not intersect."""
    s1 = Segment(Point(1, 1), Point(2, 2), 1)
    s2 = Segment(Point(4, 4), Point(5, 5), 2)

    assert not segments_intersect(s1, s2)

    point = intersection_point(s1, s2)

    assert point is None

    print("PASS: Non-intersecting segments")


def test_multiple_intersections():
    """Test the example from the laboratory instructions."""
    segments = [
        (Point(1, 1), Point(5, 5)),
        (Point(2, 4), Point(4, 2)),
        (Point(3.1, 1), Point(6.1, 4)),
    ]

    algorithm = BentleyOttmann(segments)
    result = algorithm.find_intersections()

    points = get_points(result)

    assert len(points) == 1

    point = points[0]

    assert abs(point.x - 3.0) < 1e-6
    assert abs(point.y - 3.0) < 1e-6

    print("PASS: Bentley-Ottmann example")


def test_vertical_segment():
    """Test a vertical segment intersecting a horizontal segment."""
    s1 = Segment(Point(3, 1), Point(3, 5), 1)
    s2 = Segment(Point(1, 3), Point(5, 3), 2)

    assert segments_intersect(s1, s2)

    point = intersection_point(s1, s2)

    assert point is not None
    assert abs(point.x - 3.0) < 1e-6
    assert abs(point.y - 3.0) < 1e-6

    print("PASS: Vertical segment")


def test_endpoint_intersection():
    """Test two segments intersecting at an endpoint."""
    s1 = Segment(Point(1, 1), Point(3, 3), 1)
    s2 = Segment(Point(3, 3), Point(5, 1), 2)

    assert segments_intersect(s1, s2)

    point = intersection_point(s1, s2)

    assert point is not None
    assert abs(point.x - 3.0) < 1e-6
    assert abs(point.y - 3.0) < 1e-6

    print("PASS: Endpoint intersection")


def test_parallel_segments():
    """Test parallel non-intersecting segments."""
    s1 = Segment(Point(1, 1), Point(4, 1), 1)
    s2 = Segment(Point(1, 3), Point(4, 3), 2)

    assert not segments_intersect(s1, s2)

    point = intersection_point(s1, s2)

    assert point is None

    print("PASS: Parallel segments")


def test_three_segments():
    """Test a larger set of segments."""
    segments = [
        (Point(0, 0), Point(10, 10)),
        (Point(0, 10), Point(10, 0)),
        (Point(0, 5), Point(10, 5)),
    ]

    algorithm = BentleyOttmann(segments)
    result = algorithm.find_intersections()

    points = get_points(result)

    # All three segments intersect at (5, 5).
    # Depending on the implementation's handling of
    # multiple intersections, the point should appear once.
    assert len(points) >= 1

    found = False

    for point in points:
        if abs(point.x - 5.0) < 1e-6 and abs(point.y - 5.0) < 1e-6:
            found = True
            break

    assert found

    print("PASS: Three-segment intersection")


def test_bentley_ottmann_no_intersections():
    """Test Bentley-Ottmann with segments that do not intersect."""
    segments = [
        (Point(0, 0), Point(1, 1)),
        (Point(3, 0), Point(4, 1)),
        (Point(6, 0), Point(7, 1)),
    ]

    algorithm = BentleyOttmann(segments)
    result = algorithm.find_intersections()

    assert len(result) == 0

    print("PASS: Bentley-Ottmann without intersections")


def test_bentley_ottmann_two_intersections():
    """Test a set containing multiple intersections."""
    segments = [
        (Point(0, 0), Point(10, 10)),
        (Point(0, 10), Point(10, 0)),
        (Point(0, 4), Point(10, 4)),
    ]

    algorithm = BentleyOttmann(segments)
    result = algorithm.find_intersections()

    points = get_points(result)

    assert len(points) >= 2

    print("PASS: Multiple intersections")


def run_all_tests():
    """Run all laboratory tests."""
    tests = [
        test_crossing_segments,
        test_non_intersecting_segments,
        test_multiple_intersections,
        test_vertical_segment,
        test_endpoint_intersection,
        test_parallel_segments,
        test_three_segments,
        test_bentley_ottmann_no_intersections,
        test_bentley_ottmann_two_intersections,
    ]

    print("=" * 60)
    print("LABORATORY WORK No. 3 - TESTS")
    print("=" * 60)

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as error:
            failed += 1
            print(f"FAIL: {test.__name__}")
            print(f"       {error}")
        except Exception as error:
            failed += 1
            print(f"ERROR: {test.__name__}")
            print(f"       {type(error).__name__}: {error}")

    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests : {len(tests)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=" * 60)

    if failed == 0:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")
        raise SystemExit(1)


if __name__ == "__main__":
    run_all_tests()
