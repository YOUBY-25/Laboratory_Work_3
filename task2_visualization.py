"""
Computational Geometry - Laboratory Work No. 3

Task 2:
Visualization of line segments and their intersection points.

Vertical segments are included in the test data.
"""

import os

import matplotlib.pyplot as plt

from geometry import Point
from task1_bentley_ottmann import BentleyOttmann


RESULTS_DIR = "results"


def create_results_directory():
    """Create the results directory if it does not exist."""
    os.makedirs(RESULTS_DIR, exist_ok=True)


def visualize_segments(segments, intersections):
    """Create and save the visualization."""
    create_results_directory()

    fig, ax = plt.subplots(figsize=(10, 7))

    # Draw segments.
    for index, (p1, p2) in enumerate(segments, start=1):
        ax.plot(
            [p1.x, p2.x],
            [p1.y, p2.y],
            linewidth=2,
            label=f"S{index}",
        )

        ax.scatter(
            [p1.x, p2.x],
            [p1.y, p2.y],
            s=25,
            color="black",
            zorder=3,
        )

    # Draw intersections.
    if intersections:
        x_values = [point.x for point in intersections]
        y_values = [point.y for point in intersections]

        ax.scatter(
            x_values,
            y_values,
            color="red",
            s=70,
            marker="o",
            edgecolors="black",
            linewidths=0.8,
            zorder=5,
            label="Intersections",
        )

        for index, point in enumerate(intersections, start=1):
            ax.annotate(
                f"I{index} ({point.x:.2f}, {point.y:.2f})",
                (point.x, point.y),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=8,
            )

    ax.set_title(
        "Bentley-Ottmann Algorithm - Segment Intersections",
        fontsize=14,
    )

    ax.set_xlabel("X coordinate")
    ax.set_ylabel("Y coordinate")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.5,
    )

    ax.legend(
        loc="best",
        fontsize=8,
    )

    ax.set_aspect("equal", adjustable="box")

    plt.tight_layout()

    output_file = os.path.join(
        RESULTS_DIR,
        "task2_intersections.png",
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()
    plt.close()

    print(f"Visualization saved to: {output_file}")


def main():
    """Run Task 2."""
    segments = [
        (Point(1, 1), Point(5, 5)),
        (Point(2, 4), Point(4, 2)),
        (Point(3, 1), Point(6, 4)),
        (Point(1, 5), Point(6, 1)),

        # Vertical segment.
        (Point(2.5, 0), Point(2.5, 6)),

        # Another vertical segment.
        (Point(5, 0.5), Point(5, 6)),
    ]

    algorithm = BentleyOttmann(segments)
    intersections = algorithm.find_intersections()

    print("=" * 60)
    print("LABORATORY WORK No. 3 - TASK 2")
    print("VISUALIZATION")
    print("=" * 60)

    print(f"Segments: {len(segments)}")
    print(f"Intersections: {len(intersections)}")

    for index, point in enumerate(intersections, start=1):
        print(
            f"I{index}: "
            f"({point.x:.6f}, {point.y:.6f})"
        )

    visualize_segments(
        segments,
        intersections,
    )


if __name__ == "__main__":
    main()
