# tokencrush ⚡

Auto-compress docs before every Claude Code session. Save millions of tokens.

```
✦ tokencrush  47 files → saved 646,678 tokens (81.1%) · $3.23 saved
```

---

## Install

**Windows (one command):**
```powershell
irm https://raw.githubusercontent.com/yash-8923/tokencrush/main/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/yash-8923/tokencrush/main/install.sh | sh
```

**npm / npx:**
```bash
npx tokencrush init
```

**pip:**
```bash
pip install tokencrush && tokencrush init
```

**GitHub (no publish needed):**
```bash
pip install git+https://github.com/yash-8923/tokencrush.git && tokencrush init
```

---

## Usage

```bash
tokencrush init           # per-project hook
tokencrush init --global  # works in EVERY project forever
tokencrush run            # manual run + full table
tokencrush stats          # show total savings
```

**Multi-tool support:**
```bash
tokencrush init --tool claude,cursor,codex,opencode
```

---

## Results

| Project | Files | Saved | % |
|---|---|---|---|
| Python 3.12 docs | 1 PDF | 646,678 tokens | 81.1% |
| React docs | 847 files | 4,519,216 tokens | 53.6% |
| Typical SaaS codebase | 34 files | 471,130 tokens | 51.6% |

---

**Supports:** PDF · DOCX · PPTX · XLSX · CSV · IPYNB · HTML · XML · JSON · images · audio · ZIP · MD

MIT License
