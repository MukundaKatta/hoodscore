# HoodScore - AI Neighborhood Scorer

HoodScore is an AI-powered neighborhood scoring tool that evaluates and compares
neighborhoods across multiple dimensions including safety, schools, amenities,
and walkability.

## Features

- **Safety Scoring** - Evaluate neighborhoods based on crime rate data
- **School Scoring** - Rate nearby schools by quality, distance, and type
- **Amenity Scoring** - Count and score nearby amenities (grocery, restaurants, parks, transit, hospitals)
- **Walkability Scoring** - Compute walk scores from amenity distances
- **Composite Scoring** - Weighted overall neighborhood score (0-100)
- **Neighborhood Comparison** - Side-by-side comparison of neighborhoods
- **Trend Analysis** - Track neighborhood improvement or decline over time
- **Built-in Database** - 50+ sample neighborhoods with realistic metrics

## Installation

```bash
pip install -e .
```

## Usage

### CLI

```bash
# Score a neighborhood
hoodscore score "Downtown Portland"

# Compare neighborhoods
hoodscore compare "Downtown Portland" "Pearl District"

# List all neighborhoods
hoodscore list

# Generate a full report
hoodscore report "Downtown Portland"

# Analyze trends
hoodscore trends "Downtown Portland"
```

### Python API

```python
from hoodscore.analyzer.composite import CompositeScorer
from hoodscore.database.neighborhoods import NeighborhoodDatabase

db = NeighborhoodDatabase()
scorer = CompositeScorer()

hood = db.get_neighborhood("Downtown Portland")
score = scorer.score(hood)
print(f"Overall score: {score.overall}")
```

## Scoring Methodology

Each dimension is scored on a 0-100 scale:

| Dimension   | Weight | Description                              |
|-------------|--------|------------------------------------------|
| Safety      | 30%    | Based on crime rates per 1000 residents  |
| Schools     | 25%    | School ratings, distance, and diversity  |
| Amenities   | 25%    | Count and variety of nearby amenities    |
| Walkability | 20%    | Walk score from amenity distances        |

## Dependencies

- numpy
- pydantic
- click
- rich

## Author

Mukunda Katta
