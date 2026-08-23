from typer.testing import CliRunner  # type: ignore[import-not-found,import-untyped]
from holocron.cli import app

runner = CliRunner()

def test_cli_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Holocron Lessons" in result.stdout

def test_cli_list_track_filter():
    result = runner.invoke(app, ["list", "--track", "security"])
    assert result.exit_code == 0
    assert "security" in result.stdout

def test_cli_status():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Your Holocron Progress" in result.stdout

def test_cli_start_invalid_slug():
    result = runner.invoke(app, ["start", "non-existent-slug"])
    assert result.exit_code == 1
    assert "No lesson found" in result.stdout
