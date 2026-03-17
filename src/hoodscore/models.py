"""Data models for HoodScore."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AmenityType(str, Enum):
    """Types of amenities tracked."""

    GROCERY = "grocery"
    RESTAURANT = "restaurant"
    PARK = "park"
    TRANSIT = "transit"
    HOSPITAL = "hospital"


class CrimeCategory(str, Enum):
    """Categories of crime data."""

    VIOLENT = "violent"
    PROPERTY = "property"
    DRUG = "drug"
    OTHER = "other"


class SchoolType(str, Enum):
    """Types of schools."""

    ELEMENTARY = "elementary"
    MIDDLE = "middle"
    HIGH = "high"
    PRIVATE = "private"
    CHARTER = "charter"


class Amenity(BaseModel):
    """An amenity near a neighborhood."""

    name: str
    amenity_type: AmenityType
    distance_miles: float = Field(ge=0, description="Distance in miles from neighborhood center")
    rating: float = Field(ge=0, le=5, default=3.0, description="Rating out of 5")


class CrimeData(BaseModel):
    """Crime statistics for a neighborhood."""

    category: CrimeCategory
    incidents_per_1000: float = Field(ge=0, description="Incidents per 1000 residents per year")
    year: int = Field(default=2025)
    trend: float = Field(
        default=0.0,
        description="Year-over-year change as fraction (-0.1 = 10% decrease)",
    )


class School(BaseModel):
    """A school near the neighborhood."""

    name: str
    school_type: SchoolType
    rating: float = Field(ge=0, le=10, description="Rating out of 10")
    distance_miles: float = Field(ge=0)
    student_teacher_ratio: float = Field(ge=0, default=15.0)


class Neighborhood(BaseModel):
    """A neighborhood with all its data."""

    name: str
    city: str
    state: str
    population: int = Field(ge=0, default=10000)
    median_income: float = Field(ge=0, default=50000.0)
    median_home_price: float = Field(ge=0, default=300000.0)
    amenities: list[Amenity] = Field(default_factory=list)
    crime_data: list[CrimeData] = Field(default_factory=list)
    schools: list[School] = Field(default_factory=list)
    year: int = Field(default=2025)


class Score(BaseModel):
    """A score result for a neighborhood."""

    neighborhood_name: str
    safety_score: float = Field(ge=0, le=100)
    school_score: float = Field(ge=0, le=100)
    amenity_score: float = Field(ge=0, le=100)
    walkability_score: float = Field(ge=0, le=100)
    overall: float = Field(ge=0, le=100)
    details: dict[str, str] = Field(default_factory=dict)


class TrendData(BaseModel):
    """Trend data for a neighborhood over time."""

    neighborhood_name: str
    years: list[int]
    scores: list[float]
    direction: str = Field(description="improving, declining, or stable")
    annual_change: float = Field(description="Average annual score change")


class ComparisonResult(BaseModel):
    """Result of comparing two neighborhoods."""

    neighborhood_a: Score
    neighborhood_b: Score
    winner: str
    advantages_a: list[str] = Field(default_factory=list)
    advantages_b: list[str] = Field(default_factory=list)
