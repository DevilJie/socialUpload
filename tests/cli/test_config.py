from typer.testing import CliRunner

from cli.main import app

runner = CliRunner()


def test_config_init(tmp_path):
    data_dir = tmp_path / "sau-data"
    result = runner.invoke(app, ["--data-dir", str(data_dir), "config", "init"])
    assert result.exit_code == 0
    assert (data_dir / "db" / "database.db").exists()
    assert (data_dir / "cookiesFile").exists()
    assert (data_dir / "videoFile").exists()


def test_config_init_idempotent(tmp_path):
    data_dir = tmp_path / "sau-data"
    runner.invoke(app, ["--data-dir", str(data_dir), "config", "init"])
    result = runner.invoke(app, ["--data-dir", str(data_dir), "config", "init"])
    assert result.exit_code == 0


def test_config_show(temp_data_dir):
    result = runner.invoke(app, ["--data-dir", str(temp_data_dir), "config", "show"])
    assert result.exit_code == 0
    assert "数据目录" in result.output


def test_config_set_proxy(temp_data_dir):
    result = runner.invoke(
        app,
        ["--data-dir", str(temp_data_dir), "config", "set", "proxy_url", "http://127.0.0.1:7897"],
    )
    assert result.exit_code == 0
