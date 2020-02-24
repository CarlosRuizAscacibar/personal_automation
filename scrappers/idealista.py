import browser
from bs4 import BeautifulSoup
import time


def get_page_source(driver, url):
    str_html = ''
    driver.get(url)
    for i in range(20):
        driver.execute_script(f'window.scrollTo(0,{str(500*i)})')
        time.sleep(.25)
    str_html = driver.page_source
    return str_html

def get_idealista_links_url(driver, url):
    str_html = get_page_source(driver, url)
    b = BeautifulSoup(str_html)
    return [x.attrs['href'] for x in b.select('a[class="item-link"]')]

def get_all_links():
    driver = None
    str_html = ''
    links = []
    try:
        driver = browser.init_browser()
        initial_url = 'https://www.idealista.com/venta-viviendas/madrid-madrid/?ordenado-por=fecha-publicacion-desc'
        links.extend(get_idealista_links_url(driver, initial_url))
        for i in range(2,10):
            links.extend(get_idealista_links_url(driver, f'https://www.idealista.com/venta-viviendas/madrid-madrid/pagina-{i}.htm?ordenado-por=fecha-publicacion-desc'))
    finally:
        if driver != None:
            driver.close()
    return links