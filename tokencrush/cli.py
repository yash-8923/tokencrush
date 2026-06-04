import sys
import os
import argparse
import shutil
from pathlib import Path


HOOK_TEMPLATES = {
    "claude": {
        "path": ".claude/hooks/pre-session.sh",
        "content": "#!/bin/bash\n# tokencrush hook\npython -m tokencrush hook 2>/dev/null || true\n"
    },
    "cursor": {
        "path": ".cursor/hooks/pre-session.sh",
        "content": "#!/bin/bash\n# tokencrush hook\npython -m tokencrush hook 2>/dev/null || true\n"
    },
    "opencode": {
        "path": ".opencode/hooks/pre-session.sh",
        "content": "#!/bin/bash\n# tokencrush hook\npython -m tokencrush hook 2>/dev/null || true\n"
    },
    "codex": {
        "path": ".codex/hooks/pre-session.sh",
        "content": "#!/bin/bash\n# tokencrush hook\npython -m tokencrush hook 2>/dev/null || true\n"
    },
    "zshrc": {
        "path": None,  # goes in ~/.zshrc
        "content": '\n# tokencrush - auto token compression\ncd "$PWD" && python -m tokencrush hook 2>/dev/null || true\n'
    },
    "bashrc": {
        "path": None,  # goes in ~/.bashrc
        "content": '\n# tokencrush - auto token compression\ncd "$PWD" && python -m tokencrush hook 2>/dev/null || true\n'
    },
}

def cmd_init(args):
    if args.glob:
        home = os.path.expanduser("~")
        project_dir = home
        # Global claude hook
        hooks_dir = os.path.join(home, ".claude", "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        hook_path = os.path.join(hooks_dir, "pre-session.sh")
        with open(hook_path, 'w') as f:
            f.write("#!/bin/bash\n# tokencrush global hook\npython -m tokencrush hook 2>/dev/null || true\n")
        os.chmod(hook_path, 0o755)
        print(f"✓ tokencrush global hook installed → {hook_path}")
        print("Works in every Claude Code project. Forever.")
        return

    project_dir = os.path.abspath(args.dir)
    tools = args.tool.split(',') if args.tool else ['claude']

    for tool in tools:
        tool = tool.strip()
        if tool not in HOOK_TEMPLATES:
            print(f"✗ Unknown tool: {tool}. Choose from: {', '.join(HOOK_TEMPLATES.keys())}")
            continue

        tmpl = HOOK_TEMPLATES[tool]

        if tool in ('zshrc', 'bashrc'):
            rc_path = os.path.expanduser(f"~/.{tool[:-2]}rc" if tool == 'zshrc' else "~/.bashrc")
            with open(rc_path, 'a') as f:
                f.write(tmpl['content'])
            print(f"✓ tokencrush added to {rc_path}")
        else:
            hook_path = os.path.join(project_dir, tmpl['path'])
            os.makedirs(os.path.dirname(hook_path), exist_ok=True)
            with open(hook_path, 'w') as f:
                f.write(tmpl['content'])
            os.chmod(hook_path, 0o755)
            print(f"✓ tokencrush hook installed → {hook_path}")

    # Update .gitignore
    gitignore = os.path.join(project_dir, ".gitignore")
    entries = [".tokencrush_cache.json", ".tokencrush_output/"]
    if os.path.exists(gitignore):
        with open(gitignore) as f:
            existing = f.read()
        with open(gitignore, 'a') as f:
            for e in entries:
                if e not in existing:
                    f.write(f"\n{e}")
    else:
        with open(gitignore, 'w') as f:
            f.write('\n'.join(entries) + '\n')

    print("✓ .gitignore updated")
    print()
    print("Run 'tokencrush run' to compress immediately.")


def cmd_hook(args):
    """Runs silently in hook mode - minimal output"""
    from tokencrush.hook import run_hook
    run_hook(args.dir)


def cmd_run(args):
    """Full detailed run with table output"""
    from tokencrush.hook import run_detailed
    run_detailed(args.dir)


def cmd_stats(args):
    """Show cumulative stats from cache"""
    from tokencrush.cache import load_cache
    from rich.console import Console
    from rich.table import Table
    from rich import box

    console = Console()
    directory = os.path.abspath(args.dir)
    cache = load_cache(directory)

    if not cache:
        console.print("[yellow]No cache found. Run 'tokencrush run' first.[/yellow]")
        return

    total_before = sum(v.get("tokens_before", 0) for v in cache.values())
    total_after = sum(v.get("tokens_after", 0) for v in cache.values())
    total_saved = total_before - total_after
    pct = round((total_saved / total_before * 100), 1) if total_before > 0 else 0

    console.print(f"\n[bold cyan]tokencrush stats[/bold cyan] — {len(cache)} files indexed\n")
    console.print(f"  Tokens before : {total_before:>12,}")
    console.print(f"  Tokens after  : {total_after:>12,}")
    console.print(f"  [bold green]Tokens saved  : {total_saved:>12,}  ({pct}%)[/bold green]")
    console.print()

    from tokencrush.counter import PRICING
    console.print("  [bold]Cost saved per query:[/bold]")
    for model, price in PRICING.items():
        saved = (total_saved / 1_000_000) * price
        console.print(f"    {model:<22} ${saved:.4f}")
    console.print()


def main():
    parser = argparse.ArgumentParser(
        prog="tokencrush",
        description="Auto-compress docs for Claude Code. Save tokens. Show numbers."
    )
    parser.add_argument("--dir", default=".", help="Target directory (default: current)")
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Install pre-session hook")
    p_init.add_argument("--tool", default="claude",
        help="Tool(s) to install for. Comma-separated: claude,cursor,codex,opencode,zshrc,bashrc (default: claude)")
    p_init.add_argument("--global", dest="glob", action="store_true",
        help="Install globally — works in every project, forever")
    sub.add_parser("run", help="Compress all files and show full report")
    sub.add_parser("hook", help="Run hook mode (used internally by Claude Code)")
    sub.add_parser("stats", help="Show token savings stats from cache")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "run":
        cmd_run(args)
    elif args.command == "hook":
        cmd_hook(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
