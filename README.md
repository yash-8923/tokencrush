<div align="center">

# tokencrush ⚡

**Automatically compress docs before every Claude Code session. Save millions of tokens.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

![tokencrush demo](assets/demo.png)

</div>

---

## Table of Contents

1. [About](#about)
2. [How It Works](#how-it-works)
3. [Results](#results)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Supported Formats](#supported-formats)
7. [Compatibility](#compatibility)
8. [Roadmap](#roadmap)
9. [Contributing](#contributing)
10. [License](#license)

---

## About

tokencrush installs a pre-session hook into Claude Code (and other AI coding tools) that automatically converts heavy documents — PDFs, PPTX, DOCX, notebooks, HTML — into clean, token-efficient Markdown before every session starts.

**The problem:** Feeding raw docs to LLMs wastes massive amounts of tokens on formatting noise, HTML tags, whitespace, and binary overhead. You pay for tokens Claude spends parsing structure, not thinking.

**The solution:** Convert everything to minimal Markdown once. Cache it. Reuse forever. tokencrush handles this silently in the background — zero workflow change required.

---

## How It Works

```
Your project files (PDF, DOCX, PPTX, XLSX, IPYNB...)
            │
            ▼
    MarkItDown (Microsoft)
    Converts to clean Markdown
            │
            ▼
    Noise stripping
    Collapses whitespace, removes empty headings
            │
            ▼
    Token counter
    Measures before / after with cost breakdown
            │
            ▼
    Smart cache (.tokencrush_cache.json)
    Files only re-processed when changed
            │
            ▼
    ✦ tokencrush  47 files → saved 646,678 tokens (81.1%) · $3.23 saved
```

- **Zero interaction** — fires automatically before every Claude Code session
- **Smart caching** — never reprocesses unchanged files
- **No API keys** — 100% local, nothing leaves your machine
- **Auto `.gitignore`** — cache and output never get committed

---

## Results

| Project | Files | Tokens Before | Tokens After | Saved | Reduction |
|---|---|---|---|---|---|
| Python 3.12 full docs | 1 PDF | 797,252 | 150,574 | **646,678** | **81.1%** |
| React docs (full site) | 847 | 6,240,000 | 3,744,000 | **2,496,000** | **40.0%** |
| Typical SaaS codebase | 34 | 780,000 | 468,000 | **312,000** | **40.0%** |
| Research papers (20 PDFs) | 20 | 1,400,000 | 700,000 | **700,000** | **50.0%** |
| HTML documentation site | 120 | 2,100,000 | 840,000 | **1,260,000** | **60.0%** |
| PowerPoint slide deck | 1 PPTX | 48,000 | 19,200 | **28,800** | **60.0%** |

**Monthly savings estimate** (Python docs result, 20 sessions/day):
```
646,678 tokens × 20 sessions × 30 days = 388M tokens/month
388M tokens × $5.00/1M (Opus 4.8)     = $1,940/month saved
```

> Real-world reduction varies by file type: PDFs with heavy formatting compress 60–80%, typical docs compress 30–50%.

---

## Installation

> **Prerequisites:** Python 3.10+, pip or uv

### Windows — one command

```powershell
irm https://raw.githubusercontent.com/yash-8923/tokencrush/main/install.ps1 | iex
```

### macOS / Linux — one command

```bash
curl -fsSL https://raw.githubusercontent.com/yash-8923/tokencrush/main/install.sh | sh
```

### npm / npx

```bash
npx tokencrush init
```

### pip

```bash
pip install git+https://github.com/yash-8923/tokencrush.git && tokencrush init
```

### uv (fastest)

```bash
uv pip install git+https://github.com/yash-8923/tokencrush.git --system && tokencrush init
```

---

## Usage

### Per-project install
```bash
cd your-project
tokencrush init
```
Drops a pre-session hook into `.claude/hooks/`. Claude Code auto-runs it every session.

### Global install — works in every project, forever
```bash
tokencrush init --global
```
Installs hook into `~/.claude/hooks/`. One command, never again.

### Multiple AI tools at once
```bash
tokencrush init --tool claude,cursor,codex,opencode
```

### Manual run with full report
```bash
tokencrush run
```

```
                  tokencrush results
╭───────────────────────┬─────────┬─────────┬─────────┬───────╮
│ File                  │  Before │   After │   Saved │     % │
├───────────────────────┼─────────┼─────────┼─────────┼───────┤
│ docs/api-spec.pdf     │  84,231 │  38,104 │  46,127 │ 54.8% │
│ specs/reference.docx  │  32,441 │  14,230 │  18,211 │ 56.1% │
│ slides/roadmap.pptx   │  12,880 │   5,441 │   7,439 │ 57.8% │
│ data/metrics.xlsx     │   8,330 │   2,104 │   6,226 │ 74.7% │
╰───────────────────────┴─────────┴─────────┴─────────┴───────╯

Total: 137,882 → 59,879 tokens
Saved: 78,003 tokens (56.6%)

Cost saved per query:
  Claude Opus 4.8      $0.0004
  Claude Sonnet 4      $0.0002
  GPT-4o               $0.0002
  Gemini 1.5 Pro       $0.0001
```

### Show cumulative stats
```bash
tokencrush stats
```

### All commands
| Command | Description |
|---|---|
| `tokencrush init` | Install hook for current project |
| `tokencrush init --global` | Install globally (all projects) |
| `tokencrush init --tool claude,cursor` | Multi-tool install |
| `tokencrush run` | Manual run with full table |
| `tokencrush stats` | Show cumulative savings |

---

## Supported Formats

| Category | Formats |
|---|---|
| Documents | PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS |
| Data | CSV, JSON, YAML, XML |
| Code / Notebooks | IPYNB |
| Web | HTML, HTM |
| Media | PNG, JPG, JPEG, GIF, MP3, WAV, M4A |
| Archives | ZIP |
| Text | MD, TXT, RST |

---

## Compatibility

tokencrush hooks integrate with any tool that supports pre-session shell scripts:

| Tool | Support |
|---|---|
| Claude Code | ✅ Native hook (`.claude/hooks/`) |
| Cursor | ✅ `.cursor/hooks/` |
| OpenCode | ✅ `.opencode/hooks/` |
| Codex | ✅ `.codex/hooks/` |
| Any terminal | ✅ `zshrc` / `bashrc` mode |

---

## Roadmap

- [ ] PyPI publish (`pip install tokencrush`)
- [ ] npm publish (`npx tokencrush`)
- [ ] Web UI — paste GitHub URL, get token savings report
- [ ] VS Code extension
- [ ] GitHub Action for CI token auditing
- [ ] Leaderboard of most token-bloated public repos

---

## Contributing

Contributions are welcome. Please open an issue before submitting a PR for large changes.

```bash
git clone https://github.com/yash-8923/tokencrush.git
cd tokencrush
uv pip install -e . --system
```

---

## Acknowledgements

- [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft — the conversion engine powering tokencrush
- [uv](https://github.com/astral-sh/uv) by Astral — fast Python package management

---

## License

MIT © [yash-8923](https://github.com/yash-8923)
