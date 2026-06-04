Write-Host "Installing tokencrush..." -ForegroundColor Cyan

# Install uv if missing
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..." -ForegroundColor Yellow
    pip install uv --quiet
}

# Install tokencrush
uv pip install git+https://github.com/yash-8923/tokencrush.git --system --quiet

# Init global
python -m tokencrush init --global

Write-Host ""
Write-Host "Done! Auto-runs in every Claude Code session." -ForegroundColor Green
Write-Host "Run 'tokencrush run' to test now." -ForegroundColor Yellow
