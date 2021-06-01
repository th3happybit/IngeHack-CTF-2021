from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions

async def do_report(url):

    options = Options()
    # options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('user-agent=Ingehack/2.0')
    browser = webdriver.Chrome('chromedriver', options=options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])

    try:
        browser.get('http://0.0.0.0:9090/')
        browser.add_cookie({
            'name': 'flag',
            'value': 'Ingehack{f4k3_fl4g_f0r_t3st1ng}',
            'domain': "0.0.0.0"
        })
    except exceptions.InvalidCookieDomainException as e:
        print("exception ------>: ", e.args)

    try:
        browser.get(url)
        WebDriverWait(browser, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    except:
        pass
    finally:
        browser.quit()
