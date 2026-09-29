"""
Computational Geometry - Laboratory Work No. 3

Task 3:
Comparison of the Bentley-Ottmann algorithm with the naive
O(n^2) pairwise algorithm.

The program measures execution time for:
n = 10, 50, 100, 500
"""

import os
import random
import time

import matplotlib.pyplot as plt

from geometry import Point, Segment, intersection_point
from task1_bentley_ottmann import BentleyOttmann


RESULTS_DIR = "results"


def create_results_directory():
    """Create the results directory."""
    os.makedirs(RESULTS_DIR, exist_ok=True)


def generate_random_segments(
    number_of_segments,
    seed=42,
):
    """Generate random non-vertical segments."""
    random.seed(seed + number_of_segments)

    segments = []

    for _ in range(number_of_segments):
        x1 = random.uniform(0, 100)
        x2 = random.uniform(0, 100)

        # Avoid vertical segments in the benchmark.
        while abs(x1 - x2) < 1e-6:
            x2 = random.uniform(0, 100)

        y1 = random.uniform(0, 100)
        y2 = random.uniform(0, 100)

        segments.append(
            (
                Point(x1, y1),
                Point(x2, y2),
            )
        )

    return segments


def naive_intersections(segments):
    """
    Find intersections using the naive O(n^2) algorithm.
    """
    result = set()

    segment_objects = [
        Segment(p1, p2, index)
        for index, (p1, p2)
        in enumerate(segments)
    ]

    for i in range(len(segment_objects)):
        for j in range(i + 1, len(segment_objects)):
            point = intersection_point(
                segment_objects[i],
                segment_objects[j],
            )

            if point is not None:
                result.add(
                    (
                        round(point.x, 9),
                        round(point.y, 9),
                    )
                )

    return result


def measure_naive(segments):
    """Measure naive algorithm execution time."""
    start = time.perf_counter()

    result = naive_intersections(segments)

    elapsed = time.perf_counter() - start

    return elapsed, len(result)


def measure_bentley_ottmann(segments):
    """Measure Bentley-Ottmann execution time."""
    start = time.perf_counter()

    algorithm = BentleyOttmann(segments)
    result = algorithm.find_intersections()

    elapsed = time.perf_counter() - start

    return elapsed, len(result)


def save_results_table(results):
    """Save experimental results as a text file."""
    output_file = os.path.join(
        RESULTS_DIR,
        "task3_results.txt",
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
            "Laboratory Work No. 3 - Performance Comparison\n"
        )
        file.write("=" * 70 + "\n\n")

        file.write(
            "n | Intersections | Naive Time (s) | "
            "Bentley-Ottmann Time (s)\n"
        )

        file.write("-" * 70 + "\n")

        for result in results:
            file.write(
                f"{result['n']} | "
                f"{result['k']} | "
                f"{result['naive_time']:.8f} | "
                f"{result['bo_time']:.8f}\n"
            )

    print(f"Results saved to: {output_file}")


def create_time_graph(results):
    """Create execution-time comparison graph."""
    n_values = [
        result["n"]
        for result in results
    ]

    naive_times = [
        result["naive_time"]
        for result in results
    ]

    bo_times = [
        result["bo_time"]
        for result in results
    ]

    plt.figure(figsize=(9, 6))

    plt.plot(
        n_values,
        naive_times,
        marker="o",
        linewidth=2,
        label="Naive O(n²)",
    )

    plt.plot(
        n_values,
        bo_times,
        marker="s",
        linewidth=2,
        label="Bentley-Ottmann",
    )

    plt.xlabel("Number of segments (n)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Execution Time Comparison")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.tight_layout()

    output_file = os.path.join(
        RESULTS_DIR,
        "task3_time_comparison.png",
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Graph saved to: {output_file}")


def create_intersection_graph(results):
    """Create graph showing execution time versus intersections."""
    k_values = [
        result["k"]
        for result in results
    ]

    naive_times = [
        result["naive_time"]
        for result in results
    ]

    bo_times = [
        result["bo_time"]
        for result in results
    ]

    plt.figure(figsize=(9, 6))

    plt.scatter(
        k_values,
        naive_times,
        s=60,
        label="Naive O(n²)",
    )

    plt.scatter(
        k_values,
        bo_times,
        s=60,
        label="Bentley-Ottmann",
    )

    plt.xlabel("Number of intersections (k)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Execution Time vs Number of Intersections")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.tight_layout()

    output_file = os.path.join(
        RESULTS_DIR,
        "task3_time_vs_k.png",
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Graph saved to: {output_file}")


def main():
    """Run the complete performance experiment."""
    create_results_directory()

    sizes = [10, 50, 100, 500]

    results = []

    print("=" * 70)
    print("LABORATORY WORK No. 3 - TASK 3")
    print("PERFORMANCE COMPARISON")
    print("=" * 70)

    for n in sizes:
        print()
        print(f"Testing n = {n}")

        segments = generate_random_segments(n)

        naive_time, naive_k = measure_naive(
            segments
        )

        bo_time, bo_k = measure_bentley_ottmann(
            segments
        )

        # The numbers should normally match.
        # Use the Bentley-Ottmann result as the reported k.
        k = bo_k

        print(f"Intersections: {k}")
        print(
            f"Naive time: "
            f"{naive_time:.8f} seconds"
        )
        print(
            f"Bentley-Ottmann time: "
            f"{bo_time:.8f} seconds"
        )

        if naive_k != bo_k:
            print(
                "WARNING: The algorithms returned different "
                "numbers of intersections."
            )

        results.append(
            {
                "n": n,
                "k": k,
                "naive_time": naive_time,
                "bo_time": bo_time,
            }
        )

    print()
    print("=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print(
        f"{'n':>8}"
        f"{'k':>15}"
        f"{'Naive':>20}"
        f"{'Bentley-Ottmann':>25}"
    )

    for result in results:
        print(
            f"{result['n']:>8}"
            f"{result['k']:>15}"
            f"{result['naive_time']:>20.8f}"
            f"{result['bo_time']:>25.8f}"
        )

    save_results_table(results)
    create_time_graph(results)
    create_intersection_graph(results)


if __name__ == "__main__":
    main()
