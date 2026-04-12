# StockLens Usage Guide

50+ prompt examples and how to write good questions.

[🇰🇷 한국어](../ko/USAGE.md) | [TOOLS](TOOLS.md) | [INSTALL](INSTALL.md)

---

## 3 Elements of a Good Question

```
❌ Bad:  "How about Samsung Electronics?"
✅ Good: "Analyze Samsung Electronics 120-day candles using 20-day MA,
         combine with investor flow, and give a buy/hold opinion"
```

| Element | Description | Example |
|---------|-------------|---------|
| **Data Range** | What and how much | "120-day candles", "20-day flow" |
| **Analysis Method** | How to analyze | "using 20-day MA", "via RSI" |
| **Desired Output** | What form of answer | "buy/hold judgment", "as a table" |

---

## Level 1: Basic Queries

```
Samsung Electronics current price
SK Hynix 120-day daily candles
Kakao 20-day foreign/institutional flow
Hyundai Motor PER and PBR
Current KOSPI value
```

**Note**: Korean stock codes are 6 digits. Samsung = `005930`, SK Hynix = `000660`, Hyundai = `005380`, Kakao = `035720`, Naver = `035420`.

---

## Level 2: Chart Analysis

```
Analyze Samsung Electronics 120-day candles using 20-day MA trend

Find support and resistance levels in SK Hynix weekly chart (60 bars)

Kakao 120-day candles with 5/20/60/120-day MAs — 
is it in bullish alignment or bearish?

Calculate Bollinger Bands for Hyundai Motor 120-day chart,
determine if overbought or oversold

Calculate 14-day RSI for Naver 60-day chart.
Tell me if it's in oversold territory.
```

---

## Level 3: Flow Analysis

```
Analyze Samsung 20-day flow — are foreigners consistently buying?

Find days when both institutional and foreign investors 
net-bought SK Hynix

Check if retail sells while foreigners buy in Kakao flow

Compare Hyundai Motor flow against price trend —
does flow lead price?
```

---

## Level 4: Stock Comparison

```
Compare Samsung Electronics and SK Hynix 60-day charts —
which is relatively stronger?

Compare Kakao and Naver comprehensively (chart + flow + financial) 
and summarize as a table

Compare Hyundai Motor and Kia recent flow —
which do foreigners prefer?
```

---

## Level 5: Comprehensive Reports

```
Analyze Samsung Electronics with chart + flow + financials.
Write like an analyst report. End with buy/hold/sell conclusion.

Analyze SK Hynix in this structure:
1. Trend (via moving averages)
2. Momentum (RSI, volume changes)
3. Flow (foreign/institutional direction)
4. Valuation (PER/PBR)
5. Conclusion
```

---

## Level 6: Screening

```
Today's strongest 10 themes

Among semiconductor-related theme stocks, pick those currently rising

From top 50 KOSPI volume, find stocks with PER under 15

From top 100 market cap, find stocks down 30%+ from 52-week high

Today's strongest 3 themes, then analyze each theme's leader
```

---

## Level 7: Complex Queries

```
SK Hynix 120-day candles with 20-day MA trend analysis,
plus 20-day flow — is this a good buy timing?

Compare Samsung and SK Hynix recent 60-day charts.
Which is stronger? Summarize by change rate, volume, and flow direction as a table.

From top 30 volume, pick 3 stocks where foreign+institutional both net-bought,
then analyze each chart

I hold Samsung, Hyundai Motor, and Kakao.
Check 20-day flow and financials for all three.
Any risky stocks right now?
```

---

## Level 8: Excel Snapshot Workflow

```
Create snapshot of top 200 market cap

(After the above)
From that snapshot, find stocks with PER under 10 AND drawdown over -20%

(Same file)
Now show top 5 by foreign net buying

Save Samsung 180-day chart data as Excel
```

**Tip**: Once you make a snapshot, subsequent queries take **0.02 seconds**.

---

## Level 9: Multi-AI Integration (Gemini/GPT)

```
Save Samsung 120-day chart data as Excel
→ Upload the file to Gemini/ChatGPT
→ Ask: "Do technical analysis on this data"

Create snapshot of top 100 market cap
→ Upload Excel to Gemini
→ "Filter by PER and drawdown, suggest buy candidates"
```

Use Claude to collect data, then other AIs to analyze.

---

## Prompt Tips

### 1. Specify Numbers
```
❌ "Show recent chart"
✅ "Show 120-day daily chart"
```

### 2. Specify Analysis Method
```
❌ "Analyze the trend"
✅ "Analyze trend using 20-day MA"
```

### 3. Request Output Format
```
❌ "Give a general opinion"
✅ "Conclude with buy/hold/sell"
```

### 4. Encourage Tool Combination
```
"Combine chart + flow + financials"
"Check PER alongside drawdown"
```

### 5. Snapshot Once, Query Many
```
Once: "Create snapshot of top 100"
Repeat: "Filter by [condition]"
```
