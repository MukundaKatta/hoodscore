"""Tests for scoring modules."""

import pytest

from hoodscore.models import (
    Amenity,
    AmenityType,
    CrimeCategory,
    CrimeData,
    Neighborhood,
    School,
    SchoolType,
)
from hoodscore.scorer.amenities import AmenityScorer
from hoodscore.scorer.safety import SafetyScorer
from hoodscore.scorer.schools import SchoolScorer
from hoodscore.scorer.walkability import WalkabilityScorer


def _make_neighborhood(**kwargs) -> Neighborhood:
    defaults = dict(name="Test", city="Portland", state="OR")
    defaults.update(kwargs)
    return Neighborhood(**defaults)


class TestSafetyScorer:
    def setup_method(self):
        self.scorer = SafetyScorer()

    def test_no_crime_data_returns_neutral(self):
        hood = _make_neighborhood()
        assert self.scorer.score(hood) == 50.0

    def test_low_crime_scores_high(self):
        hood = _make_neighborhood(
            crime_data=[
                CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=0.5),
                CrimeData(category=CrimeCategory.PROPERTY, incidents_per_1000=5.0),
            ]
        )
        score = self.scorer.score(hood)
        assert score > 75.0

    def test_high_crime_scores_low(self):
        hood = _make_neighborhood(
            crime_data=[
                CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=8.0),
                CrimeData(category=CrimeCategory.PROPERTY, incidents_per_1000=40.0),
            ]
        )
        score = self.scorer.score(hood)
        assert score < 30.0

    def test_score_bounded(self):
        hood = _make_neighborhood(
            crime_data=[
                CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=100.0),
            ]
        )
        score = self.scorer.score(hood)
        assert 0.0 <= score <= 100.0

    def test_get_details(self):
        hood = _make_neighborhood(
            crime_data=[CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=2.0)]
        )
        details = self.scorer.get_details(hood)
        assert "violent" in details


class TestSchoolScorer:
    def setup_method(self):
        self.scorer = SchoolScorer()

    def test_no_schools_returns_low(self):
        hood = _make_neighborhood()
        assert self.scorer.score(hood) == 30.0

    def test_good_schools_score_high(self):
        hood = _make_neighborhood(
            schools=[
                School(name="A", school_type=SchoolType.ELEMENTARY, rating=9.0, distance_miles=0.3),
                School(name="B", school_type=SchoolType.MIDDLE, rating=8.5, distance_miles=0.5),
                School(name="C", school_type=SchoolType.HIGH, rating=9.0, distance_miles=0.8),
            ]
        )
        score = self.scorer.score(hood)
        assert score > 70.0

    def test_far_schools_score_lower(self):
        hood_close = _make_neighborhood(
            schools=[School(name="A", school_type=SchoolType.ELEMENTARY, rating=8.0, distance_miles=0.3)]
        )
        hood_far = _make_neighborhood(
            schools=[School(name="A", school_type=SchoolType.ELEMENTARY, rating=8.0, distance_miles=4.0)]
        )
        assert self.scorer.score(hood_close) > self.scorer.score(hood_far)

    def test_get_details(self):
        hood = _make_neighborhood(
            schools=[School(name="Lincoln", school_type=SchoolType.HIGH, rating=8.0, distance_miles=1.0)]
        )
        details = self.scorer.get_details(hood)
        assert details["total_schools"] == "1"
        assert "Lincoln" in details["best_school"]


class TestAmenityScorer:
    def setup_method(self):
        self.scorer = AmenityScorer()

    def test_no_amenities_returns_low(self):
        hood = _make_neighborhood()
        assert self.scorer.score(hood) == 20.0

    def test_many_amenities_score_high(self):
        amenities = []
        for i in range(5):
            amenities.append(Amenity(name=f"G{i}", amenity_type=AmenityType.GROCERY, distance_miles=0.2 * (i + 1)))
        for i in range(12):
            amenities.append(Amenity(name=f"R{i}", amenity_type=AmenityType.RESTAURANT, distance_miles=0.1 * (i + 1)))
        for i in range(4):
            amenities.append(Amenity(name=f"P{i}", amenity_type=AmenityType.PARK, distance_miles=0.2 * (i + 1)))
        for i in range(6):
            amenities.append(Amenity(name=f"T{i}", amenity_type=AmenityType.TRANSIT, distance_miles=0.05 * (i + 1)))
        amenities.append(Amenity(name="H1", amenity_type=AmenityType.HOSPITAL, distance_miles=1.0))
        hood = _make_neighborhood(amenities=amenities)
        score = self.scorer.score(hood)
        assert score > 60.0

    def test_get_counts(self):
        amenities = [
            Amenity(name="G1", amenity_type=AmenityType.GROCERY, distance_miles=0.5),
            Amenity(name="G2", amenity_type=AmenityType.GROCERY, distance_miles=3.0),  # Too far
        ]
        hood = _make_neighborhood(amenities=amenities)
        counts = self.scorer.get_counts(hood)
        assert counts["grocery"] == 1


class TestWalkabilityScorer:
    def setup_method(self):
        self.scorer = WalkabilityScorer()

    def test_no_amenities_returns_low(self):
        hood = _make_neighborhood()
        assert self.scorer.score(hood) == 15.0

    def test_close_amenities_score_high(self):
        amenities = [
            Amenity(name="G", amenity_type=AmenityType.GROCERY, distance_miles=0.1),
            Amenity(name="R", amenity_type=AmenityType.RESTAURANT, distance_miles=0.05),
            Amenity(name="P", amenity_type=AmenityType.PARK, distance_miles=0.1),
            Amenity(name="T", amenity_type=AmenityType.TRANSIT, distance_miles=0.02),
            Amenity(name="H", amenity_type=AmenityType.HOSPITAL, distance_miles=0.5),
        ]
        hood = _make_neighborhood(amenities=amenities)
        score = self.scorer.score(hood)
        assert score > 70.0

    def test_far_amenities_score_low(self):
        amenities = [
            Amenity(name="G", amenity_type=AmenityType.GROCERY, distance_miles=3.0),
            Amenity(name="T", amenity_type=AmenityType.TRANSIT, distance_miles=2.0),
        ]
        hood = _make_neighborhood(amenities=amenities)
        score = self.scorer.score(hood)
        assert score < 30.0

    def test_get_details(self):
        amenities = [
            Amenity(name="G", amenity_type=AmenityType.GROCERY, distance_miles=0.5),
        ]
        hood = _make_neighborhood(amenities=amenities)
        details = self.scorer.get_details(hood)
        assert "grocery" in details
        assert "mi" in details["grocery"]
