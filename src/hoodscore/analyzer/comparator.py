"""Side-by-side neighborhood comparison."""

from __future__ import annotations

from hoodscore.analyzer.composite import CompositeScorer
from hoodscore.models import ComparisonResult, Neighborhood, Score


class NeighborhoodComparator:
    """Compares two neighborhoods side by side across all dimensions."""

    def __init__(self, scorer: CompositeScorer | None = None) -> None:
        self.scorer = scorer or CompositeScorer()

    def compare(
        self, hood_a: Neighborhood, hood_b: Neighborhood
    ) -> ComparisonResult:
        """Compare two neighborhoods and return detailed results."""
        score_a = self.scorer.score(hood_a)
        score_b = self.scorer.score(hood_b)

        advantages_a = self._find_advantages(score_a, score_b)
        advantages_b = self._find_advantages(score_b, score_a)

        winner = (
            hood_a.name
            if score_a.overall > score_b.overall
            else hood_b.name
            if score_b.overall > score_a.overall
            else "Tie"
        )

        return ComparisonResult(
            neighborhood_a=score_a,
            neighborhood_b=score_b,
            winner=winner,
            advantages_a=advantages_a,
            advantages_b=advantages_b,
        )

    def _find_advantages(self, better: Score, worse: Score) -> list[str]:
        """Identify dimensions where 'better' outperforms 'worse'."""
        advantages: list[str] = []
        dimensions = [
            ("Safety", better.safety_score, worse.safety_score),
            ("Schools", better.school_score, worse.school_score),
            ("Amenities", better.amenity_score, worse.amenity_score),
            ("Walkability", better.walkability_score, worse.walkability_score),
        ]
        for name, a_val, b_val in dimensions:
            diff = a_val - b_val
            if diff > 5:
                advantages.append(f"{name}: +{diff:.1f} points")
        return advantages
