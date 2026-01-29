TICKERS_MAPPER = {
    # === Индексы ===
    "Dow Jones": "djia",
    "S&P 500": "sp500i",
    "Nasdaq 100": "nasd100",
    "FTSE 100": "ftse100",
    "Euro Stoxx 50": "Euro_Stoxx_50",
    "DAX": "dax",
    "CAC 40": "cac40",
    "RTS": "rts",
    "MOEX": "mmvb",
    "USD Index": "usd_index",

    # === Облигации ===
    "US 10y": "us_10_year_bond_yield",
    "UK 10y": "uk_10_year_bond_yield",
    "Canada 10y": "canada_10_year_bond_yield",
    "Germany 10y": "germany_10_year_bond_yield",
    "India 10y": "india_10_year_bond_yield",
    "China 10y": "china_10_year_bond_yield",
    "Japan 10y": "japan_10_year_bond_yield",
    "Australia 10y": "australia_10_year_bond_yield",

    # === Товарные рынки (Металлы, Нефть, Газ) ===
    "Gold": "gold",
    "Silver": "silver",
    "Platinum": "platinum",
    "Palladium": "palladium",
    "Aluminum": "aluminum",
    "Copper": "copper",
    "Nickel": "nickel",
    "Brent Oil": "brent",
    "Crude Oil": "wti",
    "Urals Oil": "urals",
    "US Gas": "natural_gas",
    "TTF Gas": "ttf_gas",

    # === Курс рубля ===
    "USD/RUB": "usdrub",
    "EUR/RUB": "eurrub",
    "CNY/RUB": "cnyrub",

    # === Фьючерсы на индексы (из предыдущей таблицы) ===
    "Dow Jones (FUT)": "djiaf",
    "S&P 500 (FUT)": "sp500f",
    "Nasdaq 100 (FUT)": "nasd100f",
    "Nikkei 225 (FUT)": "nikf",
    "RTS (FUT)": "rtsf",
    "MOEX (FUT)": "mmvbf",

    # === Валюты (Forex, из предыдущей таблицы) ===
    "AUD/JPY": "audjpy",
    "AUD/USD": "audusd",
    "EUR/AUD": "euraud",
    "EUR/CAD": "eurcad",
    "EUR/CHF": "eurchf",
    "EUR/GBP": "eurgbp",
    "EUR/JPY": "eurjpy",
    "EUR/USD": "eurusd",
    "GBP/CHF": "gbpchf",
    "GBP/JPY": "gbpjpy",
    "GBP/USD": "gbpusd",
    "USD/CAD": "usdcad",
    "USD/CHF": "usdchf",
    "USD/CNH": "usdcnh",
    "USD/JPY": "usdjpy",
    "USD/KZT": "usdkzt",
    "USD/MXN": "usdmxn",
    "USD/TRY": "usdtry",

    # === Криптовалюты (из предыдущей таблицы) ===
    "Bitcoin": "bitcoin",
    "Ethereum": "etherium",
    "Ripple": "ripple",

    # === Валютные фьючерсы (из предыдущей таблицы) ===
    "USDRUB (F)": "usdrub_f",
    "USDRUB (FUT)": "rub",
    "EURRUB (F)": "eurrub_f",
    "EURRUB (FUT)": "eurrub_futures",
    "CNYRUB (F)": "cnyrub_f",
    "CNYRUB (FUT)": "cnyrub_futures"
}


CANDLES = ['1Min', '5Min', '15Min', '30Min',
           '1Hour', '2Hour', '4Hour', '1Day', '1Week']


DEFAULT_CHOICE = ['Gold', 'Silver', 'Platinum', 'Palladium',
                  'Copper', 'Brent Oil', 'Bitcoin', 'Nasdaq 100 (FUT)']


BASE_URL = 'https://www.profinance.ru/chart/{ticker}'


def get_url(ticker: str) -> str:
    return BASE_URL.format(ticker=TICKERS_MAPPER[ticker])
