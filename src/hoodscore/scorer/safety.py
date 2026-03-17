"""Safety scoring based on crime rate data."""

from __future__ import annotations

import numpy as np

from hoodscore.models import CrimeCategory, CrimeData, Neighborhood


# National average crime rates per 1000 residents
_NATIONAL_AVERAGES: dict[CrimeCategory, float] = {
    CrimeCategory.VIOLENT: 4.0,
    CrimeCategory.PROPERTY: 20.0,
    CrimeCategory.DRUG: 5.0,
    CrimeCategory.OTHER: 8.0,
}

# Weight each crime category by severity
_CATEGORY_WEIGHTS: dict[CrimeCategory, float] = {
    CrimeCategory.VIOLENT: 0.45,
    CrimeCategory.PROPERTY: 0.30,
    CrimeCategory.DRUG: 0.15,
    CrimeCategory.OTHER: 0.10,
}


class SafetyScorer:
    """Scores neighborhood safety based on crime rate data.

    The score is computed by comparing local crime rates against national
    averages, weighted by crime severity category. A score of 100 means
    virtually no crime; 0 means extremely high crime.
    """

    def __init__(
        self,
        national_averages: dict[CrimeCategory, float] | None = None,
        category_weights: dict[CrimeCategory, float] | None = None,
    ) -> None:
        self.national_averages = national_averages or _NATIONAL_AVERAGES
        self.category_weights = category_weights or _CATEGORY_WEIGHTS

    def score(self, neighborhood: Neighborhood) -> float:
        """Compute a safety score from 0 to 100 for the neighborhood."""
        if not neighborhood.crime_data:
            return 50.0  # No data, return neutral score

        category_scores: list[float] = []
        weights: list[float] = []

        for crime in neighborhood.crime_data:
            avg = self.national_averages.get(crime.category, 10.0)
            ratio = crime.incidents_per_1000 / avg if avg > 0 else 1.0
            # Convert ratio to score: ratio=0 -> 100, ratio=1 -> 50, ratio=2 -> 0
            raw_score = max(0.0, min(100.0, 100.0 * (1.0 - ratio / 2.0)))
            category_scores.append(raw_score)
            weights.append(self.category_weights.get(crime.category, 0.1))

        weights_arr = np.array(weights)
        scores_arr = np.array(category_scores)
        total_weight = weights_arr.sum()
        if total_weight == 0:
            return 50.0

        weighted_score = float(np.dot(scores_arr, weights_arr) / total_weight)
        return round(max(0.0, min(100.0, weighted_score)), 1)

    def get_details(self, neighborhood: Neighborhood) -> dict[str, str]:
        """Return detailed breakdown of safety scoring."""
        details: dict[str, str] = {}
        for crime in neighborhood.crime_data:
            avg = self.national_averages.get(crime.category, 10.0)
            ratio = crime.incidents_per_1000 / avg if avg > 0 else 1.0
            if ratio < 0.5:
                assessment = "Well below average"
            elif ratio < 0.8:
                assessment = "Below average"
            elif ratio < 1.2:
                assessment = "Near average"
            elif ratio < 1.5:
                assessment = "Above average"
            else:
                assessment = "Well above average"
            details[crime.category.value] = (
                f"{crime.incidents_per_1000:.1f}/1000 ({assessment}, "
                f"national avg: {avg:.1f}/1000)"
            )
        return details
