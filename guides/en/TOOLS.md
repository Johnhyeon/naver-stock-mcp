# StockLens Tool Reference

19 tools organized by category.

[🇰🇷 한국어](../ko/TOOLS.md) | [USAGE](USAGE.md) | [INSTALL](INSTALL.md)

---

## 📊 Basic Queries (6)

### `search`
Search stocks by name or code.

**Parameters**
- `query` (str): Stock name or code

**Example**
```
"Find Samsung Electronics code"
"Search for SK Hynix"
```

---

### `get_chart`
Get daily/weekly/monthly OHLCV data.

**Parameters**
- `code` (str): 6-digit Korean stock code
- `timeframe` (str): `"day"` / `"week"` / `"month"` (default: `"day"`)
- `count` (int): Number of bars (default: 120, max: 500)

**Example**
```
"Show Samsung Electronics 120-day daily candles"
"SK Hynix weekly chart, 60 bars"
```

---

### `get_price`
Real-time current price + open/high/low/volume.

**Parameters**
- `code` (str): 6-digit stock code

**Example**
```
"Samsung Electronics current price"
"Hyundai Motor price now"
```

---

### `get_flow`
Investor flow (foreign / institutional net buying).

**Parameters**
- `code` (str): 6-digit stock code
- `days` (int): Days to retrieve (default: 20, max: 60)

**Example**
```
"Kakao 20-day foreign/institutional flow"
"SK Hynix recent month investor flow"
```

**Note**: Retail investor flow is not available from Naver Finance.

---

### `get_financial`
Financial metrics (PER, PBR, Market Cap, EPS, BPS, etc.).

**Parameters**
- `code` (str): 6-digit stock code

**Example**
```
"Naver PER and PBR"
"Hyundai Motor financials"
```

---

### `get_index`
KOSPI / KOSDAQ index values.

**Parameters**
- None

**Example**
```
"How is KOSPI today?"
"Market indices"
```

---

## 🔍 Screening (7)

### `list_themes`
Theme list from Naver Finance (sorted by daily change).

**Parameters**
- `page` (int): Page (default: 1, max: 7)

**Example**
```
"Show today's top 10 strongest themes"
"Theme list page 2"
```

40 themes per page, 7 pages total (~280 themes).

---

### `get_theme_stocks`
Stocks belonging to a specific theme.

**Parameters**
- `theme_name` (str): Theme name (partial match supported)
- `count` (int): Max stocks to return (default: 30, max: 50)
- `include_reason` (bool): Include inclusion reason (default: `true`)

**Example**
```
"AI semiconductor theme stocks"
"Battery-related stocks, top 20"
```

---

### `list_sectors`
Sector list (~79 sectors, sorted by change rate).

**Parameters**
- None

**Example**
```
"Sector overview"
"List all sectors"
```

---

### `get_sector_stocks`
Stocks in a specific sector.

**Parameters**
- `sector_name` (str): Sector name (partial match)
- `count` (int): Max count (default: 30, max: 50)

**Example**
```
"Telecom equipment sector stocks"
"Semiconductor sector, 30 stocks"
```

---

### `get_volume_ranking`
Top stocks by volume.

**Parameters**
- `market` (str): `"KOSPI"` / `"KOSDAQ"` / `"ALL"` (default: `"ALL"`)
- `count` (int): Count (default: 50, max: 500)

**Example**
```
"Today's top 50 by volume"
"KOSPI volume top 100"
```

---

### `get_change_ranking`
Top gainers / losers.

**Parameters**
- `direction` (str): `"up"` / `"down"` (default: `"up"`)
- `market` (str): `"KOSPI"` / `"KOSDAQ"` / `"ALL"` (default: `"ALL"`)
- `count` (int): Count (default: 50, max: 500)

**Example**
```
"Today's upper-limit stocks"
"KOSDAQ losers top 20"
```

---

### `get_market_cap_ranking`
Top stocks by market cap.

**Parameters**
- `market` (str): `"KOSPI"` / `"KOSDAQ"` (default: `"KOSPI"`)
- `count` (int): Count (default: 50, max: 500)

**Example**
```
"Top 100 by market cap"
"KOSDAQ market cap top 50"
```

---

## ⚡ Bulk Queries (2)

### `get_multi_stocks`
Parallel fetch basic info (price/volume) for multiple stocks.

**Parameters**
- `codes` (list[str]): Stock code list (max 30)

**Example**
```
"Show Samsung, SK Hynix, Hyundai Motor at once"
```

---

### `get_multi_chart_stats`
Parallel fetch chart statistics (52-week high/low/drawdown).

**Parameters**
- `codes` (list[str]): Stock code list (max 100)
- `days` (int): Period (default: 260 = 52 weeks)

**Example**
```
"52-week drawdown for top 100 market cap"
```

**Returns**: `current_price`, `high`, `high_date`, `low`, `low_date`, `drawdown_pct`, `recovery_pct`, `period_return_pct`, `avg_volume`

---

## 📁 Excel Export (3)

### `export_to_excel`
Save single stock data to Excel.

**Parameters**
- `data_type` (str): `"chart"` / `"flow"` / `"financial"`
- `code` (str): 6-digit stock code
- `days` (int): Chart/flow period (default: 180)
- `filename` (str): Filename (auto-generated if empty)

**Example**
```
"Save Samsung chart data to Excel"
"Export Hyundai flow to Excel"
```

**Use case**: Upload to Gemini/GPT for cross-AI analysis.

---

### `scan_to_excel`
Scan multiple stocks and save as Excel snapshot.

**Parameters**
- `codes` (list[str]): Stock code list (max 500)
- `days` (int): Chart stats period (default: 260)
- `include_financial` (bool): Include financials (default: `true`)
- `filename` (str): Filename

**Example**
```
"Create snapshot of top 100 market cap"
```

**Workflow**: Scan once (10~20s) → Query repeatedly via `query_excel` (16ms).

---

### `query_excel`
Filter saved Excel snapshot instantly.

**Parameters**
- `file_path` (str): Path from `scan_to_excel`
- `filters` (dict): Filter conditions (e.g., `{"per_max": 10, "drawdown_pct_max": -30}`)
- `sort_by` (str): Sort column
- `descending` (bool): Descending (default: `true`)
- `limit` (int): Top N (default: 30)

**Example**
```
"Find PER under 10 from that snapshot"
"Only stocks with drawdown below -20%"
```

---

## 🔧 Debugging (1)

### `get_metrics_summary`
Tool usage statistics for the last N days.

**Parameters**
- `days` (int): Days (default: 1, max: 30)

**Example**
```
"Today's tool usage stats"
"Last week's token usage"
```

**Log location**: `~/Downloads/kstock/logs/metrics_YYYYMMDD.jsonl`

---

## File Storage

Excel snapshots, chart files, metric logs are stored at:

- Windows: `%USERPROFILE%\Downloads\kstock\`
- macOS/Linux: `~/Downloads/kstock/`

All files stay on your local machine. Nothing is transmitted externally.
