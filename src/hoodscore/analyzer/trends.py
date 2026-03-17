"""Trend analysis tracking neighborhood improvement or decline."""

from __future__ import annotations

import numpy as np

from hoodscore.models import Neighborhood, TrendData


class TrendAnalyzer:
    """Tracks neighborhood score trends over time.

    Analyzes historical data to determine whether a neighborhood is
    improving, declining, or stable. Uses crime trend data and
    amenity changes to project trajectory.
    """

    IMPROVING_THRESHOLD = 1.0  # Annual score change above this = improving
    DECLINING_THRESHOLD = -1.0  # Annual score change below this = declining

    def analyze(self, neighborhoods: list[Neighborhood]) -> TrendData:
        """Analyze trend from a list of neighborhood snapshots over time.

        Each Neighborhood in the list should represent the same neighborhood
        at different points in time (identified by .year).
        """
        if not neighborhoods:
            raise ValueError("At least one neighborhood snapshot is required")

        if len(neighborhoods) == 1:
            hood = neighborhoods[0]
            return TrendData(
                neighborhood_name=hood.name,
                years=[hood.year],
                scores=[self._quick_score(hood)],
                direction="stable",
                annual_change=0.0,
            )

        # Sort by year
        sorted_hoods = sorted(neighborhoods, key=lambda n: n.year)
        years = [n.year for n in sorted_hoods]
        scores = [self._quick_score(n) for n in sorted_hoods]

        # Linear regression for trend
        years_arr = np.array(years, dtype=float)
        scores_arr = np.array(scores, dtype=float)
        if len(years_arr) >= 2:
            coeffs = np.polyfit(years_arr, scores_arr, 1)
            annual_change = float(coeffs[0])
        else:
            annual_change = 0.0

        if annual_change > self.IMPROVING_THRESHOLD:
            direction = "improving"
        elif annual_change < self.DECLINING_THRESHOLD:
            direction = "declining"
        else:
            direction = "stable"

        return TrendData(
            neighborhood_name=sorted_hoods[0].name,
            years=years,
            scores=[round(s, 1) for s in scores],
            direction=direction,
            annual_change=round(annual_change, 2),
        )

    def _quick_score(self, neighborhood: Neighborhood) -> float:
        """Compute a quick composite score for trend tracking."""
        from hoodscore.analyzer.composite import CompositeScorer

        scorer = CompositeScorer()
        result = scorer.score(neighborhood)
        return result.overall

    def project(
        self, trend: TrendData, years_ahead: int = 5
    ) -> list[tuple[int, float]]:
        """Project future scores based on current trend."""
        if not trend.years or not trend.scores:
            return []

        last_year = trend.years[-1]
        last_score = trend.scores[-1]
        projections: list[tuple[int, float]] = []

        for i in range(1, years_ahead + 1):
            future_year = last_year + i
            projected = last_score + trend.annual_change * i
            projected = max(0.0, min(100.0, projected))
            projections.append((future_year, round(projected, 1)))

        return projections
