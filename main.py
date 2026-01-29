from string import punctuation

import streamlit as st
from selenium.common.exceptions import TimeoutException

from loader import get_url, TICKERS_MAPPER, CANDLES, DEFAULT_CHOICE
from data_parser import get_df, get_driver_and_wait, get_excel_workbook
from config import logger


def remove_punct(string: str) -> str:
    for sym in punctuation:
        string = string.replace(sym, "_")
    string = string.strip("_")
    return string


tickers_choice = st.multiselect(
    label='Ticker', default=DEFAULT_CHOICE, options=TICKERS_MAPPER.keys())
candle_choice = st.selectbox(
    label='Timeframe', placeholder='1Hour', options=CANDLES)
submit_btn = st.button('Submit')

st.session_state.setdefault("driver", None)
st.session_state.setdefault("wait", None)
st.session_state.setdefault("excel_bytes", None)

if submit_btn:
    if st.session_state.driver is None or st.session_state.wait is None:
        st.session_state.driver, st.session_state.wait = get_driver_and_wait()
        logger.info("Session is opened successfully")

    dfs = []
    for ticker in tickers_choice:
        url = get_url(ticker)
        try:
            df = get_df(st.session_state.driver, st.session_state.wait,
                        url, candle_choice)
            dfs.append(df)
        except TimeoutException as e:
            logger.error(f"{e} - ticker:{ticker}")
    if dfs:
        tickers_choice = list(map(remove_punct, tickers_choice))
        st.session_state.excel_bytes = get_excel_workbook(dfs, tickers_choice)
        logger.info(f"Excel file is uploaded successfully: {tickers_choice}")

if st.session_state.excel_bytes:
    st.download_button(
        label="Excel file",
        data=st.session_state.excel_bytes,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        file_name="quotes_profinance.xlsx",
        on_click='ignore'
    )
    logger.info(f"Excel file is dowloaded successfully: {tickers_choice}")
