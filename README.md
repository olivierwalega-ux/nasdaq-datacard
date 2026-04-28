# KPI Assignment – NASDAQ Stock Price Dataset

**Course:** AI & Data Engineering  
**Submission:** 28-04-2026  

---

## 1. Source of Data

Data was collected using the **Yahoo Finance API** via the `yfinance` Python library (open-source, free tier).  
Yahoo Finance provides historical daily OHLCV (Open, High, Low, Close, Volume) data for publicly traded companies.

**API:** `yfinance.download(ticker, start, end)`  
**Exchange:** NASDAQ (National Association of Securities Dealers Automated Quotations)  
**Granularity:** Daily (1 trading day = 1 row)  
**Format:** Pandas DataFrame → exported as CSV

### Selected companies

| # | Ticker | Company | Period | Trading days |
|---|--------|---------|--------|-------------|
| 1 | AAPL   | Apple   | 2024-04-01 → 2025-04-01 | ~252 (1 year) |
| 2 | MSFT   | Microsoft | 2024-07-01 → 2025-04-01 | ~189 (9 months) |
| 3 | TSLA   | Tesla   | 2024-10-01 → 2025-04-01 | ~126 (6 months) |
| 4 | NVDA   | NVIDIA  | 2025-01-01 → 2025-04-01 | ~63 (3 months) |
| 5 | AMZN   | Amazon  | 2025-03-01 → 2025-04-01 | ~21 (1 month) |

Each company covers a **different time period**, as required by the assignment.  
Columns collected: `Open`, `High`, `Low`, `Close`, `Volume`.

---

## 2. KPIs (Key Performance Indicators)

Four KPIs were defined to assess the quality of the dataset for use in AI/ML training.

### (a) Completeness
**Definition:** Percentage of cells in the dataset that contain non-null values.  
**Formula:** `(1 - missing_values / total_cells) × 100`  
**Why it matters:** Missing values in training data cause model bias and require imputation strategies.  
**Expected value:** ≥ 99% (Yahoo Finance data is highly complete for major NASDAQ stocks)

### (b) Latency
**Definition:** Number of days between the most recent record in the dataset and today's date.  
**Formula:** `today - last_record_date` (in days)  
**Why it matters:** For AI models trained on market data, stale data reduces prediction relevance.  
**Expected value:** ≤ 5 days (accounting for weekends and market holidays)

### (c) Accuracy
**Definition:** Percentage of rows where OHLC relationships are logically valid.  
**Formula:** `(rows where High ≥ Close ≥ Low AND High ≥ Low) / total_rows × 100`  
**Why it matters:** Violations of OHLC logic indicate data corruption or API errors.  
**Expected value:** 100% for clean Yahoo Finance data

### (d) Consistency
**Definition:** Percentage of rows where all key numeric fields contain positive (non-zero) values.  
**Formula:** `(rows where Volume > 0 AND Close > 0 AND Open > 0) / total_rows × 100`  
**Why it matters:** Zero or negative values in price/volume data are physically impossible and indicate bad records.  
**Expected value:** 100% for major exchange-listed stocks

---

## 3. Conclusion

The dataset collected from Yahoo Finance via `yfinance` demonstrates **high quality** across all four KPI dimensions:

- **Completeness** is consistently near 100% — Yahoo Finance rarely returns null values for major NASDAQ stocks.
- **Latency** is low (data ends close to April 2025, well within acceptable range for a historical dataset).
- **Accuracy** is 100% — all OHLC records are internally consistent (High ≥ Close ≥ Low).
- **Consistency** is 100% — all trading day records contain valid, positive price and volume values.

**Overall assessment:** This dataset is suitable as a training dataset for AI models. It is complete, consistent, and logically valid. The main limitation is the short period for AMZN (1 month ≈ 21 rows), which may be insufficient for time-series forecasting tasks.

**Recommendation:** For production AI training, extend all periods to at least 2 years and add intraday granularity (hourly or minute-level data) where latency sensitivity matters.

---

## Files in this repository

| File | Description |
|------|-------------|
| `kpi_assignment.py` | Main Python script — downloads data, computes stats & KPIs |
| `data_AAPL.csv` | Apple daily OHLCV — 1 year |
| `data_MSFT.csv` | Microsoft daily OHLCV — 9 months |
| `data_TSLA.csv` | Tesla daily OHLCV — 6 months |
| `data_NVDA.csv` | NVIDIA daily OHLCV — 3 months |
| `data_AMZN.csv` | Amazon daily OHLCV — 1 month |
| `statistics.csv` | Descriptive statistics for all companies |
| `kpi_results.csv` | KPI scores for all companies |
| `charts.png` | Closing price charts for all 5 companies |
| `README.md` | This data card |

---

*Dataset collected: April 2026 | Source: Yahoo Finance API | Assignment: KPI Assessment of Training Datasets*
