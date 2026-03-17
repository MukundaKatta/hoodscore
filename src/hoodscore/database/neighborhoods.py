"""Database of 50+ sample neighborhoods with realistic metrics."""

from __future__ import annotations

from hoodscore.models import (
    Amenity,
    AmenityType,
    CrimeCategory,
    CrimeData,
    Neighborhood,
    School,
    SchoolType,
)


def _make_amenities(
    grocery: list[float],
    restaurants: list[float],
    parks: list[float],
    transit: list[float],
    hospitals: list[float],
) -> list[Amenity]:
    """Helper to build amenity lists from distance lists."""
    amenities: list[Amenity] = []
    for i, d in enumerate(grocery):
        amenities.append(Amenity(name=f"Grocery {i+1}", amenity_type=AmenityType.GROCERY, distance_miles=d, rating=round(3.0 + d % 2, 1)))
    for i, d in enumerate(restaurants):
        amenities.append(Amenity(name=f"Restaurant {i+1}", amenity_type=AmenityType.RESTAURANT, distance_miles=d, rating=round(3.5 + (i % 3) * 0.5, 1)))
    for i, d in enumerate(parks):
        amenities.append(Amenity(name=f"Park {i+1}", amenity_type=AmenityType.PARK, distance_miles=d, rating=round(4.0 + (i % 2) * 0.5, 1)))
    for i, d in enumerate(transit):
        amenities.append(Amenity(name=f"Transit Stop {i+1}", amenity_type=AmenityType.TRANSIT, distance_miles=d, rating=3.5))
    for i, d in enumerate(hospitals):
        amenities.append(Amenity(name=f"Hospital {i+1}", amenity_type=AmenityType.HOSPITAL, distance_miles=d, rating=round(3.8 + (i % 3) * 0.3, 1)))
    return amenities


def _make_crime(violent: float, prop: float, drug: float, other: float) -> list[CrimeData]:
    return [
        CrimeData(category=CrimeCategory.VIOLENT, incidents_per_1000=violent),
        CrimeData(category=CrimeCategory.PROPERTY, incidents_per_1000=prop),
        CrimeData(category=CrimeCategory.DRUG, incidents_per_1000=drug),
        CrimeData(category=CrimeCategory.OTHER, incidents_per_1000=other),
    ]


def _make_schools(specs: list[tuple[str, SchoolType, float, float]]) -> list[School]:
    return [
        School(name=name, school_type=stype, rating=rating, distance_miles=dist)
        for name, stype, rating, dist in specs
    ]


def _build_neighborhoods() -> list[Neighborhood]:
    """Build the full database of sample neighborhoods."""
    hoods: list[Neighborhood] = []

    # --- Portland, OR ---
    hoods.append(Neighborhood(
        name="Downtown Portland", city="Portland", state="OR",
        population=12500, median_income=55000, median_home_price=450000,
        amenities=_make_amenities([0.2, 0.4, 0.8], [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.3, 0.6, 1.0], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3], [1.0, 2.5]),
        crime_data=_make_crime(3.5, 25.0, 6.0, 9.0),
        schools=_make_schools([("Lincoln HS", SchoolType.HIGH, 7.5, 1.0), ("Chapman ES", SchoolType.ELEMENTARY, 8.0, 0.5), ("West Sylvan MS", SchoolType.MIDDLE, 7.0, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Pearl District", city="Portland", state="OR",
        population=8000, median_income=75000, median_home_price=550000,
        amenities=_make_amenities([0.2, 0.5], [0.1, 0.15, 0.2, 0.3, 0.35, 0.4, 0.5, 0.55, 0.6, 0.7], [0.2, 0.8], [0.05, 0.1, 0.15, 0.2, 0.25], [1.5]),
        crime_data=_make_crime(2.0, 18.0, 3.0, 5.0),
        schools=_make_schools([("Emerson ES", SchoolType.ELEMENTARY, 7.0, 0.8), ("Metropolitan Learning Center", SchoolType.CHARTER, 8.5, 0.6)]),
    ))

    hoods.append(Neighborhood(
        name="Alberta Arts District", city="Portland", state="OR",
        population=9500, median_income=62000, median_home_price=480000,
        amenities=_make_amenities([0.3, 0.7, 1.2], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.2, 0.5, 0.9], [0.1, 0.2, 0.3, 0.4], [2.0]),
        crime_data=_make_crime(2.5, 15.0, 4.0, 6.0),
        schools=_make_schools([("Vernon ES", SchoolType.ELEMENTARY, 7.5, 0.4), ("Beaumont MS", SchoolType.MIDDLE, 7.0, 1.0), ("Grant HS", SchoolType.HIGH, 8.0, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Hawthorne", city="Portland", state="OR",
        population=11000, median_income=58000, median_home_price=520000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.2, 0.4, 0.7], [0.1, 0.15, 0.2, 0.3, 0.4], [1.8]),
        crime_data=_make_crime(1.8, 14.0, 3.5, 5.5),
        schools=_make_schools([("Sunnyside ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Hosford MS", SchoolType.MIDDLE, 7.5, 0.8), ("Cleveland HS", SchoolType.HIGH, 8.0, 1.2)]),
    ))

    hoods.append(Neighborhood(
        name="Sellwood-Moreland", city="Portland", state="OR",
        population=14000, median_income=72000, median_home_price=560000,
        amenities=_make_amenities([0.4, 0.8, 1.3], [0.2, 0.3, 0.5, 0.6, 0.8, 1.0], [0.1, 0.3, 0.6, 1.0], [0.2, 0.3, 0.4], [2.5]),
        crime_data=_make_crime(1.2, 10.0, 2.0, 4.0),
        schools=_make_schools([("Llewellyn ES", SchoolType.ELEMENTARY, 9.0, 0.3), ("Sellwood MS", SchoolType.MIDDLE, 8.0, 0.6), ("Cleveland HS", SchoolType.HIGH, 8.0, 1.5), ("Portland Waldorf", SchoolType.PRIVATE, 8.5, 1.0)]),
    ))

    # --- San Francisco, CA ---
    hoods.append(Neighborhood(
        name="Mission District", city="San Francisco", state="CA",
        population=60000, median_income=85000, median_home_price=1200000,
        amenities=_make_amenities([0.1, 0.3, 0.5, 0.7], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6], [0.2, 0.5, 0.8], [0.05, 0.08, 0.1, 0.12, 0.15, 0.2], [1.5, 3.0]),
        crime_data=_make_crime(5.0, 30.0, 8.0, 10.0),
        schools=_make_schools([("Buena Vista Horace Mann", SchoolType.ELEMENTARY, 6.5, 0.4), ("Everett MS", SchoolType.MIDDLE, 6.0, 0.8), ("Mission HS", SchoolType.HIGH, 6.5, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="Noe Valley", city="San Francisco", state="CA",
        population=22000, median_income=145000, median_home_price=1800000,
        amenities=_make_amenities([0.2, 0.5, 0.9], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.3, 0.6], [0.1, 0.2, 0.3, 0.4], [2.0]),
        crime_data=_make_crime(1.5, 12.0, 2.0, 4.0),
        schools=_make_schools([("Alvarado ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("James Lick MS", SchoolType.MIDDLE, 7.0, 1.0), ("SF Waldorf", SchoolType.PRIVATE, 9.0, 0.8)]),
    ))

    hoods.append(Neighborhood(
        name="Pacific Heights", city="San Francisco", state="CA",
        population=18000, median_income=190000, median_home_price=3500000,
        amenities=_make_amenities([0.3, 0.7], [0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.2, 0.4, 0.8], [0.15, 0.2, 0.3, 0.4], [1.0, 2.5]),
        crime_data=_make_crime(0.8, 8.0, 1.0, 3.0),
        schools=_make_schools([("Sherman ES", SchoolType.ELEMENTARY, 8.0, 0.5), ("Marina MS", SchoolType.MIDDLE, 7.5, 1.0), ("Sacred Heart", SchoolType.PRIVATE, 9.5, 0.6), ("Drew HS", SchoolType.HIGH, 7.0, 2.0)]),
    ))

    hoods.append(Neighborhood(
        name="SoMa", city="San Francisco", state="CA",
        population=15000, median_income=95000, median_home_price=950000,
        amenities=_make_amenities([0.3, 0.6], [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.5, 1.0], [0.05, 0.1, 0.15, 0.2, 0.25], [1.2]),
        crime_data=_make_crime(6.0, 35.0, 10.0, 12.0),
        schools=_make_schools([("Bessie Carmichael ES", SchoolType.ELEMENTARY, 5.5, 0.6)]),
    ))

    hoods.append(Neighborhood(
        name="Richmond District", city="San Francisco", state="CA",
        population=45000, median_income=78000, median_home_price=1100000,
        amenities=_make_amenities([0.2, 0.4, 0.7, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.1, 0.3], [0.1, 0.2, 0.3, 0.4, 0.5], [2.0, 3.5]),
        crime_data=_make_crime(1.8, 14.0, 3.0, 5.0),
        schools=_make_schools([("Sutro ES", SchoolType.ELEMENTARY, 7.5, 0.4), ("Presidio MS", SchoolType.MIDDLE, 7.0, 0.9), ("Washington HS", SchoolType.HIGH, 7.5, 1.0)]),
    ))

    # --- New York, NY ---
    hoods.append(Neighborhood(
        name="Upper West Side", city="New York", state="NY",
        population=210000, median_income=105000, median_home_price=1500000,
        amenities=_make_amenities([0.1, 0.2, 0.3, 0.5], [0.05, 0.1, 0.12, 0.15, 0.18, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6], [0.1, 0.2], [0.02, 0.05, 0.08, 0.1, 0.12, 0.15], [0.5, 1.5]),
        crime_data=_make_crime(2.5, 15.0, 3.0, 6.0),
        schools=_make_schools([("PS 87", SchoolType.ELEMENTARY, 9.0, 0.2), ("MS 245", SchoolType.MIDDLE, 8.0, 0.5), ("Beacon HS", SchoolType.HIGH, 9.0, 0.8), ("Trinity School", SchoolType.PRIVATE, 10.0, 0.4)]),
    ))

    hoods.append(Neighborhood(
        name="Park Slope", city="New York", state="NY",
        population=70000, median_income=115000, median_home_price=1400000,
        amenities=_make_amenities([0.1, 0.3, 0.5, 0.7], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7], [0.05, 0.1], [0.05, 0.08, 0.1, 0.15, 0.2], [1.0, 2.0]),
        crime_data=_make_crime(1.5, 10.0, 2.0, 4.0),
        schools=_make_schools([("PS 321", SchoolType.ELEMENTARY, 9.5, 0.2), ("MS 51", SchoolType.MIDDLE, 8.5, 0.5), ("Millennium Brooklyn HS", SchoolType.HIGH, 9.0, 1.0), ("Berkeley Carroll", SchoolType.PRIVATE, 9.5, 0.3)]),
    ))

    hoods.append(Neighborhood(
        name="Williamsburg", city="New York", state="NY",
        population=80000, median_income=82000, median_home_price=950000,
        amenities=_make_amenities([0.1, 0.3, 0.6], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8], [0.2, 0.5, 0.8], [0.05, 0.1, 0.15, 0.2, 0.25], [1.5, 3.0]),
        crime_data=_make_crime(3.0, 18.0, 5.0, 7.0),
        schools=_make_schools([("PS 84", SchoolType.ELEMENTARY, 7.0, 0.3), ("IS 318", SchoolType.MIDDLE, 8.0, 0.6), ("EBC HS", SchoolType.HIGH, 7.5, 1.2)]),
    ))

    hoods.append(Neighborhood(
        name="Harlem", city="New York", state="NY",
        population=120000, median_income=48000, median_home_price=650000,
        amenities=_make_amenities([0.2, 0.4, 0.7], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.2, 0.3, 0.5], [0.05, 0.1, 0.15, 0.2, 0.25], [1.0, 2.5]),
        crime_data=_make_crime(5.5, 22.0, 7.0, 9.0),
        schools=_make_schools([("PS 175", SchoolType.ELEMENTARY, 6.0, 0.3), ("Thurgood Marshall MS", SchoolType.MIDDLE, 6.5, 0.8), ("Frederick Douglass Academy", SchoolType.HIGH, 7.5, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="Greenwich Village", city="New York", state="NY",
        population=30000, median_income=125000, median_home_price=1800000,
        amenities=_make_amenities([0.1, 0.3, 0.5], [0.03, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5], [0.1, 0.2, 0.4], [0.02, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2], [0.8, 1.5]),
        crime_data=_make_crime(2.0, 12.0, 3.0, 5.0),
        schools=_make_schools([("PS 41", SchoolType.ELEMENTARY, 8.5, 0.2), ("IS 70", SchoolType.MIDDLE, 7.5, 0.5), ("Stuyvesant HS", SchoolType.HIGH, 10.0, 1.5), ("Friends Seminary", SchoolType.PRIVATE, 9.5, 0.3)]),
    ))

    # --- Chicago, IL ---
    hoods.append(Neighborhood(
        name="Lincoln Park", city="Chicago", state="IL",
        population=65000, median_income=95000, median_home_price=580000,
        amenities=_make_amenities([0.2, 0.4, 0.7, 1.0], [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.1, 0.2, 0.3, 0.5], [0.05, 0.1, 0.15, 0.2, 0.3], [1.0, 2.5]),
        crime_data=_make_crime(2.0, 18.0, 3.0, 5.0),
        schools=_make_schools([("Lincoln ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Lincoln Park MS", SchoolType.MIDDLE, 7.5, 0.8), ("Lincoln Park HS", SchoolType.HIGH, 8.5, 0.5), ("Latin School", SchoolType.PRIVATE, 9.5, 1.0)]),
    ))

    hoods.append(Neighborhood(
        name="Wicker Park", city="Chicago", state="IL",
        population=35000, median_income=78000, median_home_price=480000,
        amenities=_make_amenities([0.2, 0.5, 0.9], [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.3, 0.6], [0.05, 0.1, 0.15, 0.2, 0.25], [1.5, 3.0]),
        crime_data=_make_crime(3.5, 22.0, 5.0, 7.0),
        schools=_make_schools([("Pulaski ES", SchoolType.ELEMENTARY, 7.0, 0.5), ("Wicker Park MS", SchoolType.MIDDLE, 6.5, 0.9), ("Roberto Clemente HS", SchoolType.HIGH, 6.0, 1.2)]),
    ))

    hoods.append(Neighborhood(
        name="Hyde Park", city="Chicago", state="IL",
        population=25000, median_income=65000, median_home_price=350000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0], [0.1, 0.2, 0.5, 0.8], [0.1, 0.2, 0.3, 0.4], [0.8, 2.0]),
        crime_data=_make_crime(4.0, 20.0, 4.0, 7.0),
        schools=_make_schools([("Bret Harte ES", SchoolType.ELEMENTARY, 7.0, 0.4), ("Murray Lang MS", SchoolType.MIDDLE, 6.5, 0.7), ("Kenwood Academy", SchoolType.HIGH, 7.5, 1.0), ("U Chicago Lab", SchoolType.PRIVATE, 10.0, 0.3)]),
    ))

    hoods.append(Neighborhood(
        name="Lakeview", city="Chicago", state="IL",
        population=98000, median_income=82000, median_home_price=420000,
        amenities=_make_amenities([0.2, 0.4, 0.6, 0.9], [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7], [0.1, 0.3, 0.5], [0.05, 0.1, 0.15, 0.2, 0.25], [1.2, 2.8]),
        crime_data=_make_crime(2.5, 20.0, 4.0, 6.0),
        schools=_make_schools([("Nettlehorst ES", SchoolType.ELEMENTARY, 8.0, 0.3), ("Lake View MS", SchoolType.MIDDLE, 7.0, 0.7), ("Lake View HS", SchoolType.HIGH, 7.0, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="Logan Square", city="Chicago", state="IL",
        population=73000, median_income=62000, median_home_price=380000,
        amenities=_make_amenities([0.3, 0.6, 1.1], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.2, 0.4, 0.7], [0.05, 0.1, 0.2, 0.3], [2.0, 3.5]),
        crime_data=_make_crime(3.0, 19.0, 5.0, 7.0),
        schools=_make_schools([("Brentano ES", SchoolType.ELEMENTARY, 7.0, 0.4), ("Palmer ES", SchoolType.ELEMENTARY, 7.5, 0.6), ("Logan Square MS", SchoolType.MIDDLE, 6.5, 1.0)]),
    ))

    # --- Austin, TX ---
    hoods.append(Neighborhood(
        name="Downtown Austin", city="Austin", state="TX",
        population=12000, median_income=72000, median_home_price=550000,
        amenities=_make_amenities([0.2, 0.5, 0.8], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8], [0.3, 0.5], [0.1, 0.15, 0.2, 0.3, 0.4], [1.0, 2.0]),
        crime_data=_make_crime(4.5, 28.0, 6.0, 9.0),
        schools=_make_schools([("Mathews ES", SchoolType.ELEMENTARY, 6.5, 1.0), ("Kealing MS", SchoolType.MIDDLE, 8.0, 1.5), ("Austin HS", SchoolType.HIGH, 7.0, 2.0)]),
    ))

    hoods.append(Neighborhood(
        name="South Congress", city="Austin", state="TX",
        population=15000, median_income=68000, median_home_price=620000,
        amenities=_make_amenities([0.3, 0.7, 1.2], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.2, 0.5, 0.8], [0.15, 0.2, 0.3, 0.4], [1.5, 3.0]),
        crime_data=_make_crime(3.0, 20.0, 4.0, 6.0),
        schools=_make_schools([("Becker ES", SchoolType.ELEMENTARY, 7.0, 0.5), ("Fulmore MS", SchoolType.MIDDLE, 7.0, 1.0), ("Travis HS", SchoolType.HIGH, 7.5, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Mueller", city="Austin", state="TX",
        population=10000, median_income=92000, median_home_price=500000,
        amenities=_make_amenities([0.3, 0.6], [0.2, 0.3, 0.5, 0.6, 0.8], [0.1, 0.2, 0.4, 0.6], [0.2, 0.3, 0.4], [1.0, 2.5]),
        crime_data=_make_crime(1.0, 8.0, 1.5, 3.0),
        schools=_make_schools([("Mueller ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Martin MS", SchoolType.MIDDLE, 7.5, 1.0), ("LBJ HS", SchoolType.HIGH, 7.0, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="East Austin", city="Austin", state="TX",
        population=30000, median_income=52000, median_home_price=420000,
        amenities=_make_amenities([0.4, 0.8, 1.5], [0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0], [0.3, 0.6, 1.0], [0.15, 0.25, 0.35, 0.45], [2.0]),
        crime_data=_make_crime(4.0, 22.0, 6.0, 8.0),
        schools=_make_schools([("Sanchez ES", SchoolType.ELEMENTARY, 6.0, 0.5), ("Martin MS", SchoolType.MIDDLE, 6.5, 1.0), ("Eastside Memorial HS", SchoolType.HIGH, 5.5, 1.2)]),
    ))

    # --- Denver, CO ---
    hoods.append(Neighborhood(
        name="LoDo Denver", city="Denver", state="CO",
        population=10000, median_income=88000, median_home_price=520000,
        amenities=_make_amenities([0.2, 0.5], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7], [0.3, 0.5], [0.05, 0.1, 0.15, 0.2, 0.25], [1.0, 2.0]),
        crime_data=_make_crime(4.0, 30.0, 7.0, 10.0),
        schools=_make_schools([("Greenlee ES", SchoolType.ELEMENTARY, 6.0, 1.0), ("Morey MS", SchoolType.MIDDLE, 6.5, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Capitol Hill Denver", city="Denver", state="CO",
        population=18000, median_income=55000, median_home_price=380000,
        amenities=_make_amenities([0.2, 0.4, 0.7], [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7], [0.1, 0.3, 0.5], [0.05, 0.1, 0.15, 0.2, 0.25], [1.0, 2.5]),
        crime_data=_make_crime(5.0, 32.0, 8.0, 11.0),
        schools=_make_schools([("Dora Moore ES", SchoolType.ELEMENTARY, 7.0, 0.5), ("Morey MS", SchoolType.MIDDLE, 6.5, 0.8), ("East HS", SchoolType.HIGH, 8.0, 1.0)]),
    ))

    hoods.append(Neighborhood(
        name="Highlands Denver", city="Denver", state="CO",
        population=22000, median_income=85000, median_home_price=620000,
        amenities=_make_amenities([0.2, 0.5, 0.8], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.2, 0.4, 0.6], [0.1, 0.15, 0.2, 0.3], [1.5, 3.0]),
        crime_data=_make_crime(2.0, 15.0, 3.0, 5.0),
        schools=_make_schools([("Centennial ES", SchoolType.ELEMENTARY, 8.0, 0.4), ("Skinner MS", SchoolType.MIDDLE, 7.5, 0.8), ("North HS", SchoolType.HIGH, 7.0, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Washington Park Denver", city="Denver", state="CO",
        population=16000, median_income=95000, median_home_price=700000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.2, 0.3, 0.4, 0.5, 0.6, 0.8], [0.05, 0.1, 0.2, 0.4], [0.1, 0.2, 0.3, 0.4], [1.5, 2.5]),
        crime_data=_make_crime(1.5, 12.0, 2.0, 4.0),
        schools=_make_schools([("Steele ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Grant MS", SchoolType.MIDDLE, 7.5, 0.7), ("South HS", SchoolType.HIGH, 8.0, 1.0), ("Denver Academy", SchoolType.PRIVATE, 9.0, 0.5)]),
    ))

    # --- Seattle, WA ---
    hoods.append(Neighborhood(
        name="Capitol Hill Seattle", city="Seattle", state="WA",
        population=35000, median_income=78000, median_home_price=620000,
        amenities=_make_amenities([0.1, 0.3, 0.5, 0.8], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.4], [0.03, 0.05, 0.08, 0.1, 0.15, 0.2], [0.8, 2.0]),
        crime_data=_make_crime(3.5, 25.0, 5.0, 8.0),
        schools=_make_schools([("Stevens ES", SchoolType.ELEMENTARY, 7.5, 0.4), ("Meany MS", SchoolType.MIDDLE, 7.0, 0.8), ("Garfield HS", SchoolType.HIGH, 8.5, 1.0)]),
    ))

    hoods.append(Neighborhood(
        name="Ballard", city="Seattle", state="WA",
        population=50000, median_income=92000, median_home_price=720000,
        amenities=_make_amenities([0.2, 0.4, 0.7], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.2, 0.3, 0.5], [0.1, 0.15, 0.2, 0.3, 0.4], [2.0, 3.5]),
        crime_data=_make_crime(1.8, 16.0, 3.0, 5.0),
        schools=_make_schools([("Salmon Bay ES", SchoolType.ELEMENTARY, 8.0, 0.4), ("Whitman MS", SchoolType.MIDDLE, 7.5, 0.8), ("Ballard HS", SchoolType.HIGH, 8.0, 0.6)]),
    ))

    hoods.append(Neighborhood(
        name="Fremont", city="Seattle", state="WA",
        population=15000, median_income=88000, median_home_price=680000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.2, 0.4, 0.7], [0.1, 0.15, 0.2, 0.3], [2.0, 3.0]),
        crime_data=_make_crime(1.5, 14.0, 2.5, 4.5),
        schools=_make_schools([("BF Day ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Hamilton MS", SchoolType.MIDDLE, 8.0, 0.7), ("Lincoln HS", SchoolType.HIGH, 7.5, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Queen Anne", city="Seattle", state="WA",
        population=28000, median_income=95000, median_home_price=750000,
        amenities=_make_amenities([0.3, 0.5, 0.8], [0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.1, 0.3, 0.5], [0.1, 0.15, 0.2, 0.3, 0.4], [1.0, 2.5]),
        crime_data=_make_crime(1.2, 12.0, 2.0, 4.0),
        schools=_make_schools([("Coe ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("McClure MS", SchoolType.MIDDLE, 8.0, 0.6), ("Rainier Beach HS", SchoolType.HIGH, 6.5, 2.0), ("Northwest School", SchoolType.PRIVATE, 9.0, 1.0)]),
    ))

    # --- Boston, MA ---
    hoods.append(Neighborhood(
        name="Back Bay", city="Boston", state="MA",
        population=26000, median_income=120000, median_home_price=1200000,
        amenities=_make_amenities([0.1, 0.3, 0.5], [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6], [0.1, 0.2, 0.3], [0.03, 0.05, 0.08, 0.1, 0.12, 0.15], [0.5, 1.5]),
        crime_data=_make_crime(2.0, 16.0, 3.0, 5.0),
        schools=_make_schools([("Kingsley ES", SchoolType.ELEMENTARY, 7.5, 0.5), ("Timilty MS", SchoolType.MIDDLE, 7.0, 1.0), ("Boston Latin", SchoolType.HIGH, 9.5, 1.5), ("Winsor School", SchoolType.PRIVATE, 9.5, 0.8)]),
    ))

    hoods.append(Neighborhood(
        name="Cambridge", city="Boston", state="MA",
        population=118000, median_income=98000, median_home_price=950000,
        amenities=_make_amenities([0.2, 0.4, 0.6, 0.9], [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7], [0.1, 0.2, 0.4, 0.6], [0.05, 0.08, 0.1, 0.15, 0.2, 0.25], [0.8, 2.0]),
        crime_data=_make_crime(1.8, 14.0, 2.5, 5.0),
        schools=_make_schools([("Cambridge ES", SchoolType.ELEMENTARY, 8.0, 0.3), ("Cambridge MS", SchoolType.MIDDLE, 8.0, 0.7), ("Cambridge Rindge & Latin", SchoolType.HIGH, 8.0, 1.0), ("Buckingham Browne", SchoolType.PRIVATE, 9.5, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="South End Boston", city="Boston", state="MA",
        population=30000, median_income=88000, median_home_price=850000,
        amenities=_make_amenities([0.2, 0.4, 0.7], [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.2, 0.4, 0.6], [0.05, 0.1, 0.15, 0.2, 0.25], [0.8, 2.0]),
        crime_data=_make_crime(3.0, 20.0, 4.0, 7.0),
        schools=_make_schools([("Hurley ES", SchoolType.ELEMENTARY, 7.0, 0.4), ("Blackstone ES", SchoolType.ELEMENTARY, 7.5, 0.6), ("Timilty MS", SchoolType.MIDDLE, 7.0, 0.8)]),
    ))

    hoods.append(Neighborhood(
        name="Beacon Hill", city="Boston", state="MA",
        population=10000, median_income=135000, median_home_price=1500000,
        amenities=_make_amenities([0.2, 0.4], [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6], [0.05, 0.1, 0.2], [0.05, 0.08, 0.1, 0.15, 0.2], [0.5, 1.5]),
        crime_data=_make_crime(1.5, 12.0, 2.0, 4.0),
        schools=_make_schools([("Eliot ES", SchoolType.ELEMENTARY, 8.0, 0.3), ("Advent School", SchoolType.PRIVATE, 9.0, 0.2)]),
    ))

    # --- Nashville, TN ---
    hoods.append(Neighborhood(
        name="East Nashville", city="Nashville", state="TN",
        population=40000, median_income=62000, median_home_price=420000,
        amenities=_make_amenities([0.3, 0.7, 1.2], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.2, 0.4, 0.7], [0.2, 0.3, 0.4, 0.5], [2.0, 3.5]),
        crime_data=_make_crime(3.5, 22.0, 5.0, 7.0),
        schools=_make_schools([("Lockeland ES", SchoolType.ELEMENTARY, 7.5, 0.4), ("Bailey MS", SchoolType.MIDDLE, 6.5, 1.0), ("Maplewood HS", SchoolType.HIGH, 6.0, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="The Gulch Nashville", city="Nashville", state="TN",
        population=8000, median_income=82000, median_home_price=550000,
        amenities=_make_amenities([0.3, 0.6], [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7], [0.4, 0.8], [0.1, 0.15, 0.2, 0.3], [1.5, 2.5]),
        crime_data=_make_crime(3.0, 25.0, 4.0, 7.0),
        schools=_make_schools([("Eakin ES", SchoolType.ELEMENTARY, 7.0, 1.0), ("West End MS", SchoolType.MIDDLE, 6.5, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Germantown Nashville", city="Nashville", state="TN",
        population=5000, median_income=75000, median_home_price=480000,
        amenities=_make_amenities([0.3, 0.5, 0.9], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.2, 0.4], [0.15, 0.2, 0.3, 0.4], [1.5, 3.0]),
        crime_data=_make_crime(3.0, 20.0, 4.0, 6.0),
        schools=_make_schools([("Buena Vista ES", SchoolType.ELEMENTARY, 6.5, 0.5), ("Hume-Fogg HS", SchoolType.HIGH, 8.5, 1.5), ("MLK MS", SchoolType.MIDDLE, 6.0, 1.0)]),
    ))

    # --- Minneapolis, MN ---
    hoods.append(Neighborhood(
        name="Uptown Minneapolis", city="Minneapolis", state="MN",
        population=35000, median_income=58000, median_home_price=320000,
        amenities=_make_amenities([0.2, 0.4, 0.7], [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.3, 0.5], [0.1, 0.15, 0.2, 0.25, 0.3], [1.5, 3.0]),
        crime_data=_make_crime(4.0, 28.0, 6.0, 8.0),
        schools=_make_schools([("Whittier ES", SchoolType.ELEMENTARY, 7.0, 0.5), ("Ramsey MS", SchoolType.MIDDLE, 6.5, 0.8), ("South HS", SchoolType.HIGH, 7.0, 1.0)]),
    ))

    hoods.append(Neighborhood(
        name="Northeast Minneapolis", city="Minneapolis", state="MN",
        population=30000, median_income=55000, median_home_price=290000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.8, 0.9], [0.2, 0.4, 0.6], [0.1, 0.2, 0.3, 0.4], [2.0, 3.5]),
        crime_data=_make_crime(3.5, 22.0, 5.0, 7.0),
        schools=_make_schools([("Waite Park ES", SchoolType.ELEMENTARY, 7.0, 0.4), ("Northeast MS", SchoolType.MIDDLE, 6.5, 0.9), ("Edison HS", SchoolType.HIGH, 6.5, 1.0)]),
    ))

    # --- Miami, FL ---
    hoods.append(Neighborhood(
        name="Coconut Grove", city="Miami", state="FL",
        population=20000, median_income=85000, median_home_price=780000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.3, 0.5], [0.2, 0.3, 0.4, 0.5], [1.5, 3.0]),
        crime_data=_make_crime(2.5, 18.0, 3.5, 5.5),
        schools=_make_schools([("Coconut Grove ES", SchoolType.ELEMENTARY, 7.5, 0.4), ("Ponce MS", SchoolType.MIDDLE, 7.0, 0.8), ("Coral Gables HS", SchoolType.HIGH, 8.0, 1.5), ("Ransom Everglades", SchoolType.PRIVATE, 9.5, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="Wynwood", city="Miami", state="FL",
        population=8000, median_income=45000, median_home_price=420000,
        amenities=_make_amenities([0.4, 0.8], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.3, 0.6], [0.15, 0.2, 0.3, 0.4], [2.0, 3.5]),
        crime_data=_make_crime(5.0, 30.0, 8.0, 10.0),
        schools=_make_schools([("Phillis Wheatley ES", SchoolType.ELEMENTARY, 5.5, 0.5), ("Jose de Diego MS", SchoolType.MIDDLE, 5.0, 1.0)]),
    ))

    hoods.append(Neighborhood(
        name="Coral Gables", city="Miami", state="FL",
        population=50000, median_income=105000, median_home_price=900000,
        amenities=_make_amenities([0.2, 0.5, 0.8, 1.2], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.2, 0.3, 0.5, 0.7], [0.15, 0.2, 0.3, 0.4, 0.5], [1.0, 2.5]),
        crime_data=_make_crime(1.5, 12.0, 2.0, 4.0),
        schools=_make_schools([("Coral Gables ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Ponce MS", SchoolType.MIDDLE, 8.0, 0.7), ("Coral Gables HS", SchoolType.HIGH, 8.5, 1.0), ("Gulliver Prep", SchoolType.PRIVATE, 9.0, 1.5)]),
    ))

    # --- Philadelphia, PA ---
    hoods.append(Neighborhood(
        name="Rittenhouse Square", city="Philadelphia", state="PA",
        population=20000, median_income=95000, median_home_price=550000,
        amenities=_make_amenities([0.1, 0.2, 0.4, 0.6], [0.05, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7], [0.05, 0.1, 0.3], [0.05, 0.08, 0.1, 0.15, 0.2, 0.25], [0.5, 1.5]),
        crime_data=_make_crime(2.5, 18.0, 3.0, 6.0),
        schools=_make_schools([("Greenfield ES", SchoolType.ELEMENTARY, 8.0, 0.4), ("Science Leadership Academy", SchoolType.CHARTER, 9.0, 0.8), ("Central HS", SchoolType.HIGH, 9.5, 1.0), ("Friends Select", SchoolType.PRIVATE, 9.0, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="Fishtown", city="Philadelphia", state="PA",
        population=18000, median_income=62000, median_home_price=380000,
        amenities=_make_amenities([0.2, 0.5, 0.8], [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [0.3, 0.5, 0.8], [0.1, 0.15, 0.2, 0.3], [1.5, 3.0]),
        crime_data=_make_crime(3.5, 22.0, 5.0, 8.0),
        schools=_make_schools([("Adaire ES", SchoolType.ELEMENTARY, 6.5, 0.4), ("Masterman MS", SchoolType.MIDDLE, 9.0, 1.5), ("Frankford HS", SchoolType.HIGH, 5.5, 1.0)]),
    ))

    # --- Phoenix, AZ ---
    hoods.append(Neighborhood(
        name="Scottsdale Old Town", city="Scottsdale", state="AZ",
        population=15000, median_income=85000, median_home_price=550000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.3, 0.5, 0.8], [0.2, 0.3, 0.4, 0.5], [1.5, 3.0]),
        crime_data=_make_crime(2.0, 18.0, 3.0, 5.0),
        schools=_make_schools([("Tavan ES", SchoolType.ELEMENTARY, 7.5, 0.5), ("Cocopah MS", SchoolType.MIDDLE, 7.0, 1.0), ("Scottsdale HS", SchoolType.HIGH, 7.5, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="Arcadia Phoenix", city="Phoenix", state="AZ",
        population=25000, median_income=110000, median_home_price=850000,
        amenities=_make_amenities([0.3, 0.6, 1.0, 1.5], [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0], [0.2, 0.4, 0.7], [0.3, 0.4, 0.5, 0.6], [1.5, 3.0]),
        crime_data=_make_crime(1.0, 10.0, 1.5, 3.0),
        schools=_make_schools([("Hopi ES", SchoolType.ELEMENTARY, 9.0, 0.4), ("Ingleside MS", SchoolType.MIDDLE, 8.5, 0.8), ("Arcadia HS", SchoolType.HIGH, 8.5, 1.0), ("Phoenix Country Day", SchoolType.PRIVATE, 9.5, 1.5)]),
    ))

    # --- Atlanta, GA ---
    hoods.append(Neighborhood(
        name="Midtown Atlanta", city="Atlanta", state="GA",
        population=30000, median_income=78000, median_home_price=450000,
        amenities=_make_amenities([0.2, 0.4, 0.7], [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.3], [0.05, 0.1, 0.15, 0.2, 0.25], [1.0, 2.0]),
        crime_data=_make_crime(4.0, 28.0, 5.0, 8.0),
        schools=_make_schools([("Morningside ES", SchoolType.ELEMENTARY, 8.0, 0.5), ("Inman MS", SchoolType.MIDDLE, 8.0, 0.8), ("Grady HS", SchoolType.HIGH, 7.5, 1.0)]),
    ))

    hoods.append(Neighborhood(
        name="Virginia-Highland", city="Atlanta", state="GA",
        population=12000, median_income=92000, median_home_price=650000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.1, 0.2, 0.4, 0.6], [0.15, 0.2, 0.3, 0.4], [1.5, 3.0]),
        crime_data=_make_crime(2.0, 15.0, 2.5, 5.0),
        schools=_make_schools([("Morningside ES", SchoolType.ELEMENTARY, 8.0, 0.3), ("Inman MS", SchoolType.MIDDLE, 8.0, 0.6), ("Grady HS", SchoolType.HIGH, 7.5, 1.2), ("Paideia School", SchoolType.PRIVATE, 9.5, 0.5)]),
    ))

    hoods.append(Neighborhood(
        name="Decatur", city="Atlanta", state="GA",
        population=24000, median_income=82000, median_home_price=520000,
        amenities=_make_amenities([0.2, 0.5, 0.8, 1.2], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.3, 0.5, 0.7], [0.1, 0.15, 0.2, 0.3, 0.4], [1.5, 2.5]),
        crime_data=_make_crime(1.8, 14.0, 2.5, 4.5),
        schools=_make_schools([("Oakhurst ES", SchoolType.ELEMENTARY, 8.5, 0.3), ("Renfroe MS", SchoolType.MIDDLE, 8.0, 0.7), ("Decatur HS", SchoolType.HIGH, 8.5, 0.9), ("Friends School", SchoolType.PRIVATE, 9.0, 0.5)]),
    ))

    # --- Raleigh, NC ---
    hoods.append(Neighborhood(
        name="Downtown Raleigh", city="Raleigh", state="NC",
        population=12000, median_income=65000, median_home_price=380000,
        amenities=_make_amenities([0.3, 0.6, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.2, 0.4], [0.1, 0.15, 0.2, 0.3, 0.4], [1.0, 2.5]),
        crime_data=_make_crime(3.5, 25.0, 5.0, 8.0),
        schools=_make_schools([("Moore Square ES", SchoolType.ELEMENTARY, 7.0, 0.5), ("Ligon MS", SchoolType.MIDDLE, 8.0, 1.0), ("Broughton HS", SchoolType.HIGH, 8.5, 1.5)]),
    ))

    hoods.append(Neighborhood(
        name="North Hills Raleigh", city="Raleigh", state="NC",
        population=18000, median_income=95000, median_home_price=520000,
        amenities=_make_amenities([0.2, 0.4, 0.7, 1.0], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.2, 0.4, 0.6], [0.15, 0.2, 0.3, 0.4], [1.5, 3.0]),
        crime_data=_make_crime(1.5, 12.0, 2.0, 4.0),
        schools=_make_schools([("Sanderson HS", SchoolType.HIGH, 8.0, 1.0), ("Carroll MS", SchoolType.MIDDLE, 7.5, 0.8), ("Wiley ES", SchoolType.ELEMENTARY, 8.0, 0.4)]),
    ))

    # --- Salt Lake City, UT ---
    hoods.append(Neighborhood(
        name="Sugar House SLC", city="Salt Lake City", state="UT",
        population=20000, median_income=55000, median_home_price=420000,
        amenities=_make_amenities([0.2, 0.5, 0.8], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], [0.1, 0.2, 0.3, 0.5], [0.1, 0.15, 0.2, 0.3, 0.4], [1.5, 3.0]),
        crime_data=_make_crime(2.5, 20.0, 4.0, 6.0),
        schools=_make_schools([("Hawthorne ES", SchoolType.ELEMENTARY, 7.5, 0.3), ("Highland HS", SchoolType.HIGH, 7.5, 0.8), ("Clayton MS", SchoolType.MIDDLE, 7.0, 0.6)]),
    ))

    hoods.append(Neighborhood(
        name="The Avenues SLC", city="Salt Lake City", state="UT",
        population=15000, median_income=68000, median_home_price=520000,
        amenities=_make_amenities([0.3, 0.6], [0.2, 0.3, 0.4, 0.5, 0.6, 0.7], [0.1, 0.2, 0.4], [0.15, 0.2, 0.3, 0.4], [0.8, 2.0]),
        crime_data=_make_crime(2.0, 16.0, 3.0, 5.0),
        schools=_make_schools([("Ensign ES", SchoolType.ELEMENTARY, 8.0, 0.3), ("Bryant MS", SchoolType.MIDDLE, 7.5, 0.7), ("East HS", SchoolType.HIGH, 8.0, 1.0)]),
    ))

    return hoods


class NeighborhoodDatabase:
    """In-memory database of sample neighborhoods with metrics.

    Contains 50+ neighborhoods across major US cities with realistic
    crime, school, amenity, and demographic data.
    """

    def __init__(self) -> None:
        self._neighborhoods: dict[str, Neighborhood] = {}
        for hood in _build_neighborhoods():
            self._neighborhoods[hood.name.lower()] = hood

    @property
    def count(self) -> int:
        """Return total number of neighborhoods in the database."""
        return len(self._neighborhoods)

    def get_neighborhood(self, name: str) -> Neighborhood | None:
        """Look up a neighborhood by name (case-insensitive)."""
        return self._neighborhoods.get(name.lower())

    def search(self, query: str) -> list[Neighborhood]:
        """Search neighborhoods by partial name match."""
        query_lower = query.lower()
        return [
            hood
            for key, hood in self._neighborhoods.items()
            if query_lower in key
        ]

    def list_all(self) -> list[Neighborhood]:
        """Return all neighborhoods sorted by name."""
        return sorted(self._neighborhoods.values(), key=lambda n: n.name)

    def list_by_city(self, city: str) -> list[Neighborhood]:
        """Return neighborhoods in a given city."""
        city_lower = city.lower()
        return [
            hood
            for hood in self._neighborhoods.values()
            if hood.city.lower() == city_lower
        ]

    def list_by_state(self, state: str) -> list[Neighborhood]:
        """Return neighborhoods in a given state."""
        state_upper = state.upper()
        return [
            hood
            for hood in self._neighborhoods.values()
            if hood.state.upper() == state_upper
        ]

    def list_cities(self) -> list[str]:
        """Return sorted list of unique cities."""
        return sorted({hood.city for hood in self._neighborhoods.values()})
