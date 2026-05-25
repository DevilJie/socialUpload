from pathlib import Path
from typer.testing import CliRunner

from cli.main import app
from cli.db import get_connection

runner = CliRunner()


def test_materials_list_empty(temp_data_dir):
    result = runner.invoke(app, ["--data-dir", str(temp_data_dir), "materials", "list"])
    assert result.exit_code == 0


def test_materials_upload(temp_data_dir):
    video_file = temp_data_dir / "test.mp4"
    video_file.write_bytes(b"fake video content")

    result = runner.invoke(
        app,
        ["--data-dir", str(temp_data_dir), "materials", "upload", str(video_file)],
    )
    assert result.exit_code == 0
    assert "test.mp4" in result.output

    conn = get_connection(temp_data_dir / "db" / "database.db")
    row = conn.execute("SELECT * FROM file_records WHERE filename = 'test.mp4'").fetchone()
    conn.close()
    assert row is not None


def test_materials_delete(temp_data_dir):
    video_file = temp_data_dir / "test.mp4"
    video_file.write_bytes(b"fake video content")
    runner.invoke(app, ["--data-dir", str(temp_data_dir), "materials", "upload", str(video_file)])

    result = runner.invoke(
        app,
        ["--data-dir", str(temp_data_dir), "materials", "delete", "1", "--yes"],
    )
    assert result.exit_code == 0

    conn = get_connection(temp_data_dir / "db" / "database.db")
    count = conn.execute("SELECT COUNT(*) FROM file_records").fetchone()[0]
    conn.close()
    assert count == 0
