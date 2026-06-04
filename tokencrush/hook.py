import warnings
warnings.filterwarnings("ignore")

import logging
logging.disable(logging.CRITICAL)

import os
import sys
from pathlib import Path

def run_hook(directory: str = "."):
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.text import Text
        console = Console()
    except ImportError:
        console = None

    from .converter import find_convertible_files, convert_file
    from .counter import calc_savings
    from .cache import load_cache, save_cache, is_cached, cache_file, save_markdown

    directory = os.path.abspath(directory)
    files = find_convertible_files(directory)

    if not files:
        return

    cache = load_cache(directory)

    total_before = 0
    total_after = 0
    processed = 0
    skipped = 0
    errors = 0

    for path in files:
        if is_cached(path, cache):
            # Still count cached stats toward totals
            cached = cache.get(path, {})
            total_before += cached.get("tokens_before", 0)
            total_after += cached.get("tokens_after", 0)
            skipped += 1
            continue

        try:
            # Read original for token count
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    original_text = f.read()
            except Exception:
                original_text = ""

            markdown = convert_file(path)
            stats = calc_savings(original_text or markdown, markdown)

            save_markdown(directory, path, markdown)
            cache_file(path, cache, stats)

            total_before += stats["tokens_before"]
            total_after += stats["tokens_after"]
            processed += 1

        except Exception as e:
            errors += 1
            continue

    save_cache(directory, cache)

    total_saved = total_before - total_after
    total_files = processed + skipped

    if total_files == 0 or total_saved <= 0:
        return

    pct = round((total_saved / total_before * 100), 1) if total_before > 0 else 0
    sonnet_saved = round((total_saved / 1_000_000) * 3.00, 2)

    if console:
        text = Text()
        text.append("✦ tokencrush ", style="bold cyan")
        text.append(f"{total_files} files → ", style="white")
        text.append(f"saved {total_saved:,} tokens ", style="bold green")
        text.append(f"({pct}%)", style="green")
        text.append(f" · ${sonnet_saved:.2f} saved", style="bold yellow")
        if processed > 0:
            text.append(f" · {processed} new", style="dim")
        console.print(text)
    else:
        print(f"✦ tokencrush: {total_files} files → saved {total_saved:,} tokens ({pct}%) · ${sonnet_saved:.2f} saved")


def run_detailed(directory: str = "."):
    """Full detailed report with table"""
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    from rich import box

    from .converter import find_convertible_files, convert_file
    from .counter import calc_savings, PRICING
    from .cache import load_cache, save_cache, is_cached, cache_file, save_markdown

    console = Console()
    directory = os.path.abspath(directory)
    files = find_convertible_files(directory)

    if not files:
        console.print("[yellow]No convertible files found.[/yellow]")
        return

    cache = load_cache(directory)

    table = Table(title="tokencrush results", box=box.ROUNDED, show_header=True)
    table.add_column("File", style="cyan", max_width=40)
    table.add_column("Before", justify="right")
    table.add_column("After", justify="right")
    table.add_column("Saved", justify="right", style="green")
    table.add_column("%", justify="right", style="bold green")

    total_before = 0
    total_after = 0

    for path in files:
        rel = os.path.relpath(path, directory)

        if is_cached(path, cache):
            data = cache.get(path, {})
            b = data.get("tokens_before", 0)
            a = data.get("tokens_after", 0)
            s = b - a
            p = round((s / b * 100), 1) if b > 0 else 0
            total_before += b
            total_after += a
            table.add_row(rel[:40], f"{b:,}", f"{a:,}", f"{s:,}", f"{p}%")
            continue

        try:
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    original_text = f.read()
            except Exception:
                original_text = ""

            markdown = convert_file(path)
            stats = calc_savings(original_text or markdown, markdown)
            save_markdown(directory, path, markdown)
            cache_file(path, cache, stats)
            save_cache(directory, cache)

            b = stats["tokens_before"]
            a = stats["tokens_after"]
            s = stats["tokens_saved"]
            p = stats["percent_saved"]
            total_before += b
            total_after += a

            table.add_row(rel[:40], f"{b:,}", f"{a:,}", f"{s:,}", f"{p}%")

        except Exception as e:
            table.add_row(rel[:40], "—", "—", f"[red]error[/red]", "—")

    console.print(table)

    total_saved = total_before - total_after
    pct = round((total_saved / total_before * 100), 1) if total_before > 0 else 0

    console.print()
    console.print(f"[bold]Total:[/bold] {total_before:,} → {total_after:,} tokens")
    console.print(f"[bold green]Saved: {total_saved:,} tokens ({pct}%)[/bold green]")
    console.print()

    console.print("[bold]Cost savings per model:[/bold]")
    for model, price in PRICING.items():
        saved_usd = (total_saved / 1_000_000) * price
        console.print(f"  {model:<20} ${saved_usd:.4f} per query · ${saved_usd * 100:.2f} per 100 queries")
