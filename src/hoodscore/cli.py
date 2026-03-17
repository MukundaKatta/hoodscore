"""CLI interface for HoodScore using Click."""

from __future__ import annotations

import click
from rich.console import Console

from hoodscore.analyzer.comparator import NeighborhoodComparator
from hoodscore.analyzer.composite import CompositeScorer
from hoodscore.database.neighborhoods import NeighborhoodDatabase
from hoodscore.report import ReportGenerator

console = Console()
db = NeighborhoodDatabase()
scorer = CompositeScorer()
reporter = ReportGenerator(console)


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """HoodScore - AI Neighborhood Scorer.

    Evaluate and compare neighborhoods across safety, schools,
    amenities, and walkability dimensions.
    """


@cli.command()
@click.argument("name")
def score(name: str) -> None:
    """Score a neighborhood by name."""
    hood = db.get_neighborhood(name)
    if hood is None:
        results = db.search(name)
        if results:
            console.print(f"[yellow]'{name}' not found. Did you mean:[/yellow]")
            for r in results:
                console.print(f"  - {r.name}")
        else:
            console.print(f"[red]Neighborhood '{name}' not found.[/red]")
        return

    result = scorer.score(hood)
    reporter.print_score(result, hood)


@cli.command()
@click.argument("name_a")
@click.argument("name_b")
def compare(name_a: str, name_b: str) -> None:
    """Compare two neighborhoods side by side."""
    hood_a = db.get_neighborhood(name_a)
    hood_b = db.get_neighborhood(name_b)

    if hood_a is None:
        console.print(f"[red]Neighborhood '{name_a}' not found.[/red]")
        return
    if hood_b is None:
        console.print(f"[red]Neighborhood '{name_b}' not found.[/red]")
        return

    comparator = NeighborhoodComparator(scorer)
    result = comparator.compare(hood_a, hood_b)
    reporter.print_comparison(result)


@cli.command(name="list")
@click.option("--city", default=None, help="Filter by city name")
@click.option("--state", default=None, help="Filter by state abbreviation")
def list_neighborhoods(city: str | None, state: str | None) -> None:
    """List all neighborhoods in the database."""
    if city:
        hoods = db.list_by_city(city)
    elif state:
        hoods = db.list_by_state(state)
    else:
        hoods = db.list_all()

    if not hoods:
        console.print("[yellow]No neighborhoods found.[/yellow]")
        return

    reporter.print_list(hoods)


@cli.command()
@click.argument("name")
def report(name: str) -> None:
    """Generate a full report for a neighborhood."""
    hood = db.get_neighborhood(name)
    if hood is None:
        console.print(f"[red]Neighborhood '{name}' not found.[/red]")
        return

    result = scorer.score(hood)
    reporter.print_score(result, hood)


@cli.command()
@click.argument("name")
def trends(name: str) -> None:
    """Analyze trends for a neighborhood (simulated multi-year data)."""
    from hoodscore.analyzer.trends import TrendAnalyzer
    from hoodscore.models import Neighborhood

    hood = db.get_neighborhood(name)
    if hood is None:
        console.print(f"[red]Neighborhood '{name}' not found.[/red]")
        return

    # Create simulated historical snapshots
    snapshots: list[Neighborhood] = []
    for year_offset in range(-4, 1):
        year = hood.year + year_offset
        snapshot = hood.model_copy(deep=True)
        snapshot.year = year
        # Simulate slight changes in crime data over time
        for crime in snapshot.crime_data:
            factor = 1.0 + year_offset * 0.03  # 3% change per year
            crime.incidents_per_1000 = max(0.1, crime.incidents_per_1000 * factor)
        snapshots.append(snapshot)

    analyzer = TrendAnalyzer()
    trend = analyzer.analyze(snapshots)
    reporter.print_trend(trend)

    projections = analyzer.project(trend)
    if projections:
        console.print("\n[bold]5-Year Projections:[/bold]")
        for year, proj_score in projections:
            console.print(f"  {year}: {proj_score:.1f}")


if __name__ == "__main__":
    cli()
