from decimal import Decimal
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import pandas as pd
import passwords
import notification
import browser
from log import _print

def wait_element_css(driver, css, wait=5):
    r = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css))
    )
    time.sleep(.2)
    return r


def exists_element_css(driver, css):
    result = None
    try:
        result = wait_element_css(driver, css, 1).is_displayed()
    except:
        result = False
    return result


def parse_movment_table(driver):
    table = wait_element_css(driver, '#movimientosC_wrapper')
    rows = []
    for x in table.find_elements_by_tag_name('tr'):
        fila = {}
        for i, y in enumerate(x.find_elements_by_tag_name('td')):
            if i == 1:
                fila['fecha'] = y.text
            if i == 2:
                fila['descripcion'] = y.text
            if i == 3:
                fila['importe'] = y.text.replace(
                    '-', '').replace('.','').replace(',', '.').replace('EUR', '').strip()
                if y.text.count('-') > 0:
                    fila['signo'] = '-'
                else:
                    fila['signo'] = '+'
        if len(fila.keys()) > 0 and not (i == 3 and y.text.count('-') == 0):
            rows.append(fila)
    return rows


def scrap_evo():
    mattr = None
    saldo = None
    driver = None
    try:
        _print(f'Start scraping')
        driver = browser.init_browser()
        _print(f'Browser starts')
        driver.get('https://www.evobanco.com/')
        time.sleep(2)
        _print(f'On evo.com')
        time.sleep(2)
        wait_element_css(driver, '#client_login').click()
        vault_evo = passwords.get_entry('evo')
        username = driver.find_element_by_css_selector(
            'form#form1 div.form_row input[type="text"]')
        password = driver.find_element_by_css_selector(
            'form#form1 div.form_row input[type="password"]')
        username.send_keys(vault_evo.username)
        pass_element_id = password.get_attribute('id')
        driver.execute_script(f'document.querySelector("#{pass_element_id}").value ="{vault_evo.password}"')
        wait_element_css(driver, '#continuar').click()

        _print('Logged successfully on evo')
        saldo = wait_element_css(driver,'#cant_saldo').text
        wait_element_css(driver, '#movimientosCta__0').click()
        next_movments_page_css_id = '#movimientosC_next'
        mattr = parse_movment_table(driver)
        while exists_element_css(driver, next_movments_page_css_id):
            wait_element_css(driver, next_movments_page_css_id).click()
            mattr.extend(parse_movment_table(driver))
            time.sleep(0.5)
        _print(f'Has {len(mattr)} movments')
    finally:
        if driver != None:
            driver.close()    
    return (mattr, saldo)


def get_df_periodo(mattr,days=8):
    dates = [datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=-x), "%d/%m/%Y") for x in range(8)]

    acum = {}
    for x in mattr:
        if x['fecha'] in dates:
            if list(acum.keys()).count(x['fecha']) == 0:
                acum[x['fecha']] = 0
            acum[x['fecha']] = acum[x['fecha']] + Decimal(x['importe'])

    df = pd.DataFrame(mattr)
    df['importe'] = df.apply(lambda x: Decimal(x['importe']), axis=1)

    df_periodo = pd.merge(pd.Series(dates, name="fecha"),
                        df, how='inner', on="fecha")
    df_agg_dia = df_periodo[df_periodo['signo'] == '-'].groupby('fecha').agg(
        lambda x: x.sum() if x.name == 'importe' else ' ; '.join(x))
    return (df_periodo, df_agg_dia)

def weekly_report_html(budget):
    """
        Creates HTML report
    """
    report_html = ''
    mattr, saldo = scrap_evo()
    report_html = report_html + f'<h2>Saldo {saldo}</h2>'
    df_periodo, df_agg_dia = get_df_periodo(mattr)
    df_periodo_mes, df_agg_mes_dias = get_df_periodo(mattr, days=datetime.date.today().day + 1)
    total_periodo = df_periodo[df_periodo['signo'] == '-']['importe'].sum()
    total_mes = df_periodo_mes[df_periodo_mes['signo'] == '-']['importe'].sum()
    report_html = report_html + f'<h2>Total gastado estos 7 días {total_periodo}</h2>'
    report_html = report_html + f'<h3>Total gastado este mes {total_mes} {total_mes*100/budget}</h3>'
    report_html = report_html + f'<h3>Gastos estos 7 días</h3>'
    report_html = report_html + df_periodo[df_periodo['signo'] == '-'].to_html()
    report_html = report_html + f'<h3>Gastos estos 7 días por día</h3>'
    report_html = report_html + df_agg_dia.to_html()
    return report_html

def weekly_report_text(budget):
    """
        Creates HTML report to send by email
    """
    report_text = ''
    mattr, saldo = scrap_evo()
    report_text = report_text + f'Saldo {saldo} \n'
    df_periodo, df_agg_dia = get_df_periodo(mattr)
    df_periodo_mes, df_agg_mes_dias = get_df_periodo(mattr, days=datetime.date.today().day + 1)
    total_periodo = df_periodo[df_periodo['signo'] == '-']['importe'].sum()
    total_mes = df_periodo_mes[df_periodo_mes['signo'] == '-']['importe'].sum()
    report_text = report_text + f'Total gastado estos 7 días {total_periodo} \n'
    report_text = report_text + f'Total gastado este mes {total_mes} {total_mes*100/budget}  \n'
    report_text = report_text + f'Gastos estos 7 días  \n'
    report_text = report_text + df_periodo[df_periodo['signo'] == '-'].to_string()
    report_text = report_text + f'Gastos estos 7 días por día  \n'
    report_text = report_text + df_agg_dia.to_string()
    return report_text

