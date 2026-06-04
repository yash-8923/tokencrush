import re

# Pricing per 1M input tokens (USD) as of 2025
PRICING = {
    "Claude Opus 4.8":   5.00,
    "Claude Sonnet 4":   3.00,
    "GPT-4o":            2.50,
    "Gemini 1.5 Pro":    1.25,
}

def count_tokens(text: str) -> int:
    """
    Fast offline token estimation.
    Splits on whitespace + punctuation — ~10% accurate vs tiktoken,
    good enough for savings reporting.
    """
    if not text:
        return 0
    # Split on whitespace and punctuation boundaries
    tokens = re.findall(r"\w+|[^\w\s]", text)
    return len(tokens)

def calc_savings(original_text: str, compressed_text: str) -> dict:
    before = count_tokens(original_text)
    after = count_tokens(compressed_text)
    saved = before - after
    pct = (saved / before * 100) if before > 0 else 0

    costs = {}
    for model, price_per_million in PRICING.items():
        saved_dollars = (saved / 1_000_000) * price_per_million
        costs[model] = round(saved_dollars, 4)

    return {
        "tokens_before": before,
        "tokens_after": after,
        "tokens_saved": saved,
        "percent_saved": round(pct, 1),
        "cost_saved": costs,
    }
