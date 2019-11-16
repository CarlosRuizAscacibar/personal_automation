

from selenium.webdriver.common.keys import Keys
import time
import re
import datetime
import json
import os
import fotocasa_db
import browser
from log import _print


def get_text_css_element(driver, css):
    if len(driver.find_elements_by_css_selector(css)) > 0:
        return driver.find_element_by_css_selector(css).text
    else:
        return ''


def scrap_segunda_mano(driver, ad_dir):
    ad_dir['label_slider'] = get_text_css_element(
        driver, '.re-DetailSlider-label')
    ad_dir['price'] = get_text_css_element(driver,'.re-DetailHeader-price')
    features = [x.text.replace('.', '') for x in driver.find_elements_by_css_selector(
        '.re-DetailHeader-featuresItem')]
    ad_dir['direccion'] = get_text_css_element(driver, '.re-DetailMap-address')
    ad_dir['titulo'] = get_text_css_element(
        driver, '.re-DetailHeader-propertyTitle')
    ad_dir['descripcion'] = get_text_css_element(
        driver, '.fc-DetailDescription')
    ad_dir['aditional_info'] = {}
    ad_dir['date_updated'] = datetime.datetime.now()
    for x in driver.find_elements_by_css_selector('.re-DetailFeaturesList .re-DetailFeaturesList-featureContent'):
        tupla = x.text.split('\n')
        ad_dir['aditional_info'][tupla[0]] = tupla[1]
    for x in driver.find_elements_by_css_selector('.re-DetailExtras-listItem'):
        ad_dir['aditional_info'][x.text] = True
    for x in features:
        if x.find('habs') >= 0:
            ad_dir['habitaciones'] = int(x.replace('habs', ''))
        if x.find('baño') >= 0:
            ad_dir['banios'] = int(re.sub('baños?', '', x))
        if x.find('€/m²') >= 0:
            ad_dir['eur_m2'] = int(x.replace('€/m²', ''))
        else:
            if x.find('m²') >= 0:
                ad_dir['m2'] = x.replace('m²', '')


def scrap_obra_nueva(driver, ad_dir):
    pass
    #ad_dir['tipo_ad'] = 'obra-nueva'



def periodic_scrap():
    new_links = []
    driver = None
    try:
        driver = browser.init_browser()
        existing_ad_ids = fotocasa_db.get_existing_ad_ids()
        found_existing_url = False
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        _print(f'Begin periodic scrap now_str:{now_str}')
        j = 1
        existing_counter = 0
        while found_existing_url == False and existing_counter < 5:
            driver.get(
                'https://www.fotocasa.es/es/comprar/viviendas/madrid-provincia/todas-las-zonas/l/'+str(j)+'?sortType=publicationDate')
            time.sleep(2)
            j = j+1
            no_results = driver.find_elements_by_css_selector('.re-SearchNoResults-image')
            if len(no_results) == 0 or no_results[0].is_displayed() == False:
                for i in range(20):
                    driver.execute_script(f'window.scrollTo(0,{str(500*i)})')
                    time.sleep(.25)
                    links = driver.execute_script(
                        'return Array.from(document.querySelectorAll("a.re-Card-link")).map(c => c.getAttribute("href"))')
                for x in links:
                    if x.find('parking') == -1:
                        ad_id = re.findall("\d{6,}", x)[0]
                        if ad_id in existing_ad_ids:
                            existing_counter = existing_counter + 1
                        else:
                            fotocasa_db.insert_ad({'id': ad_id, 'date_created': now, 'url': x})
                            new_links.append(x)
                            if existing_counter > 0:
                                existing_counter = existing_counter - 1

            else:
                _print('Found url that already existed in the db')
                found_existing_url = True
        _print(f'Found {len(new_links)} new links')
    finally:
        if driver != None:
            driver.close()
    update_urls(new_links)

def update_all():
    driver = browser.init_browser()
    urls = fotocasa_db.get_existing_ads_url()
    update_urls(urls)

def update_urls(urls):
    driver = browser.init_browser()
    _print(f'Updating urls totals: {len(urls)}')
    try:
        for url in urls:
            driver.get("https://www.fotocasa.es" + url)
            for i in range(4):
                driver.execute_script(f'window.scrollTo(0,{str(500*i)})')
                time.sleep(.5)
            #html = driver.execute_script("return document.body.innerHTML")
            current_url = driver.execute_script("return window.location.href")
            ad_dir = {}
            ad_dir['id'] = re.findall("\d{6,}", url)[0]
            ad_dir['url'] = url
            if current_url.find('obra-nueva') > 0:
                scrap_obra_nueva(driver, ad_dir)
            else:
                scrap_segunda_mano(driver, ad_dir)
            fotocasa_db.update_ad(ad_dir)
            # save_page_html(html, re.findall("\d{6,}", url)[0] + ".html")
    finally:
        if driver != None:
            driver.close()
