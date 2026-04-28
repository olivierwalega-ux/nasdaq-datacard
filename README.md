# NASDAQ Share-Price Dataset — Data Card

> A small, reproducible dataset of daily share prices for five NASDAQ companies across different sectors, collected from Yahoo Finance. Intended as a training / benchmark dataset for time-series and data-quality exercises.

| Field | Value |
|---|---|
| **Maintainer** | Olivier Wierzbicki |
| **Course** | Assignment on Data-Quality KPIs for AI training data |
| **Collection date** | 2025-04-01 (last observation in every ticker) |
| **License** | Data © Yahoo. Personal / educational use only. Code: MIT. |
| **Primary task** | Univariate time-series forecasting, data-quality analysis |
| **File format** | CSV (one file per ticker), UTF-8, comma-separated |
| **Total rows** | 644 (251 + 188 + 124 + 60 + 21) |

---

## 1. Source of Data — full description

All price data is pulled from **Yahoo Finance** (https://finance.yahoo.com) through the open-source Python package [`yfinance`](https://github.com/ranaroussi/yfinance).

Yahoo Finance aggregates official end-of-day OHLCV (Open, High, Low, Close, Volume) data from the listing exchange — NASDAQ in our case. The figures are **auto-adjusted for splits and dividends** (`auto_adjust=True`), so the Close price is directly comparable across time.

### 1.1 Companies and look-back windows

Each ticker was downloaded with a **different look-back window on purpose**, as required by the brief. The actual periods collected by this run:

| # | Company | Ticker | Exchange | Requested | First date | Last date | Rows |
|---|---|---|---|---|---|---|---|
| 1 | CrowdStrike Holdings | `CRWD` | NASDAQ | 1 year | 2024-04-01 | 2025-04-01 | 251 |
| 2 | MercadoLibre Inc. | `MELI` | NASDAQ | 9 months | 2024-07-01 | 2025-04-01 | 188 |
| 3 | Celsius Holdings Inc. | `CELH` | NASDAQ | 6 months | 2024-10-01 | 2025-04-01 | 124 |
| 4 | Duolingo Inc. | `DUOL` | NASDAQ | 3 months | 2025-01-01 | 2025-04-01 | 60 |
| 5 | Rocket Lab USA Inc. | `RKLB` | NASDAQ | 1 month | 2025-03-01 | 2025-04-01 | 21 |

The five tickers were chosen to represent distinct market segments: cybersecurity (CRWD), Latin American e-commerce (MELI), consumer beverages (CELH), EdTech (DUOL), and commercial aerospace (RKLB). This gives the dataset meaningful diversity in volatility profiles and sector exposure.

### 1.2 Schema (columns in every per-ticker CSV)

| Column | Type | Description |
|---|---|---|
| `Date` | `datetime` (index) | Trading day, US/Eastern close |
| `Open` | `float` | Adjusted opening price (USD) |
| `High` | `float` | Adjusted intra-day high (USD) |
| `Low` | `float` | Adjusted intra-day low (USD) |
| `Close` | `float` | Adjusted closing price (USD) |
| `Volume` | `int` | Shares traded on that day |

### 1.3 How to reproduce

```bash
pip install yfinance pandas matplotlib
python3 kpi_assignment.py
```

Artifacts produced by the script:

- `data/CRWD.csv`, `data/MELI.csv`, `data/CELH.csv`, `data/DUOL.csv`, `data/RKLB.csv`
- `statistics.csv` — descriptive statistics per ticker
- `kpi_results.csv` — machine-readable KPI summary
- `charts.png` — closing-price visualisation for all five tickers

### 1.4 Descriptive statistics (Close price, this run)

| Ticker | Mean Close | Std | Min | Max |
|---|---|---|---|---|
| CRWD | 331.79 | 50.42 | 217.89 | 455.36 |
| MELI | 1937.25 | 155.61 | 1591.44 | 2260.00 |
| CELH | 28.50 | 3.29 | 21.28 | 35.62 |
| DUOL | 342.01 | 44.92 | 272.49 | 441.39 |
| RKLB | 18.74 | 0.85 | 17.12 | 20.40 |

MELI dominates by absolute price — expected for a high-value Latin American e-commerce platform. CELH shows the tightest price range, reflecting a period of consolidation after a sharp drawdown from its all-time highs. RKLB has the smallest standard deviation in absolute terms but is among the most volatile on a percentage basis given its low share price.

---

## 2. Data-Quality KPIs

All KPIs are reported on a `[0, 1]` scale (higher = better). Values below come from the actual run of `kpi_assignment.py` on **2025-04-01**.

### 2.1 Completeness — 1.00

*Share of non-null cells across all downloaded records.*

Formula: `score = 1 − NaN_cells / total_cells`

**Result:** 1.00 for every ticker. Yahoo Finance returned no missing values for any of the five tickers across all OHLCV columns. This is consistent with the behaviour expected for liquid, actively traded NASDAQ constituents with continuous price history.

### 2.2 Latency — 0.00

*Freshness of the most recent observation relative to today.*

Formula: `score = max(0, 1 − age_days / 5)`, where `age_days = today − last_obs`.

**Result:** 0.00 — age = 393 days. This dataset was collected as a **historical snapshot** ending 2025-04-01 and is intentionally not kept up to date. For a production pipeline the script would be re-run daily; a same-day run after market close yields score = 1.00. The low latency score here is a feature of the assignment design, not a data defect.

### 2.3 Accuracy — 1.00

*Internal consistency of OHLC values.*

For every row the following relations must hold:

- `High ≥ Open`, `High ≥ Close`, `High ≥ Low`
- `Low ≤ Open`, `Low ≤ Close`
- `Close > 0`, `Open > 0`, `High > 0`, `Low > 0`

**Result:** 1.00 across all tickers. Zero OHLC violations were found. Yahoo Finance's auto-adjustment pipeline ensures these invariants hold before delivery.

### 2.4 Consistency — 1.00

*Structural uniformity: positive volume and prices on every trading day.*

Formula: `score = rows where Volume > 0 AND Close > 0 AND Open > 0 / total_rows`

**Result:** 1.00 across all tickers. Every record contains valid, positive price and volume values. No zero-volume or zero-price anomalies were detected, which is expected for large-cap and mid-cap NASDAQ names with deep liquidity.

---

## 3. Conclusion

### 3.1 What the numbers say

The Yahoo Finance NASDAQ dataset scores **0.75 / 1.00** overall — three KPIs are perfect; the single weakness is Latency, which is 0.00 by design because this is a fixed historical snapshot rather than a live feed.

- **Accuracy** is perfect — OHLC invariants hold for every row across all five tickers.
- **Completeness** is perfect (1.00) — no missing values in any column.
- **Consistency** is perfect (1.00) — all volume and price fields are positive on every trading day.
- **Latency** is 0.00 — the dataset ends on 2025-04-01 (393 days ago). This is expected for a historical assignment dataset and would be resolved by re-running the collection script against the current date.

### 3.2 Fitness for AI training

For models that need price history — baseline forecasting, volatility estimation, pair-trading experiments, or intro-level reinforcement learning — the dataset is **training-ready as downloaded**. No imputation, no OHLC repair, and no volume filtering are required.

For production applications additional concerns apply:

- **Look-ahead bias**: adjusted prices change retroactively when a new split or dividend is declared. Always snapshot the dataset with a fixed `collection_date` (see `kpi_results.csv`) before training.
- **Survivorship bias**: only currently listed NASDAQ companies are included; delisted tickers are absent.
- **Coverage**: 5 tickers × 644 rows is sufficient for teaching; serious work needs broader coverage (the full NASDAQ-100 or NASDAQ-Composite).
- **Latency**: for any real-time or near-real-time application, the collection script must be scheduled to run after each daily market close.
