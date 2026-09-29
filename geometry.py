"""
Geometry utilities for Computational Geometry Laboratory Work No. 3.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


EPSILON = 1e-10


@dataclass(frozen=True)
class Point:
    """Two-dimensional point."""

    x: float
    y: float

    def __lt__(self, other):
        """Compare points lexicographically."""
        if not isinstance(other, Point):
            return NotImplemented

        if abs(self.x - other.x) > EPSILON:
            return self.x < other.x

        return self.y < other.y


@dataclass
class Segment:
    """Line segment defined by two endpoints."""

    p1: Point
    p2: Point
    id: int = 0

    def left_right_endpoints(self) -> Tuple[Point, Point]:
        """
        Return endpoints ordered from left to right.

        For equal X coordinates, the lower point is considered first.
        """
        if self.p1.x < self.p2.x:
            return self.p1, self.p2

        if self.p1.x > self.p2.x:
            return self.p2, self.p1

        if self.p1.y <= self.p2.y:
            return self.p1, self.p2

        return self.p2, self.p1

    def y_at_x(self, x: float) -> float:
        """Calculate Y-coordinate of the segment at X."""
        if abs(self.p2.x - self.p1.x) < EPSILON:
            return min(self.p1.y, self.p2.y)

        t = (
            (x - self.p1.x)
            / (self.p2.x - self.p1.x)
        )

        return self.p1.y + t * (
            self.p2.y - self.p1.y
        )


def orientation(
    p: Point,
    q: Point,
    r: Point
) -> float:
    """Calculate orientation of three points."""
    return (
        (q.x - p.x) * (r.y - p.y)
        - (q.y - p.y) * (r.x - p.x)
    )


def on_segment(
    p: Point,
    q: Point,
    r: Point
) -> bool:
    """Check whether q lies on segment pr."""
    return (
        min(p.x, r.x) - EPSILON <= q.x <=
        max(p.x, r.x) + EPSILON
        and
        min(p.y, r.y) - EPSILON <= q.y <=
        max(p.y, r.y) + EPSILON
    )


def segments_intersect(
    s1: Segment,
    s2: Segment
) -> bool:
    """Check whether two segments intersect."""
    if s1 is None or s2 is None:
        return False

    o1 = orientation(
        s1.p1,
        s1.p2,
        s2.p1
    )

    o2 = orientation(
        s1.p1,
        s1.p2,
        s2.p2
    )

    o3 = orientation(
        s2.p1,
        s2.p2,
        s1.p1
    )

    o4 = orientation(
        s2.p1,
        s2.p2,
        s1.p2
    )

    if (
        ((o1 > EPSILON and o2 < -EPSILON) or
         (o1 < -EPSILON and o2 > EPSILON))
        and
        ((o3 > EPSILON and o4 < -EPSILON) or
         (o3 < -EPSILON and o4 > EPSILON))
    ):
        return True

    if abs(o1) <= EPSILON and on_segment(
        s1.p1,
        s2.p1,
        s1.p2
    ):
        return True

    if abs(o2) <= EPSILON and on_segment(
        s1.p1,
        s2.p2,
        s1.p2
    ):
        return True

    if abs(o3) <= EPSILON and on_segment(
        s2.p1,
        s1.p1,
        s2.p2
    ):
        return True

    if abs(o4) <= EPSILON and on_segment(
        s2.p1,
        s1.p2,
        s2.p2
    ):
        return True

    return False


def intersection_point(
    s1: Segment,
    s2: Segment
) -> Optional[Point]:
    """
    Calculate the intersection point of two segments.

    Returns None when there is no single intersection point.
    """
    if s1 is None or s2 is None:
        return None

    if not segments_intersect(s1, s2):
        return None

    x1, y1 = s1.p1.x, s1.p1.y
    x2, y2 = s1.p2.x, s1.p2.y

    x3, y3 = s2.p1.x, s2.p1.y
    x4, y4 = s2.p2.x, s2.p2.y

    denominator = (
        (x1 - x2) * (y3 - y4)
        - (y1 - y2) * (x3 - x4)
    )

    # Parallel or collinear segments.
    if abs(denominator) < EPSILON:
        # Handle common endpoint intersections.
        candidates = [
            s1.p1,
            s1.p2,
            s2.p1,
            s2.p2
        ]

        for point in candidates:
            if (
                on_segment(s1.p1, point, s1.p2)
                and
                on_segment(s2.p1, point, s2.p2)
            ):
                return point

        return None

    numerator_x = (
        (x1 * y2 - y1 * x2) * (x3 - x4)
        - (x1 - x2)
        * (x3 * y4 - y3 * x4)
    )

    numerator_y = (
        (x1 * y2 - y1 * x2) * (y3 - y4)
        - (y1 - y2)
        * (x3 * y4 - y3 * x4)
    )

    x = numerator_x / denominator
    y = numerator_y / denominator

    point = Point(x, y)

    if (
        on_segment(s1.p1, point, s1.p2)
        and
        on_segment(s2.p1, point, s2.p2)
    ):
        return point

    return None
