import typer
from rich.panel import Panel

from cli.db import get_connection, ensure_db
from cli.output import console, print_success, print_error
from cli.state import state

app = typer.Typer(help="配置管理", no_args_is_help=True)


@app.command("init")
def config_init():
    """初始化数据目录和数据库"""
    data_dir = state.data_dir
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "db").mkdir(exist_ok=True)
    (data_dir / "cookiesFile").mkdir(exist_ok=True)
    (data_dir / "videoFile").mkdir(exist_ok=True)
    (data_dir / "frames").mkdir(exist_ok=True)
    (data_dir / "logs").mkdir(exist_ok=True)

    ensure_db(state.db_path)
    print_success(f"数据目录已初始化: {data_dir}")


@app.command("show")
def config_show():
    """显示当前配置"""
    data_dir = state.data_dir
    db_exists = state.db_path.exists()

    lines = [
        f"[bold]数据目录:[/bold] {data_dir}",
        f"[bold]数据库:[/bold] {'✅ 存在' if db_exists else '❌ 不存在 (运行 sau config init)'}",
    ]

    if db_exists:
        conn = get_connection(state.db_path)
        try:
            row = conn.execute(
                "SELECT value FROM settings WHERE key = 'proxy_url'"
            ).fetchone()
            proxy = row["value"] if row else "未设置"
            lines.append(f"[bold]代理地址:[/bold] {proxy}")

            account_count = conn.execute("SELECT COUNT(*) FROM user_info").fetchone()[0]
            lines.append(f"[bold]账号数量:[/bold] {account_count}")
        finally:
            conn.close()

    console.print(Panel("\n".join(lines), title="SAU 配置"))


@app.command("set")
def config_set(
    key: str = typer.Argument(help="配置键名"),
    value: str = typer.Argument(help="配置值"),
):
    """设置配置项"""
    valid_keys = {"proxy_url"}
    if key not in valid_keys:
        print_error(f"未知配置项: {key}。可用: {', '.join(valid_keys)}")
        raise typer.Exit(1)

    conn = get_connection(state.db_path)
    try:
        conn.execute(
            "INSERT INTO settings (key, value, updated_at) VALUES (?, ?, datetime('now')) "
            "ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = datetime('now')",
            (key, value, value),
        )
        conn.commit()
    finally:
        conn.close()

    print_success(f"{key} = {value}")
