import time
from typing import List
import io

from bs4 import BeautifulSoup as bs
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class ChromeWebDriverSingleton(webdriver.Chrome, Singleton):
    pass


class WebDriverWaitSingleton(WebDriverWait, Singleton):
    pass


def get_driver_and_wait(timeout=8):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("disable-dev-shm-usage")

    driver = ChromeWebDriverSingleton(options=chrome_options)
    wait = WebDriverWaitSingleton(driver, timeout=timeout)

    return driver, wait


def safe_click(driver, element, attempts: int = 5, pause: float = 0.15):
    """
    Надёжный клик по WebElement.

    - Скроллит элемент в центр
    - Кликает через ActionChains
    - Делает несколько попыток при перехвате клика / stale element

    :param driver: WebDriver
    :param element: WebElement (уже найденный)
    :param attempts: количество попыток
    :param pause: пауза между попытками (сек)
    """
    last_exc = None

    for _ in range(attempts):
        try:
            # скроллим элемент в центр экрана
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center', inline:'center'});",
                element
            )

            # небольшой тайм-аут, чтобы закончились анимации
            time.sleep(pause)

            # клик через ActionChains (обходит overlay/hover-баги)
            ActionChains(driver) \
                .move_to_element(element) \
                .pause(pause) \
                .click(element) \
                .perform()

            return

        except (ElementClickInterceptedException, StaleElementReferenceException) as e:
            last_exc = e
            time.sleep(pause)

    raise last_exc


def table_signature(driver) -> tuple:
    """
    Возвращает сигнатуру текущего состояния таблицы:
    (кол-во строк, текст первой строки, текст последней строки)
    """
    rows = driver.find_elements(By.CSS_SELECTOR, "#table_history tbody tr")
    n = len(rows)
    first = rows[0].text if n else ""
    last = rows[-1].text if n else ""
    return (n, first, last)


def wait_table_updated(driver, wait, old_sig, timeout=10):
    """
    Ждёт, пока таблица изменит сигнатуру относительно old_sig.
    """
    local_wait = wait if timeout is None else WebDriverWait(driver, timeout)
    return local_wait.until(lambda d: table_signature(d) != old_sig)


def get_data(driver, wait, url, target="1Hour"):
    driver.get(url)

    driver.execute_script("""
    document.querySelectorAll("iframe[src*='yastatic.net/safeframe']").forEach(f => {
    f.style.display = 'none';
    f.style.visibility = 'hidden';
    f.style.pointerEvents = 'none';
    });
    """)

    show_table_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "chart_input_history")))
    safe_click(driver, show_table_btn)

    table = wait.until(EC.visibility_of_element_located(
        (By.ID, "table_history")))
    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#table_history tbody tr:nth-child(2) td")))

    chart_input_tt_btn = wait.until(EC.element_to_be_clickable(
        (By.ID, "chart_input_tt_btn")))
    safe_click(driver, chart_input_tt_btn)

    wait.until(EC.visibility_of_element_located((By.ID, "tt_div")))

    target_cell = wait.until(EC.presence_of_element_located(
        (By.XPATH,
         f"//table[@id='tt_table']//td[normalize-space()='{target}']")
    ))

    safe_click(driver, target_cell)

    more_data_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#chart_button_minus")))

    for _ in range(8):
        old_sig = table_signature(driver)

        safe_click(driver, more_data_btn)

        # ждём, что таблица реально обновилась
        if old_sig[0] == 3001:
            break
        try:
            wait_table_updated(driver, wait, old_sig, timeout=5)
        except TimeoutException:
            # на всякий случай: иногда клик прошёл, но данных больше нет / сервер не отдаёт
            break

    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#table_history tbody tr:nth-child(2) td")))
    html = driver.page_source
    soup = bs(html, features="lxml")

    table = soup.find('table', id='table_history')
    rows = table.find_all('tr')
    rows = [[value.text for value in row.find_all('td')] for row in rows]

    return rows


def parse_rows_to_df(rows: list):
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df.dropna(inplace=True)
    df[['Open',	'High',	'Low',	'Close']] = df[[
        'Open',	'High',	'Low',	'Close']].map(str.strip)

    df[['Open',	'High',	'Low',	'Close']] = df[[
        'Open',	'High',	'Low',	'Close']].astype(float)
    df['Время'] = pd.to_datetime(df['Время'], dayfirst=True)
    df.rename(axis=1, mapper={'Время': 'Datetime'}, inplace=True)

    df.sort_values(by=['Datetime'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['Date'] = df['Datetime'].dt.date
    df['Hour'] = df['Datetime'].dt.hour

    return df


def get_df(driver, wait, url, target='1Hour'):
    data = get_data(driver, wait, url, target)
    df = parse_rows_to_df(data)
    return df


def get_excel_workbook(df_list: List[pd.DataFrame], labels: List[str]):
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, mode='w') as writer:
        for df, label in zip(df_list, labels):
            df.to_excel(writer, sheet_name=label, index=False)

    return buffer
