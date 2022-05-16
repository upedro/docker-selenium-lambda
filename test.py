from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
import json

def handler(event=None, context=None):
    #configurando o chrome para rodar na AWS
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    chrome = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    #entrando no site
    chrome.get("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")
    #encontrando os cards
    #busquei em todos os elementos rows, porém identifiquei quais teriam cards dentro
    products_cards = chrome.find_elements(By.CLASS_NAME, 'row')
    card_list = []
    for i in products_cards:
        have_card = i.find_elements(By.CLASS_NAME,'col-sm-4')
        if len(have_card) > 1:
            card_list = have_card
    pcs_lenovo = []
    # em posse dos cards, faço a extração e tratamento dos dados
    for card in card_list:
        c = {}
        #havia tentando fazer um find para cada elemento, mas demorava muito, então optei em fazer apartir do texto
        card_splited = card.text.split('\n')
        #aqui eu filtro somento os lenovos
        c['title'] = card_splited[1]
        if 'Lenovo' in c['title']:
            c['price'] = card_splited[0]
            splited_price = c['price'].split('$')
            c['price'] = float(splited_price[1])
            c['description'] = card_splited[2]
            c['reviews'] = card_splited[3]
            splited_review = c['reviews'].split(' ')
            c['review_int'] = int(splited_review[0])
            pcs_lenovo.append(c)
        else:
            continue
        
    #aqui eu faço a ordenção por preço
    pcs_lenovos_descend_sort = sorted(pcs_lenovo, key=lambda d: d['price'], reverse=False)
    response = {
        "statusCode": 200,
        "body": json.dumps(pcs_lenovos_descend_sort)
    }
    return response
