from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
import shutil

def init_browser():
    opts = Options()

    headless = os.environ.get('PA_HEADLESS', 'no')
    if headless == 'no':
        opts.headless = False
    else:
        opts.headless = True
    opts.binary_location = shutil.which('firefox')
    
    return webdriver.Firefox(options=opts, log_path='test.log')