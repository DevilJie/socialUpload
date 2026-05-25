import asyncio
import threading
from queue import Queue, Empty

import typer
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from cli.db import get_connection
from cli.output import print_success, print_error, print_info
from cli.platform import resolve_platform, get_platform_name
from cli.state import state

app = typer.Typer(help="登录管理", no_args_is_help=True)


def _run_login(platform_id: int, account_id: str, status_queue: Queue):
    """Run platform login in a new event loop (called from a thread)."""
    from impl.registry import get_platform

    platform = get_platform(platform_id)
    if not platform:
        status_queue.put({"type": "error", "message": f"不支持的平台 ID: {platform_id}"})
        return

    try:
        asyncio.run(platform.login(account_id, status_queue))
    except Exception as e:
        status_queue.put({"type": "error", "message": str(e)})


def do_login(platform_name: str):
    """扫码登录平台账号"""
    platform_id = resolve_platform(platform_name)
    if platform_id is None:
        print_error(f"未知平台: {platform_name}")
        print_info("支持的平台: douyin, xiaohongshu, bilibili, kuaishou, channels, baijiahao, tiktok, youtube, tencent_video, iqiyi")
        raise typer.Exit(1)

    platform_display = get_platform_name(platform_id)
    console = Console()

    # Ensure data directories exist
    state.cookies_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique account ID for this login session
    import uuid
    account_id = str(uuid.uuid4())

    # Create status queue and start login in background thread
    status_queue = Queue()
    thread = threading.Thread(
        target=_run_login,
        args=(platform_id, account_id, status_queue),
        daemon=True,
    )
    thread.start()

    console.print(f"\n🔐 正在打开{platform_display}登录页面...\n")
    console.print(f"请用手机[bold]{platform_display}[/bold]扫描浏览器中的二维码登录")

    # Poll status queue and display updates
    login_success = False
    with Live(Spinner("dots", text=Text("等待扫码... (Ctrl+C 取消)")), console=console):
        while thread.is_alive():
            try:
                msg = status_queue.get(timeout=0.2)
                msg_type = msg.get("type", "status") if isinstance(msg, dict) else "status"

                if isinstance(msg, str):
                    console.print(f"  {msg}")
                elif msg_type == "qr_url":
                    pass
                elif msg_type == "status":
                    console.print(f"  {msg.get('message', msg)}")
                elif msg_type == "success":
                    console.print(f"[green]  {msg.get('message', '')}[/green]")
                    login_success = True
                    break
                elif msg_type == "error":
                    print_error(msg.get("message", "登录失败"))
                    raise typer.Exit(1)
            except Empty:
                continue

    thread.join(timeout=5)

    if login_success:
        console.print()
        print_success(f"登录成功 ({platform_display})")
        console.print("   Cookie 已保存，可开始发布")
