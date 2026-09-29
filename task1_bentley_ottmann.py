"""
Laboratory Work No. 3
Computational Geometry

Task 1:
Implementation of the Bentley-Ottmann algorithm for finding
intersection points of line segments.

The implementation uses:
- Point
- Segment
- Event
- StatusStructure
- BentleyOttmann

The program also supports vertical segments in the geometric
intersection calculation.
"""

import heapq
from typing import List, Optional, Set, Tuple

from geometry import Point, Segment, intersection_point


class Event:
    """
    Event stored in the priority queue.

    Event types:
        left          - left endpoint of a segment
        right         - right endpoint of a segment
        intersection  - intersection between two segments
    """

    TYPE_ORDER = {
        "left": 0,
        "intersection": 1,
        "right": 2,
    }

    def __init__(
        self,
        point: Point,
        typ: str,
        segment: Optional[Segment] = None,
        segment2: Optional[Segment] = None,
        intersection_point_value: Optional[Point] = None,
    ):
        self.point = point
        self.typ = typ
        self.segment = segment
        self.segment2 = segment2
        self.intersection_point = intersection_point_value

    def __lt__(self, other):
        """
        Compare events by x-coordinate, y-coordinate and type.

        This prevents Python from trying to compare Segment objects
        when two events have equal coordinates.
        """
        if not isinstance(other, Event):
            return NotImplemented

        if self.point.x != other.point.x:
            return self.point.x < other.point.x

        if self.point.y != other.point.y:
            return self.point.y < other.point.y

        return self.TYPE_ORDER.get(
            self.typ, 99
        ) < self.TYPE_ORDER.get(other.typ, 99)


class StatusStructure:
    """
    Sweep-line status structure.

    The structure stores active segments and determines their
    vertical order at the current x-coordinate.

    A heap is used internally. Segment IDs are included in heap
    entries so that Segment objects are never compared directly.
    """

    def __init__(self):
        self.heap = []
        self.segments = {}

    def add(self, segment: Segment, x: float):
        """Add a segment to the active status."""
        y = segment.y_at_x(x)

        heapq.heappush(
            self.heap,
            (y, segment.id, segment)
        )

        self.segments[segment.id] = segment

    def remove(self, segment: Segment, x: float):
        """
        Remove a segment from the active status.

        Lazy deletion is used because rebuilding the heap is simpler
        and safer for this educational implementation.
        """
        if segment.id in self.segments:
            del self.segments[segment.id]

    def rebuild(self, x: float):
        """Rebuild the heap using the current x-coordinate."""
        self.heap = []

        for segment in self.segments.values():
            y = segment.y_at_x(x)

            heapq.heappush(
                self.heap,
                (y, segment.id, segment)
            )

    def ordered_segments(self, x: float):
        """Return active segments ordered from bottom to top."""
        active = []

        for segment in self.segments.values():
            y = segment.y_at_x(x)

            active.append(
                (y, segment.id, segment)
            )

        active.sort(
            key=lambda item: (item[0], item[1])
        )

        return active

    def get_neighbors(
        self,
        segment: Segment,
        x: float
    ) -> Tuple[Optional[Segment], Optional[Segment]]:
        """
        Return the segments immediately above and below a segment.
        """
        active = self.ordered_segments(x)

        for index, (_, segment_id, current_segment) in enumerate(
            active
        ):
            if segment_id == segment.id:

                below = None
                above = None

                if index > 0:
                    below = active[index - 1][2]

                if index < len(active) - 1:
                    above = active[index + 1][2]

                return above, below

        return None, None


class BentleyOttmann:
    """
    Bentley-Ottmann sweep-line algorithm.

    The algorithm processes segment endpoints and intersection
    events from left to right.
    """

    EPSILON = 1e-10

    def __init__(
        self,
        segments: List[Tuple[Point, Point]]
    ):
        self.segments = [
            Segment(point1, point2, index)
            for index, (point1, point2) in enumerate(segments)
        ]

        self.intersections: Set[Point] = set()
        self.event_queue = []
        self.status = StatusStructure()

        self.scheduled_pairs = set()

    def _event_key(
        self,
        segment1: Segment,
        segment2: Segment
    ):
        """Create a unique key for a segment pair."""
        return tuple(
            sorted(
                (segment1.id, segment2.id)
            )
        )

    def _left_and_right_points(self, segment: Segment):
        """
        Return the left and right endpoints.

        Vertical segments are ordered by y-coordinate.
        """
        p1 = segment.p1
        p2 = segment.p2

        if p1.x < p2.x:
            return p1, p2

        if p2.x < p1.x:
            return p2, p1

        if p1.y <= p2.y:
            return p1, p2

        return p2, p1

    def _initialize_events(self):
        """Create endpoint events for every segment."""
        for segment in self.segments:

            left, right = self._left_and_right_points(segment)

            heapq.heappush(
                self.event_queue,
                Event(
                    left,
                    "left",
                    segment=segment
                )
            )

            heapq.heappush(
                self.event_queue,
                Event(
                    right,
                    "right",
                    segment=segment
                )
            )

    def find_intersections(self) -> Set[Point]:
        """
        Find all intersection points.

        Returns:
            A set containing Point objects representing intersections.
        """
        self.event_queue = []
        self.intersections = set()
        self.scheduled_pairs = set()
        self.status = StatusStructure()

        self._initialize_events()

        while self.event_queue:

            event = heapq.heappop(
                self.event_queue
            )

            if event.typ == "left":
                self.handle_left_event(event)

            elif event.typ == "right":
                self.handle_right_event(event)

            elif event.typ == "intersection":
                self.handle_intersection_event(event)

        return self.intersections

    def handle_left_event(self, event: Event):
        """Process the left endpoint of a segment."""
        segment = event.segment

        if segment is None:
            return

        x = event.point.x

        self.status.add(
            segment,
            x
        )

        above, below = self.status.get_neighbors(
            segment,
            x
        )

        if above is not None:
            self.check_intersection(
                segment,
                above,
                x
            )

        if below is not None:
            self.check_intersection(
                segment,
                below,
                x
            )

    def handle_right_event(self, event: Event):
        """Process the right endpoint of a segment."""
        segment = event.segment

        if segment is None:
            return

        x = event.point.x

        above, below = self.status.get_neighbors(
            segment,
            x
        )

        self.status.remove(
            segment,
            x
        )

        if above is not None and below is not None:
            self.check_intersection(
                above,
                below,
                x
            )

    def handle_intersection_event(self, event: Event):
        """Process an intersection event."""
        segment1 = event.segment
        segment2 = event.segment2
        point = event.point

        if segment1 is None or segment2 is None:
            return

        if point in self.intersections:
            return

        self.intersections.add(point)

        x = point.x

        # Rebuild the status immediately around the intersection.
        #
        # At x + epsilon the two segments have exchanged vertical
        # order. We determine the new neighbors using a slightly
        # shifted x-coordinate.
        test_x = x + self.EPSILON

        active = self.status.ordered_segments(test_x)

        # If the two segments are not active anymore, there is
        # nothing more to schedule.
        active_ids = {
            item[1]
            for item in active
        }

        if (
            segment1.id not in active_ids
            or segment2.id not in active_ids
        ):
            return

        # Find the two segments in the active order.
        index1 = None
        index2 = None

        for index, (_, segment_id, _) in enumerate(active):

            if segment_id == segment1.id:
                index1 = index

            if segment_id == segment2.id:
                index2 = index

        if index1 is None or index2 is None:
            return

        # Check neighbors around both segments after the crossing.
        lower_index = min(index1, index2)
        upper_index = max(index1, index2)

        if lower_index > 0:
            lower_neighbor = active[lower_index - 1][2]

            self.check_intersection(
                segment1 if index1 == lower_index else segment2,
                lower_neighbor,
                x
            )

        if upper_index < len(active) - 1:
            upper_neighbor = active[upper_index + 1][2]

            self.check_intersection(
                segment2 if index2 == upper_index else segment1,
                upper_neighbor,
                x
            )

    def check_intersection(
        self,
        segment1: Segment,
        segment2: Segment,
        current_x: float
    ):
        """
        Check two neighboring segments.

        If their intersection lies to the right of the sweep line,
        add a future intersection event.
        """
        if segment1.id == segment2.id:
            return

        point = intersection_point(
            segment1,
            segment2
        )

        if point is None:
            return

        if point.x <= current_x + self.EPSILON:
            return

        pair = self._event_key(
            segment1,
            segment2
        )

        if pair in self.scheduled_pairs:
            return

        self.scheduled_pairs.add(pair)

        heapq.heappush(
            self.event_queue,
            Event(
                point,
                "intersection",
                segment=segment1,
                segment2=segment2,
                intersection_point_value=point
            )
        )


def print_results(
    segments: List[Tuple[Point, Point]],
    intersections: Set[Point]
):
    """Print the input segments and calculated intersections."""

    print("Input segments:")

    for index, (point1, point2) in enumerate(
        segments,
        start=1
    ):
        print(
            f"S{index}: "
            f"({point1.x:g}, {point1.y:g}) -> "
            f"({point2.x:g}, {point2.y:g})"
        )

    print()
    print("=" * 50)
    print("Bentley-Ottmann Algorithm")
    print("=" * 50)

    print(
        f"Number of intersections: "
        f"{len(intersections)}"
    )

    ordered = sorted(
        intersections,
        key=lambda point: (
            point.x,
            point.y
        )
    )

    for index, point in enumerate(
        ordered,
        start=1
    ):
        print(
            f"{index}. "
            f"({point.x:.6f}, {point.y:.6f})"
        )

    print("=" * 50)


def main():
    """Run the laboratory example."""

    segments = [
        (
            Point(1, 1),
            Point(5, 5)
        ),
        (
            Point(2, 4),
            Point(4, 2)
        ),
        (
            Point(3.1, 1),
            Point(6.1, 4)
        ),
    ]

    algorithm = BentleyOttmann(
        segments
    )

    intersections = algorithm.find_intersections()

    print_results(
        segments,
        intersections
    )


if __name__ == "__main__":
    main()
