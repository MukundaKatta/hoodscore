"""Amenity scoring based on nearby amenity count and quality."""

from __future__ import annotations

from collections import Counter

import numpy as np

from hoodscore.models import Amenity, AmenityType, Neighborhood


# Ideal number of each amenity type within walking distance
_IDEAL_COUNTS: dict[AmenityType, int] = {
    AmenityType.GROCERY: 3,
    AmenityType.RESTAURANT: 10,
    AmenityType.PARK: 3,
    AmenityType.TRANSIT: 5,
    AmenityType.HOSPITAL: 1,
}

# Maximum distance to be counted (miles)
_MAX_DISTANCE: dict[AmenityType, float] = {
    AmenityType.GROCERY: 1.5,
    AmenityType.RESTAURANT: 1.0,
    AmenityType.PARK: 1.0,
    AmenityType.TRANSIT: 0.5,
    AmenityType.HOSPITAL: 5.0,
}

# Weight per amenity type
_TYPE_WEIGHTS: dict[AmenityType, float] = {
    AmenityType.GROCERY: 0.25,
    AmenityType.RESTAURANT: 0.15,
    AmenityType.PARK: 0.20,
    AmenityType.TRANSIT: 0.25,
    AmenityType.HOSPITAL: 0.15,
}


class AmenityScorer:
    """Scores neighborhoods based on nearby amenity count and variety.

    Counts grocery stores, restaurants, parks, transit stops, and hospitals
    within defined radius thresholds. Scores are based on proximity to
    ideal amenity counts.
    """

    def __init__(self) -> None:
        self.ideal_counts = _IDEAL_COUNTS
        self.max_distances = _MAX_DISTANCE
        self.type_weights = _TYPE_WEIGHTS

    def score(self, neighborhood: Neighborhood) -> float:
        """Compute amenity score from 0 to 100."""
        if not neighborhood.amenities:
            return 20.0

        type_scores: list[float] = []
        weights: list[float] = []

        for amenity_type in AmenityType:
            nearby = self._count_nearby(neighborhood.amenities, amenity_type)
            ideal = self.ideal_counts.get(amenity_type, 3)
            ratio = min(nearby / ideal, 1.5) if ideal > 0 else 0
            # Score: 0 amenities = 0, ideal = 80, 1.5x ideal = 100
            raw = min(100.0, ratio / 1.5 * 100.0) if ratio <= 1.0 else min(100.0, 80.0 + (ratio - 1.0) * 40.0)
            type_scores.append(raw)
            weights.append(self.type_weights.get(amenity_type, 0.1))

        weights_arr = np.array(weights)
        scores_arr = np.array(type_scores)
        total_weight = weights_arr.sum()
        if total_weight == 0:
            return 20.0

        overall = float(np.dot(scores_arr, weights_arr) / total_weight)
        return round(max(0.0, min(100.0, overall)), 1)

    def _count_nearby(self, amenities: list[Amenity], amenity_type: AmenityType) -> int:
        """Count amenities of a given type within the max distance."""
        max_dist = self.max_distances.get(amenity_type, 2.0)
        return sum(
            1
            for a in amenities
            if a.amenity_type == amenity_type and a.distance_miles <= max_dist
        )

    def get_counts(self, neighborhood: Neighborhood) -> dict[str, int]:
        """Return count of each amenity type within range."""
        counts: dict[str, int] = {}
        for amenity_type in AmenityType:
            counts[amenity_type.value] = self._count_nearby(
                neighborhood.amenities, amenity_type
            )
        return counts

    def get_details(self, neighborhood: Neighborhood) -> dict[str, str]:
        """Return detailed breakdown of amenity scoring."""
        counts = self.get_counts(neighborhood)
        details: dict[str, str] = {}
        for amenity_type in AmenityType:
            count = counts[amenity_type.value]
            ideal = self.ideal_counts.get(amenity_type, 3)
            details[amenity_type.value] = f"{count} nearby (ideal: {ideal})"
        details["total"] = str(len(neighborhood.amenities))
        return details
