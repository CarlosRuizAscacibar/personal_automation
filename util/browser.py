from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import shutil

def init_browser():
    opts = Options()

    selenum_url = os.environ.get('PA_SELENUM_URL', None)

    if selenum_url != None:
        o = webdriver.ChromeOptions()
        o.add_argument("disable-dev-shm-usage")
        o.add_argument("--no-sandbox")
        o.add_argument('--disable-gpu')
        o.add_argument('--disable-setuid-sandbox')

        d = webdriver.Remote(selenum_url, DesiredCapabilities.CHROME, options=o)
    else:
        headless = os.environ.get('PA_HEADLESS', 'no')
        if headless == 'no':
            opts.headless = False
        else:
            opts.headless = True
        opts.binary_location = shutil.which('firefox')
        d = webdriver.Firefox(options=opts, log_path='test.log')
    
    d.set_window_size(1600,900)
    return d