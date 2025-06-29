"""Command-line interface for FixtureGPT."""

import os
import typer
import json
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .main import get_fixture_stats, diff_fixture

app = typer.Typer(
    name="fixturegpt",
    help="FixtureGPT - Record and replay expensive outputs for AI/LLM development"
)
console = Console()


@app.command()
def stats():
    """Show statistics about saved fixtures."""
    stats_data = get_fixture_stats()
    
    # Cloud sync configuration
    api_key = os.getenv('FIXTUREGPT_API_KEY')
    sync_mode = os.getenv('FIXTUREGPT_SYNC_MODE', 'local')
    api_url = os.getenv('FIXTUREGPT_API_URL', 'https://app.fixturegpt.com')
    
    # Cloud sync status panel
    if api_key:
        cloud_status = f"""
☁️  Cloud Sync: [green]ENABLED[/green]
🔑 API Key: [dim]{api_key[:12]}...[/dim]
🔄 Sync Mode: [cyan]{sync_mode}[/cyan]
🌐 Dashboard: [link]{api_url}[/link]
        """
    else:
        cloud_status = f"""
☁️  Cloud Sync: [red]DISABLED[/red]
💡 Enable with: export FIXTUREGPT_API_KEY='your-key'
🌐 Get API key: [link]https://app.fixturegpt.com/dashboard/api-keys[/link]
        """
    
    console.print(Panel(cloud_status.strip(), title="Cloud Sync Status", border_style="blue"))
    
    if stats_data["count"] == 0:
        console.print("📭 No local fixtures found.", style="yellow")
        if api_key and sync_mode in ['cloud', 'both']:
            console.print("💡 You may have fixtures in the cloud dashboard.", style="dim")
        return
    
    # Create summary panel
    summary = f"""
📊 Local Fixtures: {stats_data['count']}
💾 Total Size: {stats_data['total_size']:,} bytes ({stats_data['total_size'] / 1024:.1f} KB)
    """
    console.print(Panel(summary.strip(), title="Local Fixture Stats", border_style="green"))
    
    # Create table of fixtures
    table = Table(title="Local Fixture Details")
    table.add_column("Name", style="cyan")
    table.add_column("Filename", style="magenta")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Timestamp", style="dim")
    
    for fixture in stats_data["fixtures"]:
        size_kb = fixture["size"] / 1024
        table.add_row(
            fixture["name"],
            fixture["filename"],
            f"{size_kb:.1f} KB",
            fixture["timestamp"][:19] if fixture["timestamp"] != "unknown" else "unknown"
        )
    
    console.print(table)
    
    # Estimate cost savings (bonus feature)
    estimated_calls = stats_data["count"]
    if estimated_calls > 0:
        # Rough estimates - these would be more accurate with actual API pricing
        estimated_cost_per_call = 0.002  # ~$0.002 per call (rough GPT-3.5 estimate)
        total_saved = estimated_calls * estimated_cost_per_call
        
        savings_panel = f"""
💰 Estimated Cost Savings: ${total_saved:.3f}
🔄 API Calls Avoided: {estimated_calls}
⚡ Based on average $0.002 per LLM call
        """
        console.print(Panel(savings_panel.strip(), title="Cost Savings", border_style="green"))


@app.command()
def config():
    """Show current FixtureGPT configuration."""
    mode = os.getenv('FIXTUREGPT_MODE', 'record')
    api_key = os.getenv('FIXTUREGPT_API_KEY')
    sync_mode = os.getenv('FIXTUREGPT_SYNC_MODE', 'local')
    api_url = os.getenv('FIXTUREGPT_API_URL', 'https://app.fixturegpt.com')
    
    config_info = f"""
🎯 Mode: [cyan]{mode}[/cyan] (record/replay)
☁️  Sync Mode: [cyan]{sync_mode}[/cyan] (local/cloud/both)
🔑 API Key: {'[green]SET[/green]' if api_key else '[red]NOT SET[/red]'}
🌐 API URL: [link]{api_url}[/link]
    """
    
    console.print(Panel(config_info.strip(), title="FixtureGPT Configuration", border_style="blue"))
    
    if not api_key:
        console.print("\n💡 To enable cloud sync:")
        console.print("1. Get API key: https://app.fixturegpt.com/dashboard/api-keys")
        console.print("2. Set environment variable: export FIXTUREGPT_API_KEY='your-key'")
        console.print("3. Set sync mode: export FIXTUREGPT_SYNC_MODE='both'")


@app.command()
def diff(name: str):
    """Re-run function with stored args and show differences."""
    console.print(f"🔍 Analyzing fixtures for '{name}'...")
    
    diff_results = diff_fixture(name)
    
    if "error" in diff_results:
        console.print(f"❌ {diff_results['error']}", style="red")
        return
    
    fixtures = diff_results["fixtures"]
    if not fixtures:
        console.print(f"📭 No fixtures found for '{name}'", style="yellow")
        return
    
    for i, fixture in enumerate(fixtures, 1):
        if "error" in fixture:
            console.print(f"❌ {fixture['filename']}: {fixture['error']}", style="red")
            continue
        
        console.print(f"\n📄 Fixture {i}: {fixture['filename']}")
        console.print(f"🕐 Recorded: {fixture['timestamp']}")
        
        # Show args and kwargs
        if fixture.get("args"):
            console.print("📥 Args:")
            console.print(json.dumps(fixture["args"], indent=2, default=str))
        
        if fixture.get("kwargs"):
            console.print("🔧 Kwargs:")
            console.print(json.dumps(fixture["kwargs"], indent=2, default=str))
        
        # Show original response (truncated if too long)
        response_str = json.dumps(fixture["original_response"], indent=2, default=str)
        if len(response_str) > 500:
            response_str = response_str[:500] + "..."
        
        console.print("📤 Original Response:")
        console.print(response_str)
        
        console.print("ℹ️  Note: To see actual differences, re-run with the same function in your code")


@app.command()
def clear():
    """Clear all saved fixtures."""
    from pathlib import Path
    import shutil
    
    fixtures_dir = Path("./fixtures")
    if fixtures_dir.exists():
        confirm = typer.confirm("Are you sure you want to delete all fixtures?")
        if confirm:
            shutil.rmtree(fixtures_dir)
            console.print("🗑️  All fixtures cleared!", style="green")
        else:
            console.print("❌ Operation cancelled", style="yellow")
    else:
        console.print("📭 No fixtures directory found", style="yellow")


if __name__ == "__main__":
    app() 