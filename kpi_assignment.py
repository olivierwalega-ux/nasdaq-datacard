import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

companies = [
    {"ticker": "CRWD", "name": "CrowdStrike",     "start": "2024-04-01", "end": "2025-04-01"},
    {"ticker": "MELI", "name": "MercadoLibre",    "start": "2024-07-01", "end": "2025-04-01"},
    {"ticker": "CELH", "name": "Celsius Holdings","start": "2024-10-01", "end": "2025-04-01"},
    {"ticker": "DUOL", "name": "Duolingo",        "start": "2025-01-01", "end": "2025-04-01"},
    {"ticker": "RKLB", "name": "Rocket Lab",      "start": "2025-03-01", "end": "2025-04-01"},
]

all_data = {}

for c in companies:
    df = yf.download(c['ticker'], start=c['start'], end=c['end'], progress=False)
    df = df[['Close', 'Open', 'High', 'Low', 'Volume']]
    df.columns = ['Close', 'Open', 'High', 'Low', 'Volume']
    all_data[c['ticker']] = {
        'df': df,
        'name': c['name'],
        'start': c['start'],
        'end': c['end']
    }
    print(f"{c['ticker']} ({c['name']}): {len(df)} rows")

# descriptive statistics

stats_rows = []

for ticker, info in all_data.items():
    close = info['df']['Close']
    stats_rows.append({
        'Ticker': ticker,
        'Company': info['name'],
        'Period': f"{info['start']} / {info['end']}",
        'Trading_days': len(info['df']),
        'Mean': round(float(close.mean()), 2),
        'Std': round(float(close.std()), 2),
        'Min': round(float(close.min()), 2),
        'Max': round(float(close.max()), 2),
        'Median': round(float(close.median()), 2),
    })

stats_df = pd.DataFrame(stats_rows)
print("\nDescriptive statistics:")
print(stats_df[['Ticker', 'Trading_days', 'Mean', 'Std', 'Min', 'Max']].to_string(index=False))

# visualization

colors = ['#E63946', '#2A9D8F', '#E9C46A', '#457B9D', '#A8DADC']

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle('NASDAQ – Closing Prices\nKPI Assignment Dataset', fontsize=13, fontweight='bold')

for idx, (ticker, info) in enumerate(all_data.items()):
    r, c = divmod(idx, 3)
    ax = axes[r][c]
    df = info['df']
    ax.plot(df.index, df['Close'], color=colors[idx], linewidth=1.4)
    ax.fill_between(df.index, df['Close'], alpha=0.08, color=colors[idx])
    ax.set_title(f"{ticker} – {info['name']}", fontweight='bold', fontsize=9)
    ax.set_ylabel('Price (USD)', fontsize=8)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right', fontsize=7)
    ax.tick_params(axis='y', labelsize=7)
    ax.grid(True, alpha=0.25, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

ax_t = axes[1][2]
ax_t.axis('off')
tdata = [[r['Ticker'], r['Trading_days'], r['Mean'], r['Min'], r['Max']] for r in stats_rows]
tbl = ax_t.table(cellText=tdata, colLabels=['Ticker', 'Days', 'Mean', 'Min', 'Max'],
                 loc='center', cellLoc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)
tbl.scale(1, 1.6)
ax_t.set_title('Summary', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('charts.png', dpi=150, bbox_inches='tight')
print("\nSaved: charts.png")

# KPI assessment

kpi_rows = []

for ticker, info in all_data.items():
    df = info['df']
    n = len(df)

    missing = int(df.isnull().sum().sum())
    completeness = round((1 - missing / (n * len(df.columns))) * 100, 2)

    last_date = df.index[-1].to_pydatetime().replace(tzinfo=None)
    latency = (datetime.today() - last_date).days

    valid_ohlc = ((df['High'] >= df['Close']) &
                  (df['Close'] >= df['Low']) &
                  (df['High'] >= df['Low'])).sum()
    accuracy = round(float(valid_ohlc) / n * 100, 2)

    consistent = ((df['Volume'] > 0) &
                  (df['Close'] > 0) &
                  (df['Open'] > 0)).sum()
    consistency = round(float(consistent) / n * 100, 2)

    kpi_rows.append({
        'Ticker': ticker,
        'Company': info['name'],
        'Completeness (%)': completeness,
        'Latency (days)': latency,
        'Accuracy (%)': accuracy,
        'Consistency (%)': consistency,
    })

kpi_df = pd.DataFrame(kpi_rows)
print("\nKPI results:")
print(kpi_df.to_string(index=False))

# export

for ticker, info in all_data.items():
    info['df'].to_csv(f'data_{ticker}.csv')

stats_df.to_csv('statistics.csv', index=False)
kpi_df.to_csv('kpi_results.csv', index=False)
print("\nAll files saved.")
