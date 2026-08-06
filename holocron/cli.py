"""
Holocron — AshcrestHQ's learn-by-doing CLI.

Two tracks, one XP system:
  - security: the CyberHeaven-style fundamentals track
  - dev:      practical open source contribution skills (git, PRs, review)

Both tracks exist to funnel toward the same outcome: someone who finishes
enough of this is ready to open a real PR on Janus or Aegis.
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import BarColumn, Progress as RichProgress, TextColumn
from rich.table import Table

from holocron.core.lesson import Lesson, discover_lessons
from holocron.core.progress import load_progress, record_completion

app = typer.Typer(help="Holocron — learn security and open source contribution, one lesson at a time.")
console = Console()

LESSONS_DIR = Path(__file__).parent / "lessons"

TRACK_COLORS = {"security": "bright_red", "dev": "bright_blue"}
LEVEL_XP = 100  # xp needed per level, for a simple level display


def _level_for(xp: int) -> int:
    return xp // LEVEL_XP + 1


@app.command()
def list(track: str = typer.Option(None, help="Filter by track: security or dev")):
    """List all available lessons."""
    lessons = discover_lessons(LESSONS_DIR)
    progress = load_progress()

    if track:
        lessons = [l for l in lessons if l.track == track]

    table = Table(title="Holocron Lessons", show_lines=False)
    table.add_column("Status")
    table.add_column("Slug", style="bold")
    table.add_column("Title")
    table.add_column("Track")
    table.add_column("Difficulty")
    table.add_column("XP", justify="right")

    for lesson in lessons:
        done = "[green]done[/green]" if lesson.slug in progress.completed else "[dim]--[/dim]"
        color = TRACK_COLORS.get(lesson.track, "white")
        table.add_row(done, lesson.slug, lesson.title, f"[{color}]{lesson.track}[/{color}]", lesson.difficulty, str(lesson.xp))

    console.print(table)


@app.command()
def start(slug: str):
    """Start a lesson by its slug."""
    lessons = discover_lessons(LESSONS_DIR)
    match = next((l for l in lessons if l.slug == slug), None)
    if not match:
        console.print(f"[red]No lesson found with slug '{slug}'.[/red] Run [bold]holocron list[/bold] to see options.")
        raise typer.Exit(code=1)

    color = TRACK_COLORS.get(match.track, "white")
    console.print(Panel(Markdown(match.read_content()), title=f"[{color}]{match.title}[/{color}]", subtitle=f"{match.xp} XP · {match.difficulty}"))

    answer = typer.prompt("\nYour answer")
    progress = load_progress()

    if match.check(answer):
        already_done = slug in progress.completed
        progress = record_completion(progress, slug, match.xp)
        if already_done:
            console.print("[green]Correct![/green] (already completed before, no extra XP)")
        else:
            console.print(f"[bold green]Correct! +{match.xp} XP[/bold green]  (streak: {progress.streak_days} day(s))")
    else:
        console.print("[red]Not quite.[/red] Try again with [bold]holocron start " + slug + "[/bold]")


@app.command()
def status():
    """Show your XP, level, streak, and completed lessons."""
    progress = load_progress()
    lessons = discover_lessons(LESSONS_DIR)
    level = _level_for(progress.xp)
    xp_into_level = progress.xp % LEVEL_XP

    console.print(Panel.fit(
        f"[bold]Level {level}[/bold]   {progress.xp} XP total\n"
        f"Streak: {progress.streak_days} day(s)\n"
        f"Completed: {len(progress.completed)} / {len(lessons)} lessons",
        title="Your Holocron Progress",
    ))

    with RichProgress(TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as bar:
        task = bar.add_task(f"Level {level} -> {level + 1}", total=LEVEL_XP)
        bar.update(task, completed=xp_into_level)


@app.command()
def track(name: str):
    """Show only lessons from one track (security or dev)."""
    list(track=name)

@app.command()
def link():
    """Link your Discord account via OAuth2."""
    import os
    import json
    import webbrowser
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs

    api_url = os.environ.get("FORGE_API_URL", "https://api.ashcresthq.com")
    # strip trailing slash
    if api_url.endswith("/"):
        api_url = api_url[:-1]

    class OAuthCallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_path = urlparse(self.path)
            if parsed_path.path == "/complete":
                query = parse_qs(parsed_path.query)
                token = query.get("token", [""])[0]
                username = query.get("username", [""])[0]
                
                if token:
                    config_path = Path.home() / ".holocron" / "config.json"
                    config_path.parent.mkdir(parents=True, exist_ok=True)
                    config = {}
                    if config_path.exists():
                        with open(config_path, "r") as f:
                            try:
                                config = json.load(f)
                            except:
                                pass
                    
                    config["forge_token"] = token
                    config["discord_username"] = username
                    config["worker_url"] = api_url
                    
                    with open(config_path, "w") as f:
                        json.dump(config, f)
                    
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<html><head><style>body { background-color: #0D1117; color: #E6EDF3; font-family: sans-serif; text-align: center; margin-top: 50px; }</style></head><body><h1>Account Linked Successfully!</h1><p>You can close this tab and return to your terminal.</p><script>setTimeout(() => window.close(), 3000);</script></body></html>")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing token")
                    
                # Store that we succeeded
                self.server.oauth_success = True

        def log_message(self, format, *args):
            pass # suppress logging

    # Start server on random free port
    server = HTTPServer(("127.0.0.1", 0), OAuthCallbackHandler)
    server.oauth_success = False
    port = server.server_address[1]

    # Open browser
    auth_url = f"{api_url}/link/start?port={port}"
    console.print(f"Opening browser to link account: [bold blue]{auth_url}[/bold blue]")
    console.print("Waiting for callback...")
    webbrowser.open(auth_url)

    # Wait for a single request
    server.handle_request()
    
    if server.oauth_success:
        console.print("[bold green]Account successfully linked![/bold green] You can now run [bold]holocron sync[/bold].")
    else:
        console.print("[red]Linking failed or was interrupted.[/red]")


@app.command()
def sync():
    """Sync your progress to the AshcrestHQ leaderboard."""
    import os
    import json
    import urllib.request
    
    config_path = Path.home() / ".holocron" / "config.json"
    config = {}
    if config_path.exists():
        with open(config_path, "r") as f:
            try:
                config = json.load(f)
            except:
                pass

    api_url = os.environ.get("FORGE_API_URL", config.get("worker_url", "https://api.ashcresthq.com"))
    if api_url.endswith("/"):
        api_url = api_url[:-1]
        
    token = os.environ.get("FORGE_API_TOKEN", config.get("forge_token"))
    
    if not token:
        token = typer.prompt("Enter your Holocron Token (or run holocron link)", hide_input=True)
        
    progress = load_progress()
    lessons = discover_lessons(LESSONS_DIR)
    
    # Calculate tracks
    dev_count = 0
    sec_count = 0
    for slug in progress.completed:
        match = next((l for l in lessons if l.slug == slug), None)
        if match:
            if match.track == "dev":
                dev_count += 1
            elif match.track == "security":
                sec_count += 1

    data = {
        "xp": progress.xp,
        "completed": progress.completed,
        "tracks": {
            "dev": dev_count,
            "security": sec_count
        },
        "streak_days": progress.streak_days,
        "last_active": progress.last_active
    }
    
    sync_url = f"{api_url}/sync"
    console.print(f"Syncing to {sync_url}...")
    try:
        req = urllib.request.Request(sync_url, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("User-Agent", "Holocron-CLI/1.0")
        
        json_data = json.dumps(data).encode("utf-8")
        
        with urllib.request.urlopen(req, data=json_data, timeout=5) as response:
            if response.status in (200, 201):
                resp_data = json.loads(response.read().decode("utf-8"))
                console.print("[bold green]Sync successful![/bold green]")
                if resp_data.get("roleGranted"):
                    console.print("[bold yellow]🎉 You've unlocked the Discord Contributor role! 🎉[/bold yellow]")
            else:
                console.print(f"[red]Sync failed with status {response.status}[/red]")
    except Exception as e:
        console.print(f"[red]Failed to sync: {e}[/red]")


def main():
    app()


if __name__ == "__main__":
    main()
