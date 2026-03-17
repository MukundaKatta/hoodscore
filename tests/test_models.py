"""Tests for HoodScore data models."""

import pytest
from pydantic import ValidationError

from hoodscore.models import (
    Amenity,
    AmenityType,
    ComparisonResult,
    CrimeCategory,
    CrimeData,
    Neighborhood,
    School,
    SchoolType,
    Score,
    TrendData,
)


class TestAmenity:
    def test_create_amenity(self):
        a = Amenity(name="Safeway", amenity_type=AmenityType.GROCERY, distance_miles=0.5)
        assert a.name == "Safeway"
        assert a.amenity_type == AmenityType.GROCERY
        assert a.distance_miles == 0.5
        assert a.rating == 3.0

    def test_amenity_negative_distance_fails(self):
        with pytest.raises(ValidationError):
            Amenity(name="X", amenity_type=AmenityType.PARK, distance_miles=-1.0)

    def test_amenity_rating_bounds(self):
        with pytest.raises(ValidationError):
            Amenity(name="X", amenity_type=AmenityType.PARK, distance_miles=1.0, rating=6.0)


class TestCrimeData:
    def test_create_crime_data(self):
        c = CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=3.5)
        assert c.category == CrimeCategory.VIOLENT
        assert c.incidents_per_1000 == 3.5
        assert c.year == 2025

    def test_negative_incidents_fails(self):
        with pytest.raises(ValidationError):
            CrimeData(category=CrimeCategory.PROPERTY, incidents_per_1000=-1.0)


class TestSchool:
    def test_create_school(self):
        s = School(name="Lincoln HS", school_type=SchoolType.HIGH, rating=8.5, distance_miles=1.0)
        assert s.name == "Lincoln HS"
        assert s.rating == 8.5

    def test_rating_out_of_range(self):
        with pytest.raises(ValidationError):
            School(name="X", school_type=SchoolType.HIGH, rating=11.0, distance_miles=1.0)


class TestNeighborhood:
    def test_create_neighborhood(self):
        n = Neighborhood(name="Test Hood", city="Portland", state="OR")
        assert n.name == "Test Hood"
        assert n.population == 10000
        assert n.amenities == []

    def test_neighborhood_with_data(self):
        n = Neighborhood(
            name="Test",
            city="Portland",
            state="OR",
            amenities=[Amenity(name="A", amenity_type=AmenityType.GROCERY, distance_miles=0.5)],
            crime_data=[CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=2.0)],
            schools=[School(name="S", school_type=SchoolType.HIGH, rating=7.0, distance_miles=1.0)],
        )
        assert len(n.amenities) == 1
        assert len(n.crime_data) == 1
        assert len(n.schools) == 1


class TestScore:
    def test_create_score(self):
        s = Score(
            neighborhood_name="Test",
            safety_score=80.0,
            school_score=70.0,
            amenity_score=60.0,
            walkability_score=50.0,
            overall=65.0,
        )
        assert s.overall == 65.0

    def test_score_out_of_range(self):
        with pytest.raises(ValidationError):
            Score(
                neighborhood_name="Test",
                safety_score=110.0,
                school_score=70.0,
                amenity_score=60.0,
                walkability_score=50.0,
                overall=65.0,
            )


class TestTrendData:
    def test_create_trend(self):
        t = TrendData(
            neighborhood_name="Test",
            years=[2020, 2021, 2022],
            scores=[60.0, 62.0, 65.0],
            direction="improving",
            annual_change=2.5,
        )
        assert t.direction == "improving"
        assert len(t.years) == 3


class TestComparisonResult:
    def test_create_comparison(self):
        score_a = Score(neighborhood_name="A", safety_score=80, school_score=70, amenity_score=60, walkability_score=50, overall=65)
        score_b = Score(neighborhood_name="B", safety_score=60, school_score=80, amenity_score=70, walkability_score=60, overall=68)
        result = ComparisonResult(neighborhood_a=score_a, neighborhood_b=score_b, winner="B")
        assert result.winner == "B"
