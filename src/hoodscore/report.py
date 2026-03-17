"""Report generation for HoodScore using Rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from hoodscore.models import ComparisonResult, Neighborhood, Score, TrendData


def _score_color(score: float) -> str:
    """Return color based on score value."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "yellow"
    elif score >= 40:
        return "dark_orange"
    else:
        return "red"


def _score_bar(score: float, width: int = 20) -> str:
    """Create a visual bar for a score."""
    filled = int(score / 100 * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


class ReportGenerator:
    """Generates rich formatted reports for neighborhoods."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def print_score(self, score: Score, neighborhood: Neighborhood | None = None) -> None:
        """Print a formatted score report."""
        table = Table(title=f"HoodScore Report: {score.neighborhood_name}", show_header=True)
        table.add_column("Dimension", style="bold")
        table.add_column("Score", justify="right")
        table.add_column("Rating", justify="center")
        table.add_column("Bar", justify="left")

        dimensions = [
            ("Safety", score.safety_score),
            ("Schools", score.school_score),
            ("Amenities", score.amenity_score),
            ("Walkability", score.walkability_score),
        ]

        for name, val in dimensions:
            color = _score_color(val)
            table.add_row(
                name,
                f"[{color}]{val:.1f}[/{color}]",
                f"[{color}]{_rating_label(val)}[/{color}]",
                f"[{color}]{_score_bar(val)}[/{color}]",
            )

        table.add_section()
        overall_color = _score_color(score.overall)
        table.add_row(
            "[bold]OVERALL[/bold]",
            f"[bold {overall_color}]{score.overall:.1f}[/bold {overall_color}]",
            f"[bold {overall_color}]{_rating_label(score.overall)}[/bold {overall_color}]",
            f"[bold {overall_color}]{_score_bar(score.overall)}[/bold {overall_color}]",
        )

        self.console.print(table)

        if neighborhood:
            self._print_neighborhood_info(neighborhood)

    def _print_neighborhood_info(self, neighborhood: Neighborhood) -> None:
        """Print neighborhood demographic info."""
        info = (
            f"City: {neighborhood.city}, {neighborhood.state}\n"
            f"Population: {neighborhood.population:,}\n"
            f"Median Income: ${neighborhood.median_income:,.0f}\n"
            f"Median Home Price: ${neighborhood.median_home_price:,.0f}\n"
            f"Schools: {len(neighborhood.schools)} | "
            f"Amenities: {len(neighborhood.amenities)}"
        )
        self.console.print(Panel(info, title="Neighborhood Info", border_style="blue"))

    def print_comparison(self, result: ComparisonResult) -> None:
        """Print a side-by-side comparison."""
        table = Table(title="Neighborhood Comparison", show_header=True)
        table.add_column("Dimension", style="bold")
        table.add_column(result.neighborhood_a.neighborhood_name, justify="right")
        table.add_column(result.neighborhood_b.neighborhood_name, justify="right")
        table.add_column("Diff", justify="right")

        dimensions = [
            ("Safety", result.neighborhood_a.safety_score, result.neighborhood_b.safety_score),
            ("Schools", result.neighborhood_a.school_score, result.neighborhood_b.school_score),
            ("Amenities", result.neighborhood_a.amenity_score, result.neighborhood_b.amenity_score),
            ("Walkability", result.neighborhood_a.walkability_score, result.neighborhood_b.walkability_score),
        ]

        for name, val_a, val_b in dimensions:
            diff = val_a - val_b
            diff_color = "green" if diff > 0 else "red" if diff < 0 else "white"
            diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
            table.add_row(
                name,
                f"[{_score_color(val_a)}]{val_a:.1f}[/{_score_color(val_a)}]",
                f"[{_score_color(val_b)}]{val_b:.1f}[/{_score_color(val_b)}]",
                f"[{diff_color}]{diff_str}[/{diff_color}]",
            )

        table.add_section()
        oa, ob = result.neighborhood_a.overall, result.neighborhood_b.overall
        diff = oa - ob
        diff_color = "green" if diff > 0 else "red" if diff < 0 else "white"
        diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
        table.add_row(
            "[bold]OVERALL[/bold]",
            f"[bold {_score_color(oa)}]{oa:.1f}[/bold {_score_color(oa)}]",
            f"[bold {_score_color(ob)}]{ob:.1f}[/bold {_score_color(ob)}]",
            f"[bold {diff_color}]{diff_str}[/bold {diff_color}]",
        )

        self.console.print(table)
        self.console.print(f"\n[bold green]Winner: {result.winner}[/bold green]")

        if result.advantages_a:
            self.console.print(f"\n[bold]{result.neighborhood_a.neighborhood_name} advantages:[/bold]")
            for adv in result.advantages_a:
                self.console.print(f"  + {adv}")

        if result.advantages_b:
            self.console.print(f"\n[bold]{result.neighborhood_b.neighborhood_name} advantages:[/bold]")
            for adv in result.advantages_b:
                self.console.print(f"  + {adv}")

    def print_trend(self, trend: TrendData) -> None:
        """Print trend analysis."""
        direction_color = {
            "improving": "green",
            "declining": "red",
            "stable": "yellow",
        }
        color = direction_color.get(trend.direction, "white")

        self.console.print(
            Panel(
                f"[bold]Direction:[/bold] [{color}]{trend.direction.upper()}[/{color}]\n"
                f"[bold]Annual Change:[/bold] [{color}]{trend.annual_change:+.2f} pts/year[/{color}]",
                title=f"Trend Analysis: {trend.neighborhood_name}",
                border_style=color,
            )
        )

        if len(trend.years) > 1:
            table = Table(title="Score History")
            table.add_column("Year", justify="right")
            table.add_column("Score", justify="right")
            for year, score_val in zip(trend.years, trend.scores):
                table.add_row(str(year), f"{score_val:.1f}")
            self.console.print(table)

    def print_list(self, neighborhoods: list[Neighborhood]) -> None:
        """Print a list of neighborhoods."""
        table = Table(title=f"Neighborhoods ({len(neighborhoods)} total)")
        table.add_column("#", justify="right", style="dim")
        table.add_column("Name", style="bold")
        table.add_column("City")
        table.add_column("State")
        table.add_column("Population", justify="right")
        table.add_column("Median Income", justify="right")

        for i, hood in enumerate(neighborhoods, 1):
            table.add_row(
                str(i),
                hood.name,
                hood.city,
                hood.state,
                f"{hood.population:,}",
                f"${hood.median_income:,.0f}",
            )

        self.console.print(table)


def _rating_label(score: float) -> str:
    """Convert numeric score to rating label."""
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Great"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Fair"
    elif score >= 50:
        return "Average"
    elif score >= 40:
        return "Below Avg"
    else:
        return "Poor"
