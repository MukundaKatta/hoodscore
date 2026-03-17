"""Walkability scoring based on amenity distances."""

from __future__ import annotations

import numpy as np

from hoodscore.models import Amenity, AmenityType, Neighborhood


# Distance decay parameters: how quickly score drops with distance
_DECAY_RATES: dict[AmenityType, float] = {
    AmenityType.GROCERY: 1.5,
    AmenityType.RESTAURANT: 2.0,
    AmenityType.PARK: 1.8,
    AmenityType.TRANSIT: 3.0,
    AmenityType.HOSPITAL: 0.5,
}

# Importance weights for walkability
_WALK_WEIGHTS: dict[AmenityType, float] = {
    AmenityType.GROCERY: 0.25,
    AmenityType.RESTAURANT: 0.15,
    AmenityType.PARK: 0.15,
    AmenityType.TRANSIT: 0.35,
    AmenityType.HOSPITAL: 0.10,
}


class WalkabilityScorer:
    """Computes a walk score from amenity distances.

    Uses exponential distance decay to penalize far-away amenities.
    Transit access is weighted most heavily, followed by grocery and parks.
    The score considers the closest amenity of each type.
    """

    def __init__(self) -> None:
        self.decay_rates = _DECAY_RATES
        self.walk_weights = _WALK_WEIGHTS

    def score(self, neighborhood: Neighborhood) -> float:
        """Compute walk score from 0 to 100."""
        if not neighborhood.amenities:
            return 15.0

        type_scores: list[float] = []
        weights: list[float] = []

        for amenity_type in AmenityType:
            closest_dist = self._closest_distance(
                neighborhood.amenities, amenity_type
            )
            if closest_dist is None:
                type_scores.append(0.0)
            else:
                decay = self.decay_rates.get(amenity_type, 1.5)
                # Exponential decay: score = 100 * exp(-decay * distance)
                raw = 100.0 * float(np.exp(-decay * closest_dist))
                type_scores.append(raw)
            weights.append(self.walk_weights.get(amenity_type, 0.1))

        weights_arr = np.array(weights)
        scores_arr = np.array(type_scores)
        total_weight = weights_arr.sum()
        if total_weight == 0:
            return 15.0

        overall = float(np.dot(scores_arr, weights_arr) / total_weight)
        return round(max(0.0, min(100.0, overall)), 1)

    def _closest_distance(
        self, amenities: list[Amenity], amenity_type: AmenityType
    ) -> float | None:
        """Find the distance to the closest amenity of a given type."""
        matching = [
            a.distance_miles for a in amenities if a.amenity_type == amenity_type
        ]
        return min(matching) if matching else None

    def get_details(self, neighborhood: Neighborhood) -> dict[str, str]:
        """Return detailed breakdown of walkability scoring."""
        details: dict[str, str] = {}
        for amenity_type in AmenityType:
            closest = self._closest_distance(
                neighborhood.amenities, amenity_type
            )
            if closest is not None:
                walk_mins = closest * 20  # ~3mph walking speed
                details[amenity_type.value] = (
                    f"{closest:.2f} mi ({walk_mins:.0f} min walk)"
                )
            else:
                details[amenity_type.value] = "None nearby"
        return details
