import pandas as pd
import numpy as np

# ---------- helpers ----------

def compute_log_return(price_series):
    price_series = pd.to_numeric(price_series, errors="coerce")
    return np.log(price_series / price_series.shift(1))

def assign_trading_day(ts_series, cutoff_hour=16):
    ts = pd.to_datetime(ts_series, utc=True, errors="coerce")
    ts = ts.dt.tz_convert("America/New_York")

    td = ts - pd.Timedelta(hours=cutoff_hour)
    td = td.dt.normalize()
    td = pd.Series(td)

    return td

def extract_daily_counts(df, timestamp_col):
    temp = df.copy()
    temp["trading_day"] = assign_trading_day(temp[timestamp_col])
    return temp.groupby("trading_day").size()

def extract_unique_editors(df, timestamp_col, user_col):
    temp = df.copy()
    temp["trading_day"] = assign_trading_day(temp[timestamp_col])
    return temp.groupby("trading_day")[user_col].nunique()


# ---------- TESLA ----------
tesla = pd.read_csv("data/datasets/STOCK_tesla.csv")
tesla["Date"] = pd.to_datetime(tesla["Date"], utc=True)
tesla["Date"] = tesla["Date"].dt.tz_convert("America/New_York").dt.normalize()
tesla = tesla.sort_values("Date").set_index("Date")

log_return = compute_log_return(tesla["Close"])
tsla_volume = tesla["Volume"]
tsla_volume.name = "tsla_volume"
log_return.name = "log_return"


# ---------- SP500 ----------
sp500 = pd.read_csv("data/datasets/STOCK_sp500.csv", skiprows=[1, 2], index_col=0)
sp500.index = pd.to_datetime(sp500.index)
sp500.index = sp500.index.tz_localize("America/New_York").normalize()
sp500 = sp500.sort_index()

mkt_return = compute_log_return(sp500["Close"])
mkt_volume = sp500["Volume"]
mkt_return.name = "mkt_return"
mkt_volume.name = "mkt_volume"


# ---------- VIEWS ----------
views = pd.read_csv("data/datasets/tesla-musk-views.csv")
views["Date"] = (
    pd.to_datetime(views["Date"])
    .dt.tz_localize("America/New_York")
    .dt.normalize()
)
views = views.set_index("Date")

msk_wiki_views = views["Elon Musk"]
msk_wiki_views.name = "msk_wiki_views"

tsla_wiki_views = views["Tesla, Inc."]
tsla_wiki_views.name = "tsla_wiki_views"


# ---------- WIKI ----------
wiki_musk = pd.read_csv("data/datasets/WIKI_elon_musk.csv")
wiki_tsla = pd.read_csv("data/datasets/WIKI_tesla.csv")

msk_edits = extract_daily_counts(wiki_musk, "timestamp")
msk_edits.name = "msk_edits"

tsla_edits = extract_daily_counts(wiki_tsla, "timestamp")
tsla_edits.name = "tsla_edits"

msk_unique_editors = extract_unique_editors(wiki_musk, "timestamp", "user")
msk_unique_editors.name = "msk_unique_editors"

tsla_unique_editors = extract_unique_editors(wiki_tsla, "timestamp", "user")
tsla_unique_editors.name = "tsla_unique_editors"


# ---------- TWEETS ----------
tweets = pd.read_csv("data/datasets/all_musk_posts.csv")
msk_tweets = extract_daily_counts(tweets, "createdAt")
msk_tweets.name = "msk_tweets"

series_list = [
    log_return,
    mkt_return,
    tsla_volume,
    mkt_volume,
    tsla_wiki_views,
    tsla_edits,
    tsla_unique_editors,
    msk_wiki_views,
    msk_edits,
    msk_unique_editors,
    msk_tweets,
]

start = max(s.dropna().index.min() for s in series_list)
end   = min(s.dropna().index.max() for s in series_list)

master_idx = log_return.loc[start:end].index

aligned = []

for s in series_list:
    aligned.append(s.reindex(master_idx))

df = pd.concat(aligned, axis=1)

# event processes → zero is meaningful
for col in ["msk_edits", "tsla_edits", "msk_tweets",
            "msk_unique_editors", "tsla_unique_editors"]:
    df[col] = df[col].fillna(0)

# views — debatable, depends on data collection
df["msk_wiki_views"] = df["msk_wiki_views"].fillna(0)
df["tsla_wiki_views"] = df["tsla_wiki_views"].fillna(0)

# returns — never fill
df = df.dropna(subset=["log_return", "mkt_return"])

df.to_csv("master.csv")