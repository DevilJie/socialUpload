from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class AppState:
    data_dir: Path = field(default_factory=lambda: Path.cwd() / "data")

    @property
    def db_path(self) -> Path:
        return self.data_dir / "db" / "database.db"

    @property
    def cookies_dir(self) -> Path:
        return self.data_dir / "cookiesFile"

    @property
    def video_dir(self) -> Path:
        return self.data_dir / "videoFile"

    def resolve_data_dir(self, cli_arg: str | None) -> None:
        """Resolve data directory from CLI arg > env var > project data/ > ~/.sau/data/"""
        import os

        if cli_arg:
            self.data_dir = Path(cli_arg)
            return

        env_dir = os.environ.get("SAU_DATA_DIR")
        if env_dir:
            self.data_dir = Path(env_dir)
            return

        project_data = Path(__file__).parent.parent / "data"
        if project_data.exists():
            self.data_dir = project_data
            return

        self.data_dir = Path.home() / ".sau" / "data"


state = AppState()
