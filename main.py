import streamlit as st

from loader import get_url, TICKERS_MAPPER, CANDLES
from data_parser import get_df, get_driver_and_wait, get_excel_workbook



tickers_choice = st.multiselect(label='Ticker', placeholder='Gold', options=TICKERS_MAPPER.keys())
candle_choice = st.selectbox(label='Timeframe', placeholder='1Hour', options=CANDLES)
submit_btn = st.button('Submit')

st.session_state.setdefault("driver", None)
st.session_state.setdefault("wait", None)
st.session_state.setdefault("excel_bytes", None)

if submit_btn:
    if st.session_state.driver is None or st.session_state.wait is None:
        st.session_state.driver, st.session_state.wait = get_driver_and_wait()
    
    dfs = []
    for ticker in tickers_choice:
        url = get_url(ticker)
        print(url)
        
        df = get_df(st.session_state.driver, st.session_state.wait, 
                    url, candle_choice)
        dfs.append(df)
    
    
    st.session_state.excel_bytes = get_excel_workbook(dfs, tickers_choice)

if st.session_state.excel_bytes:
    st.download_button(
        label="Excel file",
        data=st.session_state.excel_bytes,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        file_name="quotes_profinance.xlsx",
    )