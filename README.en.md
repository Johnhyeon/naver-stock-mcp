<div align="center">

<img src="assets/logo.svg" width="120" height="120" alt="StockLens logo">

# StockLens

**AI-powered Korean stock analysis with real data**

[![PyPI](https://img.shields.io/pypi/v/naver-stock-mcp.svg)](https://pypi.org/project/naver-stock-mcp/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[🇰🇷 한국어](README.md) | 🇺🇸 **English**

</div>

---

## Why StockLens

When you show AI a chart image, it **guesses the numbers and often gets them wrong** (hallucination).

**StockLens** connects Claude directly to live data from Naver Finance (Korea's largest stock portal), so AI **reads real numbers instead of guessing**.

```
❌ "Samsung Electronics is around 80,000 KRW" (guess, wrong)
✅ "Samsung Electronics at 206,000 KRW, +5.3% vs 20-day MA" (real data)
```

## Features

- 📊 **19 tools** — Prices, charts, investor flows, financials, screening, Excel export
- 🔑 **No API key required** — Uses public Naver Finance data
- 🚀 **Fast responses** — TTL cache + Semaphore optimization
- 📁 **Excel snapshots** — Scan once, query instantly
- 🤖 **Gemini/GPT compatible** — Export to Excel for use with other AIs

## Quick Start

### Method A: Developers (2 commands)

```bash
pip install naver-stock-mcp
stock-mcp-setup
```

### Method B: Non-developers (one-click)

Download [install.bat](https://raw.githubusercontent.com/Johnhyeon/naver-stock-mcp/main/install.bat) (Windows) or [install.sh](https://raw.githubusercontent.com/Johnhyeon/naver-stock-mcp/main/install.sh) (Mac/Linux) and double-click.

Then **fully quit and restart Claude Desktop**.

## Verify Installation

In Claude:
```
Show me Samsung Electronics (005930) current price
```

If you see the stock name, price, and volume, you're all set.

## Example Queries

```
"Analyze SK Hynix 120-day candles using the 20-day MA trend"
"Check Kakao's foreign/institutional investor flow for the last 20 days"
"Find stocks in top-100 market cap with PER under 15"
"Show today's strongest 3 themes and analyze the leader of each"
```

## Learn More

- [📘 **All 19 Tools** →](guides/en/TOOLS.md)
- [💡 **50 Prompt Examples** →](guides/en/USAGE.md)
- [🔧 **Installation & Troubleshooting** →](guides/en/INSTALL.md)

## Supported Environments

| Environment | Support |
|-------------|---------|
| Claude Desktop (app) | ✅ Main target |
| Claude Code (CLI) | ✅ |
| Claude.ai (web) | ❌ Local MCP not supported |
| ChatGPT / Gemini | Via Excel export workaround |

## Important Note for International Users

StockLens is designed for **Korean stock market (KOSPI/KOSDAQ)** data from Naver Finance. Stock codes are 6-digit Korean tickers (e.g., `005930` for Samsung Electronics, `000660` for SK Hynix). US/global stock support is planned for a future version.

## Contributing

Issues and PRs are welcome. Please open an [Issue](https://github.com/Johnhyeon/naver-stock-mcp/issues) for bugs or feature requests.

## License

MIT License
