import shutil
from datetime import datetime
from pathlib import Path

import typer

from cli.db import get_connection
from cli.output import console, print_success, print_error, create_table
from cli.state import state

app = typer.Typer(help="素材管理", no_args_is_help=True)


@app.command("upload")
def materials_upload(
    file_path: str = typer.Argument(help="文件路径"),
):
    """上传素材文件"""
    src = Path(file_path).resolve()
    if not src.exists():
        print_error(f"文件不存在: {file_path}")
        raise typer.Exit(1)

    dest_dir = state.video_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        dest = dest_dir / f"{stem}_{timestamp}{suffix}"

    shutil.copy2(str(src), str(dest))
    file_size = dest.stat().st_size

    conn = get_connection(state.db_path)
    try:
        conn.execute(
            "INSERT INTO file_records (filename, filesize, upload_time, file_path) VALUES (?, ?, datetime('now'), ?)",
            (dest.name, file_size, str(dest)),
        )
        conn.commit()
    finally:
        conn.close()

    size_mb = file_size / (1024 * 1024)
    print_success(f"已上传: {dest.name} ({size_mb:.1f}MB)")


@app.command("list")
def materials_list():
    """列出所有素材"""
    conn = get_connection(state.db_path)
    try:
        rows = conn.execute("SELECT * FROM file_records ORDER BY id DESC").fetchall()
    finally:
        conn.close()

    if not rows:
        console.print("[dim]暂无素材。运行 sau materials upload <文件> 添加。[/dim]")
        return

    table = create_table("素材列表", ["ID", "文件名", "大小", "上传时间"])
    for row in rows:
        size_kb = row["filesize"] / 1024
        if size_kb > 1024:
            size_str = f"{size_kb / 1024:.1f}MB"
        else:
            size_str = f"{size_kb:.1f}KB"
        table.add_row(str(row["id"]), row["filename"], size_str, row["upload_time"] or "")

    console.print(table)


@app.command("delete")
def materials_delete(
    file_id: int = typer.Argument(help="素材 ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过确认"),
):
    """删除素材"""
    conn = get_connection(state.db_path)
    try:
        row = conn.execute("SELECT * FROM file_records WHERE id = ?", (file_id,)).fetchone()
    finally:
        conn.close()

    if not row:
        print_error(f"素材不存在: {file_id}")
        raise typer.Exit(1)

    if not yes:
        confirm = typer.confirm(f"确定删除素材 {row['filename']}？")
        if not confirm:
            raise typer.Abort()

    file_path = Path(row["file_path"]) if row["file_path"] else None
    if file_path and file_path.exists():
        file_path.unlink()

    conn = get_connection(state.db_path)
    try:
        conn.execute("DELETE FROM file_records WHERE id = ?", (file_id,))
        conn.commit()
    finally:
        conn.close()

    print_success(f"已删除: {row['filename']}")
