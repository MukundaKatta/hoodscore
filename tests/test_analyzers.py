"""Tests for analyzer modules."""

import pytest

from hoodscore.analyzer.comparator import NeighborhoodComparator
from hoodscore.analyzer.composite import CompositeScorer
from hoodscore.analyzer.trends import TrendAnalyzer
from hoodscore.database.neighborhoods import NeighborhoodDatabase
from hoodscore.models import (
    Amenity,
    AmenityType,
    CrimeCategory,
    CrimeData,
    Neighborhood,
    School,
    SchoolType,
)


def _make_hood(name: str = "Test", crime_rate: float = 3.0) -> Neighborhood:
    return Neighborhood(
        name=name,
        city="Portland",
        state="OR",
        amenities=[
            Amenity(name="G1", amenity_type=AmenityType.GROCERY, distance_miles=0.3),
            Amenity(name="R1", amenity_type=AmenityType.RESTAURANT, distance_miles=0.2),
            Amenity(name="P1", amenity_type=AmenityType.PARK, distance_miles=0.2),
            Amenity(name="T1", amenity_type=AmenityType.TRANSIT, distance_miles=0.1),
            Amenity(name="H1", amenity_type=AmenityType.HOSPITAL, distance_miles=1.5),
        ],
        crime_data=[
            CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=crime_rate),
            CrimeData(category=CrimeCategory.PROPERTY, incidents_per_1000=crime_rate * 5),
        ],
        schools=[
            School(name="ES", school_type=SchoolType.ELEMENTARY, rating=8.0, distance_miles=0.3),
            School(name="MS", school_type=SchoolType.MIDDLE, rating=7.0, distance_miles=0.8),
            School(name="HS", school_type=SchoolType.HIGH, rating=7.5, distance_miles=1.0),
        ],
    )


class TestCompositeScorer:
    def setup_method(self):
        self.scorer = CompositeScorer()

    def test_score_returns_score_object(self):
        hood = _make_hood()
        result = self.scorer.score(hood)
        assert result.neighborhood_name == "Test"
        assert 0 <= result.overall <= 100
        assert 0 <= result.safety_score <= 100
        assert 0 <= result.school_score <= 100
        assert 0 <= result.amenity_score <= 100
        assert 0 <= result.walkability_score <= 100

    def test_safe_hood_scores_higher(self):
        safe = _make_hood("Safe", crime_rate=0.5)
        unsafe = _make_hood("Unsafe", crime_rate=7.0)
        safe_score = self.scorer.score(safe)
        unsafe_score = self.scorer.score(unsafe)
        assert safe_score.overall > unsafe_score.overall

    def test_details_populated(self):
        hood = _make_hood()
        result = self.scorer.score(hood)
        assert len(result.details) > 0

    def test_custom_weights(self):
        scorer = CompositeScorer(safety_weight=1.0, school_weight=0.0, amenity_weight=0.0, walkability_weight=0.0)
        hood = _make_hood()
        result = scorer.score(hood)
        safety_only = SafetyScorer_score(hood)
        # When only safety has weight, overall should equal safety
        assert abs(result.overall - result.safety_score) < 0.2


def SafetyScorer_score(hood):
    from hoodscore.scorer.safety import SafetyScorer
    return SafetyScorer().score(hood)


class TestNeighborhoodComparator:
    def test_compare_returns_result(self):
        hood_a = _make_hood("A", crime_rate=1.0)
        hood_b = _make_hood("B", crime_rate=5.0)
        comparator = NeighborhoodComparator()
        result = comparator.compare(hood_a, hood_b)
        assert result.winner == "A"
        assert len(result.advantages_a) > 0

    def test_compare_tie(self):
        hood_a = _make_hood("A", crime_rate=3.0)
        hood_b = _make_hood("B", crime_rate=3.0)
        comparator = NeighborhoodComparator()
        result = comparator.compare(hood_a, hood_b)
        assert result.winner == "Tie"


class TestTrendAnalyzer:
    def setup_method(self):
        self.analyzer = TrendAnalyzer()

    def test_single_snapshot(self):
        hood = _make_hood()
        hood.year = 2025
        trend = self.analyzer.analyze([hood])
        assert trend.direction == "stable"
        assert trend.annual_change == 0.0

    def test_improving_trend(self):
        snapshots = []
        for year in range(2020, 2026):
            hood = _make_hood()
            hood.year = year
            # Decreasing crime rate = improving
            for crime in hood.crime_data:
                crime.incidents_per_1000 *= max(0.1, 1.0 - (year - 2020) * 0.15)
            snapshots.append(hood)
        trend = self.analyzer.analyze(snapshots)
        assert trend.direction == "improving"
        assert trend.annual_change > 0

    def test_project(self):
        hood = _make_hood()
        hood.year = 2025
        trend = self.analyzer.analyze([hood])
        projections = self.analyzer.project(trend, years_ahead=3)
        assert len(projections) == 3
        assert projections[0][0] == 2026

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            self.analyzer.analyze([])


class TestDatabase:
    def setup_method(self):
        self.db = NeighborhoodDatabase()

    def test_has_50_plus_neighborhoods(self):
        assert self.db.count >= 50

    def test_get_by_name(self):
        hood = self.db.get_neighborhood("Downtown Portland")
        assert hood is not None
        assert hood.city == "Portland"

    def test_case_insensitive_lookup(self):
        hood = self.db.get_neighborhood("downtown portland")
        assert hood is not None

    def test_get_nonexistent_returns_none(self):
        assert self.db.get_neighborhood("Nonexistent Place") is None

    def test_search(self):
        results = self.db.search("Portland")
        assert len(results) > 0

    def test_list_all(self):
        all_hoods = self.db.list_all()
        assert len(all_hoods) >= 50

    def test_list_by_city(self):
        portland = self.db.list_by_city("Portland")
        assert len(portland) >= 3
        for hood in portland:
            assert hood.city == "Portland"

    def test_list_by_state(self):
        oregon = self.db.list_by_state("OR")
        assert len(oregon) >= 3

    def test_list_cities(self):
        cities = self.db.list_cities()
        assert "Portland" in cities
        assert "Seattle" in cities

    def test_neighborhoods_have_data(self):
        for hood in self.db.list_all():
            assert len(hood.amenities) > 0, f"{hood.name} has no amenities"
            assert len(hood.crime_data) > 0, f"{hood.name} has no crime data"
            assert len(hood.schools) > 0, f"{hood.name} has no schools"
