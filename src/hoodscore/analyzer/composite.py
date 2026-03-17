"""Composite scorer combining all dimensions into a weighted overall score."""

from __future__ import annotations

import numpy as np

from hoodscore.models import Neighborhood, Score
from hoodscore.scorer.amenities import AmenityScorer
from hoodscore.scorer.safety import SafetyScorer
from hoodscore.scorer.schools import SchoolScorer
from hoodscore.scorer.walkability import WalkabilityScorer


class CompositeScorer:
    """Combines safety, schools, amenities, and walkability into one score.

    Default weights:
        - Safety: 30%
        - Schools: 25%
        - Amenities: 25%
        - Walkability: 20%
    """

    def __init__(
        self,
        safety_weight: float = 0.30,
        school_weight: float = 0.25,
        amenity_weight: float = 0.25,
        walkability_weight: float = 0.20,
    ) -> None:
        self.weights = np.array([
            safety_weight,
            school_weight,
            amenity_weight,
            walkability_weight,
        ])
        self.safety_scorer = SafetyScorer()
        self.school_scorer = SchoolScorer()
        self.amenity_scorer = AmenityScorer()
        self.walkability_scorer = WalkabilityScorer()

    def score(self, neighborhood: Neighborhood) -> Score:
        """Compute a composite score for the neighborhood."""
        safety = self.safety_scorer.score(neighborhood)
        schools = self.school_scorer.score(neighborhood)
        amenities = self.amenity_scorer.score(neighborhood)
        walkability = self.walkability_scorer.score(neighborhood)

        components = np.array([safety, schools, amenities, walkability])
        overall = float(np.dot(components, self.weights) / self.weights.sum())
        overall = round(max(0.0, min(100.0, overall)), 1)

        # Gather details from all scorers
        details: dict[str, str] = {}
        for key, val in self.safety_scorer.get_details(neighborhood).items():
            details[f"safety_{key}"] = val
        for key, val in self.school_scorer.get_details(neighborhood).items():
            details[f"school_{key}"] = val
        for key, val in self.amenity_scorer.get_details(neighborhood).items():
            details[f"amenity_{key}"] = val
        for key, val in self.walkability_scorer.get_details(neighborhood).items():
            details[f"walk_{key}"] = val

        return Score(
            neighborhood_name=neighborhood.name,
            safety_score=safety,
            school_score=schools,
            amenity_score=amenities,
            walkability_score=walkability,
            overall=overall,
            details=details,
        )
