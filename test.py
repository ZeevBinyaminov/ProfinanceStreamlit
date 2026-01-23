import streamlit as st

from loader import get_url
from data_parser import get_df, get_driver_and_wait



choice = 'Gold'

driver, wait = get_driver_and_wait()
 
if choice:
    url = get_url(choice)
    df = get_df(driver, wait, url)
    print(df.shape)
