"""School scoring based on ratings, distance, and type."""

from __future__ import annotations

import numpy as np

from hoodscore.models import Neighborhood, School, SchoolType


# Ideal distance thresholds in miles
_DISTANCE_THRESHOLDS: dict[SchoolType, float] = {
    SchoolType.ELEMENTARY: 1.0,
    SchoolType.MIDDLE: 2.0,
    SchoolType.HIGH: 3.0,
    SchoolType.PRIVATE: 3.0,
    SchoolType.CHARTER: 2.5,
}


class SchoolScorer:
    """Scores neighborhoods based on nearby school quality.

    Considers school ratings (0-10), distance from neighborhood center,
    and diversity of school types available.
    """

    def __init__(self, max_distance_miles: float = 5.0) -> None:
        self.max_distance = max_distance_miles

    def score(self, neighborhood: Neighborhood) -> float:
        """Compute a school score from 0 to 100."""
        if not neighborhood.schools:
            return 30.0  # No data, low score

        rating_score = self._rating_score(neighborhood.schools)
        distance_score = self._distance_score(neighborhood.schools)
        diversity_score = self._diversity_score(neighborhood.schools)

        # Weighted combination
        weights = np.array([0.50, 0.25, 0.25])
        components = np.array([rating_score, distance_score, diversity_score])
        overall = float(np.dot(components, weights))
        return round(max(0.0, min(100.0, overall)), 1)

    def _rating_score(self, schools: list[School]) -> float:
        """Score based on average school ratings (0-10 scale -> 0-100)."""
        if not schools:
            return 0.0
        ratings = np.array([s.rating for s in schools])
        avg_rating = float(np.mean(ratings))
        return avg_rating * 10.0

    def _distance_score(self, schools: list[School]) -> float:
        """Score based on proximity. Closer schools score higher."""
        if not schools:
            return 0.0
        scores = []
        for school in schools:
            ideal = _DISTANCE_THRESHOLDS.get(school.school_type, 2.0)
            if school.distance_miles <= ideal:
                scores.append(100.0)
            elif school.distance_miles >= self.max_distance:
                scores.append(0.0)
            else:
                fraction = (school.distance_miles - ideal) / (self.max_distance - ideal)
                scores.append(100.0 * (1.0 - fraction))
        return float(np.mean(scores))

    def _diversity_score(self, schools: list[School]) -> float:
        """Score based on variety of school types available."""
        types_present = {s.school_type for s in schools}
        # Core types: elementary, middle, high
        core_types = {SchoolType.ELEMENTARY, SchoolType.MIDDLE, SchoolType.HIGH}
        core_coverage = len(types_present & core_types) / len(core_types)
        # Bonus for additional types
        bonus_types = types_present - core_types
        bonus = min(len(bonus_types) * 10.0, 20.0)
        return min(100.0, core_coverage * 80.0 + bonus)

    def get_details(self, neighborhood: Neighborhood) -> dict[str, str]:
        """Return detailed breakdown of school scoring."""
        details: dict[str, str] = {}
        details["total_schools"] = str(len(neighborhood.schools))
        if neighborhood.schools:
            ratings = [s.rating for s in neighborhood.schools]
            details["avg_rating"] = f"{np.mean(ratings):.1f}/10"
            details["best_school"] = max(
                neighborhood.schools, key=lambda s: s.rating
            ).name
            types = {s.school_type.value for s in neighborhood.schools}
            details["school_types"] = ", ".join(sorted(types))
        return details
